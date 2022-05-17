from sqlite3 import connect
from django.db import connection
from home.dataaccess import to_dict

def db_add_homework(hw_id, due, set_id, instructor_id):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM homework_homework WHERE hw_id=%s;", [hw_id])
    res = cursor.fetchone()

    if res != None:
        print("Invalid add homework request: Homework already exists")
        return

    cursor.execute("INSERT INTO homework_homework VALUES (%s, %s, %s);", [hw_id, due, set_id])
    cursor.execute("INSERT INTO instructor_assigns_hw VALUES(%s, %s);", [hw_id, instructor_id])
   
def db_give_homework_to_coursesection(course_id, section, semester, year, hw_id):
    cursor = connection.cursor()
    """
    cursor.execute("SELECT * FROM coursesection_has_hw WHERE course_id=%s AND section=%s AND semester=%s AND year=%s AND hw_id=%s;", [course_id, section, semester, year, hw_id])
    res = cursor.fetchone()

    if res != None:
        print("Invalid add homework to coursesection: Homework already in coursesection")
        return
    """
    cursor.execute("INSERT INTO student_has_hw (student_id, hw_id) SELECT * FROM (SELECT user_id AS student_id FROM user_student NATURAL JOIN student_takes_course WHERE course_id=%s), (SELECT %s);", [course_id, hw_id])

def db_give_homework_to_student(student_ids, hw_id):
    cursor = connection.cursor()
    for student_id in student_ids:
        cursor.execute("INSERT INTO student_has_hw VALUES(%s, %s);", [student_id, hw_id])

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

def db_delete_homework(hw_id):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM homework_homework WHERE hw_id=%s;",[hw_id])
    res = cursor.fetchone()

    if res == None:
        print("Invalid delete homework request: Homework does not exist")
        return

    cursor.execute("DELETE FROM homework_homework WHERE hw_id=%s;", [hw_id])

#def db_get_all_past_hws():

#def db_get_all_future_hws():
def db_get_all_homeworks_instructor(user_id):
     cursor = connection.cursor()
     cursor.execute("SELECT hw_id,due,set_id FROM homework_homework NATURAL JOIN instructor_assigns_hw WHERE instructor_id=%s ORDER BY due DESC;",[user_id])
     res = to_dict(cursor)
     return res
"""
def db_get_all_homeworks_student(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT hw_id FROM student_takes_course NATURAL JOIN coursesection_has_hw WHERE student_id=%s ORDER BY due DESC;",[user_id])
    res = to_dict(cursor)
    return res
"""
def db_get_students_homeworks(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT hw_id FROM student_has_hw WHERE student_id=%s;", [user_id])
    res_dict = to_dict(cursor)
    return res_dict
    
def db_add_coursesection(course_id, section, semester, year, instructor_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM course_section WHERE course_id=%s AND section=%s AND semester=%s AND year=%s;", [course_id, section, semester, year])
    res = cursor.fetchone()

    if res != None:
        print("Invalid add course section request: Course section already exists")
        return

    cursor.execute("INSERT INTO course_section VALUES(%s, %s, %s, %s, %s);", [course_id, section, semester, year, instructor_id])

def db_get_all_courses_instructor(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM course_section WHERE instructor_id=%s ORDER BY year DESC, semester DESC;",[user_id])
    res = to_dict(cursor)
    return res

def db_get_all_materialsets_instructor(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM instructor_has_set WHERE instructor_id=%s;",[user_id])
    res = to_dict(cursor)
    return res

def db_get_all_students_of_instructor(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM course_section NATURAL JOIN student_takes_course WHERE instructor_id=%s;",[user_id])
    res = to_dict(cursor)
    return res

def db_get_all_courses():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM course_section")
    res = to_dict(cursor)
    return res

