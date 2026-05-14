from datetime import datetime

from bs4 import Tag
from fastapi import FastAPI
from pydantic import BaseModel

GRADESCOPE_DATETIME_FSTRING = "%Y-%m-%d %H:%M:%S %z"

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
                    str(due_date_tags[0]["datetime"]), GRADESCOPE_DATETIME_FSTRING
                )
            if len(due_date_tags) > 1:
                late_due_date = datetime.strptime(
                    str(due_date_tags[1]["datetime"]), GRADESCOPE_DATETIME_FSTRING
                )

        return Assignment(
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


class Login(BaseModel):
    email: str
    password: str


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/api/login/")
def login(credentials: Login):
    pass


@app.get("/api/courses/")
def get_courses():
    pass


@app.get("/api/courses/{course_id}")
def get_course(course_id: str):
    pass
