import streamlit as st
from utils.auth_utils import authenticate_user, get_user_by_email

def app():
    st.title("Login")
    
    with st.form(key='login_form'):
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")
        submit_button = st.form_submit_button("Entrar")
    
    if submit_button:
        if authenticate_user(email, password):
            # Autenticação bem-sucedida
            st.session_state.logged_in = True

            # Armazenar informações do usuário no session_state
            user = get_user_by_email(email)  # Pega os dados do usuário pelo email
            st.session_state['user_id'] = user['user_id']
            st.session_state['user_email'] = user['email']

            st.success("Login bem-sucedido!")
            st.rerun()  # Recarrega a página para redirecionar
        else:
            st.error("Email ou senha incorretos.")
