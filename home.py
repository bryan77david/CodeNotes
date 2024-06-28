import streamlit as st
import pandas as pd


import sqlite3

def fetch_table():
    """
    Fetch all records from the 'projects' table.
    """
    try:
        with sqlite3.connect('projects.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects")  # Fetch all columns
            rows = cursor.fetchall()
            # Create a list of dictionaries for better data structure handling
            columns = [description[0] for description in cursor.description]
            projects = [dict(zip(columns, row)) for row in rows]
            return projects
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []



def download_projects():
    details = fetch_table()
    df = pd.DataFrame(details).set_index('id')
    df.to_excel('Projects.xlsx')
    st.success("Projects file downloaded successfully!")

# function for the HOME page (Projects Overview)
def HOME():
    st.write('''
             This is a Place Holder String''')

    st.button("download Projects",on_click=download_projects)
    



    