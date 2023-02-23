from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, broswer):
        self.broswer = broswer

    def open_url(self, url):
        """打开url"""
        self.broswer.get(url)

    def get_current_url(self):
        """获取当前网页的url"""
        return self.broswer.current_url

    def locator_element(self, *args):
        """元素定位"""
        # 通过 显示等待 完成统一的元素定位
        # 不管是通过id/name/class等方式，都用此函数定位
        return WebDriverWait(self.broswer, 5).until(EC.presence_of_element_located(*args))
