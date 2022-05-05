from django.db import connection
import decimal
from user.models import *
from django.db.models.expressions import RawSQL

def to_dict(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row) for row in cursor.fetchall())]

# update tables
def db_register_mainuser(username, balance, registrar_id, type):
    connection.cursor().execute("INSERT INTO user_mainuser VALUES (%s, %s, %s, %s);", [username, decimal.Decimal(balance), registrar_id, type])

def db_register_librarian(user, specialization):
    connection.cursor().execute("INSERT INTO user_librarian VALUES (%s, %s);", [user.id, specialization])

def db_register_student(user,department,gpa):
    connection.cursor().execute("INSERT INTO user_student VALUES (%s, %s, %s);", [user.id, department, gpa])

def db_register_instructor(user,office,department,tenure):
    connection.cursor().execute("INSERT INTO user_instructor VALUES (%s, %s, %s,%s);", [user.id, office,department,tenure])

def db_register_outside_member(user,card_no,expire_date):
    connection.cursor().execute("INSERT INTO user_outsidemember VALUES (%s, CURDATE(), %s,%s);", [user.id,card_no,expire_date])

def get_user_type(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT type FROM user_mainuser WHERE user_id=%s;", [user_id])
    res = cursor.fetchone()
    #print("get_user_type(): " , res[0])
    return res[0]

def get_all_users(type):
    #return User.objects.raw("SELECT * FROM auth_user ORDER BY first_name,last_name")
    cursor = connection.cursor()
    cursor.execute("SELECT A.username, A.first_name, A.last_name FROM auth_user A, user_mainuser U WHERE A.username=U.user_id AND U.type=%s ORDER BY A.first_name,A.last_name;", [type])
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    return data

def remove_user(username):
    table_type = get_user_type(username)
    if table_type:
        connection.cursor().execute("DELETE FROM auth_user WHERE username=%s;",[username])
        connection.cursor().execute(("DELETE FROM user_mainuser WHERE user_id=%s",[username]))
        connection.cursor().execute(("DELETE FROM user_%s WHERE user_id=%s",[table_type,username]))
    else:
        print("Remove failed")

