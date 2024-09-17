import streamlit as st
import pandas as pd
import altair as alt
import os

def app():
    st.title("Gerenciamento de Despesas")

    # Caminho para os arquivos de despesas e categorias
    expenses_file = 'data/expenses.parquet'
    categories_file = 'data/categories.parquet'

    # Verificar se os arquivos existem e carregar as despesas e categorias
    if os.path.exists(expenses_file):
        expenses = pd.read_parquet(expenses_file)
    else:
        expenses = pd.DataFrame(columns=['expense_id', 'user_id', 'expense_name', 'amount', 'date', 'category', 'status'])

    if os.path.exists(categories_file):
        categories = pd.read_parquet(categories_file)
    else:
        categories = pd.DataFrame(columns=['category_id', 'user_id', 'category_name', 'type'])

    # Pegar o ID do usuário logado
    user_id = st.session_state.get('user_id')

    # Filtrar despesas e categorias do usuário logado
    user_expenses = expenses[expenses['user_id'] == user_id]
    user_categories = categories[categories['user_id'] == user_id]

    st.subheader("Minhas Despesas")

    # Verificar se o DataFrame de despesas está vazio
    if not user_expenses.empty:
        # Certifique-se de que as datas não sejam nulas antes de calcular min e max
        min_date = user_expenses['date'].min() if user_expenses['date'].notna().any() else pd.Timestamp.today()
        max_date = user_expenses['date'].max() if user_expenses['date'].notna().any() else pd.Timestamp.today()

        # Filtros avançados
        with st.expander("Filtrar Despesas"):
            category_filter = st.selectbox("Filtrar por Categoria", ["Todas"] + list(user_categories['category_name'].unique()))
            start_date = st.date_input("Data inicial", min_date)
            end_date = st.date_input("Data final", max_date)
            
            if category_filter != "Todas":
                user_expenses = user_expenses[user_expenses['category'] == category_filter]
            user_expenses = user_expenses[(user_expenses['date'] >= pd.to_datetime(start_date)) & 
                                          (user_expenses['date'] <= pd.to_datetime(end_date))]

        # Exibir as despesas com uma tabela mais organizada e opção de filtro
        st.dataframe(user_expenses[['expense_name', 'category', 'amount', 'date', 'status']])

        # Gráfico das despesas por categoria
        st.subheader("Resumo das Despesas por Categoria")
        chart = alt.Chart(user_expenses).mark_bar().encode(
            x='category:N',
            y='sum(amount):Q',
            color='category:N',
            tooltip=['category', 'sum(amount)', 'status']
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
    else:
        st.write("Nenhuma despesa registrada.")

    # Formulário para adicionar ou editar despesa
    st.subheader("Adicionar ou Editar Despesa")
    with st.form(key='expense_form'):
        expense_id = st.selectbox("Selecione uma despesa para editar", ["Nova Despesa"] + list(user_expenses['expense_id'].astype(str)))
        
        if expense_id != "Nova Despesa":
            # Preencher com os dados existentes para edição
            expense_data = user_expenses[user_expenses['expense_id'] == int(expense_id)].iloc[0]
            expense_name = st.text_input("Nome da Despesa", value=expense_data['expense_name'])
            category = st.selectbox("Categoria", user_categories['category_name'], index=user_categories[user_categories['category_name'] == expense_data['category']].index[0])
            amount = st.number_input("Valor (R$)", min_value=0.0, step=0.01, format="%.2f", value=expense_data['amount'])
            date = st.date_input("Data", value=pd.to_datetime(expense_data['date']))
            status = st.selectbox("Status", ["Pago", "Pendente"], index=["Pago", "Pendente"].index(expense_data['status']))
        else:
            # Novo registro
            expense_name = st.text_input("Nome da Despesa", placeholder="Ex: Aluguel, Supermercado, Transporte")
            category = st.selectbox("Categoria", user_categories['category_name'])
            amount = st.number_input("Valor (R$)", min_value=0.0, step=0.01, format="%.2f")
            date = st.date_input("Data")
            status = st.selectbox("Status", ["Pago", "Pendente"])
        
        submit_button = st.form_submit_button("Salvar Despesa")

    # Botão de exclusão separado do formulário de edição
    if expense_id != "Nova Despesa":
        delete_button = st.button("Excluir Despesa")

    # Validação e salvamento da nova ou editada despesa
    if submit_button:
        if not expense_name or amount <= 0:
            st.error("Por favor, preencha todos os campos corretamente.")
        else:
            if expense_id == "Nova Despesa":
                # Gerar o próximo ID único
                next_expense_id = expenses['expense_id'].max() + 1 if not expenses.empty else 1

                new_expense = pd.DataFrame({
                    'expense_id': [next_expense_id],
                    'user_id': [user_id],
                    'expense_name': [expense_name],
                    'category': [category],
                    'amount': [amount],
                    'date': [date],
                    'status': [status]
                })
                # Adiciona nova despesa
                updated_expenses = pd.concat([expenses, new_expense], ignore_index=True)
                st.success("Despesa adicionada com sucesso!")
            else:
                # Atualiza despesa existente
                expenses.loc[expenses['expense_id'] == int(expense_id), ['expense_name', 'category', 'amount', 'date', 'status']] = [expense_name, category, amount, date, status]
                updated_expenses = expenses
                st.success("Despesa atualizada com sucesso!")

            # Salvar as alterações no arquivo Parquet
            updated_expenses.to_parquet(expenses_file)
            st.rerun()  # Recarregar a página para atualizar os dados
    
    # Exclusão de despesa
    if delete_button:
        updated_expenses = expenses[expenses['expense_id'] != int(expense_id)]
        updated_expenses.to_parquet(expenses_file)
        st.success("Despesa excluída com sucesso!")
        st.rerun()  # Recarregar a página para atualizar os dados
