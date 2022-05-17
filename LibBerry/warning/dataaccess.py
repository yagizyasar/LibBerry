from sqlite3 import connect
from django.db import connection
from django.shortcuts import redirect
from user.models import *
from home.dataaccess import to_dict
from datetime import datetime

def db_send_overdue_warning(message,user_id, librarian_id, mat_id,debt):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO warning VALUES(%s,%s,NOW(),%s,%s);",[user_id,mat_id,librarian_id,message])
    cursor.execute("INSERT INTO overdue_warning VALUES(%s,%s,NOW(),%s);",[user_id,mat_id,debt])

def db_send_neardue_warning(message,user_id, librarian_id, mat_id,remaining_days):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO warning VALUES(%s,%s,NOW(),%s,%s);",[user_id,mat_id,librarian_id,message])
    cursor.execute("INSERT INTO near_due_warning VALUES(%s, %s,NOW(),%s);", [user_id,mat_id,remaining_days])

def db_get_user_borrowed_books(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT mat_id, title FROM user_reserves_mat WHERE status='borrowed' AND user_id=%s;", [user_id])
    res = to_dict(cursor)
    return res

def db_get_due_date(user_id, mat_id):
    cursor = connection.cursor()
    cursor.execute("SELECT due_date FROM user_reserves_mat WHERE user_id=%s AND mat_id=%s AND status='borrowed';", [user_id, mat_id])
    res = to_dict(cursor)
    return res

def db_get_user_near_due_warnings(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM warning NATURAL JOIN near_due_warning WHERE user_id=%s;", [user_id])
    res = to_dict(cursor)
    return res

def db_get_user_overdue_warnings(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM warning NATURAL JOIN overdue_warning WHERE user_id=%s;", [user_id])
    res = to_dict(cursor)
    return res