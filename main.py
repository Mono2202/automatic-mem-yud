from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

from datetime import datetime
from dateutil import tz

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/forms.body"
]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
TIMEZONE = tz.gettz("Asia/Jerusalem")
HEBREW_DAYS = [
    "ראשון",
    "שני",
    "שלישי",
    "רביעי",
    "חמישי",
    "שישי",
    "שבת"
]
DESCRIPTION = """\u202Bהיי! כמו בכל יום מ״י!
מקווים שהיה יום מהנה ומלמד :)
מעכשיו המ"י יעבור בלוז מוגדר במהלך היום - כרגע בעזרת לפטופים ומי שלא יקבל ימלא בדף ואז בטלפון בסוף השעת טש.
המטרה היא להקל כמה שיותר על המילוי ושזה לא יפול על השעת טש
אנחנו עובדים על אישור לשימוש בטלפון בזמן הלוז - כרגע אין אישור רשמי
מספר נקודות חדשות במ"י: 
1. השאלות של הדירוג הם אינם חובה! המטרה היא שמי שלא היה במופע לא ידרג (או מי שהעביר את המופע)
2. שיפור ושימור זה חובה, אם לא הייתם במופע תכתבו "לא הייתי" בשיפור ובשימור
3. למופעים יהיו תיאורים ושאלות מנחות על מנת להקל עליכם - השאלות המנחות הן לא חובה אלא נועדו לעזור לכם
4. תנסו כמה שיותר לדקור נקודות מהפקלון מישוב כדי לתמצת את המישוב שלכם (תפרטו ותסבירו את הנקודה כמובן)
5. הוספנו פקלון מישוב כדי להקל עליכם 
6. נוספה שאלה חדשה - "משהו שלקחתי/למדתי מהיום" המטרה היא לקבל תמונה יותר טובה על מה היה לכם משמעותי באותו היום\u202C"""
PAKALON_MISHUV_FILE_ID = "1T6yEF90wd0RZjPbJC0ZT8EFTx8baLg86"

def get_google_creds():
    store = file.Storage("token.json")
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
        creds = tools.run_flow(flow, store)
    return creds


def get_google_forms_service(credentials):
    return discovery.build(
        "forms",
        "v1",
        http=credentials.authorize(Http()),
        discoveryServiceUrl=DISCOVERY_DOC,
    )


def get_google_drive_service(credentials):
    return discovery.build(
        "drive",
        "v3",
        credentials=credentials
    )


def create_form(google_forms_service, title: str):
    form = {
        "info": {
            "title": title,
        },
    }
    result = google_forms_service.forms().create(body=form).execute()
    return result["formId"]


def rename_form(google_drive_service, form_id: str, name: str):
    google_drive_service.files().update(
        fileId=form_id,
        body={"name": name}
    ).execute()    


def get_daily_form_title():
    now = datetime.now(TIMEZONE)
    return f'מ"י יום {HEBREW_DAYS[(now.weekday() + 1) % 7]} {now.day}.{now.month}'


def daily_form_prologue(google_forms_service, form_id: str):
    update = {
        "requests": [
            {
                "updateFormInfo": {
                    "info": {
                        "description": DESCRIPTION
                    },
                    "updateMask": "description",
                }
            },
            {
                "createItem": {
                    "item": {
                        "title": "פקלון מישוב",
                        "imageItem": {
                            "image": {
                                "sourceUri": f"https://drive.google.com/uc?id={PAKALON_MISHUV_FILE_ID}"
                            }
                        },
                    },
                    "location": {"index": 0},
                }
            },
            {
                "createItem": {
                    "item": {
                        "title": "צוות",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [
                                        {"value": "1"},
                                        {"value": "2"},
                                        {"value": "3"},
                                        {"value": "4"},
                                        {"value": "5"},
                                    ]
                                }
                            }
                        }
                    },
                    "location": {"index": 1},
                }
            }
        ]
    }

    google_forms_service.forms().batchUpdate(formId=form_id, body=update).execute()


def create_question(google_forms_service, form_id: str, title: str, index: int):
    update = {
        "requests": [
            {
                "createItem": {
                    "item": {
                        "title": f"{title} - דירוג",
                        "questionItem": {
                            "question": {
                                "ratingQuestion": {
                                    "ratingScaleLevel": 7,
                                    "iconType": "STAR"
                                }
                            }
                        }
                    },
                    "location": {"index": index}
                }
            },
            {
            "createItem": {
                    "item": {
                        "title": f"{title} - שימור",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {
                                    "paragraph": False
                                }
                            }
                        }
                    },
                    "location": {"index": index + 1}
                },
            },
            {
                "createItem": {
                    "item": {
                        "title": f"{title} - שיפור",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {
                                    "paragraph": False
                                }
                            }
                        },
                    },
                    "location": {"index": index + 2}
                },
            }
        ]
    }

    google_forms_service.forms().batchUpdate(formId=form_id, body=update).execute()
    

def update_daily_form(google_forms_service, form_id: str):
    daily_events = ""
    with open("daily_events.txt", "r", encoding="utf-8") as file:
        daily_events = file.read().splitlines()

    index = 2
    for event in daily_events:
        create_question(google_forms_service, form_id, event, index)
        index += 3
    return index


def daily_form_epilogue(google_forms_service, form_id: str, index: int):
    update = {
        "requests": [
            {
            "createItem": {
                    "item": {
                        "title": "משהו שלקחתי/למדתי מהיום",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {
                                    "paragraph": False
                                }
                            }
                        }
                    },
                    "location": {"index": index}
                },
            },
            {
                "createItem": {
                    "item": {
                        "title": "נקודות נוספות",
                        "questionItem": {
                            "question": {
                                "textQuestion": {
                                    "paragraph": False
                                }
                            }
                        },
                    },
                    "location": {"index": index + 1}
                },
            }
        ]
    }

    google_forms_service.forms().batchUpdate(formId=form_id, body=update).execute()


def main():
    credentials = get_google_creds()
    google_forms_service = get_google_forms_service(credentials)
    google_drive_service = get_google_drive_service(credentials)

    form_title = get_daily_form_title()
    form_id = create_form(google_forms_service, form_title)
    rename_form(google_drive_service, form_id, form_title)

    daily_form_prologue(google_forms_service, form_id)
    last_index = update_daily_form(google_forms_service, form_id)
    daily_form_epilogue(google_forms_service, form_id, last_index)

if __name__ == "__main__":
    main()
