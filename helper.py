import sqlite3

DB_PATH = './todo.db'
NOTSTARTED = 'Not Started'
INPROGRESS = 'In Progress'
COMPLETED = 'Completed'

def add_to_list(title, description):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('insert into items(title, description) values(?,?)', (title,description))
        conn.commit()
        return {"title": title,"description": description, "done": False}
    except Exception as e:
        print('Error: ', e)
        return None

todo_list = {}

def get_all_items():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('select * from items')
        rows = c.fetchall()
        todos = []
        for i in rows:
            todos.append({"id": i[0], "title": i[1], "description": i[2], "done": i[3]})
        return { "count": len(rows), "todos": todos }
    except Exception as e:
        print('Error: ', e)
        return None

def get_item(item_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select * from items where id='%d'" % item_id)
        result = c.fetchone()
        return result
    except Exception as e:
        print('Error: ', e)
        return None
    
def update_status(id, title, description, done):
    
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('update items set title=?, description=?, done=? where id=?', (title, description,done, id))
        conn.commit()
        return {"title": title, "description": description, "done":done}
    except Exception as e:
        print('Error: ', e)
        return None

def delete_item(id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('delete from items where id=?', (id,))
        conn.commit()
        return {'id': id}
    except Exception as e:
        print('Error: ', e)
        return None