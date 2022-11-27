import os, sys, json
from unittest import mock

sys.path.append('../src')
from RequestHandler import handle, Result

TESTS_DIR = "tests"
OKGREEN = '\033[92m'
FAILRED = '\033[91m'


def get_mocked_closure(resp_json):
    def mocked(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse(resp_json, 200)

    return mocked


def run_test(resp_json, ans_json):
    @mock.patch('requests.get', side_effect=get_mocked_closure(resp_json))
    def test_closure(self):
        return handle(len(resp_json), lambda x: x)[1] == ans_json

    return test_closure()


if __name__ == '__main__':
    test_dirs = [f.path for f in os.scandir(TESTS_DIR) if f.is_dir()]
    for test_dir in test_dirs:
        with open(f'{test_dir}/response.json') as resp:
            with open(f'{test_dir}/answer.json') as ans:
                passed = run_test(json.load(resp), json.load(ans))
                if passed:
                    print(f"{OKGREEN}{test_dir} passed")
                else:
                    print(f"{FAILRED}{test_dir} failed")
