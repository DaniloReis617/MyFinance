import pandas as pd
import streamlit as st

# Funções auxiliares para buscar dados nos arquivos Parquet
def load_data(file_name):
    try:
        return pd.read_parquet(f"data/{file_name}")
    except FileNotFoundError:
        st.error(f"Arquivo {file_name} não encontrado.")
        return pd.DataFrame()

def get_user_data(email):
    users = load_data("users.parquet")
    user = users[users['email'] == email]
    if user.empty:
        return None
    return user.iloc[0]

def get_goals(user_id):
    goals = load_data("goals.parquet")
    return goals[goals['user_id'] == user_id]

def get_incomes(user_id):
    incomes = load_data("incomes.parquet")
    return incomes[incomes['user_id'] == user_id]

def get_expenses(user_id):
    expenses = load_data("expenses.parquet")
    return expenses[expenses['user_id'] == user_id]

# Função para gerar respostas baseadas nas perguntas
def generate_response(prompt, email):
    user_data = get_user_data(email)
    if user_data is None:
        return "Usuário não encontrado. Verifique o e-mail fornecido."
    
    user_id = user_data['user_id']
    
    if "metas" in prompt.lower():
        goals = get_goals(user_id)
        if goals.empty:
            return "Você não tem metas registradas."
        return f"Sua(s) meta(s) registrada(s): {goals[['goal_name', 'goal_amount']].to_dict(orient='records')}"
    
    if "receitas" in prompt.lower():
        incomes = get_incomes(user_id)
        if incomes.empty:
            return "Você não tem receitas registradas."
        return f"Sua(s) receita(s) registrada(s): {incomes[['income_name', 'amount']].to_dict(orient='records')}"
    
    if "despesas" in prompt.lower():
        expenses = get_expenses(user_id)
        if expenses.empty:
            return "Você não tem despesas registradas."
        return f"Sua(s) despesa(s) registrada(s): {expenses[['expense_name', 'amount']].to_dict(orient='records')}"
    
    return "Desculpe, não entendi a sua pergunta. Pergunte sobre metas, receitas ou despesas."

def app():
    st.title("Chatbot")

    # Inicializar o histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibir mensagens do histórico
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Aceitar entrada do usuário
    email = st.text_input("Digite seu e-mail para autenticação", placeholder="Seu e-mail", key="email")
    if email:
        if prompt := st.chat_input("O que você deseja saber?"):
            # Adicionar mensagem do usuário ao histórico
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Exibir mensagem do usuário no container de mensagens
            with st.chat_message("user"):
                st.markdown(prompt)

            # Gerar e exibir resposta do assistente
            response = generate_response(prompt, email)
            with st.chat_message("assistant"):
                st.markdown(response)
            
            # Adicionar resposta do assistente ao histórico
            st.session_state.messages.append({"role": "assistant", "content": response})
