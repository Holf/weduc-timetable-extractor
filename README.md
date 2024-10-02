# weduc-timetable-extractor

A utility that extracts lesson timetables from [Weduc](https://www.reachmoreparents.com/) and pushes the events within to iCalendar files or Google Calendars.

## Modes

**weduc-timetable-extractor** has two modes. In both cases it will log on to Weduc, extract the timetable data for one or more students, and then:

### `ical` mode

In `ical` mode the extracted timetable data will be written out to `.ics` files in **iCalender** format, one file per student.

```sh
> weduc-timetable-extractor.exe ical
```

### `api` mode

In `api` mode, the extracted timetable data will be written directly to Google Calendars; a different calendar can be specified per student.

```sh
> weduc-timetable-extractor.exe api
```

## Setup

Setting up **weduc-timetable-extractor** requires you to follow these steps:

### Download the latest release

This is available [here](https://github.com/Holf/weduc-timetable-extractor/releases/latest).

There are versions available for:

- Windows
- MacOS
- Ubuntu 20.04
- Ubuntu 22.04

Download the executable suitable for your OS.

### Install Google Chrome browser

**weduc-timetable-extractor** relies on the Playwright end-to-end testing framework to drive a Chrome browser instance that interacts with the Weduc site.

You can install Chrome for your OS by following the instructions [here](https://www.google.com/intl/en_uk/chrome/).

> **weduc-timetable-extractor** will look for the Chrome browser instance in the default install location for the OS it is running on:
>
> | OS      | Path                                                           |
> | ------- | -------------------------------------------------------------- |
> | Windows | `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`  |
> | MacOS   | `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` |
> | Ubuntu  | `/usr/bin/google-chrome`                                       |
>
> If you wish to use a Chrome executable installed to a non-default location, you can specify the path in the `config.ini` file (see below for more info).

### Create `config.ini`

This can be done by:

- downloading [`config.ini.template`](https://github.com/Holf/weduc-timetable-extractor/blob/main/config.ini.template)
- renaming it to `config.ini`
- populating it as described in the inline comments.

The `config.ini` file should be placed in the same folder as the **weduc-timetable-extractor** executable you should have already downloaded.

#### Example config

An example `config.ini` might be:

```ini
[weduc]
username = john_smith
password = password123

[ical]
output_folder_path = ./student_calendars ; only needed for ical mode

[student_1]
school_name = Grange Hill Primary School
student_name = Tucker Jenkins
calendar_to_update = Tucker - School Timetable ; only needed for api mode

[student_2]
school_name = Grange Hill Secondary School
student_name = Zammo Maguire
calendar_to_update = Zammo - School Timetable ; only needed for api mode
```

Further detail on each entry:

#### `weduc`

| Entry         | Purpose                                                                                     |
| ------------- | ------------------------------------------------------------------------------------------- |
| `username`    | The Username you use for logging in to Weduc.<br>_Optional_.                                |
| `password`    | The Password you use for logging in to Weduc.<br> _Optional_.                               |
| `chrome_path` | The path to the Chrome executable that will be used to interact with Weduc.<br> _Optional_. |

If both `username` and `password` values are provided, the browser instance used to extract data from Weduc will run headlessly, as no user input is required.

Should either `username` or `password` be missing, the browser instance used to extract data from Weduc will run interactively; the script will pause on the login screen so you can enter Username and Password manually.

if `chrome_path` is not specified then **weduc-timetable-extractor** will look for Chrome in the default install path.

> If you have forked this Repo for your own development, **_be wary of accidentally committing a `password`_** that might be present in `config.ini`.
>
> An entry in the `.gitingore` file should prevent this but it bears repeating.

#### `ical`

| Entry                | Purpose                                                                                                      |
| -------------------- | ------------------------------------------------------------------------------------------------------------ |
| `output_folder_path` | The path to the folder where iCalendar files should be written.<br> _Required_ if running in iCalendar mode. |

#### `student_` sections

There should be one or more of these sections present. Each section name must begin with `student_` but is otherwise permissive. `student_1`, `student_A` or `student_Bill` are all allowed, for example.

| Entry                | Purpose                                                                                                                 |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `school_name`        | The name of the school that the student goes to, precisely as it appears in Weduc.<br> _Required._                      |
| `student_name`       | The student's name, precisely as it appears in Weduc.<br> _Required._                                                   |
| `calendar_to_update` | The name of the Google Calendar to which Weduc timetable events will be pushed. <br> _Required_ if running in API mode. |

### Set up Google Calendar API

> This is only necessary if you plan to use **API mode**.
>
> Setting up Google Calendar API is quite involved, so you may prefer to use **iCal mode** and import iCalendar files to Google Calendar manually.
>
> You would also want to use **iCal mode** if you plan to import Weduc timetable events into calendars other than Google Calendar.

To set up Google Calendar API, complete the three tasks described [here](https://developers.google.com/calendar/api/quickstart/python#set-up-environment). You only need to complete the tasks in the _'Set up your environment'_ section.

Having gone through this process, you should be prompted to download some client credentials. This will be a JSON file with a name along the lines of:

`client_secret_XXXXX.apps.googleusercontent.com.json`

**weduc-timetable-extractor** expects to find this, but it looks for a file named `credentials.json`.

Make sure the file you have downloaded is renamed as such, and is placed in the same folder as the downloaded `weduc-timetable-extractor` executable, alongside `config.ini`.

> ### A note on auth. token expiry
>
> Unless you are prepared to go through an arduous verification process, you will have to leave the project created for Calendar API access in **test mode**. Unfortunately, this means the token issued when authenticating with Google has a short expiry, of seven days.
>
> This is fine if you are running **weduc-timetable-extractor** manually, as you can re-authenticate when prompted.
>
> It will, however, be a barrier if you want to automate timetable extraction.
>
> #### A workaround (for some)
>
> If you have a [Google Workspace](https://workspace.google.com/intl/en_uk/) set up, then you can create Calendar API projects that do not have to be in test mode.
>
> Thus, you can push events to a user's calendar within your organization and then share the calendar externally with any other Google Calendar user.

## Running **weduc-timetable-extractor**

Having carried out the setup steps above, you should have these files in the same folder:

```ini
timetable-extractor/
  |─ weduc-timetable-extractor.exe
  |─ config.ini
  |─ credentials.json # only needed for API mode
```

You can then run **weduc-timetable-extractor** by doing either:

```sh
> weduc-timetable-extractor.exe ical
```

```sh
> weduc-timetable-extractor.exe api
```

... depending on which mode you are using.

## Development environment setup

The following setup steps should be carried out:

### Install Python

**weduc-timetable-extractor** was written to work with Python `3.12.6`, so this is the ideal version to install.

It may well work with other `3.x` versions of Python (including those installed by default on Linux) but this is untested.

### Install `pipenv`

**[pipenv](https://pipenv.pypa.io/en/latest/)** manages the project environment and installation of dependent packages.

See the `pipenv` documentation for further details.

### Install dependencies

Once `pipenv` is installed, run the following commands to install the necessary dependencies:

```sh
pipenv shell
pipenv install
```

There are some development scripts present in the included [`pipfile`](https://github.com/Holf/weduc-timetable-extractor/blob/main/Pipfile) which can be run by issuing, for example:

```sh
pipenv run test
```

## Why was this written?

Viewing a timetable in Weduc requires you to log on and then carry out a number of navigation steps to get to the correct screen.

Viewing events in Google Calendar (or the calendaring system of your choice) is usually just a matter of getting your phone out of your pocket and opening the calendar app.

Furthermore, those calendars can then be shared with your kids so they, too, have easy access to their timetable.

_Yes, they should already have a timetable. And yes, it always seems to get lost within a week. Or it falls apart in their pockets._

### A chance to play with Python

I wanted a project with a little bit of depth to help me learn some Python.

I am a fairly seasoned developer in other languages but am relatively new to Python. I have tried to be [pythonic](https://en.wikipedia.org/wiki/Zen_of_Python), where I can, but there will undoubtedly be areas in this project where I have failed.

I have learnt a lot doing this, though, and really enjoyed it. I am starting to get what all the fuss is about with Python.
