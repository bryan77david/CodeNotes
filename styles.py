import streamlit as st

def status_color(status):
    if status == 'In Progress':
        st.caption(f":green[{status}]")
    if status == 'Completed':
        st.caption(f":blue[{status}]")
    if status == 'On Hold':
        st.caption(f":violet[{status}]")
    if status == 'Abandoned':
        st.caption(f":red[{status}]")



