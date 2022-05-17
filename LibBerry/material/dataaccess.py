from django.db import connection
from django.shortcuts import redirect
from user.models import *
from home.dataaccess import to_dict
from datetime import datetime

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
    
    if (amount) > result_amount[0]:
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

def db_add_material_set(creator_id, publicity, set_id):
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM material_material_set WHERE set_id=%s;", [set_id])
    res = cursor.fetchone()
    if res != None:
        print("Invalid add material set request: Set id already exists")
        return
    
    cursor.execute("INSERT INTO material_material_set VALUES(%s, %s, %s);", [set_id,publicity,set_id])
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
    return db_generate_find_mat_query({"rating_threshold":0, "published_after":"1000-01-01", "published_before":"3000-01-01"})

def db_get_all_audiovisuals():
    return db_generate_find_audiovisual_query({"rating_threshold":0, "published_after":"1000-01-01", "published_before":"3000-01-01"})

def db_get_all_periodicals():
    return db_generate_find_periodical_query({"rating_threshold":0, "published_after":"1000-01-01", "published_before":"3000-01-01"})

def db_get_all_printeds():
    return db_generate_find_printed_query({"rating_threshold":0, "published_after":"1000-01-01", "published_before":"3000-01-01"})

def db_generate_find_mat_query(params):
    #query = "SELECT * FROM (material_material NATURAL JOIN ((SELECT T1.mat_id, 0 AS available FROM (SELECT DISTINCT T4.mat_id AS mat_id FROM material_material T4 WHERE T4.mat_id NOT IN (SELECT DISTINCT T3.mat_id AS mat_id FROM user_reserves_mat AS T3 WHERE T3.status='borrowed' OR T3.status='on hold')) AS T1 UNION SELECT T2.mat_id AS mat_id, COUNT(*) AS available FROM user_reserves_mat AS T2 WHERE T2.status='borrowed' OR T2.status='on hold' GROUP BY T2.mat_id) AS T5) AS T9) AS M;"
    query = "SELECT * FROM material_material AS M WHERE "

    # TODO search by multiple fields?
    # search fields
    title = params.get("title")
    authors = params.get("author")
    date = params.get("date")
    genre = params.get("genre")
    sets = params.get("set")

    if title != None and title != "":
        if "%" in title or "_" in title:
            query += "M.title LIKE \"{}\" AND ".format(title)
        else:
            query += "M.title=\"{}\" AND ".format(title)
    if authors != None and len(authors) > 0:
        for author in authors:
            query += "EXISTS (SELECT * FROM is_author_of I WHERE author_id={} AND mat_id=M.mat_id) AND ".format(author)
    if genre != None and genre != "":
        query += "M.genre=\"{}\" AND ".format(genre)

    if sets != None and len(sets) > 0:
        for set in sets:
            query += "EXISTS (SELECT * FROM set_contains_mat C WHERE C.set_id={} AND C.mat_id=M.mat_id) AND ".format(set)
    
    # rating threshold
    query += "(M.rating IS NULL OR M.rating>={}) AND ".format(params.get("rating_threshold"))
    
    # published after threshold
    query += "M.publish_date>=\"{}\" AND ".format(params.get("published_after"))
    
    # published before
    query += "M.publish_date<=\"{}\" ".format(params.get("published_before"))

    #query = query[:-3]
    if query[-6:] == "WHERE ":
        query = query[:-7]
    query += ";"
    print(query)
    cursor = connection.cursor()
    cursor.execute(query)
    res = to_dict(cursor)
    #cursor.execute()
    print(res)
    print(len(res))
    return res

def db_generate_find_audiovisual_query(params):
    #query = "SELECT * FROM (material_material NATURAL JOIN ((SELECT T1.mat_id, 0 AS available FROM (SELECT DISTINCT T4.mat_id AS mat_id FROM material_material T4 WHERE T4.mat_id NOT IN (SELECT DISTINCT T3.mat_id AS mat_id FROM user_reserves_mat AS T3 WHERE T3.status='borrowed' OR T3.status='on hold')) AS T1 UNION SELECT T2.mat_id AS mat_id, COUNT(*) AS available FROM user_reserves_mat AS T2 WHERE T2.status='borrowed' OR T2.status='on hold' GROUP BY T2.mat_id) AS T5) AS T9) AS M;"
    query = "SELECT * FROM (SELECT * FROM material_material NATURAL JOIN material_audiovisual) AS M WHERE "

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
    if genre != None and genre != "":
        query += "M.genre=\"{}\" AND ".format(genre)

    if sets != None and len(sets) > 0:
        for set in sets:
            query += "EXISTS (SELECT * FROM set_contains_mat C WHERE C.set_id={} AND C.mat_id=M.mat_id) AND ".format(set)
    
    # rating threshold
    query += "(M.rating IS NULL OR M.rating>={}) AND ".format(params.get("rating_threshold"))
    
    # published after threshold
    query += "M.publish_date>=\"{}\" AND ".format(params.get("published_after"))
    
    # published before
    query += "M.publish_date<=\"{}\" ".format(params.get("published_before"))
    
    #query = query[:-3]
    if query[-6:] == "WHERE ":
        query = query[:-7]
    query += ";"
    print(query)
    cursor = connection.cursor()
    cursor.execute(query)
    res = to_dict(cursor)
    #cursor.execute()
    print(res)
    print(len(res))
    return res

def db_generate_find_printed_query(params):
    #query = "SELECT * FROM (material_material NATURAL JOIN ((SELECT T1.mat_id, 0 AS available FROM (SELECT DISTINCT T4.mat_id AS mat_id FROM material_material T4 WHERE T4.mat_id NOT IN (SELECT DISTINCT T3.mat_id AS mat_id FROM user_reserves_mat AS T3 WHERE T3.status='borrowed' OR T3.status='on hold')) AS T1 UNION SELECT T2.mat_id AS mat_id, COUNT(*) AS available FROM user_reserves_mat AS T2 WHERE T2.status='borrowed' OR T2.status='on hold' GROUP BY T2.mat_id) AS T5) AS T9) AS M;"
    query = "SELECT * FROM (SELECT * FROM material_material NATURAL JOIN material_printed ) AS M WHERE "

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
    if genre != None and genre != "":
        query += "M.genre=\"{}\" AND ".format(genre)

    if sets != None and len(sets) > 0:
        for set in sets:
            query += "EXISTS (SELECT * FROM set_contains_mat C WHERE C.set_id={} AND C.mat_id=M.mat_id) AND ".format(set)
    
    # rating threshold
    query += "(M.rating IS NULL OR M.rating>={}) AND ".format(params.get("rating_threshold"))
    
    # published after threshold
    query += "M.publish_date>=\"{}\" AND ".format(params.get("published_after"))
    
    # published before
    query += "M.publish_date<=\"{}\" ".format(params.get("published_before"))
    
    #query = query[:-3]
    if query[-6:] == "WHERE ":
        query = query[:-7]
    query += ";"
    print(query)
    cursor = connection.cursor()
    cursor.execute(query)
    res = to_dict(cursor)
    #cursor.execute()
    print(res)
    print(len(res))
    return res

def db_generate_find_periodical_query(params):
    #query = "SELECT * FROM (material_material NATURAL JOIN ((SELECT T1.mat_id, 0 AS available FROM (SELECT DISTINCT T4.mat_id AS mat_id FROM material_material T4 WHERE T4.mat_id NOT IN (SELECT DISTINCT T3.mat_id AS mat_id FROM user_reserves_mat AS T3 WHERE T3.status='borrowed' OR T3.status='on hold')) AS T1 UNION SELECT T2.mat_id AS mat_id, COUNT(*) AS available FROM user_reserves_mat AS T2 WHERE T2.status='borrowed' OR T2.status='on hold' GROUP BY T2.mat_id) AS T5) AS T9) AS M;"
    query = "SELECT * FROM (SELECT * FROM material_material NATURAL JOIN material_periodical) AS M WHERE "

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
    if genre != None and genre != "":
        query += "M.genre=\"{}\" AND ".format(genre)

    if sets != None and len(sets) > 0:
        for set in sets:
            query += "EXISTS (SELECT * FROM set_contains_mat C WHERE C.set_id={} AND C.mat_id=M.mat_id) AND ".format(set)
    
    # rating threshold
    query += "(M.rating IS NULL OR M.rating>={}) AND ".format(params.get("rating_threshold"))
    
    # published after threshold
    query += "M.publish_date>=\"{}\" AND ".format(params.get("published_after"))
    
    # published before
    query += "M.publish_date<=\"{}\" ".format(params.get("published_before"))
    
    #query = query[:-3]
    if query[-6:] == "WHERE ":
        query = query[:-7]
    query += ";"
    print(query)
    cursor = connection.cursor()
    cursor.execute(query)
    res = to_dict(cursor)
    #cursor.execute()
    print(res)
    print(len(res))
    return res

def db_get_unavailable_counts():
    cursor = connection.cursor()
    cursor.execute("SELECT mat_id, COUNT(*) AS unavailable FROM user_reserves_mat WHERE status='borrowed' OR status='on hold' GROUP BY mat_id;")
    res = to_dict(cursor)
    return res

def db_get_all_sets_of_instructor(instructor_id):
     cursor = connection.cursor()
     cursor.execute("SELECT set_id FROM instructor_has_set WHERE instructor_id=%s;", [instructor_id])
     res = to_dict(cursor)
     return res

def db_get_all_courses_of_instructor(instructor_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM course_section WHERE instructor_id=%s ORDER BY year DESC, semester DESC;",[instructor_id])
    res = to_dict(cursor)
    return res

def db_send_hold_request(user_id, mat_id, message=""):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_reserves_mat WHERE user_id=%s AND mat_id=%s AND (status='on hold' OR status='borrowed');", [user_id, mat_id])
    res = cursor.fetchone()
    if res != None:
        print("Invalid borrow request: User already borrowed or has on hold material")
        return

    cursor.execute("SELECT COUNT(*) FROM user_reserves_mat WHERE mat_id=%s AND (status='borrowed' OR status='on hold');", [mat_id])
    unavailable_amount = (cursor.fetchone())[0]
    cursor.execute("SELECT amount FROM material_material WHERE mat_id=%s;", [mat_id])
    total_amount = (cursor.fetchone())[0]

    if unavailable_amount >= total_amount:
        print("Invalid send hold request: Material not available")
        return

    cursor.execute("INSERT INTO user_reserves_mat VALUES(%s, %s, NOW(), '1', NULL, NULL, 'on hold', %s, NULL);", [user_id, mat_id, message])

def db_cancel_hold_request(user_id, mat_id):
    cursor = connection.cursor()
    cursor.execute("UPDATE user_reserves_mat SET status='cancelled', ret_date=NOW() WHERE user_id=%s, mat_id=%s;", [user_id, mat_id])

def db_conclude_hold_request(user_id, mat_id, librarian_id, accepted, message="", due=""):
    cursor = connection.cursor()

    # TODO constraint checking
    if accepted:
        cursor.execute("UPDATE user_reserves_mat SET status='borrowed', message=%s, librarian_id=%s, reserve_date=NOW(), due_date=%s WHERE user_id=%s AND mat_id=%s AND status='on hold';", [message, librarian_id, due, user_id, mat_id])
    else:
        cursor.execute("UPDATE user_reserves_mat SET status='rejected', message=%s, librarian_id=%s, reserve_date=NOW(), due_date=%s WHERE user_id=%s AND mat_id=%s AND status='on hold';", [message, librarian_id, due, user_id, mat_id])

def db_return_book(user_id, mat_id, message="", overdue_amount=0):
    cursor = connection.cursor()
    cursor.execute("SELECT due_date FROM user_reserves_mat WHERE user_id=%s AND mat_id=%s AND status='borrowed';", [user_id, mat_id])
    due = cursor.fetchone()[0]
    print(due)
    print(type(due))
    #due = datetime.strptime(due, "%y-%m-%d %H:%M:%S")
    overdue_amount = int(overdue_amount)
    if message == "" and due < datetime.now():
        dif = datetime.now() - due
        overdue_message = "Overdue by {} days, {} hours and {} minutes.".format(dif.days, dif.seconds // 3600, dif.seconds // 60)
        balance_message = ""
        if overdue_amount > 0:
            balance_message = " {} liras were added to debt.".format(overdue_amount)
        message = overdue_message + balance_message

    cursor.execute("UPDATE user_reserves_mat SET status='returned', message=%s, return_date=NOW() WHERE user_id=%s AND mat_id=%s AND status='borrowed';", [message, user_id, mat_id])
    oldbal = db_get_user_balance(user_id)
    cursor.execute("UPDATE user_mainuser SET balance=%s WHERE user_id=%s;", [oldbal + overdue_amount, user_id])

def db_get_reservation_requests(status):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_reserves_mat WHERE status=%s;", [status])
    res_dict = to_dict(cursor)
    return res_dict

def db_get_all_reservation_requests():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_reserves_mat")
    res_dict = to_dict(cursor)
    return res_dict

def db_rate_mat(user_id, mat_id, rating):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_rates_mat WHERE user_id=%s AND mat_id=%s;", [user_id, mat_id])
    res = cursor.fetchone()
    if res != None:
        cursor.execute("UPDATE user_rates_mat SET rating=%s WHERE user_id=%s AND mat_id=%s;", [rating, user_id, mat_id])
    else:
        cursor.execute("INSERT INTO user_rates_mat VALUES(%s, %s, %s);", [user_id, mat_id, rating])

def db_get_mat_unavailable_amounts():
    cursor = connection.cursor()
    cursor.execute("(SELECT mat_id, COUNT(*) AS unavailable FROM user_reserves_mat WHERE status='on hold' OR status='borrowed' GROUP BY mat_id) UNION (SELECT mat_id, 0 AS unavailable FROM material_material WHERE mat_id NOT IN (SELECT mat_id FROM user_reserves_mat WHERE status='on hold' OR status='borrowed'));")
    res = to_dict(cursor)
    print(len(res))
    return res

def db_get_user_balance(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT balance FROM user_mainuser WHERE user_id=%s;", [user_id])
    res = (cursor.fetchone())[0]
    return res