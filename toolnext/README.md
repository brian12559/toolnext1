This project contains a few scripts for testing the tool next tools.  XRay, Codebeamer, TestLab and Practitest.
This require selenium.  I will add other requirements as I figure them out.

## Installation

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

Also install latest version of geckodriver (use at least version v0.19.1 or newer) from https://github.com/mozilla/geckodriver/releases. E.g.:

    copy the geckodriver file into /usr/bin
    wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
    tar xf geckodriver-v0.24.0-linux64.tar.gz
    mv geckodriver venv/bin/
    rm -f geckodriver-v0.24.0-linux64.tar.gz
