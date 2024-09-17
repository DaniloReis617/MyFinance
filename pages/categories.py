import streamlit as st
import pandas as pd
import os

def app():
    st.title("Cadastro de Categorias")

    # Caminho para o arquivo de categorias
    categories_file = 'data/categories.parquet'

    # Verificar se o diretório "data" existe, caso contrário, criá-lo
    if not os.path.exists('data'):
        os.makedirs('data')

    # Verificar se o arquivo existe e carregar as categorias
    if os.path.exists(categories_file):
        categories = pd.read_parquet(categories_file)
    else:
        categories = pd.DataFrame(columns=['category_id', 'user_id', 'category_name', 'type'])

    # Pegar o ID do usuário logado
    user_id = st.session_state.get('user_id', None)

    if user_id is None:
        st.error("Usuário não está logado.")
        return

    # Filtrar categorias do usuário logado
    user_categories = categories[categories['user_id'] == user_id]

    # Exibir categorias cadastradas
    st.subheader("Categorias Cadastradas")
    if not user_categories.empty:
        st.dataframe(user_categories[['category_name', 'type']])
    else:
        st.write("Nenhuma categoria cadastrada.")

    # Formulário para adicionar nova categoria
    st.subheader("Adicionar Nova Categoria")
    with st.form(key='category_form'):
        category_name = st.text_input("Nome da Categoria", placeholder="Ex: Alimentação, Transporte", label_visibility="collapsed")
        category_type = st.selectbox("Tipo de Categoria", ["Despesa", "Receita"], label_visibility="collapsed")
        submit_category = st.form_submit_button("Adicionar Categoria")
    
    if submit_category:
        if category_name:
            # Gerar o próximo category_id
            next_category_id = categories['category_id'].max() + 1 if not categories.empty else 1

            # Adicionar nova categoria
            new_category = pd.DataFrame({
                'category_id': [next_category_id],
                'user_id': [user_id],
                'category_name': [category_name],
                'type': [category_type]
            })

            # Concatenar a nova categoria ao DataFrame existente e salvar
            try:
                categories = pd.concat([categories, new_category], ignore_index=True)
                categories.to_parquet(categories_file, index=False)
                st.success(f"Categoria '{category_name}' adicionada com sucesso!")
                st.experimental_rerun()  # Recarregar a página para exibir a nova categoria
            except Exception as e:
                st.error(f"Erro ao salvar a categoria: {e}")
        else:
            st.error("Por favor, insira o nome da categoria.")

if __name__ == "__main__":
    app()
