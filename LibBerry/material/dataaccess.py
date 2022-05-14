from django.db import connection
from user.models import *

def db_add_material(mat_id,title,genre,publish_date,amount,location):
    cursor = connection.cursor()
    cursor.execute("SELECT amount FROM material_material WHERE mat_id=%s;",[mat_id])
    result_amount = cursor.fetchone()
    if result_amount != None:
        updated_result = result_amount[0]
        updated_result += amount
        cursor.execute("UPDATE material_material SET amount = %s WHERE mat_id=%s",[updated_result,mat_id])
        return True
    else:   
        cursor.execute("INSERT INTO material_material VALUES (%s, %s, %s, %s,%s,%s);", [mat_id, title, genre,publish_date,amount,location])
        return False
    
def db_add_material_periodical(mat_id,title,genre,publish_date,amount,location,pages,period):
    db_add_material(mat_id,title,genre,publish_date,amount,location)
    connection.cursor().execute("INSERT INTO material_periodical VALUES (%s, %s, %s);", [mat_id,pages,period])

def db_add_material_printed(mat_id,title,genre,publish_date,amount,location,pages):
    if(not db_add_material(mat_id,title,genre,publish_date,amount,location)):
        connection.cursor().execute("INSERT INTO material_printed VALUES (%s, %s);", [mat_id,pages])

def db_remove_material(mat_id, amount):
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM material_printed WHERE mat_id=%s;", [mat_id])
    result = cursor.fetchone()


def db_generate_find_mat_query(params):
    query = "SELECT * FROM material_material WHERE "

    # TODO search by multiple fields?
    # search fields
    match params.get("search_param_type"):
        case "title":
            query += "title=\"{}\" AND ".format(params.get("title"))
        case "author":
            return # TODO
        case "date":
            query += "publish_date=\"{}\" AND ".format(params.get("publish_date"))
        case "genre":
            query += "genre=\"{}\" AND ".format(params.get("genre"))
        case "set":
            return # TODO

    # rating threshold
    query += "rating>={} AND ".format(params.get("rating_threshold"))
    
    # published after threshold
    query += "publish_date>=\"{}\"".format(params.get("published_after"))

    query = query[:-3]
    query += ";"
    print(query)
    #cursor = connection.cursor()
    #cursor.execute(query)
    # TODO process query result

