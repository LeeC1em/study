from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from page.Flask_Blog_Page.index_page import IndexPage


browser = webdriver.Chrome()
page = IndexPage(browser)
page.open_url('http://localhost:5000/')

browser.quit()
