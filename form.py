from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
from google_utils import GoogleUtils

class Form:
    SCOPES = [
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/forms.body"
    ]
    DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

    def __init__(self, title: str, name: str):
        self._title = title
        self._name = name
        self._google_credentials = GoogleUtils.get_google_creds(self.SCOPES)
        self._google_forms_service = GoogleUtils.get_google_forms_service(self._google_credentials, self.DISCOVERY_DOC)
        self._google_drive_service = GoogleUtils.get_google_drive_service(self._google_credentials)
        self._index = 0

    def create_form(self):
        form = {
            "info": {
                "title": self._title,
            },
        }
        result = self._google_forms_service.forms().create(body=form).execute()
        self._form_id = result["formId"]
        self.rename_form()

    def rename_form(self):
        self._google_drive_service.files().update(
            fileId=self._form_id,
            body={"name": self._name}
        ).execute()    

    def update_form_info(self, info: dict):
        metadata = {
            "requests": [
                {
                    "updateFormInfo": info
                }
            ]
        }
        self._google_forms_service.forms().batchUpdate(formId=self._form_id, body=metadata).execute()

    def update_form_body(self, requests: list[dict]):
        for request in requests:
            request["createItem"]["location"] = {"index": self._index}
            self._index += 1

        metadata = {
            "requests": requests
        }
        self._google_forms_service.forms().batchUpdate(formId=self._form_id, body=metadata).execute()
