# Conversational

## Setup Instructions

1. Install a package manager if you have not already (this will make your life going forward much easier)
    1. For Windows: https://chocolatey.org/install
    2. For Mac/Linux: https://brew.sh/
2. Open Terminal in Linux/Mac or Powershell as admin in Windows
3. Make sure you have Python 3.9 installed
    1. You can check with `python3 --version`
    2. If not,
        1. Linux/Mac: `brew install python3`
        2. Windows: `choco install python3`
4. Check that pip3 is installed (`pip3 --version`)
   1. If not,
       1. Linux/Mac: `brew install pip3`
       2. Windows: `choco install pip3`
5. Check for Django 3.2 install: `python3 -m django --version`
    1. If not, install Django with `pip3 install django`
6. **Important** - To initally setup the database, from the project root directory (the one with manage.py in it):
    1. `python3 manage.py migrate`

## Startup Instructions
1. From project root: `python3 manage.py runserver`
2. In browser, open: http://127.0.0.1:8000

## Testing Instructions
From project root: `python3 manage.py test conversational`
Find tests in: conversational/tests.py