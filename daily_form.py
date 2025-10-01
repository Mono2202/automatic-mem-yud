from datetime import datetime
from dateutil import tz

from form import Form

class DailyForm(Form):
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
    DAILY_EVENTS_FILE_PATH = "daily_events.txt"
    KAHADIM_EMAILS = [
        "Naftaliwieder@gmail.com",
        "talmor.rotem@gmail.com",
        "noa.paz2004@gmail.com",
        "maya539539@gmail.com",
        "oribiran26@gmail.com",
        "agur.hadas@gmail.com"
    ]

    def __init__(self):
        now = datetime.now(self.TIMEZONE)
        form_title =  f'מ"י יום {self.HEBREW_DAYS[(now.weekday() + 1) % 7]} {now.day}.{now.month}'
        super().__init__(form_title, form_title)

    def create_form(self):
        super().create_form()
        self.daily_form_prologue()

        self.get_daily_events()
        for event in self._daily_events:
            self.daily_event_question(event)

        self.daily_form_epilogue()
        self.add_permissions(self.KAHADIM_EMAILS, "writer")

    def get_daily_events(self):
        self._daily_events = []
        with open(self.DAILY_EVENTS_FILE_PATH, "r", encoding="utf-8") as file:
            self._daily_events = file.read().splitlines()
        return self._daily_events

    def daily_form_prologue(self):
        info = {"info": {"description": self.DESCRIPTION}, "updateMask": "description"}
        self.update_form_info(info)

        requests = [
            {
                "createItem": {
                    "item": {
                        "title": "פקלון מישוב",
                        "imageItem": {
                            "image": {
                                "sourceUri": f"https://drive.google.com/uc?id={self.PAKALON_MISHUV_FILE_ID}"
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
        self.update_form_body(requests)

    def daily_event_question(self, event: str):
        requests = [
                {
                    "createItem": {
                        "item": {
                            "title": f"{event} - דירוג",
                            "questionItem": {
                                "question": {
                                    "ratingQuestion": {
                                        "ratingScaleLevel": 7,
                                        "iconType": "STAR"
                                    }
                                }
                            }
                        },
                    }
                },
                {
                "createItem": {
                        "item": {
                            "title": f"{event} - שימור",
                            "questionItem": {
                                "question": {
                                    "required": True,
                                    "textQuestion": {
                                        "paragraph": False
                                    }
                                }
                            }
                        },
                    },
                },
                {
                    "createItem": {
                        "item": {
                            "title": f"{event} - שיפור",
                            "questionItem": {
                                "question": {
                                    "required": True,
                                    "textQuestion": {
                                        "paragraph": False
                                    }
                                }
                            },
                        },
                    },
                }
            ]
    
        self.update_form_body(requests)
        
    def daily_form_epilogue(self):
        requests = [
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
                    },
                }
            ]
        self.update_form_body(requests)
