from page.Flask_Blog_Page.index_page import IndexPage
from setting import INDEX_URL
import pytest
from conftest import read_data


class TestLogo:
    def test_logo(self, broswer):
        """logo-图片url"""
        page = IndexPage(broswer)
        page.open_url(INDEX_URL)
        logo_url = page.get_logo_url()
        assert logo_url == 'http://localhost:5000/blog/static/img/logo.png'


class TestNavbar:
    def test_navbar_index_text(self, broswer):
        """导航栏_首页按钮-显示文本"""
        page = IndexPage(broswer)
        page.open_url(INDEX_URL)
        index_text = page.get_index_btn_text()
        assert index_text == '首页'

    def test_navbar_2_text(self, broswer):
        """导航栏_第二个导航按钮-显示文本"""
        page = IndexPage(broswer)
        page.open_url(INDEX_URL)
        navbar_2_text = page.get_navbar_btn_2_text()
        assert navbar_2_text == 'python'

    def test_navbar_3_text(self, broswer):
        """导航栏_第三个导航按钮-显示文本"""
        page = IndexPage(broswer)
        page.open_url(INDEX_URL)
        navbar_3_text = page.get_navbar_btn_3_text()
        assert navbar_3_text == 'flask'

    def test_index_click(self, broswer):
        """导航栏_首页按钮-点击跳转"""
        page = IndexPage(broswer)
        page.open_url(INDEX_URL)
        page.click_index_btn()
        # 添加截屏功能
        index_url = page.get_current_url()
        assert index_url == 'http://localhost:5000/'

    def test_navbar_2_click(self, broswer):
        """导航栏_第二个导航按钮-点击跳转"""
        page = IndexPage(broswer)
        page.open_url(INDEX_URL)
        page.click_navbar_btn_2()
        # 添加截屏功能
        navbar_2_url = page.get_current_url()
        assert navbar_2_url == 'http://localhost:5000/blog/category/10'

    def test_navbar_3_click(self, broswer):
        """导航栏_第三个导航按钮-点击跳转"""
        page = IndexPage(broswer)
        page.open_url(INDEX_URL)
        page.click_navbar_btn_3()
        # 添加截屏功能
        navbar_3_url = page.get_current_url()
        assert navbar_3_url == 'http://localhost:5000/blog/category/11'


class TestLogin:
    def test_login_text(self, broswer):
        """登录按钮-显示文本"""
        page = IndexPage(broswer)
        page.open_url(INDEX_URL)
        login_text = page.get_login_btn_text()
        assert login_text == 'Log in'

    def test_login_click(self, broswer):
        """登录按钮-点击跳转"""
        page = IndexPage(broswer)
        page.open_url(INDEX_URL)
        page.click_login_btn()
        # 添加截屏功能
        login_url = page.get_current_url()
        assert login_url == 'http://localhost:5000/auth/login'


class TestSignup:
    def test_signup_text(self, broswer):
        """注册按钮-显示文本"""
        page = IndexPage(broswer)
        page.open_url(INDEX_URL)
        signup_text = page.get_signup_btn_text()
        assert signup_text == 'Sign up'

    def test_login_click(self, broswer):
        """注册按钮-点击跳转"""
        page = IndexPage(broswer)
        page.open_url(INDEX_URL)
        page.click_signup_btn()
        # 添加截屏功能
        signup_url = page.get_current_url()
        assert signup_url == 'http://localhost:5000/auth/register'


if __name__ == '__main__':
    pytest.main(['-vs'])
