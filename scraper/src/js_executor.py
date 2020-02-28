import time
import json


class JsExecutor:
    driver = None

    def __init__(self):
        self.driver = JsExecutor.driver

    # TODO: find out why JsExecutor.driver couldn't be used
    def execute(self, url, js):
        self.driver.get(url)
        time.sleep(5)

        result = self.driver.execute_script(js)

        try:
            parsed_result = json.loads(result)
            return parsed_result
        except ValueError:
            raise ValueError('CONFIG is not a valid JSON')
