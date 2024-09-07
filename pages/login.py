import streamlit as st
import re
from utils import auth_utils, db_utils

def app():
    login()

def login():
    with st.container():
        col1, col2, col3 = st.columns([0.5, 8, 0.5])
        with col2:
            st.subheader("Login")
            with st.form(key='login_form'):
                username = st.text_input("E-mail", placeholder="Digite seu Email")
                password = st.text_input("Senha", placeholder="Digite sua senha", type='password')
                if st.form_submit_button('Entrar'):
                    result = auth_utils.login_user(username, password)
                    if result == "user_not_found":
                        st.error("Usuário não encontrado.")
                    elif result == "incorrect_password":
                        st.error("Senha incorreta.")
                    else:
                        st.session_state.logged_in = True
                        st.session_state.user_id = result
                        st.session_state.page = "Dashboard"
                        st.rerun()
