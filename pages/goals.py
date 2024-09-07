import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

def app():
    st.title("Cadastro de Metas")

    # Função para salvar a meta
    def save_goal(name, amount, date, user_id, goal_id=None):
        if goal_id is None:
            # Gerar um ID único para a nova meta
            goal_id = str(uuid.uuid4())
        
        goal_data = {
            "goal_id": goal_id,
            "goal_name": name,
            "goal_amount": amount,
            "date": date,
            "user_id": user_id
        }
        
        try:
            goals_df = pd.read_parquet("data/goals.parquet")
        except FileNotFoundError:
            goals_df = pd.DataFrame(columns=["goal_id", "goal_name", "goal_amount", "date", "user_id"])

        if goal_id in goals_df["goal_id"].values:
            # Atualizar meta existente
            goals_df.update(pd.DataFrame([goal_data]))
        else:
            # Adicionar nova meta
            goals_df = pd.concat([goals_df, pd.DataFrame([goal_data])], ignore_index=True)

        goals_df.to_parquet("data/goals.parquet", index=False)
        return True

    # Função para excluir a meta
    def delete_goal(goal_id):
        try:
            goals_df = pd.read_parquet("data/goals.parquet")
        except FileNotFoundError:
            goals_df = pd.DataFrame(columns=["goal_id", "goal_name", "goal_amount", "date", "user_id"])
        
        goals_df = goals_df[goals_df["goal_id"] != goal_id]
        goals_df.to_parquet("data/goals.parquet", index=False)

    # Obtém o ID do usuário logado
    user_id = st.session_state.get("user_id")

    if not user_id:
        st.error("Usuário não autenticado. Por favor, faça login para acessar esta página.")
        return  # Sai da função se o usuário não estiver autenticado

    # Campos do formulário
    with st.form(key='goal_form'):
        goal_name = st.text_input("Nome da Meta", placeholder="Digite o nome da meta")
        goal_amount = st.number_input("Valor da Meta", min_value=0.0, format="%.2f")
        goal_date = st.date_input("Data da Meta", min_value=datetime.today())
        
        # ID da meta sendo editada
        goal_id = st.session_state.get("editing_goal_id", None)

        submit_button = st.form_submit_button("Salvar Meta")

        if submit_button:
            if not goal_name:
                st.error("O nome da meta é obrigatório.")
            elif goal_amount <= 0:
                st.error("O valor da meta deve ser maior que zero.")
            else:
                success = save_goal(goal_name, goal_amount, goal_date, user_id, goal_id)
                if success:
                    st.success("Meta cadastrada com sucesso!")
                    st.session_state.editing_goal_id = None  # Limpar ID de edição
                    st.rerun()  # Atualiza a página para limpar o formulário
                else:
                    st.error("Erro ao cadastrar a meta. Tente novamente.")

    # Exibir a tabela de metas
    st.write("### Lançamentos de Metas")

    try:
        goals_df = pd.read_parquet("data/goals.parquet")
    except FileNotFoundError:
        goals_df = pd.DataFrame(columns=["goal_id", "goal_name", "goal_amount", "date", "user_id"])

    if not goals_df.empty:
        # Adiciona botões de editar e excluir
        def edit_goal(goal_id):
            st.session_state.editing_goal_id = goal_id
            st.experimental_rerun()

        def remove_goal(goal_id):
            delete_goal(goal_id)
            st.experimental_rerun()

        # Exibe a tabela com ações
        for index, row in goals_df.iterrows():
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"{row['goal_name']} - {row['goal_amount']} - {row['date']}")
            with col2:
                if st.button("Editar", key=f"edit_{row['goal_id']}"):
                    edit_goal(row['goal_id'])
            with col3:
                if st.button("Excluir", key=f"delete_{row['goal_id']}"):
                    remove_goal(row['goal_id'])
    else:
        st.write("Nenhuma meta cadastrada ainda.")
