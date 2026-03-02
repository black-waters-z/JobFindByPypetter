from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncio
from datetime import datetime
from typing import Any, Dict, Optional

from search_manage import WorkSearch

qq_email = APIRouter(prefix="/qq_email", tags=["qq邮箱投递"])


class CrawlerInput(BaseModel):
    chrome_driver_path: str = ""
    search_file_path: str = ""
    file_path: str = ""


class CrawlerManager:
    """Manage the lifecycle of the WorkSearch crawler task."""

    def __init__(self) -> None:
        self._task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()
        self._work_search: Optional[WorkSearch] = None
        self._status: Dict[str, Any] = self._blank_status()

    @staticmethod
    def _blank_status() -> Dict[str, Any]:
        return {
            "is_running": False,
            "start_time": None,
            "end_time": None,
            "message": "idle",
            "error_message": "",
        }

    @property
    def status(self) -> Dict[str, Any]:
        data = dict(self._status)
        data["has_active_task"] = bool(self._task and not self._task.done())
        return data

    @property
    def is_running(self) -> bool:
        return bool(self._task and not self._task.done())

    async def start(self, **kwargs) -> Dict[str, Any]:
        async with self._lock:
            if self.is_running:
                raise RuntimeError("crawler task already running")

            self._status = self._blank_status()
            self._status.update(
                {
                    "is_running": True,
                    "start_time": datetime.utcnow().isoformat(),
                    "message": "crawler task started",
                }
            )

            self._task = asyncio.create_task(self._runner(**kwargs))
            return self.status

    async def stop(self) -> Dict[str, Any]:
        task: Optional[asyncio.Task] = None
        async with self._lock:
            if not self.is_running:
                raise RuntimeError("crawler task not running")

            task = self._task
            if task:
                task.cancel()

        if task:
            try:
                await task
            except asyncio.CancelledError:
                pass

        return self.status

    async def _runner(self, **kwargs) -> None:
        try:
            self._work_search = WorkSearch(**kwargs)
            await self._work_search.main()
            self._status["message"] = "crawler task finished"
        except asyncio.CancelledError:
            self._status["message"] = "crawler task cancelled"
            raise
        except Exception as exc:
            self._status["message"] = "crawler task failed"
            self._status["error_message"] = str(exc)
        finally:
            self._status["is_running"] = False
            self._status["end_time"] = datetime.utcnow().isoformat()
            await self._shutdown_browser()
            self._work_search = None
            self._task = None

    async def _shutdown_browser(self) -> None:
        browser = None
        if self._work_search is not None:
            browser = getattr(self._work_search, "browser", None)

        if browser is None:
            return

        try:
            await browser.close()
        except Exception:
            pass


crawler_manager = CrawlerManager()


@qq_email.post("/start")
async def start_crawler(crawler_input: CrawlerInput):
    try:
        status = await crawler_manager.start(**crawler_input.dict())
    except RuntimeError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

    return {"message": "crawler task scheduled", "data": status}


@qq_email.post("/stop")
async def stop_crawler():
    try:
        status = await crawler_manager.stop()
    except RuntimeError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

    return {"message": "stop signal sent", "data": status}


@qq_email.get("/status")
async def get_status():
    return {"data": crawler_manager.status}


@qq_email.get("/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "running": crawler_manager.is_running,
    }


@qq_email.on_event("shutdown")
async def _shutdown_event() -> None:
    if crawler_manager.is_running:
        try:
            await crawler_manager.stop()
        except RuntimeError:
            # If another stop call already cleaned things up we can ignore it.
            pass
