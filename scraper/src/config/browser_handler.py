import re
import os
from sys import platform
from distutils.util import strtobool
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from ..custom_downloader_middleware import CustomDownloaderMiddleware
from ..js_executor import JsExecutor


class BrowserHandler:
    @staticmethod
    def conf_need_browser(config_original_content, js_render):
        group_regex = re.compile(r'\(\?P<(.+?)>.+?\)')
        results = re.findall(group_regex, config_original_content)

        return len(results) > 0 or js_render

    @staticmethod
    def init(config_original_content, js_render, user_agent):
        driver = None

        if BrowserHandler.conf_need_browser(config_original_content,
                                            js_render):
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('user-agent={0}'.format(user_agent))

            CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH', '')
            if not CHROMEDRIVER_PATH or not os.path.isfile(CHROMEDRIVER_PATH):
                print("Could not find ChromeDriver.")
                print("Either the Env CHROMEDRIVER_PATH='{}' path is incorrect or "
                      "ChromeDriver is not installed.".format(CHROMEDRIVER_PATH))
                print("Do you want to automatically download ChromeDriver?")
                while(True):
                    user_input = input("[Y/n]: ")
                    try:
                        yes = strtobool(user_input)
                        break
                    except ValueError:
                        print("Please enter a valid input.")
                        continue
                if yes:
                    try:
                        CHROMEDRIVER_PATH = ChromeDriverManager().install()

                    except Exception as e:
                        print("Could not download ChromeDriver. "
                              "Please install ChromeDriver manually.")
                        print(e)
                        if platform == "linux" or platform == "darwin":
                            os.system('read -s -n 1 -p "Press any key to continue..."')
                        if platform == "win32":
                            os.system('pause')
                        exit(1)
                else:
                    print("Please install ChromeDriver and set the CHROMEDRIVER_PATH "
                          "environment variable or remove the render_js option.")
                    if platform == "linux" or platform == "darwin":
                        os.system('read -s -n 1 -p "Press any key to continue..."')
                    if platform == "win32":
                        os.system('pause')
                    exit(1)

            driver = webdriver.Chrome(
                CHROMEDRIVER_PATH,
                options=chrome_options)
            CustomDownloaderMiddleware.driver = driver
            JsExecutor.driver = driver
        return driver

    @staticmethod
    def destroy(driver):
        # Start browser if needed
        if driver is not None:
            driver.quit()
            driver = None

        return driver
