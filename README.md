# weduc-timetable-extractor

A utility that extracts the lesson timetable from [Weduc](https://www.reachmoreparents.com/) and pushes the events within to Google Calendar.

There is also an option to output iCalendar files, instead.

## Why?

Viewing a timetable in Weduc requires you to log on and then carry out a few navigation steps to get to the correct screen.

Viewing events in Google Calendar (or the calendaring system of your choice) is usually just a matter of getting your phone out of your pocket and opening the calendar app.

I wrote this because it makes it quicker and easier to provide an answer when my kids say "Dad, what lessons do I have today?"

### A chance to play with Python

I wanted a project with a little bit of depth to help me learn some Python.

I am a fairly seasoned developer in other languages but am relatively new to Python. I have tried to be [pythonic](https://en.wikipedia.org/wiki/Zen_of_Python), where I can, but there will undoubtedly be areas in this project where I have failed.

I have learnt a lot doing this, though, and really enjoyed it. I am starting to get what all the fuss is about with Python.

## How it works

**weduc-timetable-extractor** uses the Playwright end-to-end testing framework to drive a browser. The browser logs in to Weduc and then, using the resulting authenticated state, makes API calls to the Weduc endpoints that serve up timetable data (this data would usually be used by Weduc to render the student's timetable).

The timetable data is then either:

- pushed to Google Calendar via the Google Calendar API.
- written out in iCalendar format to an `.ics` file, ready for you to import into a calendar system of your choice.

### Multiple are students catered for

**weduc-timetable-extractor** can extract more than one student timetable and push data to separate Google Calendars or iCalendar files. This is useful if you have more than one student in the family.

## Requirements

## Modes

There are two modes of operation:

| Mode      | Functionality                                                                                 | Command                 | Notes                                                                                                                                                                                                  |
| --------- | --------------------------------------------------------------------------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| API       | Extracts timetables from Weduc and then pushes the events within directly to Google Calender. | `pipenv run start-api`  | When running in API mode, the `student_` sections in the `config.ini` file must each have a `calendar_to_update` entry; this specifies which Google Calendar the timetable events should be pushed to. |
| iCalender | Extracts timetables from Weduc and then writes the events within out to iCalendar files.      | `pipenv run start-ical` | When running in iCalendar mode, the `ical` section in the `config.ini` file must have an `output_folder_path` entry; this specifies where iCalendar files should be written to.                        |

### Requirements for running in API mode

API mode requires you to have set up access to the Google Calendar API.

To do this, complete the three tasks described [here](https://developers.google.com/calendar/api/quickstart/python#set-up-environment). You only need to complete the tasks in the _'Set up your environment'_ section.

Having gone through this process, you should be able to download some client credentials. This will be a JSON file with a name along the lines of:

`client_secret_XXXXX.apps.googleusercontent.com.json`

... where the `XXXXX` is a long string.

**weduc-timetable-extractor** expects to find this, but it looks for a file named `credentials.json`. So, make sure the file you have downloaded is renamed as such, and is placed in the project's root folder.

## Configuration

The utility relies on a `config.ini` file being present and populated with the correct values.
Create `config.ini` by copying `config.ini.template` and filling in the values needed.

The entries that `config.ini` should contain in each section are:

### `weduc`

| Entry      | Purpose                                       |
| ---------- | --------------------------------------------- |
| `username` | The Username you use for logging in to Weduc. |
| `password` | The Password you use for logging in to Weduc. |

If both these values are provided, the browser instance used to extract data from Weduc will run headlessly, as no user input is required.

Should either value be missing, the browser instance used to extract data from Weduc will run interactively; the script will pause on the login screen so you can enter Username and Password manually.

### `ical`

| Entry                | Purpose                                                                                                             |
| -------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `output_folder_path` | The path to the folder where iCalendar files should be written.<br>This is _required_ if running in iCalendar mode. |

### `student_` sections

There should be one or more of these sections present. Each section name must begin with `student_` but is otherwise permissive. `student_1`, `student_A` or `student_Bill` are all allowed, for example.

| Entry          | Purpose                                                                                           | Where to find                                                                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `school_name`  | The name of the School that the student goes to, precisely as it appears in Weduc.<br>_Required._ |                                                                                                                                               |
| `student_name` | The Student's name, precisely as it appears in Weduc.<br>_Required._                              | Go to the 'Parents' section in Weduc and then select the Student for whom you wish to find the id.<br>The id will be present in the page URL. |

**Be wary of accidentally committing security-sensitive credentials** that might be present in `config.ini`.

_(The `.gitingore` file should prevent this but it is worth reiterating, nevertheless.)_
