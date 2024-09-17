import streamlit as st
import pandas as pd
import os

def set_user_info(user_id, user_email):
    st.session_state['current_user_id'] = user_id
    st.session_state['current_user_email'] = user_email

def app():
    st.title("Dashboard")
    
    # Exibir as informações do usuário na página
    st.write(f"Bem-vindo, {st.session_state.get('current_user_email', 'Usuário')}")

    # Função para carregar dados com verificação de existência de arquivos
    def load_parquet_file(filepath, default_columns):
        if os.path.exists(filepath):
            return pd.read_parquet(filepath)
        return pd.DataFrame(columns=default_columns)

    # Carregar dados de metas, receitas e despesas com verificação de existência
    goals = load_parquet_file('data/goals.parquet', ['goal_id', 'user_id', 'goal_name', 'goal_amount', 'date'])
    incomes = load_parquet_file('data/incomes.parquet', ['income_id', 'user_id', 'income_name', 'amount', 'date'])
    expenses = load_parquet_file('data/expenses.parquet', ['expense_id', 'user_id', 'expense_name', 'amount', 'date'])

    # Filtrar dados do usuário logado
    user_goals = goals[goals['user_id'] == st.session_state.get('current_user_id')]
    user_incomes = incomes[incomes['user_id'] == st.session_state.get('current_user_id')]
    user_expenses = expenses[expenses['user_id'] == st.session_state.get('current_user_id')]

    # Exibir resumo
    st.subheader("Resumo")
    st.write(f"Metas: {len(user_goals)}")
    st.write(f"Receitas: {len(user_incomes)}")
    st.write(f"Despesas: {len(user_expenses)}")
    
    # Exibir detalhes em tabelas
    st.subheader("Detalhes")
    
    st.write("### Metas Financeiras")
    if not user_goals.empty:
        st.dataframe(user_goals[['goal_name', 'goal_amount', 'date']])
    else:
        st.write("Nenhuma meta cadastrada.")
    
    st.write("### Receitas")
    if not user_incomes.empty:
        st.dataframe(user_incomes[['income_name', 'amount', 'date']])
    else:
        st.write("Nenhuma receita cadastrada.")
    
    st.write("### Despesas")
    if not user_expenses.empty:
        st.dataframe(user_expenses[['expense_name', 'amount', 'date']])
    else:
        st.write("Nenhuma despesa cadastrada.")
