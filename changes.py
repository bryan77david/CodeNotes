import streamlit as st
import sqlite3
import database as db

def add_project(language, name):

    with st.form("NewNotes", border=False):
        desc = st.text_area("Enter description of code:")
        code = st.text_area("Enter your code here:")

        submitted = st.form_submit_button("Submit")
        
        if submitted:
            # Check if any field is empty
            if not name or not language or not desc or not code:
                st.error("All fields are required!")
            else:
                try:
                    db.update_project_database('projects.db', name, desc, code, language)
                    st.success("Project added/updated successfully!")
                except Exception as e:
                    st.error(f"Failed to update the database: {e}")

def debbugtest():
    st.write("this is a test")

# this function deletes a project from the database
def delete_project_by_name(project_name):
    """Delete a project record from the database by its name."""
    try:
        with sqlite3.connect('projects.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM projects WHERE project_name = ?", (project_name,))
            conn.commit()  # Commit the changes to the database
            if cursor.rowcount > 0:
                print(f"Project '{project_name}' deleted successfully.")
                return True
            else:
                print(f"No project found with the name '{project_name}'.")
                return False
    except sqlite3.Error as e:
        print(f"An error occurred while trying to delete project '{project_name}': {e}")
        return False
