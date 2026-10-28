import streamlit as st
def home_screen():
    st.header("this is Home screen")
    st1,st2 = st.columns(2)
    with st1:
        st.button("this is teacher")    
        with st2:   
            st.button("this is student")
    st.button("this is student")