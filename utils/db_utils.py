# utils/db_utils.py
import pandas as pd
import os

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

# Funções para salvar dados
def save_user_data(users_df):
    """Salva os dados dos usuários."""
    save_parquet_file(users_df, 'data/users.parquet')

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
