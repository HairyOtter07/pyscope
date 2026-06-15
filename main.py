import base64
import json
import re
from datetime import datetime
from typing import Annotated

import requests
from bs4 import BeautifulSoup, Tag
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

GS_DATETIME_FSTRING = "%Y-%m-%d %H:%M:%S %z"

app = FastAPI()


class Assignment(BaseModel):
    title: str
    submission_status: str
    due_date: datetime | None
    late_due_date: datetime | None

    @classmethod
    def from_tag(cls, tag: Tag):
        title = ""
        if th := tag.find("th"):
            title = th.text

        submission_status = ""
        if submission_status_tag := tag.find("td", class_="submissionStatus"):
            status_classes = submission_status_tag["class"]
            if (
                "submissionStatus-warning" in status_classes
                or "submissionStatus-neutral" in status_classes
                or "submissionStatus-complete" in status_classes
            ):
                if status_text := submission_status_tag.find(
                    "div", class_="submissionStatus--text"
                ):
                    submission_status = status_text.text
            else:
                submission_status = "Graded: "
                if score_text := submission_status_tag.find(
                    "div", class_="submissionStatus--score"
                ):
                    submission_status += score_text.text

        due_date = None
        late_due_date = None
        if time_chart_div := tag.find("div", class_="submissionTimeChart"):
            due_date_tags = time_chart_div.find_all(
                "time", class_="submissionTimeChart--dueDate"
            )
            if len(due_date_tags) > 0:
                due_date = datetime.strptime(
                    str(due_date_tags[0]["datetime"]), GS_DATETIME_FSTRING
                )
            if len(due_date_tags) > 1:
                late_due_date = datetime.strptime(
                    str(due_date_tags[1]["datetime"]), GS_DATETIME_FSTRING
                )

        return cls(
            title=title,
            submission_status=submission_status,
            due_date=due_date,
            late_due_date=late_due_date,
        )


class Course(BaseModel):
    id: str
    title: str
    subtitle: str
    instructors: list[str]
    assignments: list[Assignment]

    @classmethod
    def from_page(cls, page: BeautifulSoup):
        id = ""
        if id_div := page.find("div", class_="courseHeader--courseID"):
            if m := re.search(r"\d+", id_div.text):
                id = m[0]

        title = ""
        if title_div := page.find("div", class_="sidebar--title"):
            if title_link := title_div.find("a"):
                title = title_link.text

        subtitle = ""
        if subtitle_div := page.find("div", class_="sidebar--subtitle"):
            subtitle = subtitle_div.text

        instructors = []
        for list_item in page.find_all("li", id=re.compile(r"sidebar-instructor-\d*")):
            if name_div := list_item.find("div", class_="sidebar--menuItemLabel"):
                instructors.append(name_div.text)

        assignments = []
        if assignments_table := page.find("table", id="assignments-student-table"):
            if table_body := assignments_table.find("tbody"):
                for tag in table_body.find_all("tr"):
                    assignments.append(Assignment.from_tag(tag))

        return cls(
            id=id,
            title=title,
            subtitle=subtitle,
            instructors=instructors,
            assignments=assignments,
        )


class Login(BaseModel):
    email: str
    password: str


class SessionManager:
    session: requests.Session
    GS_BASE_URL = "https://www.gradescope.com"

    def __init__(self, session: requests.Session) -> None:
        self.session = session

    def encode_cookie_jar(self) -> str:
        cookie_dict = self.session.cookies.get_dict()
        return base64.b64encode(json.dumps(cookie_dict).encode()).decode()

    @staticmethod
    def get_gs_endpoint(endpoint: str) -> str:
        return SessionManager.GS_BASE_URL + endpoint

    @staticmethod
    def is_valid_gs_session(session: requests.Session) -> bool:
        r = session.get(SessionManager.get_gs_endpoint("/login"))
        return r.status_code == 401

    @classmethod
    def from_credentials(cls, credentials: Login):
        session = requests.Session()

        success = False
        login_get = session.get(cls.get_gs_endpoint("/login"))
        login_page = BeautifulSoup(login_get.content, features="html.parser")
        if auth_form := login_page.find("form"):
            if auth_token_input := auth_form.find(
                "input", attrs={"name": "authenticity_token"}
            ):
                auth_token = str(auth_token_input["value"])
                login_data = {
                    "authenticity_token": auth_token,
                    "session[email]": credentials.email,
                    "session[password]": credentials.password,
                }
                login_res = session.post(cls.get_gs_endpoint("/login"), data=login_data)
                if "Course Dashboard" in login_res.text:
                    success = True

        return cls(session=session) if success else None

    @classmethod
    def from_cookies(cls, cookie_jar: str):
        session = requests.Session()

        cookie_dict = json.loads(base64.b64decode(cookie_jar).decode())
        session.cookies.update(cookie_dict)
        return (
            cls(session=session)
            if SessionManager.is_valid_gs_session(session)
            else None
        )


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/api/login/")
def login(credentials: Login):
    s = SessionManager.from_credentials(credentials)
    if s is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"cookie_jar": s.encode_cookie_jar()}


@app.get("/api/courses/")
def get_course_ids(gs_cookie_jar: Annotated[str, Header()]):
    s = SessionManager.from_cookies(gs_cookie_jar)
    if s is None:
        raise HTTPException(status_code=401, detail="Session invalid")

    r = s.session.get(s.get_gs_endpoint("/account"))
    dashboard = BeautifulSoup(r.content, features="html.parser")
    course_ids = []
    if course_list := dashboard.find("div", class_="courseList--coursesForTerm"):
        course_ids = [
            str(link_tag["href"]).split("/")[-1]
            for link_tag in course_list.find_all("a")
        ]

    return course_ids


@app.get("/api/courses/{course_id}")
def get_course(course_id: str):
    pass
