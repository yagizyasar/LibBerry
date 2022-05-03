from django.db import connection
import decimal


# update tables
def db_register_user(user, balance, registrar_id):
    if registrar_id == None:
        registrar_id = 1
    connection.cursor().execute("INSERT INTO user_mainuser VALUES (%s, %s, %s);", [user.id, decimal.Decimal(balance), registrar_id])
def db_register_librarian(user, specialization):
    connection.cursor().execute("INSERT INTO user_librarian VALUES (%s, \"%s\");", [user.id, specialization])