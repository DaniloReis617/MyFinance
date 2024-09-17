import streamlit as st
from utils.auth_utils import register_user

def app():
    st.title("Cadastro")
    
    with st.form(key='register_form'):
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")
        password_confirm = st.text_input("Confirme a senha", type="password")
        submit_button = st.form_submit_button("Registrar")
    
    if submit_button:
        if password != password_confirm:
            st.error("As senhas não coincidem.")
        else:
            # Chama a função para registrar o usuário e captura o sucesso e a mensagem
            success, message = register_user(email, password)
            
            if success:
                st.success(message)
                st.session_state.logged_in = True
                st.rerun()  # Recarrega a página para redirecionar
            else:
                st.error(message)
