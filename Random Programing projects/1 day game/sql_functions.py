import sqlite3

def SQL_select(query, params):
    connection = sqlite3.connect('Christmas_shop.db')
    c = connection.cursor()
    c.execute(query,params)
    results = c.fetchall()
    connection.close()
    return results
    
def SQL_insert(query, params):
    connection = sqlite3.connect('Christmas_shop.db')
    c = connection.cursor()
    c.execute(query, params)
    connection.commit()
    connection.close()

def SQL_update(query, params):
    connection = sqlite3.connect('Christmas_shop.db')
    c = connection.cursor()
    c.execute(query, params)
    connection.commit()
    connection.close()

def SQL_delete(query, params):
    connection = sqlite3.connect('Christmas_shop.db')
    c = connection.cursor()
    c.execute(query, params)
    connection.commit()
    connection.close()

