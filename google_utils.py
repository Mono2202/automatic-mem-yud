from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

class GoogleUtils:
    @staticmethod
    def get_google_creds(scopes):
        store = file.Storage("token.json")
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets("credentials.json", scopes)
            credentials = tools.run_flow(flow, store)
        return credentials

    @staticmethod
    def get_google_forms_service(credentials, discovery_doc):
        return discovery.build(
            "forms",
            "v1",
            http=credentials.authorize(Http()),
            discoveryServiceUrl=discovery_doc,
        )

    @staticmethod
    def get_google_drive_service(credentials):
        return discovery.build(
            "drive",
            "v3",
            credentials=credentials
        )
