import asyncio
from typing import Optional
from search_manage.base import baseManage

cookies = {
    "x-zp-client-id": "b31754cb-2bfc-4648-bc8d-73cf1bc580de",
    "sajssdk_2015_cross_new_user": "1",
    "sensorsdata2015jssdkchannel": "%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D",
    "Hm_lvt_7fa4effa4233f03d11c7e2c710749600": "1772387159",
    "HMACCOUNT": "AA3CE71C2045380C",
    "LastCity": "%E6%9D%AD%E5%B7%9E",
    "LastCity%5Fid": "653",
    "x-zp-device-sn": "daedc35641f14b02b5ffc16fc127b85c",
    "zp_passport_deepknow_sessionId": "e6c8fde6s39e9d4908b2e60d1021c2fd8376",
    "at": "42709bd62e054e8eb7453e19de9c0138",
    "rt": "26880679beb6433e8a77a2e71fa1e495",
    "sts_deviceid": "19caa82689ad72-03236406fd4fb3-4c657b58-1327104-19caa82689b1300",
    "sts_sg": "1",
    "sts_chnlsid": "Unknown",
    "zp_src_url": "https%3A%2F%2Fpassport.zhaopin.com%2F",
    "ZP_OLD_FLAG": "false",
    "locationInfo_search": "{%22code%22:%22%22}",
    "selectCity_search": "653",
    "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%221249986758%22%2C%22first_id%22%3A%2219caa81c1892d9-0b76c3ab70717f-4c657b58-1327104-19caa81c18a505%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTljYWE4MWMxODkyZDktMGI3NmMzYWI3MDcxN2YtNGM2NTdiNTgtMTMyNzEwNC0xOWNhYTgxYzE4YTUwNSIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjEyNDk5ODY3NTgifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221249986758%22%7D%2C%22%24device_id%22%3A%2219caa81c1892d9-0b76c3ab70717f-4c657b58-1327104-19caa81c18a505%22%7D",
    "Hm_lpvt_7fa4effa4233f03d11c7e2c710749600": "1772437267",
    "ZL_REPORT_GLOBAL": "{%22//www%22:{%22seid%22:%2242709bd62e054e8eb7453e19de9c0138%22%2C%22actionid%22:%22fe3f611f-f424-4afa-8852-be86d91a717a-cityPage%22}%2C%22jobs%22:{%22recommandActionidShare%22:%222584dccb-90ea-4b38-ba0f-eead7cc9d460-job%22}}"
}

domain = ".zhaopin.com"


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
    try:
        asyncio.get_event_loop().run_until_complete(zhilian.main())
    except Exception as e:
        print("任务已停止",e)
