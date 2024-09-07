import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

def app():
    st.title("Cadastro de Receitas")

    # Função para salvar ou atualizar a receita
    def save_income(name, amount, date, category, status, user_id, income_id=None):
        if income_id is None:
            # Gerar um ID único para a nova receita
            income_id = str(uuid.uuid4())
        
        income_data = {
            "income_id": income_id,
            "income_name": name,
            "amount": amount,
            "date": date,
            "category": category,
            "status": status,
            "user_id": user_id
        }
        
        try:
            incomes_df = pd.read_parquet("data/incomes.parquet")
        except FileNotFoundError:
            incomes_df = pd.DataFrame(columns=["income_id", "income_name", "amount", "date", "category", "status", "user_id"])

        if income_id in incomes_df["income_id"].values:
            # Atualizar receita existente
            incomes_df.update(pd.DataFrame([income_data]))
        else:
            # Adicionar nova receita
            incomes_df = pd.concat([incomes_df, pd.DataFrame([income_data])], ignore_index=True)

        incomes_df.to_parquet("data/incomes.parquet", index=False)
        return True

    # Função para excluir a receita
    def delete_income(income_id):
        try:
            incomes_df = pd.read_parquet("data/incomes.parquet")
        except FileNotFoundError:
            incomes_df = pd.DataFrame(columns=["income_id", "income_name", "amount", "date", "category", "status", "user_id"])
        
        incomes_df = incomes_df[incomes_df["income_id"] != income_id]
        incomes_df.to_parquet("data/incomes.parquet", index=False)

    # Sugestões de categorias
    categories = [
        "Salário", "Investimentos", "Freelance", "Vendas", "Rendimentos",
        "Aposentadoria", "Dividendos", "Comissões", "Presentes", "Outros"
    ]

    # Campo para adicionar nova categoria
    new_category = st.text_input("Adicionar Nova Categoria", placeholder="Digite uma nova categoria")

    # Identificador do usuário (exemplo)
    user_id = st.session_state.get("user_id", "unknown_user")

    if user_id == "unknown_user":
        st.error("Usuário não autenticado. Por favor, faça login para acessar esta página.")
        return  # Sai da função se o usuário não estiver autenticado

    # Campos do formulário
    with st.form(key='income_form'):
        income_name = st.text_input("Nome da Receita", placeholder="Digite o nome da receita")
        income_amount = st.number_input("Valor da Receita", min_value=0.0, format="%.2f")
        income_date = st.date_input("Data da Receita", min_value=datetime.today())

        # Atualiza a lista de categorias se houver uma nova categoria
        if new_category:
            if new_category not in categories:
                categories.append(new_category)

        income_category = st.selectbox(
            "Categoria",
            options=categories,
            index=0
        )
        income_status = st.selectbox(
            "Status",
            ["Recebido", "A Receber"]
        )

        # ID da receita sendo editada
        income_id = st.session_state.get("editing_income_id", None)

        submit_button = st.form_submit_button("Salvar Receita")

        if submit_button:
            if not income_name:
                st.error("O nome da receita é obrigatório.")
            elif income_amount <= 0:
                st.error("O valor da receita deve ser maior que zero.")
            elif not income_category:
                st.error("A categoria da receita é obrigatória.")
            else:
                success = save_income(income_name, income_amount, income_date, income_category, income_status, user_id, income_id)
                if success:
                    st.success("Receita cadastrada com sucesso!")
                    st.session_state.editing_income_id = None  # Limpar ID de edição
                    st.rerun()  # Atualiza a página para limpar o formulário
                else:
                    st.error("Erro ao cadastrar a receita. Tente novamente.")

    # Exibir a tabela de receitas
    st.write("### Lançamentos de Receitas")

    try:
        incomes_df = pd.read_parquet("data/incomes.parquet")
    except FileNotFoundError:
        incomes_df = pd.DataFrame(columns=["income_id", "income_name", "amount", "date", "category", "status", "user_id"])

    if not incomes_df.empty:
        for index, row in incomes_df.iterrows():
            st.write(f"#### Receita: {row['income_name']}")
            st.write(f"Valor: {row['amount']}")
            st.write(f"Data: {row['date']}")
            st.write(f"Categoria: {row['category']}")
            st.write(f"Status: {row['status']}")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"Editar {row['income_id']}", key=f"edit_{row['income_id']}"):
                    st.session_state.editing_income_id = row['income_id']
                    st.experimental_rerun()  # Atualiza a página para carregar o formulário com os dados da receita
            with col2:
                if st.button(f"Excluir {row['income_id']}", key=f"delete_{row['income_id']}"):
                    delete_income(row['income_id'])
                    st.success(f"Receita {row['income_id']} excluída com sucesso!")
                    st.experimental_rerun()  # Atualiza a página para refletir a exclusão
    else:
        st.write("Nenhuma receita cadastrada ainda.")
