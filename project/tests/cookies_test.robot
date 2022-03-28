*** Settings ***
Variables  configuration/constants.py
Library  itechframework/modules/browser_manager/BrowserManager.py
Library  project/steps/CookieSteps.py

Test Setup  Open Browser
Test Teardown  Close Browser  ${browser}

*** Keywords ***
Open Browser
    ${browser} =  Get Browser  ${BROWSER_TYPE}
    Set Suite Variable  ${browser}

*** Test Cases ***
Login To Wiki
    ${page_object} =  Open Wiki  ${browser}
    Login To Wiki  ${page_object}  ${login}  ${password}
    Save Cookies  ${browser}

Open With Existing Cookies
    ${browser} =  Get Browser  ${BROWSER_TYPE}
    ${page_object} =  Open Wiki  ${browser}
    Load Cookies  ${browser}
    Login To Wiki  ${page_object}  ${login}  ${password}
    Check If Logged In  ${browser}

