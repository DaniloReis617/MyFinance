import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

def app():
    st.title("Cadastro de Despesas")

    # Função para salvar dados
    def save_expense(name, amount, category, status, date, user_id, expense_id=None):
        if expense_id is None:
            # Gerar um ID único para a nova despesa
            expense_id = str(uuid.uuid4())
        
        expense_data = {
            "expense_id": expense_id,
            "expense_name": name,
            "amount": amount,
            "category": category,
            "status": status,
            "date": date,
            "user_id": user_id
        }
        
        try:
            expenses_df = pd.read_parquet("data/expenses.parquet")
        except FileNotFoundError:
            expenses_df = pd.DataFrame(columns=["expense_id", "expense_name", "amount", "category", "status", "date", "user_id"])

        if expense_id in expenses_df["expense_id"].values:
            # Atualizar despesa existente
            expenses_df = expenses_df[expenses_df["expense_id"] != expense_id]
            expenses_df = pd.concat([expenses_df, pd.DataFrame([expense_data])], ignore_index=True)
        else:
            # Adicionar nova despesa
            expenses_df = pd.concat([expenses_df, pd.DataFrame([expense_data])], ignore_index=True)

        expenses_df.to_parquet("data/expenses.parquet", index=False)
        return True

    # Função para excluir dados
    def delete_expense(expense_id):
        try:
            expenses_df = pd.read_parquet("data/expenses.parquet")
        except FileNotFoundError:
            expenses_df = pd.DataFrame(columns=["expense_id", "expense_name", "amount", "category", "status", "date", "user_id"])
        
        expenses_df = expenses_df[expenses_df["expense_id"] != expense_id]
        expenses_df.to_parquet("data/expenses.parquet", index=False)

    # Sugestões de categorias
    categories = [
        "Alimentação", "Transporte", "Lazer", "Saúde", "Educação",
        "Habitação", "Serviços Públicos", "Vestuário", "Comunicação",
        "Impostos", "Outros"
    ]

    # Campo para adicionar nova categoria
    new_category = st.text_input("Adicionar Nova Categoria", placeholder="Digite uma nova categoria")

    # Identificador do usuário (exemplo)
    user_id = st.session_state.get("user_id", "unknown_user")

    if user_id == "unknown_user":
        st.error("Usuário não autenticado. Por favor, faça login para acessar esta página.")
        return

    # Campos do formulário
    with st.form(key='expense_form'):
        expense_name = st.text_input("Nome da Despesa", placeholder="Digite o nome da despesa")
        expense_amount = st.number_input("Valor da Despesa", min_value=0.0, format="%.2f")
        expense_date = st.date_input("Data da Despesa", min_value=datetime.today())
        
        if new_category:
            if new_category not in categories:
                categories.append(new_category)

        expense_category = st.selectbox(
            "Categoria da Despesa",
            options=categories,
            index=0
        )
        
        expense_status = st.selectbox(
            "Status da Despesa",
            ["Paga", "A Pagar"]
        )

        submit_button = st.form_submit_button("Salvar Despesa")
        expense_id = st.session_state.get("editing_expense_id", None)

        if submit_button:
            if not expense_name:
                st.error("O nome da despesa é obrigatório.")
            elif expense_amount <= 0:
                st.error("O valor da despesa deve ser maior que zero.")
            elif not expense_category:
                st.error("A categoria da despesa é obrigatória.")
            else:
                success = save_expense(expense_name, expense_amount, expense_category, expense_status, expense_date, user_id, expense_id)
                if success:
                    st.success("Despesa cadastrada com sucesso!")
                    st.session_state.editing_expense_id = None  # Limpar ID de edição
                    st.rerun()  # Atualiza a página para limpar o formulário
                else:
                    st.error("Erro ao cadastrar a despesa. Tente novamente.")

    # Exibir a tabela de despesas
    st.write("### Lançamentos de Despesas")

    try:
        expenses_df = pd.read_parquet("data/expenses.parquet")
    except FileNotFoundError:
        expenses_df = pd.DataFrame(columns=["expense_id", "expense_name", "amount", "category", "status", "date", "user_id"])

    if not expenses_df.empty:
        for index, row in expenses_df.iterrows():
            expense_id = row['expense_id']
            if pd.isna(expense_id):  # Verifica se o expense_id é NaN
                expense_id = str(uuid.uuid4())  # Gere um ID único se for NaN

            st.write(f"#### Despesa: {row['expense_name']}")
            st.write(f"Valor: {row['amount']}")
            st.write(f"Categoria: {row['category']}")
            st.write(f"Status: {row['status']}")
            st.write(f"Data: {row['date']}")
            
            # Botões de Editar e Excluir com chaves únicas
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"Editar {expense_id}", key=f"edit_{expense_id}"):
                    st.session_state.editing_expense_id = expense_id
                    st.rerun()
            with col2:
                if st.button(f"Excluir {expense_id}", key=f"delete_{expense_id}"):
                    delete_expense(expense_id)
                    st.success("Despesa excluída com sucesso!")
                    st.rerun()
    else:
        st.write("Nenhuma despesa cadastrada ainda.")
