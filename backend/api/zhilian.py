from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from search_manage import ZhiLian
from fastapi import APIRouter, HTTPException, BackgroundTasks

zhilian_router = APIRouter(prefix="/zhilian", tags=["智联投递"])

running_tasks = {}
task_status = {}


class ZhilianInput(BaseModel):
    chrome_driver_path: str = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    searchKey: str
    start_page: Optional[int] = 0
    page_size: Optional[int] = 2


@zhilian_router.post("/start")
async def start_crawler(background_tasks: BackgroundTasks, zhilian_input: ZhilianInput):
    zhilian_crawler = ZhiLian(
        chrome_driver_path=zhilian_input.chrome_driver_path,
        searchKey=zhilian_input.searchKey,
        start_page=zhilian_input.start_page,
        page_size=zhilian_input.page_size
    )
    background_tasks.add_task(zhilian_crawler.main)
    task_id = f"zhilian_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    running_tasks[task_id] = zhilian_crawler
    task_status[task_id] = {
        "task_id": task_id,
        "status": "running",
        "start_time": datetime.now(),
        "message": "任务已开始"
    }
    return task_status[task_id]


@zhilian_router.get("/status")
async def get_status():
    return task_status


@zhilian_router.post("/stop")
async def stop_crawler(task_id: str):
    if task_id in running_tasks:
        await running_tasks[task_id].stop()
        task_status[task_id] = {
            "status": "stopped",
            "end_time": datetime.now(),
            "message": "任务已停止"
        }
        running_tasks.pop(task_id)
        return {"message": "任务已停止"}
    else:
        raise HTTPException(status_code=404, detail="任务未找到")
