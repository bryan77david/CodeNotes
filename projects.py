import streamlit as st
import sqlite3
import database as db
from changes import delete_project_by_name
from html_functions import set_background



# this function returns all the project names
def fetch_project_names():
    """Fetch all project names from the 'projects' table."""
    project_names = []

    try:
        with sqlite3.connect('projects.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT project_name FROM projects")
            rows = cursor.fetchall()
            project_names = [row[0] for row in rows]  # Extract project names from rows
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    return project_names

# this function returns all the project names
def fetch_project_language():
    """Fetch all project languages from the 'projects' table."""
    language_names = []

    try:
        with sqlite3.connect('projects.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT language FROM projects")
            rows = cursor.fetchall()
            language_names = [row[0] for row in rows]  # Extract project names from rows
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    return language_names


def fetch_project_names_languages():
    """Fetch all project names from the 'projects' table."""
    project_names = []
    language_names = []

    try:
        with sqlite3.connect('projects.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT project_name, language FROM projects")
            rows = cursor.fetchall()
            project_names = [row[0] for row in rows]  # Extract project names from rows
            language_names = [row[1] for row in rows]  # Extract project names from rows
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    return project_names, language_names

# this funtions returns a dictiorary with all the fields for one project
def fetch_project_details(project_name):
    """Fetch all details for a given project by name."""
    project_details = {}
    try:
        with sqlite3.connect('projects.db') as conn:
            conn.row_factory = sqlite3.Row  # This allows dictionary access
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE project_name = ?", (project_name,))
            row = cursor.fetchone()
            if row:
                project_details = dict(row)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    return project_details



def project_delete_button(project_name):
    """Displays a delete button for a project and handles its deletion."""
    with st.expander("Delete",):
        st.write("Are you sure?")
        if st.button(f"Delete Project", key=f"delete_{project_name}",type='primary'):
            # Attempt to delete the project
            deleted = delete_project_by_name(project_name)
            if deleted:
                st.success(f"Project '{project_name}' deleted successfully.")
                # Additional codeic to handle UI update or page refresh could be added here
                st.rerun()
            else:
                st.error(f"Failed to delete project '{project_name}'.")


def edit_project_button(project_name):
    """Displays an edit form for a project and handles its update."""
    with st.expander(f"Edit"):
        # Fetch current project details to pre-populate the form
        # Assuming fetch_project_details function returns a dictionary with 'name' and 'content'
        details = fetch_project_details(project_name)
        if details:
            # Form for editing project details
            with st.form(key=f"form_edit_{project_name}",border=False):
                new_content = st.text_area("Project Content", value=details['content'])
                submit_button = st.form_submit_button(label="Update Project")

                if submit_button:
                    try:
                        # Open a database connection
                        with db.get_db_connection() as conn:
                            cursor = conn.cursor()
                            # Call the function to update the project details
                            db.update_record(cursor, project_name, new_content)
                            conn.commit()  # Commit changes
                            st.success(f"Project '{project_name}' updated successfully.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to update project '{project_name}': {e}")


def code_button(project_name):
    """Displays an edit form for a project and handles its update."""
    with st.expander(f"New code Entry",):
        # Fetch current project details to pre-populate the form
        # Assuming fetch_project_details function returns a dictionary with 'name' and 'content'
        details = fetch_project_details(project_name)
        if details:
            # Form for editing project details
            with st.form(key=f"code_edit_{project_name}",border=False,clear_on_submit=True):
                new_code = st.text_area("code Content", value=details['code'])
                submit_button = st.form_submit_button(label="Update code")

                if submit_button:
                    try:
                        # Open a database connection
                        with db.get_db_connection() as conn:
                            cursor = conn.cursor()
                            # Call the function to update the project details
                            db.update_code(cursor, project_name, new_code)
                            conn.commit()  # Commit changes
                            st.success(f"Project '{project_name}' updated successfully.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to update project '{project_name}': {e}")

def edit_cluster(project_name):
    with st.popover(":gear:"):
        # Display the edit button (expander) for the project
        edit_project_button(project_name)
        # Display the delete button for the project
        project_delete_button(project_name)
        code_button(project_name)


def load_project(projects):
    for project_name, tab in projects.items():
        details = fetch_project_details(project_name)

        with tab:
            with st.container(border=True):
                col1, col2, col3 = st.columns((1.8, 2, .2))

                with col1:
                    with st.container(border=False):
                        with st.container(border=False):
                            st.header(project_name)  # Display the project name
                            with st.container():
                                st.write(details['content'])

                with col2:
                    with st.container(border=False):
                        st.caption(":blue[Code Block]")
                        with st.container(border=False):
                            st.code(f"{details['code']}", language= details['language'].lower())

                with col3:
                    # Display the edit button (expander) for the project
                    edit_cluster(project_name)


def project_selector():
    project_names, tab_titles = fetch_project_names_languages()

    # Add a global search bar at the top
    search_query = st.text_input("Search projects")

    # Filter projects based on the search query
    filtered_project_names = []
    filtered_tab_titles = []

    for project_name, tab_title in zip(project_names, tab_titles):
        details = fetch_project_details(project_name)
        if (search_query.lower() in project_name.lower() or
                search_query.lower() in details['content'].lower() or
                search_query.lower() in details['code'].lower()):
            filtered_project_names.append(project_name)
            filtered_tab_titles.append(tab_title)

    if len(filtered_tab_titles) > 0:
        # Ensure unique tab titles
        unique_tabs = list(set(filtered_tab_titles))

        # Create tabs
        tab_instances = st.tabs(unique_tabs)

        # Map each project to its corresponding tab
        projects = {}
        for project, tab_title in zip(filtered_project_names, filtered_tab_titles):
            tab_index = unique_tabs.index(tab_title)
            projects[project] = tab_instances[tab_index]

        # Load projects into corresponding tabs
        load_project(projects)
    else:
        st.write("No projects match the search query!")