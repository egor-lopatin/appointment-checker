# Appointment checker

The only purpose of this project is to check the availability of appointments for the Spanish National Police. It is not intended to be used for any other purpose.

The solution is based on the Selenium library, which is used to walk through the pages and fill required forms.
GitHub Actions are used to run the script with a schedule.

## Prep-work

Environment variables are required to run the project. You can create a `.env` file in the root of the project with the following content:

```env
export SITE_URL="https://POLICE_WEB_SITE/"
export PROVINCE="PROVINCE_NAME"
export OPTION_VALUE="SPECIAL_VALUE_OF_POLICE_DOCUMENT"
export USER_ID="NIE_id"
export USER_NAME="YOUR_NAME"
export TEXT_TO_PARSE="TEXT THAT INDICATES THAT THERE ARE NO APPOINTMENTS AVAILABLE"
```

## Usage:

Install dependencies:

```bash
make install
```

Activate the virtual environment:

```bash
pipenv shell
```

Run the script:

```bash
python main.py
```