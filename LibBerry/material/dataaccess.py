from django.db import connection
from django.shortcuts import redirect
from user.models import *
from home.dataaccess import to_dict

def db_add_material(mat_id,title,genre,publish_date,amount,location,author_ids):
    cursor = connection.cursor()
    cursor.execute("SELECT amount FROM material_material WHERE mat_id=%s;",[mat_id])
    result_amount = cursor.fetchone()
    if result_amount != None:
        updated_result = result_amount[0]
        updated_result += amount
        cursor.execute("UPDATE material_material SET amount=%s WHERE mat_id=%s",[updated_result,mat_id])
        return True
    else:   
        cursor.execute("INSERT INTO material_material VALUES (%s, %s, %s, %s,%s,%s);", [mat_id, title, genre,publish_date,amount,location])
        for author_id in author_ids:
            cursor.execute("INSERT INTO is_author_of VALUES(%s, %s);", [author_id, mat_id])
        return False
    
def db_add_material_periodical(mat_id,title,genre,publish_date,amount,location,pages,period,author_ids):
    if(not db_add_material(mat_id,title,genre,publish_date,amount,location,author_ids)):
        connection.cursor().execute("INSERT INTO material_periodical VALUES (%s, %s, %s);", [mat_id,pages,period])

def db_add_material_printed(mat_id,title,genre,publish_date,amount,location,pages,author_ids):
    if(not db_add_material(mat_id,title,genre,publish_date,amount,location,author_ids)):
        connection.cursor().execute("INSERT INTO material_printed VALUES (%s, %s);", [mat_id,pages])

def db_add_material_audiovisual(mat_id,title,genre,publish_date,amount,location,external_rating,length,author_ids):
    if(not db_add_material(mat_id,title,genre,publish_date,amount,location,author_ids)):
        connection.cursor().execute("INSERT INTO material_audiovisual VALUES (%s, %s,%s);",[mat_id, external_rating,length])

def db_remove_material(mat_id, amount):
    cursor = connection.cursor()
    
    cursor.execute("SELECT amount FROM material_material WHERE mat_id=%s;", [mat_id])
    result_amount = cursor.fetchone()

    if result_amount == None:
        print("Invalid remove material request: Material does not exist")
        return redirect('remove_material')
    
    if amount > result_amount[0]:
        print("Invalid remove material request: Requested remove amount larger than the amount in library")
        return redirect('remove_material')
    
    if amount < result_amount[0]:
        updated_result = result_amount[0]
        updated_result -= amount
        cursor.execute("UPDATE material_material SET amount=%s WHERE mat_id=%s", [updated_result, mat_id])
        return

    # last remaining possibility is amount == result_amount[0]

    cursor.execute("SELECT * FROM material_printed WHERE mat_id=%s;", [mat_id])
    result = cursor.fetchone() # should be a single row if mat_id exists in table, or None if it doesn't
    if result != None: # remove request is for a printed material
        cursor.execute("DELETE FROM material_printed WHERE mat_id=%s;", [mat_id])
        cursor.execute("DELETE FROM is_author_of WHERE mat_id=%s;", [mat_id])
        cursor.execute("DELETE FROM material_material WHERE mat_id=%s;", [mat_id])
        return

    cursor.execute("SELECT * FROM material_periodical WHERE mat_id=%s;", [mat_id])
    result = cursor.fetchone()
    if result != None: # remove request is for a periodical material
        cursor.execute("DELETE FROM material_periodical WHERE mat_id=%s;", [mat_id])
        cursor.execute("DELETE FROM is_author_of WHERE mat_id=%s;", [mat_id])
        cursor.execute("DELETE FROM material_material WHERE mat_id=%s;", [mat_id])
        return

    cursor.execute("SELECT * FROM material_audiovisual WHERE mat_id=%s;", [mat_id])
    result = cursor.fetchone()
    if result != None: # remove request is for a audiovisual material
        cursor.execute("DELETE FROM material_audiovisual WHERE mat_id=%s;", [mat_id])
        cursor.execute("DELETE FROM is_author_of WHERE mat_id=%s;", [mat_id])
        cursor.execute("DELETE FROM material_material WHERE mat_id=%s;", [mat_id])
        return

def db_add_author(author_id, name, birth, bio):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM material_author WHERE author_id=%s;", [author_id])
    res = cursor.fetchone()
    if res != None:
        print("Invalid add author request: Author id already exists")
        return
    
    cursor.execute("INSERT INTO material_author VALUES(%s, %s, %s, %s);", [author_id, name, birth, bio])

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
    cursor = connection.cursor()
    cursor.execute(query)
    
    # TODO process query result