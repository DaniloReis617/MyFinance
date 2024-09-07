import streamlit as st
import re
from utils import db_utils

def app():
    reset_password()

def reset_password():
    st.subheader("Redefinir Senha")

    # Campo para inserir o email
    email = st.text_input("E-mail", placeholder="Digite seu E-mail")
    
    # Verifica se o email é válido
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.error("Por favor, insira um email válido.")
        return
    
    # Campo para nova senha
    new_password = st.text_input("Nova Senha", placeholder="Digite sua nova senha", type='password')
    
    # Campo para confirmar a nova senha
    confirm_password = st.text_input("Confirme a Nova Senha", placeholder="Digite sua senha novamente", type='password')
    
    # Verifica se a senha e a confirmação coincidem
    if new_password != confirm_password:
        st.error("As senhas digitadas não coincidem. Por favor, tente novamente.")
        return
    
    # Botão para submeter o formulário
    if st.button('Redefinir Senha'):
        # Verifica se o email está registrado
        if db_utils.check_existing_username(email):
            # Atualiza a senha do usuário
            result = db_utils.update_user_password(email, new_password)
            if result == "update_successful":
                st.success("Senha redefinida com sucesso! Você pode agora fazer login com a nova senha.")
            else:
                st.error("Ocorreu um erro ao redefinir a senha. Tente novamente mais tarde.")
        else:
            st.error("O e-mail fornecido não está registrado. Verifique e tente novamente.")
