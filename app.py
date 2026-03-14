import streamlit as st
from agents import planner_agent, document_agent, form_agent

st.title("Yukti AI")
st.write("Government Service Assistant")

service = st.text_input("What government service do you need?")

if st.button("Analyze"):

    st.subheader("Service Plan")
    st.write(planner_agent(service))

    st.subheader("Required Documents")
    st.write(document_agent(service))

    st.subheader("Form Fields")
    st.write(form_agent(service))