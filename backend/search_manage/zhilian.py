import asyncio
from typing import Optional

from config import _get_config_path
from search_manage.base import baseManage
import json
import os
import sys

domain = ".zhaopin.com"


async def _load_config() -> dict:
    path = _get_config_path()
    if not os.path.exists(path):
        print("未找到配置文件")
        return {"cookies": None}
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            print("已找到配置文件", path)
            data = json.load(f) or {}
            # print(data)
    except Exception as e:
        print("配置文件格式错误",e)
        return {"cookies": None}
    cookies = data.get("zhilian_cookie") or None
    return {"cookies": cookies}


class ZhiLian(baseManage):
    def __init__(self, chrome_driver_path, searchKey: str, start_page: Optional[int] = 0, page_size: Optional[int] = 2):
        self.search_keywords = searchKey
        self.start_page = start_page
        self.page_size = page_size
        super().__init__(chrome_driver_path)

    async def work(self, path):
        await asyncio.sleep(2)
        await self.page.goto(path)
        elements = await self.page.querySelectorAll(".collect-and-apply__btn")
        for element in elements:
            await self.scroll_to_element(element)
            await asyncio.sleep(2)
            await element.click()
            await asyncio.sleep(5)
            await self.close_last_tab()

    async def close_last_tab(self):
        pages = await self.browser.pages()
        if len(pages) > 1:  # 如果有多个标签页
            last_page = pages[-1]  # 获取最后一个页面
            await last_page.close()
            print(f"已关闭最后一个标签页，剩余 {len(pages) - 1} 个标签页")
        else:
            print("只有一个标签页，不执行关闭操作")

    async def main(self):
        cookies = (await _load_config()).get("cookies")
        await self.setBrowser()
        cookiesSet = [
            {"name": key, "value": value, "domain": domain}
            for key, value in cookies.items()  # 使用 .items() 获取键值对
        ]
        await self.page.setCookie(*cookiesSet)
        await asyncio.sleep(5)
        for i in range(self.start_page, self.start_page + self.page_size):
            path = f"https://www.zhaopin.com/sou/jl653/kwA96NLRO/p{self.start_page}?kt=3"
            await self.work(path)


if __name__ == "__main__":
    zhilian = ZhiLian(r"C:\Program Files\Google\Chrome\Application\chrome.exe", "前端", 0)
    # try:
    asyncio.get_event_loop().run_until_complete(zhilian.main())
    # except Exception as e:
    #     print("任务已停止", e)
