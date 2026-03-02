from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from search_manage import LiepinSearch

from fastapi import APIRouter, HTTPException, BackgroundTasks

liepin = APIRouter(prefix="/liepin", tags=["猎聘投递"])

running_tasks = {}
task_status = {}


class LiepinSearchInput(BaseModel):
    chrome_driver_path: Optional[str] = ""
    search_key: Optional[str] = ""
    start_page: Optional[int] = 1
    page_size: Optional[int] = 10


class StopTaskRequest(BaseModel):
    reason: Optional[str] = "用户主动停止"


@liepin.post("/start")
async def start_crawler(background_tasks: BackgroundTasks, liepin_input: LiepinSearchInput):
    try:
        task_id = f"liepin_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        task_status[task_id] = {
            "status": "running",
            "start_time": datetime.now(),
            "message": "任务已启动"
        }
        liepin_search = LiepinSearch(
            chrome_driver_path=liepin_input.chrome_driver_path or r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            searchKey=liepin_input.search_key,
            start_page=liepin_input.start_page,
            page_size=liepin_input.page_size
        )
        running_tasks[task_id] = liepin_search
        # 将爬虫任务添加到后台任务队列
        background_tasks.add_task(run_crawler_task, task_id, liepin_search)

        return {
            "task_id": task_id,
            "status": "started",
            "message": "爬虫任务已在后台启动"
        }
    except Exception as exc:
        raise HTTPException(status_code=409, detail=str(exc))


async def run_crawler_task(task_id: str, crawler_instance: LiepinSearch):
    """
    实际执行爬虫任务的函数
    """
    try:
        print(f"开始执行任务: {task_id}")
        task_status[task_id]["message"] = "正在执行爬虫任务..."

        # 执行爬虫主逻辑
        await crawler_instance.main()

        # 更新任务完成状态
        task_status[task_id].update({
            "status": "completed",
            "end_time": datetime.now(),
            "message": "任务执行完成"
        })
        print(f"任务完成: {task_id}")

    except Exception as e:
        # 更新任务错误状态
        task_status[task_id].update({
            "status": "failed",
            "end_time": datetime.now(),
            "error": str(e),
            "message": f"任务执行失败: {str(e)}"
        })
        print(f"任务失败: {task_id}, 错误: {str(e)}")


@liepin.get("/status")
async def get_status():
    return task_status


@liepin.get("/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "active_tasks": len([t for t in task_status.values() if t["status"] == "running"])
    }


@liepin.post("/stop")
async def stop_all_crawlers(stop_request: StopTaskRequest = None):
    """停止所有运行中的爬虫任务"""
    stopped_tasks = []

    for task_id, crawler_instance in list(running_tasks.items()):
        try:
            await crawler_instance.stop()
            if task_id in task_status:
                task_status[task_id].update({
                    "status": "stopped",
                    "end_time": datetime.now(),
                    "message": f"任务已停止: {stop_request.reason if stop_request else '批量停止'}"
                })
            stopped_tasks.append(task_id)
        except Exception as e:
            print(f"停止任务 {task_id} 时出错: {e}")

    # 清空运行中任务列表
    running_tasks.clear()

    return {
        "message": f"已停止 {len(stopped_tasks)} 个任务",
        "stopped_tasks": stopped_tasks
    }
#
# @liepin.on_event("shutdown")
# async def _shutdown_event():
#     pass
