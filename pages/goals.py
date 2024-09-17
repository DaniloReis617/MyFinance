import streamlit as st
import pandas as pd
import os

def app():
    st.title("Metas Financeiras")

    # Caminho para o arquivo de metas
    goals_file = 'data/goals.parquet'

    # Verificar se o arquivo de metas existe e carregar o DataFrame
    if os.path.exists(goals_file):
        goals = pd.read_parquet(goals_file)
    else:
        goals = pd.DataFrame(columns=['goal_id', 'user_id', 'goal_name', 'goal_amount', 'date'])

    # Pegar o ID do usuário logado
    user_id = st.session_state.get('user_id')

    # Exibir metas do usuário logado
    st.subheader("Minhas Metas")
    user_goals = goals[goals['user_id'] == user_id]
    
    if not user_goals.empty:
        st.dataframe(user_goals[['goal_name', 'goal_amount', 'date']])
    else:
        st.write("Nenhuma meta cadastrada.")

    # Formulário para adicionar nova meta
    with st.form(key='goal_form'):
        st.subheader("Adicionar Nova Meta")
        goal_name = st.text_input("Nome da Meta")
        goal_amount = st.number_input("Valor da Meta", min_value=0.0)
        date = st.date_input("Data")
        submit_button = st.form_submit_button("Salvar Meta")
    
    if submit_button:
        if goal_name and goal_amount > 0:
            # Gerar o próximo goal_id
            next_goal_id = goals['goal_id'].max() + 1 if not goals.empty else 1

            # Criar a nova meta
            new_goal = pd.DataFrame({
                'goal_id': [next_goal_id],
                'user_id': [user_id],
                'goal_name': [goal_name],
                'goal_amount': [goal_amount],
                'date': [date]
            })

            # Concatenar a nova meta ao DataFrame existente
            updated_goals = pd.concat([goals, new_goal], ignore_index=True)

            # Salvar as metas no arquivo Parquet
            updated_goals.to_parquet(goals_file, index=False)

            st.success("Meta adicionada com sucesso!")
            st.rerun()  # Recarregar a página para atualizar a lista
        else:
            st.error("Por favor, preencha todos os campos corretamente.")
