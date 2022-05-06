from django.db import connection
import decimal
from user.models import *
from django.db.models.expressions import RawSQL

def to_dict(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row) for row in cursor.fetchall())]

# update tables
def db_register_mainuser(username, balance, registrar_id, type):
    try:
        connection.cursor().execute("INSERT INTO user_mainuser VALUES (%s, %s, %s, %s);", [username, decimal.Decimal(balance), registrar_id, type])
    except:
        print("main user registration failed in db")
def db_register_librarian(user, specialization):
    try:
        connection.cursor().execute("INSERT INTO user_librarian VALUES (%s, %s);", [user.id, specialization])
    except:
        print("librarian registration failed in db")
def db_register_student(user,department,gpa):
    try:
        connection.cursor().execute("INSERT INTO user_student VALUES (%s, %s, %s);", [user.id, department, gpa])
    except:
        print("student registration failed in db")
def db_register_instructor(user,office,department,tenure):
    try:
        connection.cursor().execute("INSERT INTO user_instructor VALUES (%s, %s, %s,%s);", [user.id, office,department,tenure])
    except:
        print("instructor registration failed in db")
def db_register_outside_member(user,card_no,expire_date):
    try:
        connection.cursor().execute("INSERT INTO user_outsidemember VALUES (%s, CURDATE(), %s,%s);", [user.id,card_no,expire_date])
    except:
        print("outsidemember registration failed in db")
def get_user_type(user_id):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT type FROM user_mainuser WHERE user_id=%s;", [user_id])
        res = cursor.fetchone()
        #print("get_user_type(): " , res[0])
        return res[0]
    except:
        print("get_user_type failed")

def get_all_users():
    #return User.objects.raw("SELECT * FROM auth_user ORDER BY first_name,last_name")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM auth_user A, user_mainuser U WHERE A.username=U.user_id ORDER BY A.first_name,A.last_name;")
        desc = cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        return data
    except:
        print("fetching all user data failed in get_all_users")

def remove_user(username):
    try:
        table_type = get_user_type(username)
        if table_type:
            connection.cursor().execute("DELETE FROM user_%s WHERE user_id=%s;",[table_type,username])
            connection.cursor().execute("DELETE FROM user_mainuser WHERE user_id=%s;",[username])
            connection.cursor().execute("DELETE FROM auth_user WHERE username=%s;",[username])
        else:
            print("table type for removal is null")
    except:
        print("Remove failed")

