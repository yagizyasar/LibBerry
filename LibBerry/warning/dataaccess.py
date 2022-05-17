from sqlite3 import connect
from django.db import connection
from django.shortcuts import redirect
from user.models import *
from home.dataaccess import to_dict
from datetime import datetime

def db_send_nearly_due_warning(warn_id, message, send_date, user_id, librarian_id, remaining_days, mat_id="-"):
    cursor = connection.cursor()

    if mat_id != "-":
        cursor.execute("SELECT due_date FROM user_reserves_mat WHERE user_id=%s AND mat_id=%s AND status='borrowed';", [user_id, mat_id])

    cursor.execute("INSERT INTO warning VALUES(%s, %s, %s);", [warn_id, message, send_date])
    cursor.execute("INSERT INTO nearly_due_warning VALUES(%s, %s);", [warn_id, remaining_days])

def db_send_overdue_warning(warn_id, message, send_date, user_id, librarian_id, overdue_balance, mat_id="-"):
    cursor = connection.cursor()

    if mat_id != "-":
        cursor.execute("SELECT due_date FROM user_reserves_mat WHERE user_id=%s AND mat_id=%s AND status='borrowed';", [user_id, mat_id])

    cursor.execute("INSERT INTO warning VALUES(%s, %s, %s);", [warn_id, message, send_date])
    cursor.execute("INSERT INTO overdue_warning VALUES(%s, %s);", [warn_id, overdue_balance])

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

def db_get_user_warnings(user_id):
    cursor = connection.cursor()
    cursor.execute()