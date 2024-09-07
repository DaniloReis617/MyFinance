import pandas as pd
from bcrypt import checkpw, hashpw, gensalt

def login_user(username, password):
    # Carregar dados de usuários (considere mover para uma função de inicialização)
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

# Função para registrar um novo usuário (exemplo de uso de bcrypt)
def register_user(username, password):
    # Carregar dados de usuários
    users = pd.read_parquet("data/users.parquet")
    
    # Verificar se o usuário já existe
    if not users[users['email'] == username].empty:
        return "user_exists"
    
    # Gerar hash da senha
    hashed_password = hashpw(password.encode('utf-8'), gensalt())
    
    # Adicionar novo usuário ao DataFrame
    new_user = pd.DataFrame({
        'email': [username],
        'password': [hashed_password.decode('utf-8')],
        'user_id': [generate_new_user_id()]  # Implementar função para gerar novo ID
    })
    users = pd.concat([users, new_user], ignore_index=True)
    
    # Salvar os dados de volta no arquivo Parquet
    users.to_parquet("data/users.parquet", index=False)
    
    return "registration_successful"
