import streamlit as st
import changes
import home
import projects as pr
from html_functions import set_background_SB, set_background, set_background_container

st.set_page_config("CodeNotes", ':book:', 'wide')



def main():
    navigation = st.sidebar.radio("Naviagate to:",["Home",
                                                       "Notes",
                                                       "Add Notes"])
    
    set_background_SB('Images/notebook.jpg')
    set_background_container()
    set_background('Images/notebook.avif')
    if navigation == "Home":
        home.HOME()

    if navigation == "Notes":
        pr.project_selector()
        


    if navigation == "Add Notes":
        action = st.radio("select action:",['Add','Delete'],horizontal=True, captions=['Add new notes','Delete notes'])
        if action == "Add":
            with st.container(border=True):
                language = st.selectbox("Enter programming language:",['Python','R','Javascript','SAS','SQL','Julia'])
                name = st.text_input("Enter code function:")
                changes.add_project(language,name)
        if action == "Delete":
            st.write("this feature will be available soon")



if __name__ == "__main__":
    main()
