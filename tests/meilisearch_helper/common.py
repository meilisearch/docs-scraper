MASTER_KEY = "masterKey"
BASE_URL = "http://127.0.0.1:7700"

DEFAULT_INDEX = 'index_uid'

DEFAULT_DATA_DELETE = {
                        "taskUid": 1,
                        "indexUid": DEFAULT_INDEX,
                        "status": "enqueued",
                        "type": "indexDeletion",
                        "enqueuedAt": "2023-03-30T13:24:01.789654093Z"
                        }
DEFAULT_DATA_PATCH = {
                        "taskUid": 1,
                        "indexUid": DEFAULT_INDEX,
                        "status": "enqueued",
                        "type": "settingsUpdate",
                        "enqueuedAt": "2023-03-30T13:24:01.789654093Z"
                    }

DEFAULT_ACCEPTED_STATUS = 202
