import streamlit as st
import pandas as pd
from utils.auth_utils import hash_password, get_user_by_email, save_user_data

def app():
    st.title("Perfil")

    # Carregar dados do usuário atual
    user_email = st.session_state.get('user_email')
    user_data = get_user_by_email(user_email)
    
    with st.form(key='profile_form'):
        st.write(f"Bem-vindo, {user_email}! Aqui você pode alterar sua senha.")
        
        new_password = st.text_input("Nova senha", type="password")
        confirm_password = st.text_input("Confirme a nova senha", type="password")
        
        submit_button = st.form_submit_button("Alterar Senha")
    
    if submit_button:
        # Verificar se a nova senha e a confirmação coincidem
        if new_password != confirm_password:
            st.error("As senhas não coincidem.")
        elif len(new_password) < 6:
            st.error("A senha deve ter pelo menos 6 caracteres.")
        else:
            # Atualizar a senha no banco de dados
            user_data['password'] = hash_password(new_password)
            users = pd.read_parquet('data/users.parquet')
            users.loc[users['email'] == user_email, 'password'] = user_data['password']
            
            # Salvar as alterações no arquivo Parquet
            users.to_parquet('data/users.parquet', index=False)
            st.success("Senha alterada com sucesso!")
