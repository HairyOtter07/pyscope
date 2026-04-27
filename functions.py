import pickle
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup, Tag

BASE = "https://www.gradescope.com"
GRADESCOPE_DATETIME_FSTRING = "%Y-%m-%d %H:%M:%S %z"


class Assignment:
    """
    title
    submissionStatus
    dueDate
    lateDueDate
    """

    def __init__(self, assignmentTag: Tag) -> None:
        self.title = self.__get_assignment_title(assignmentTag)
        self.submissionStatus = self.__get_assignment_submission_status(assignmentTag)
        self.dueDate = self.__get_assignment_due_date(assignmentTag)
        self.lateDueDate = self.__get_assignment_late_due_date(assignmentTag)

    def __get_assignment_title(self, assignmentTag: Tag) -> str:
        titleTag = assignmentTag.find("th")
        if titleTag is None:
            return ""
        return titleTag.text

    def __get_assignment_submission_status(self, assignmentTag: Tag) -> str:
        submissionStatusTag = assignmentTag.find("td", class_="submissionStatus")
        if submissionStatusTag is None:
            return ""
        statusClasses = submissionStatusTag["class"]
        if (
            "submissionStatus-warning" in statusClasses
            or "submissionStatus-neutral" in statusClasses
            or "submissionStatus-complete" in statusClasses
        ):
            statusText = submissionStatusTag.find(
                "div", class_="submissionStatus--text"
            )
            if statusText is None:
                return ""
            return statusText.text
        else:
            statusText = "Graded: "
            scoreText = submissionStatusTag.find(
                "div", class_="submissionStatus--score"
            )
            if scoreText is None:
                return statusText
            return statusText + scoreText.text

    def __get_assignment_due_date(self, assignmentTag: Tag) -> datetime | None:
        timeChartDiv = assignmentTag.find("div", class_="submissionTimeChart")
        if timeChartDiv is None:
            return None
        dueDateTag = timeChartDiv.find("time", class_="submissionTimeChart--dueDate")
        if dueDateTag is None:
            return None
        return datetime.strptime(
            str(dueDateTag["datetime"]), GRADESCOPE_DATETIME_FSTRING
        )

    def __get_assignment_late_due_date(self, assignmentTag: Tag) -> datetime | None:
        timeChartDiv = assignmentTag.find("div", class_="submissionTimeChart")
        if timeChartDiv is None:
            return None
        dueDateTags = timeChartDiv.find_all(
            "time", class_="submissionTimeChart--dueDate"
        )
        if len(dueDateTags) < 2:
            return None
        return datetime.strptime(
            str(dueDateTags[1]["datetime"]), GRADESCOPE_DATETIME_FSTRING
        )


class Course:
    """
    id
    title
    subtitle
    instructors
    assignments
    """

    def __init__(self, session: requests.Session, id: str) -> None:
        self.id = id
        self.session = session
        page = self.__get_course_page()

        self.title = self.__get_course_title(page)
        self.subtitle = self.__get_course_subtitle(page)
        self.instructors = self.__get_course_instructors(page)
        self.assignments = self.__get_course_assignments(page)

    def __get_course_page(self) -> BeautifulSoup:
        r = self.session.get(_endpoint(f"/courses/{self.id}"))
        coursePage = BeautifulSoup(r.content, features="html.parser")
        return coursePage

    def __get_course_title(self, coursePage: BeautifulSoup) -> str:
        titleDiv = coursePage.find("div", class_="sidebar--title")
        if titleDiv is None:
            return ""
        titleLink = titleDiv.find("a")
        if titleLink is None:
            return ""
        return titleLink.text

    def __get_course_subtitle(self, coursePage: BeautifulSoup) -> str:
        subtitleDiv = coursePage.find("div", class_="sidebar--subtitle")
        if subtitleDiv is None:
            return ""
        return subtitleDiv.text

    def __get_course_instructors(self, coursePage: BeautifulSoup) -> list[str]:
        instructorListItems = coursePage.find_all(
            "li", id=re.compile("sidebar-instructor-\d*")
        )
        instructors = []
        for listItem in instructorListItems:
            nameDiv = listItem.find("div", class_="sidebar--menuItemLabel")
            if nameDiv is not None:
                instructors.append(nameDiv.text)
        return instructors

    def __get_course_assignments(self, coursePage: BeautifulSoup) -> list[Assignment]:
        assignmentsTable = coursePage.find("table", id="assignments-student-table")
        if assignmentsTable is None:
            return []

        tableBody = assignmentsTable.find("tbody")
        if tableBody is None:
            return []

        assignmentElements = tableBody.find_all("tr")
        assignments = []
        for assignmentEl in assignmentElements:
            assignment = Assignment(assignmentEl)
            assignments.append(assignment)
        return assignments


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


def load_session() -> requests.Session | None:
    if not Path("session.pkl").exists():
        return None
    with open("session.pkl", "rb") as f:
        s = pickle.load(f)
        if not isinstance(s, requests.Session):
            raise TypeError(f"Expected requests.Session, but got {type(s).__name__}")
        return s


def get_course_ids(session: requests.Session) -> list[str]:
    r = session.get(_endpoint("/account"))
    dashboard = BeautifulSoup(r.content, features="html.parser")
    courseList = dashboard.find("div", class_="courseList--coursesForTerm")
    if courseList is None:
        return []
    linkTags = courseList.find_all("a")
    courseLinks = [str(linkTag["href"]) for linkTag in linkTags]
    courseIds = [link.split("/")[-1] for link in courseLinks]
    return courseIds


def get_course(session: requests.Session, id: str) -> Course:
    return Course(session, id)
