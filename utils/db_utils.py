import pandas as pd
from bcrypt import hashpw, gensalt, checkpw

def check_existing_username(username):
    # Carregar dados de usuários
    users = pd.read_parquet("data/users.parquet")
    
    # Verificar se o usuário já existe
    return not users[users['email'] == username].empty

def register_user(username, password):
    # Carregar dados de usuários
    users = pd.read_parquet("data/users.parquet")
    
    # Verificar se o usuário já existe
    if check_existing_username(username):
        return "user_exists"
    
    # Gerar hash da senha
    hashed_password = hashpw(password.encode('utf-8'), gensalt())
    
    # Adicionar novo usuário
    new_user = pd.DataFrame({
        "email": [username],
        "password": [hashed_password.decode('utf-8')],
        "user_id": [len(users) + 1]  # Implementar função para gerar ID único se necessário
    })
    users = pd.concat([users, new_user], ignore_index=True)
    
    # Salvar de volta no arquivo Parquet
    users.to_parquet("data/users.parquet", index=False)
    
    return "registration_successful"

def authenticate_user(username, password):
    # Carregar dados de usuários
    users = pd.read_parquet("data/users.parquet")
    
    # Verificar se o usuário existe
    user = users[users['email'] == username]
    if user.empty:
        return "user_not_found"
    
    # Verificar se a senha está correta
    hashed_password = user.iloc[0]['password'].encode('utf-8')
    if not checkpw(password.encode('utf-8'), hashed_password):
        return "incorrect_password"
    
    # Retornar o ID do usuário
    return user.iloc[0]['user_id']

def update_user_password(username, new_password):
    try:
        # Carregar dados de usuários
        users = pd.read_parquet("data/users.parquet")
        
        # Verificar se o usuário existe
        user_index = users.index[users['email'] == username].tolist()
        if not user_index:
            return "user_not_found"
        
        # Gerar hash da nova senha
        hashed_password = hashpw(new_password.encode('utf-8'), gensalt())
        
        # Atualizar a senha do usuário
        users.at[user_index[0], 'password'] = hashed_password.decode('utf-8')
        
        # Salvar de volta no arquivo Parquet
        users.to_parquet("data/users.parquet", index=False)
        
        return "update_successful"
    except Exception as e:
        print(f"Erro ao atualizar a senha: {e}")
        return "update_failed"
