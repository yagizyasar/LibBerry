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
        cursor.execute("INSERT INTO material_material VALUES (%s, %s, %s, %s,%s,%s,%s);", [mat_id, title, genre,publish_date,amount,location,"NULL"])
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
        #cursor.execute("DELETE FROM is_author_of WHERE mat_id=%s;", [mat_id])
        cursor.execute("DELETE FROM material_material WHERE mat_id=%s;", [mat_id])
        return

    cursor.execute("SELECT * FROM material_periodical WHERE mat_id=%s;", [mat_id])
    result = cursor.fetchone()
    if result != None: # remove request is for a periodical material
        cursor.execute("DELETE FROM material_periodical WHERE mat_id=%s;", [mat_id])
        #cursor.execute("DELETE FROM is_author_of WHERE mat_id=%s;", [mat_id])
        cursor.execute("DELETE FROM material_material WHERE mat_id=%s;", [mat_id])
        return

    cursor.execute("SELECT * FROM material_audiovisual WHERE mat_id=%s;", [mat_id])
    result = cursor.fetchone()
    if result != None: # remove request is for a audiovisual material
        cursor.execute("DELETE FROM material_audiovisual WHERE mat_id=%s;", [mat_id])
        #cursor.execute("DELETE FROM is_author_of WHERE mat_id=%s;", [mat_id])
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

def db_add_material_set(creator_id, publicity, set_name):
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM material_material_set WHERE set_id=%s;", [set_id])
    res = cursor.fetchone()
    if res != None:
        print("Invalid add material set request: Set id already exists")
        return
    
    cursor.execute("INSERT INTO material_material_set VALUES(%s, %s, %s);", [publicity, set_name])
    cursor.execute("INSERT INTO instructor_has_set VALUES(%s, %s)", [creator_id, set_id])

def db_add_materials_to_material_set(set_id, mat_ids):
    cursor = connection.cursor()
    for mat_id in mat_ids:
        cursor.execute("SELECT * FROM set_contains_mat WHERE set_id=%s AND mat_id=%s;", [set_id, mat_id])
        res = cursor.fetchone()

        if res != None:
            print("Invalid add material to set request: Material already in the set")
            return
    
    for mat_id in mat_ids:
        cursor.execute("INSERT INTO set_contains_mat VALUES (%s, %s);", [set_id, mat_id])

def db_remove_material_from_material_set(set_id, mat_ids):
    cursor = connection.cursor()

    for mat_id in mat_ids:
        cursor.execute("SELECT * FROM set_contains_mat WHERE set_id=%s AND mat_id=%s;", [set_id, mat_id])
        res = cursor.fetchone()

        if res == None:
            print("Invalid remove material from set request: Material not in the set")
            return
    
    for mat_id in mat_ids:
        cursor.execute("DELETE FROM set_contains_mat WHERE set_id=%s AND mat_id=%s;", [set_id, mat_id])

def db_remove_material_set(set_id):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM material_material_set WHERE set_id=%s;", [set_id])
    res = cursor.fetchone()

    if res == None:
        print("Invalid remove material set request: Set does not exist")
        return

    cursor.execute("DELETE FROM material_material_set WHERE set_id=%s;", [set_id])

def db_get_all_mats():
    return db_generate_find_mat_query({"rating_threshold":0, "published_after":"1000-01-01"})

def db_generate_find_mat_query(params):
    query = "SELECT * FROM material_material M WHERE "

    # TODO search by multiple fields?
    # search fields
    title = params.get("title")
    authors = params.get("author")
    date = params.get("date")
    genre = params.get("genre")
    sets = params.get("set")

    if title != None and title != "":
        query += "M.title=\"{}\" AND ".format(title)
    if authors != None and len(authors) > 0:
        for author in authors:
            query += "EXISTS (SELECT * FROM is_author_of I WHERE author_id={} AND mat_id=M.mat_id) AND ".format(author)
    """
    if date != None:
        query += "M.publish_date=\"{}\" AND ".format(date)
    """
    if genre != None and genre != "":
        query += "M.genre=\"{}\" AND ".format(genre)

    if sets != None and len(sets) > 0:
        for set in sets:
            query += "EXISTS (SELECT * FROM set_contains_mat C WHERE C.set_id={} AND C.mat_id=M.mat_id) AND ".format(set)
    
    # rating threshold
    query += "(M.rating IS NULL OR M.rating>={}) AND ".format(params.get("rating_threshold"))
    
    # published after threshold
    query += "M.publish_date>=\"{}\"".format(params.get("published_after"))

    #query = query[:-3]
    if query[-6:] == "WHERE ":
        query = query[:-7]
    query += ";"
    print(query)
    cursor = connection.cursor()
    cursor.execute(query)
    res = to_dict(cursor)
    #print(res)
    print(len(res))
    return res
    # TODO process query result

def db_get_all_sets_of_instructor(instructor_id):
     cursor = connection.cursor()
     cursor.execute("SELECT set_id FROM instructor_has_set WHERE instructor_id=%s;", [instructor_id])
     res = to_dict(cursor)
     return res

def db_get_all_courses_of_instructor(instructor_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM course_section WHERE instructor_id=%s;",[instructor_id])
    res = to_dict(cursor)
    return res
