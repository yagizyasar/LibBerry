from django.db import connection
from home.dataaccess import to_dict

def db_add_homework(hw_id, due, set_id, courses, creator_id):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM homework_homework WHERE hw_id=%s;", [hw_id])
    res = cursor.fetchone()

    if res != None:
        print("Invalid add homework request: Homework already exists")
        return

    cursor.execute("INSERT INTO homework_homework VALUES (%s, %s, %s);", [hw_id, due, set_id])
    cursor.execute("INSERT INTO instructor_assigns_hw VALUES(%s, %s);", [hw_id, creator_id])
    for course in courses:
        db_add_homework_to_coursesection(course.get("course_id"), course.get("section"), course.get("semester"), course.get("year"), hw_id)

def db_add_homework_to_coursesection(course_id, section, semester, year, hw_id):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM course_has_hw WHERE course_id=%s AND section=%s AND semester=%s AND year=%s AND hw_id=%s;", [course_id, section, semester, year, hw_id])
    res = cursor.fetchone()

    if res != None:
        print("Invalid add homework to coursesection: Homework already in coursesection")
        return

    cursor.execute("INSERT INTO course_has_hw VALUES (%s, %s, %s, %s, %s);", [course_id, section, semester, year, hw_id])

def db_add_instructor_to_homework(hw_id, instructor_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM instructor_assigns_hw WHERE instructor_id=%s AND hw_id=%s;", [instructor_id, hw_id])
    res = cursor.fetchone()

    if res != None:
        print("Invalid add instructor to homework request: Instructor already exists in homework")
        return
    cursor.execute("INSERT INTO instructor_assigns_hw VALUES(%s, %s);", [hw_id, instructor_id])

def db_add_student_to_coursesection(student_id,course_id,section,semester,year):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_student WHERE user_id=%s;",[student_id])
    res = cursor.fetchone()
    if res == None:
        print("Given student id does not exists")
        return
    cursor.execute("INSERT INTO student_takes_course VALUES (%s, %s, %s, %s,%s);",[student_id,course_id,section,semester,year])


def db_delete_homework():

def db_get_all_past_hws():

def db_get_all_future_hws():