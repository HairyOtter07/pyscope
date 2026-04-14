import pickle

import requests
from bs4 import BeautifulSoup

BASE = "https://www.gradescope.com"


def _endpoint(e):
    return BASE + e


def start_gradescope_session(email: str, password: str) -> requests.Session | None:
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:145.0) Gecko/20100101 Firefox/145.0"
        }
    )

    r = s.get(_endpoint("/login"))
    loginPage = BeautifulSoup(r.content, features="html.parser")
    authForm = loginPage.find("form")
    if authForm is None:
        return None
    authTokenInput = authForm.find("input", attrs={"name": "authenticity_token"})
    if authTokenInput is None:
        return None
    authToken = str(authTokenInput["value"])
    loginData = {
        "authenticity_token": authToken,
        "session[email]": email,
        "session[password]": password,
    }
    s.post(_endpoint("/login"), data=loginData)
    return s


def is_session_valid(session: requests.Session) -> bool:
    r = session.get(_endpoint("/login"))
    return r.status_code == 401


def save_session(session: requests.Session) -> None:
    with open("session.pkl", "wb") as f:
        pickle.dump(session, f)
