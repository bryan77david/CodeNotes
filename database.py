import sqlite3


def get_db_connection():
    return sqlite3.connect('projects.db')

def table_exists(cursor):
    """Check if the 'projects' table exists in the database."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
    return cursor.fetchone() is not None

def update_record(cursor, project_name, content):
    """Update an existing record in the 'projects' table."""
    cursor.execute("UPDATE projects SET content=? WHERE project_name=?", (content, project_name))


def update_code(cursor, project_name, code):
    """Update an existing record in the 'projects' table."""
    cursor.execute("UPDATE projects SET code=? WHERE project_name=?", (code, project_name))


def insert_record(cursor, project_name, content,code,language):
    """Insert a new record into the 'projects' table."""
    cursor.execute("INSERT INTO projects (project_name, content,code, language) VALUES (?, ?, ?,?,?)", (project_name, content,code,language))

def update_project_database(database_file, project_name, content,code, language):
    try:
        with sqlite3.connect(database_file) as conn:
            cursor = conn.cursor()
            # Check if table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
            table_exists = cursor.fetchone()

            if not table_exists:
                print("Table does not exist. Creating table.")
                cursor.execute('''CREATE TABLE projects (
                                    id INTEGER PRIMARY KEY,
                                    project_name TEXT UNIQUE,
                                    content TEXT,
                                    code TEXT,
                                    language TEXT
                                )''')

            # Check if the project exists
            cursor.execute("SELECT 1 FROM projects WHERE project_name = ?", (project_name,))
            project_exists = cursor.fetchone()

            if project_exists:
                print(f"Project {project_name} exists. Updating.")
                cursor.execute("UPDATE projects SET content = ?,code=?,language=? WHERE project_name = ?", (content,code,language, project_name))
            else:
                print(f"Adding new project: {project_name}")
                cursor.execute("INSERT INTO projects (project_name, content,code,language) VALUES (?,?,?,?)", (project_name, content,code,language))
                
            conn.commit()
            print("Database operation successful.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")


