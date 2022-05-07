from django.db import connection
from user.models import *

def db_add_material(mat_id,title,genre,publish_date,amount,location):
    cursor = connection.cursor()
    cursor.execute("SELECT amount FROM material_material where mat_id=%s;",[mat_id])
    result_amount = cursor.fetchone()
    if result_amount != None:
        updated_result = result_amount[0]
        updated_result += amount
        cursor.execute("UPDATE material_material SET amount = %s WHERE mat_id=%s",[updated_result,mat_id])
    else:   
        cursor.execute("INSERT INTO material_material VALUES (%s, %s, %s, %s,%s,%s);", [mat_id, title, genre,publish_date,amount,location])
    
def db_add_material_periodical(mat_id,title,genre,publish_date,amount,location,pages,period):
    db_add_material(mat_id,title,genre,publish_date,amount,location)
    connection.cursor().execute("INSERT INTO material_periodical VALUES (%s, %s, %s);", [mat_id,pages,period])

def db_add_material_printed(mat_id,title,genre,publish_date,amount,location,pages,period):
    db_add_material(mat_id,title,genre,publish_date,amount,location)
    connection.cursor().execute("INSERT INTO material_printed VALUES (%s, %s);", [mat_id,pages])
"""
def db_find_mats(params):
    query = "SELECT * FROM material_material WHERE "
    match params.get("search_param_type")
        case "title":
            query += 
"""
