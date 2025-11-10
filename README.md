# Congratulations! You're the new קה״ד פלוגתי! 🥳
## Introduction
This project was made by Ron Monosevich from Kakas 16 for my קה״ד פלוגתי of חציון ב׳, so he will have an easy way to create a Daily Mem-Yud, without any קאדר
apart from a little setup that is needed to be done (but it is worth it!). Wishing you a lot of luck in the Kakas ❤️

## Prerequisites
To use this project, you will need the following prerequisites:

1. **Python 3.7+**  
   Make sure you have Python 3.7 or newer installed.

2. **Google Cloud project and API credentials**  
   - A Google Cloud project with the Google Forms API and Google Drive API enabled.
   - Download the OAuth2 `credentials.json` for your project and place it in the project directory.

3. **Required Python packages in a virtual environment**
   - It is strongly recommended to use a Python virtual environment (venv) to manage your dependencies.  
   To create and activate a venv, run:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
   - Then install all dependencies with:
   ```
   pip install -r requirements.txt
   ```

4. **Internet access**  
   This application communicates with Google APIs and requires a stable internet connection.
   
5. **First-time Google authentication**  
   The first time you run the program, you will be prompted to grant access to your Google account. The token will be saved as `token.json` for subsequent runs.

6. **Text file with daily events**  
   Make sure you have a `daily_events.txt` file in the project directory, containing the daily activities/events (one per line, in Hebrew).

**Summary:**  
- Python 3.7+  
- Google API credentials (`credentials.json`)  
- Virtual environment (venv)  
- Install dependencies  
- Internet connection  
- Authenticate with Google on first run  
- `daily_events.txt` file with your מופעים

## Step-by-step: Setting up your Google Cloud Project

To use this project, you need to set up a Google Cloud project and enable the required APIs. Follow these detailed steps:

### 1. Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click the project drop-down (top-left) and **New Project**.
3. Enter a name (e.g., "MemYud Forms"), choose an organization if needed, and click **Create**.

### 2. Enable the Required APIs

With your new project selected:

1. In the Cloud Console, navigate to **APIs & Services > Library**.
2. Search for **Google Forms API**.  
   - Click it and then click **Enable**.
3. Repeat for **Google Drive API**.  
   - Search, select, and **Enable**.

### 3. Set Up OAuth Consent Screen

1. In **APIs & Services**, click **OAuth consent screen** on the side menu.
2. Choose **External**, then **Create**.
3. Fill in **App name** (e.g., "MemYud Forms App"), user support email, and developer contact email.
4. (Optional) Add a logo and information for better clarity.
5. Save and continue. On the **Scopes** page, keep the defaults, then save.
6. On the **Test users** page, add the Google account(s) you'll use for testing.  
   > You must use an email registered in these test users if your OAuth consent screen is not published!
7. Save and continue.

### 4. Create OAuth Client Credentials

1. In the Cloud Console, navigate to **APIs & Services > Credentials**.
2. Click **+ CREATE CREDENTIALS** and choose **OAuth client ID**.
3. For **Application type**, select **Desktop app**.
4. Name it (e.g., "MemYud Desktop App") and click **Create**.
5. Download the `credentials.json` file provided after creation.
6. Place the `credentials.json` file in this project's root directory.

### 5. (Optional) Publish OAuth Consent Screen *(if you want to use ANY Google account)*

- Once ready and if needed, return to the consent screen setup and **Publish** the app.
  - Until you do this, only test users can authorize the app.

### 6. You're done!

Now, when you run the Python program, it will use this configuration to prompt you for Google authorization.

**Troubleshooting**
- If you get permission errors, make sure:
  - The Google account you use is listed in Test Users (if not published).
  - Both the **Forms API** and **Drive API** are enabled.
  - Your `credentials.json` is in the correct project folder.

*For more Google API setup help, see the [official docs](https://developers.google.com/workspace/guides/create-credentials).*


## For Additional Help
You can always contact me on the phone: 052-5094790 😊
