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

def save_user_data(users_df):
    """Salva os dados de todos os usuários no arquivo Parquet."""
    users_df.to_parquet('data/users.parquet', index=False)

# Verifica se o arquivo Parquet existe e retorna um DataFrame vazio se não existir
def load_parquet_file(filepath, columns):
    if not os.path.exists(filepath):
        return pd.DataFrame(columns=columns)
    return pd.read_parquet(filepath)

def save_parquet_file(df, filepath):
    df.to_parquet(filepath)

# Funções para carregar dados
def get_user_data():
    """Retorna os dados dos usuários."""
    return load_parquet_file('data/users.parquet', ['user_id', 'email', 'password'])

def get_goals_data():
    """Retorna os dados das metas."""
    return load_parquet_file('data/goals.parquet', ['goal_id', 'user_id', 'goal_name', 'goal_amount', 'date'])

def get_incomes_data():
    """Retorna os dados das receitas."""
    return load_parquet_file('data/incomes.parquet', ['income_id', 'user_id', 'income_name', 'amount', 'date'])

def get_expenses_data():
    """Retorna os dados das despesas."""
    return load_parquet_file('data/expenses.parquet', ['expense_id', 'user_id', 'expense_name', 'amount', 'date'])

def save_goals_data(goals_df):
    """Salva os dados das metas."""
    save_parquet_file(goals_df, 'data/goals.parquet')

def save_incomes_data(incomes_df):
    """Salva os dados das receitas."""
    save_parquet_file(incomes_df, 'data/incomes.parquet')

def save_expenses_data(expenses_df):
    """Salva os dados das despesas."""
    save_parquet_file(expenses_df, 'data/expenses.parquet')

# Função para gerar ID único com base no último ID registrado
def get_next_id(df, id_column):
    if df.empty:
        return 1
    return df[id_column].max() + 1

# Funções para adicionar novos registros
def add_new_goal(user_id, goal_name, goal_amount, date):
    """Adiciona uma nova meta ao arquivo Parquet."""
    goals = get_goals_data()
    new_goal = pd.DataFrame({
        'goal_id': [get_next_id(goals, 'goal_id')],
        'user_id': [user_id],
        'goal_name': [goal_name],
        'goal_amount': [goal_amount],
        'date': [date]
    })
    updated_goals = pd.concat([goals, new_goal], ignore_index=True)
    save_goals_data(updated_goals)

def add_new_income(user_id, income_name, amount, date):
    """Adiciona uma nova receita ao arquivo Parquet."""
    incomes = get_incomes_data()
    new_income = pd.DataFrame({
        'income_id': [get_next_id(incomes, 'income_id')],
        'user_id': [user_id],
        'income_name': [income_name],
        'amount': [amount],
        'date': [date]
    })
    updated_incomes = pd.concat([incomes, new_income], ignore_index=True)
    save_incomes_data(updated_incomes)

def add_new_expense(user_id, expense_name, amount, date):
    """Adiciona uma nova despesa ao arquivo Parquet."""
    expenses = get_expenses_data()
    new_expense = pd.DataFrame({
        'expense_id': [get_next_id(expenses, 'expense_id')],
        'user_id': [user_id],
        'expense_name': [expense_name],
        'amount': [amount],
        'date': [date]
    })
    updated_expenses = pd.concat([expenses, new_expense], ignore_index=True)
    save_expenses_data(updated_expenses)
