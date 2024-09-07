import streamlit as st
import re
from utils import db_utils

def app():
    registro()

# Função para realizar registro de novo usuário
def registro():
    with st.container():
        col1, col2, col3 = st.columns([0.5, 8, 0.5])
        with col2:
            st.subheader("Registro")
            with st.form(key='register_form'):
                # Campo para inserir novo email
                new_username = st.text_input("E-mail", placeholder="Digite seu Email")
                # Verifica se o email é válido
                if not re.match(r"[^@]+@[^@]+\.[^@]+", new_username):
                    st.error("Por favor, insira um email válido.")
                # Campo para inserir nova senha
                new_password = st.text_input("Nova Senha", placeholder="Digite sua senha", type='password')
                # Campo para confirmar a nova senha
                confirm_password = st.text_input("Confirme a Nova Senha", placeholder="Digite sua senha novamente", type='password')
                # Verifica se a senha atende aos critérios de segurança
                if not is_password_secure(new_password):
                    st.error("A senha deve ter pelo menos 8 caracteres e incluir letras maiúsculas e números.")
                # Verifica se a senha e a confirmação coincidem
                if new_password != confirm_password:
                    st.error("As senhas digitadas não coincidem. Por favor, tente novamente.")
                # Botão para submeter o formulário de registro
                if st.form_submit_button('Criar Conta'):
                    # Verifica se o email já está em uso
                    if db_utils.check_existing_username(new_username):
                        st.error(f'O email "{new_username}" já está em uso. Por favor, escolha outro.')
                    else:
                        # Registra o usuário se o email não estiver em uso
                        db_utils.register_user(new_username, new_password)
                        st.success(f'Conta registrada com sucesso para {new_username}!')
                        st.session_state.page = "Login"
                        st.rerun()

def is_password_secure(password):
    return len(password) >= 8 and re.search(r'[A-Z]', password) and re.search(r'[0-9]', password)
