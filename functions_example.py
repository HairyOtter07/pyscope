import os

from dotenv import load_dotenv

from functions import (
    get_course,
    get_course_ids,
    is_session_valid,
    load_session,
    save_session,
    start_gradescope_session,
)

load_dotenv()

s = load_session()
if s is None:
    print("No saved session found, starting new session...")
    s = start_gradescope_session(os.environ["USERNAME"], os.environ["PASSWORD"])
elif not is_session_valid(s):
    print("Session invalid, starting new session...")
    s = start_gradescope_session(os.environ["USERNAME"], os.environ["PASSWORD"])

if s is None:
    exit()

courseIds = get_course_ids(s)

for id in courseIds:
    c = get_course(s, id)
    print(f"{c.subtitle} ({c.id})")
    print("-" * 100)
    print(f"Instructors: {' | '.join(c.instructors)}")
    for a in c.assignments:
        print(
            f"{a.title} ({a.submissionStatus}): {('Due ' + a.dueDate.strftime('%A, %B %d, %Y at %I:%M %p')) if a.dueDate else 'No Due Date'}, {'Late Due Date: ' + (a.lateDueDate.strftime('%A, %B %d, %Y at %I:%M %p') if a.lateDueDate else 'None')}"
        )
    print()

save_session(s)
