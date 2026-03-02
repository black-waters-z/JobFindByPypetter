import asyncio
import aiofiles as aiofiles
import pyppeteer
from search_manage.base import baseManage
from config import cookies


class WorkSearch(baseManage):
    def __init__(self, file_path: str, chrome_driver_path, search_file_path: str):
        self.file_path = file_path
        self.search_file_path = search_file_path
        self.search_keywords = []
        self.page = None
        super().__init__(chrome_driver_path)

    async def setBrowser(self):
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
                '--disable-dev-shm-usage'
            ]
        )
        self.page = await self.browser.newPage()

    async def verify_cookies(self):
        """验证cookie是否正确设置"""
        try:
            # 获取当前页面的所有cookie
            current_cookies = await self.page.cookies('https://wx.mail.qq.com')
            print(f"当前页面cookie数量: {len(current_cookies)}")

            # 检查关键cookie是否存在
            cookie_names = [cookie['name'] for cookie in current_cookies]
            required_cookies = ['sid', 'xm_sid', 'xm_uin']

            for required_cookie in required_cookies:
                if required_cookie in cookie_names:
                    print(f"✓ {required_cookie} cookie 存在")
                else:
                    print(f"✗ {required_cookie} cookie 缺失")

        except Exception as e:
            print(f"验证cookie失败: {e}")

    async def goToPage(self, email: str, subject: str):
        # 跳转到目标页面
        await self.page.setCookie(*cookies)
        await self.verify_cookies()
        await self.page.goto('https://wx.mail.qq.com/', {'waitUntil': 'domcontentloaded'})
        await asyncio.sleep(2)
        switch_bt = await self.page.querySelector('div.frame-sidebar-compose-btn')
        await switch_bt.click()
        await asyncio.sleep(5)
        # 1. 定位并点击收件人输入框
        receiver_editor = await self.page.querySelector('div.xmail-cmp-accounts-editor.receiver-editor')
        await receiver_editor.click()
        # 2. 输入邮箱地址
        await self.page.keyboard.type(email, delay=50)

        await self.page.evaluate('''() => {
            const event = new KeyboardEvent('keydown', { key: 'Enter' });
            document.activeElement.dispatchEvent(event);
        }''')
        await self.page.keyboard.press('Enter', delay=50)
        await self.page.keyboard.press('Enter', delay=50)

        await asyncio.sleep(5)

        # 3. 定位并点击主题输入框
        subject_input = await self.page.querySelector('div.mail-compose-subject > input.subject-input')
        await subject_input.click()

        # 4. 输入主题
        await self.page.keyboard.type(subject, delay=100)

        # 5. 拖拽附件
        file_path = self.file_path
        input_file = await self.page.querySelector('input[type="file"]')
        await input_file.uploadFile(file_path)
        await asyncio.sleep(5)
        # 6. 点击指定 class 的按钮
        button = await self.page.querySelector('.xmail-ui-btn.ui-btn-size32.ui-btn-border.ui-btn-them-blue-lighten')
        if button:
            await button.click()
            print("按钮已点击")
        else:
            print("未找到指定按钮")
        # 截图保存结果（可选）
        await self.page.screenshot({'path': 'result.png'})
        await asyncio.sleep(5)

    async def read_and_process_search_file(self, file_path):
        # 异步打开文件
        async with aiofiles.open(file_path, mode='r', encoding='utf-8') as file:
            async for line in file:
                # 去除行末的换行符并分割内容
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    email = parts[0]
                    subject = parts[1]
                    self.search_keywords.append((email, subject))

                    print(f"邮箱: {email}, 投递主题: {subject}")
                else:
                    print("无效的行格式:", line)

    async def main(self):

        # await self.goToPage()
        await self.setBrowser()
        await self.read_and_process_search_file(self.search_file_path)
        for (email, subject) in self.search_keywords:
            await self.goToPage(email, subject)
            await asyncio.sleep(10)
        await self.browser.close()


# if __name__ == '__main__':
#     work_search = WorkSearch()
#     asyncio.get_event_loop().run_until_complete(work_search.main())
