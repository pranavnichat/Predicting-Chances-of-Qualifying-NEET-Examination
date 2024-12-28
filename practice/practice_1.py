import streamlit as st

counter=0
st.write(counter)

if st.button("up"):
    counter = counter+1
    st.write(counter)