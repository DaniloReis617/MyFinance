import pandas as pd
import os

def create_parquet_if_not_exists(file_path, columns):
    if not os.path.exists(file_path):
        # Criação do DataFrame com tipos de dados definidos, se necessário
        df = pd.DataFrame(columns=columns)
        # Definindo tipos de dados para as colunas, se apropriado
        # Exemplo: df = pd.DataFrame(columns=columns).astype({"user_id": "int64", "email": "str"})
        df.to_parquet(file_path, index=False)
        print(f"Arquivo criado: {file_path}")

def initialize_data_files():
    # Criação do diretório se não existir
    os.makedirs("data", exist_ok=True)
    
    # Criação dos arquivos Parquet, com as novas colunas
    create_parquet_if_not_exists("data/users.parquet", ["user_id", "email", "password"])
    create_parquet_if_not_exists("data/goals.parquet", ["goal_id", "user_id", "goal_name", "goal_amount", "date"])
    create_parquet_if_not_exists("data/incomes.parquet", ["income_id", "user_id", "income_name", "amount", "date", "category", "status"])
    create_parquet_if_not_exists("data/expenses.parquet", ["expense_id", "user_id", "expense_name", "amount", "date", "category", "status"])

# Chamar a função de inicialização apenas se necessário
if __name__ == "__main__":
    initialize_data_files()
