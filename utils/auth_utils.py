import pandas as pd
import hashlib
import os
import re

USERS_FILE = 'data/users.parquet'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email)

def authenticate_user(email, password):
    """Autentica um usuário com base no email e senha."""
    if not os.path.exists(USERS_FILE):
        return False  # Não há usuários registrados
    
    users = pd.read_parquet(USERS_FILE)
    hashed_password = hash_password(password)
    
    user = users[(users['email'] == email) & (users['password'] == hashed_password)]
    return not user.empty

def get_user_by_email(email):
    """Retorna as informações do usuário pelo email."""
    if not os.path.exists(USERS_FILE):
        return None

    users = pd.read_parquet(USERS_FILE)
    user = users[users['email'] == email]

    if user.empty:
        return None

    return user.iloc[0]  # Retorna o primeiro usuário encontrado como um dicionário

def register_user(email, password):
    """Registra um novo usuário."""
    # Verificar formato do email
    if not is_valid_email(email):
        return False, "Email inválido."

    if not os.path.exists(USERS_FILE):
        users = pd.DataFrame(columns=['user_id', 'email', 'password'])
    else:
        users = pd.read_parquet(USERS_FILE)

    if email in users['email'].values:
        return False, "O email já está em uso."

    hashed_password = hash_password(password)
    
    new_user = pd.DataFrame({
        'user_id': [len(users) + 1],
        'email': [email],
        'password': [hashed_password]
    })
    
    updated_users = pd.concat([users, new_user], ignore_index=True)
    updated_users.to_parquet(USERS_FILE)

    return True, "Usuário registrado com sucesso."
