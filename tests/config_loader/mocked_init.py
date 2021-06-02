# coding: utf-8
class MockedInit:
    def __init__(self, expected_response=None):
        self.expected_response = expected_response

        if self.expected_response is None:
            self.expected_response = "[]"

    def implicitly_wait(self, time):
        return

    def get(self, url):
        return ""

    def execute_script(self, js):
        return self.expected_response

    def quit(self):
        return
