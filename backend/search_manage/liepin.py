import asyncio
from typing import Optional
from search_manage.base import baseManage

domain = ".liepin.com"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]


class LiepinSearch(baseManage):

    def __init__(self, chrome_driver_path, searchKey: str, start_page: Optional[int] = 0, page_size: Optional[int] = 2):
        self.search_keywords = searchKey
        self.start_page = start_page
        self.page_size = page_size
        super(LiepinSearch, self).__init__(chrome_driver_path)

    async def scroll_to_bottom(self):
        """
        滚动到页面底部
        """
        try:
            await self.page.evaluate('''() => {
                window.scrollTo({
                    top: document.body.scrollHeight,
                    behavior: 'smooth'
                });
            }''')
            print("已滚动到页面底部")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"滚动到底部失败: {e}")

    async def scroll_by_offset(self, x_offset=0, y_offset=300):
        """
        按偏移量滚动页面

        Args:
            x_offset: 水平滚动偏移量
            y_offset: 垂直滚动偏移量
        """
        try:
            await self.page.evaluate(f'''() => {{
                window.scrollBy({{x: {x_offset}, y: {y_offset}, behavior: 'smooth'}});
            }}''')
            print(f"已按偏移量滚动: x={x_offset}, y={y_offset}")
            await asyncio.sleep(1)
        except Exception as e:
            print(f"按偏移量滚动失败: {e}")

    async def get_scroll_position(self):
        """
        获取当前滚动位置

        Returns:
            dict: 包含 scrollX 和 scrollY 的字典
        """
        try:
            position = await self.page.evaluate('''() => {
                return {
                    scrollX: window.scrollX,
                    scrollY: window.scrollY
                };
            }''')
            return position
        except Exception as e:
            print(f"获取滚动位置失败: {e}")
            return None

    async def work(self):

        elements = await self.page.querySelectorAll(".job-card-right-box")

        for element in elements:
            try:
                # hover在元素上
                # 获取目标元素的选择器
                await self.scroll_to_element(element)
                await element.hover()
                # 等待3秒
                await asyncio.sleep(3)

                # 获得element内部.chat-btn-box的元素
                chat_button = await element.querySelector(".chat-btn-box")
                if chat_button:
                    # 获取元素的边界框位置
                    bounding_box = await chat_button.boundingBox()
                    if bounding_box:
                        # 移动鼠标到元素中心位置
                        x = bounding_box['x'] + bounding_box['width'] / 2
                        y = bounding_box['y'] + bounding_box['height'] / 2
                        await self.page.mouse.move(x, y)
                        await asyncio.sleep(0.5)  # 短暂等待
                        await self.page.mouse.click(x, y)  # 点击
                        print("已通过鼠标点击聊天按钮")
                        await asyncio.sleep(1)
                        file_send = await self.page.querySelector(".im-ui-action-button.action-item.action-resume")
                        if file_send:
                            await file_send.click()
                            await asyncio.sleep(1)
                            confirm = await self.page.querySelector(
                                ".ant-im-modal-confirm-btns .ant-im-btn.ant-im-btn-primary")
                            await confirm.click()
                        else:
                            print("未找到发送文件按钮")
                            await asyncio.sleep(1)

                        chat_box = await self.page.querySelector(".ant-im-modal-content")
                        chat_box_close = await chat_box.querySelector(".anticon-close")
                        await asyncio.sleep(0.5)
                        await chat_box_close.click()
                        print("已关闭聊天框")
                    else:
                        print("无法获取聊天按钮位置")
                else:
                    print("未找到聊天按钮，跳过该职位")

            except Exception as e:
                print(f"处理职位时出错: {e}")
                continue

        await self.page.close()

    async def main(self):
        await self.setBrowser()
        cookiesSet = [
            {"name": key, "value": value, "domain": domain}
            for key, value in cookies.items()  # 使用 .items() 获取键值对
        ]
        print(cookiesSet)
        await self.page.setCookie(*cookiesSet)
        # current_timestamp = int(time.time() * 1000)
        for i in range(self.start_page, self.start_page + self.page_size):
            await self.page.goto(
                f"https://www.liepin.com/zhaopin/?city=070020&dq=070020&pubTime=&currentPage={str(self.start_page)}&pageSize=40&key={self.search_keywords}&suggestTag=&workYearCode=2&compId=&compName=&compTag=&industry=&salaryCode=&jobKind=&compScale=&compKind=&compStage=&eduLevel=&otherCity=&ckId=3wml1vc9u55vctt7y4bx46i41uh1anb9&scene=condition&skId=b5iqyfmrfgaftc2a8n9zvaavilwy4tua&fkId=3wml1vc9u55vctt7y4bx46i41uh1anb9&sfrom=search_job_pc&suggestId=")
            print("已打开页面")
            await asyncio.sleep(10)
            await self.work()

        await self.page.close()
        await self.browser.close()



if __name__ == "__main__":
    boss_search = LiepinSearch(r"C:\Program Files\Google\Chrome\Application\chrome.exe", "前端", 0)
    asyncio.get_event_loop().run_until_complete(boss_search.main())
