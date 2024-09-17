import os
import pandas as pd

def initialize_data_files():
    """Verifica se os arquivos Parquet existem, caso contrário, os cria."""
    # Definindo os arquivos e seus DataFrames correspondentes
    files = {
        'data/users.parquet': pd.DataFrame(columns=['user_id', 'email', 'password', 'name', 'created_at']),
        'data/goals.parquet': pd.DataFrame(columns=['goal_id', 'user_id', 'goal_name', 'goal_amount', 'current_amount', 'target_date', 'created_at']),
        'data/incomes.parquet': pd.DataFrame(columns=['income_id', 'user_id', 'income_name', 'amount', 'date', 'category', 'status']),
        'data/expenses.parquet': pd.DataFrame(columns=['expense_id', 'user_id', 'expense_name', 'amount', 'date', 'category', 'status']),
        'data/categories.parquet': pd.DataFrame(columns=['category_id', 'user_id', 'category_name', 'type']),
        'data/transactions.parquet': pd.DataFrame(columns=['transaction_id', 'user_id', 'amount', 'date', 'type', 'category_id', 'description'])
    }

    # Verificar se os arquivos existem, se não, criar e salvar os DataFrames
    for file_path, df in files.items():
        if not os.path.exists(file_path):
            df.to_parquet(file_path)

if __name__ == "__main__":
    initialize_data_files()
