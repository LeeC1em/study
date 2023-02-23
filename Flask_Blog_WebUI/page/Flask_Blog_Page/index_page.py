from page.base_page import BasePage
from selenium.webdriver.common.by import By
# from setting import NAVBAR_NUM
from selenium.common.exceptions import TimeoutException


class IndexPage(BasePage):
    login_btn_loc = (By.CSS_SELECTOR, '.buttons .is-light')
    signup_btn_loc = (By.CSS_SELECTOR, '.buttons .is-primary')
    logo_loc = (By.CSS_SELECTOR, '.navbar-item img')
    index_btn_loc = (By.CSS_SELECTOR, '.navbar-start a:first-child')
    navbar_btn_2_loc = (By.CSS_SELECTOR, '.navbar-start a:nth-child(2)')
    navbar_btn_3_loc = (By.CSS_SELECTOR, '.navbar-start a:nth-child(3)')

    def get_element(self, element_loc):
        """获得节点"""
        return self.locator_element(element_loc)

    def get_logo_url(self):
        """获得logo图片url"""
        return self.get_element(self.logo_loc).get_attribute('src')

    def get_index_btn_text(self):
        """获取首页按钮的文本值"""
        return self.get_element(self.index_btn_loc).text

    def click_index_btn(self):
        """点击首页"""
        self.get_element(self.index_btn_loc).click()

    def get_navbar_btn_2_text(self):
        """获取导航栏第二个按钮的文本值"""
        return self.get_element(self.navbar_btn_2_loc).text

    def click_navbar_btn_2(self):
        """点击导航栏第二个按钮"""
        self.get_element(self.navbar_btn_2_loc).click()

    def get_navbar_btn_3_text(self):
        """获取导航栏第三个按钮的文本值"""
        return self.get_element(self.navbar_btn_3_loc).text

    def click_navbar_btn_3(self):
        """点击导航栏第三个按钮"""
        self.get_element(self.navbar_btn_3_loc).click()

    def get_login_btn_text(self):
        """获取登录按钮的文本值"""
        return self.get_element(self.login_btn_loc).text

    def click_login_btn(self):
        """点击登录"""
        self.get_element(self.login_btn_loc).click()

    def get_signup_btn_text(self):
        """获取注册按钮的文本值"""
        return self.get_element(self.signup_btn_loc).text

    def click_signup_btn(self):
        """点击注册"""
        self.get_element(self.signup_btn_loc).click()

    # navbar_css = '.navbar-start a:nth-child({n})'
    #
    # def get_navbar_list(self):
    #     """获得导航栏节点列表"""
    #     navbar_list = []
    #     try:
    #         for n in range(1, NAVBAR_NUM + 1):
    #             navbar_loc = (By.CSS_SELECTOR, self.navbar_css.format(n=n))
    #             navbar_list.append(self.get_element(navbar_loc))
    #         return navbar_list
    #     except TimeoutException:
    #         return navbar_list
    #
    # def get_navbar_text_list(self):
    #     text_list = []
    #     navbar_list = self.get_navbar_list()
    #     for navbar in navbar_list:
    #         text_list.append(navbar.text)
    #     return text_list
