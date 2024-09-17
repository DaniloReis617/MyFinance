import streamlit as st
import pandas as pd
import os

def app():
    st.title("Receitas")

    # Caminho para o arquivo de receitas
    incomes_file = 'data/incomes.parquet'

    # Verificar se o arquivo de receitas existe e carregar o DataFrame
    if os.path.exists(incomes_file):
        incomes = pd.read_parquet(incomes_file)
    else:
        incomes = pd.DataFrame(columns=['income_id', 'user_id', 'income_name', 'amount', 'date'])

    # Pegar o ID do usuário logado
    user_id = st.session_state.get('user_id')

    # Exibir receitas do usuário logado
    st.subheader("Minhas Receitas")
    user_incomes = incomes[incomes['user_id'] == user_id]

    if not user_incomes.empty:
        st.dataframe(user_incomes[['income_name', 'amount', 'date']])
    else:
        st.write("Nenhuma receita cadastrada.")

    # Formulário para adicionar nova receita
    with st.form(key='income_form'):
        st.subheader("Adicionar Nova Receita")
        income_name = st.text_input("Nome da Receita")
        amount = st.number_input("Valor", min_value=0.0)
        date = st.date_input("Data")
        submit_button = st.form_submit_button("Salvar Receita")
    
    if submit_button:
        if income_name and amount > 0:
            # Gerar o próximo income_id
            next_income_id = incomes['income_id'].max() + 1 if not incomes.empty else 1

            # Criar a nova receita
            new_income = pd.DataFrame({
                'income_id': [next_income_id],
                'user_id': [user_id],
                'income_name': [income_name],
                'amount': [amount],
                'date': [date]
            })

            # Concatenar a nova receita ao DataFrame existente
            updated_incomes = pd.concat([incomes, new_income], ignore_index=True)

            # Salvar as receitas no arquivo Parquet
            updated_incomes.to_parquet(incomes_file, index=False)

            st.success("Receita adicionada com sucesso!")
            st.rerun()  # Recarregar a página para atualizar a lista
        else:
            st.error("Por favor, preencha todos os campos corretamente.")
