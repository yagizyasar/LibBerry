from django.db import connection
import decimal


# update tables
def db_register_mainuser(user, balance, registrar_id):
    connection.cursor().execute("INSERT INTO user_mainuser VALUES (%s, %s, %s);", [user.id, decimal.Decimal(balance), registrar_id])

def db_register_librarian(user, specialization):
    connection.cursor().execute("INSERT INTO user_librarian VALUES (%s, %s);", [user.id, specialization])

def db_register_student(user,department,gpa):
    connection.cursor().execute("INSERT INTO user_student VALUES (%s, %s, %s);", [user.id, department, gpa])

def db_register_instructor(user,office,department,tenure):
    connection.cursor().execute("INSERT INTO user_instructor VALUES (%s, %s, %s,%s);", [user.id, office,department,tenure])

def db_register_outside_member(user,card_no,expire_date):
     connection.cursor().execute("INSERT INTO user_outsidemember VALUES (%s, CURDATE(), %s,%s);", [user.id,card_no,expire_date])

