import time
from selenium import webdriver
import pytest
import os


class Testcase():
    def test_case_01(self):
        driver = webdriver.Chrome()
        driver.get("https://www.baidu.com")
        time.sleep(2)
        driver.quit()


if __name__ == '__main__':
    pytest.main(['-s', '--alluredir', 'report/result', 'test.py'])
    split = 'allure ' + 'generate ' + './report/result ' + '-o ' + './report/html ' + '--clean'
    os.system(split)
    os.system("allure open -h 127.0.0.1 -p 8083 ./report/html")