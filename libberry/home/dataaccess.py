from django.db import connection


# update tables
def db_register_user(user, balance, registrar_id):
    connection.cursor().execute("INSERT INTO main_user ()")