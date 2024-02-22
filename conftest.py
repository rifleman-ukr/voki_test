from datetime import datetime

from appium import webdriver
from appium.options.android import UiAutomator2Options
from pytest import fixture

from test_utils import take_screenshot


@fixture(scope='session', autouse=True)
def driver_options():
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.udid = 'emulator-5554'
    options.app_package = 'com.playrix.manormatters'
    options.app_activity = 'com.playrix.manormatters.GoogleActivity'
    options.device_name = 'Pixel 3 API 34'
    options.automation_name = 'UiAutomator2'
    options.platformVersion = '13'
    options.auto_grant_permissions = True
    return options


@fixture(scope='session', autouse=True)
def driver(driver_options):
    return webdriver.Remote('http://127.0.0.1:4723', options=driver_options)


@fixture(scope='session', autouse=True)
def finalizer(driver, request):
    yield
    if request.node.testsfailed != 0:
        take_screenshot(driver, True, f'fail_{datetime.now().strftime("%m-%d-%Y_%H-%M-%S")}')
    driver.quit()
