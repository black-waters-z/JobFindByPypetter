import asyncio
import random
from typing import Optional

import pyppeteer
from pyppeteer_stealth import stealth

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]


class baseManage():
    def __init__(self, chrome_driver_path):
        self.browser = None
        self.chrome_driver_path = chrome_driver_path
        self.page = None

    async def setBrowser(self):
        user_agent = random.choice(USER_AGENTS)
        self.browser = await pyppeteer.launch(
            executablePath=self.chrome_driver_path,
            headless=False,
            handleSIGINT=False,  # 禁用信号处理
            handleSIGTERM=False,  # 禁用信号处理
            handleSIGHUP=False,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-infobars',
                '--disable-dev-shm-usage',
                # '--start-maximized',  # 启动时最大化窗口
                # '--kiosk',
                f'--user-agent={user_agent}'
            ]
        )
        self.page = await self.browser.newPage()
        await self.page.setViewport({'width': 1366, 'height': 768})
        await stealth(self.page)

    async def stop(self):
        await self.browser.close()
        return "任务已停止"

    async def scroll_to_element(self, element):
        """
        滚动到指定元素

        Args:
            element: 要滚动到的元素对象
        """
        try:
            # 方法1: 使用 scrollIntoView JavaScript API
            await self.page.evaluate('''(element) => {
                element.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center',
                    inline: 'center'
                });
            }''', element)
            print("已使用 scrollIntoView 滚动到元素")

        except Exception as e:
            print(f"scrollIntoView 方法失败: {e}")
            try:
                # 方法2: 手动计算位置并滚动
                bounding_box = await element.boundingBox()
                if bounding_box:
                    x = bounding_box['x']
                    y = bounding_box['y']
                    # 滚动到元素位置，稍微偏移以确保元素在视窗中央
                    await self.page.evaluate(f'''() => {{
                        window.scrollTo({{
                            top: {y} - window.innerHeight/2,
                            left: {x} - window.innerWidth/2,
                            behavior: 'smooth'
                        }});
                    }}''')
                    print("已使用手动滚动方法滚动到元素")
                else:
                    print("无法获取元素边界框")

            except Exception as e2:
                print(f"手动滚动方法也失败: {e2}")

        # 等待滚动完成
        await asyncio.sleep(2)