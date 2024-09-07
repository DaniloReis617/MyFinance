import streamlit as st
import pandas as pd
from utils.file_utils import initialize_data_files

def app():
    # CONFIGS
    YEAR = pd.Timestamp.now().year
    PREVIOUS_YEAR = YEAR - 1

    st.title("Dashboard de Controle Financeiro")

    # Inicializar arquivos de dados
    initialize_data_files()

    # Função para carregar e preparar dados
    @st.cache_data
    def get_and_prepare_data(file_path):
        df = pd.read_parquet(file_path).assign(
            date=lambda df: pd.to_datetime(df["date"]),
            month=lambda df: df["date"].dt.month,
            year=lambda df: df["date"].dt.year,
        )
        return df

    # Botão para atualizar os dados
    if st.button("Atualizar Dados"):
        st.rerun()

    # Carregar dados
    goals = get_and_prepare_data("data/goals.parquet")
    incomes = get_and_prepare_data("data/incomes.parquet")
    expenses = get_and_prepare_data("data/expenses.parquet")

    # Calcular receitas e despesas totais por ano
    total_incomes = incomes.groupby("year")["amount"].sum().fillna(0)
    total_expenses = expenses.groupby("year")["amount"].sum().fillna(0)

    # Calcular mudança percentual
    def calculate_change(current, previous):
        if previous == 0:
            return 0
        return ((current - previous) / previous) * 100

    income_change = calculate_change(
        total_incomes.get(YEAR, 0),
        total_incomes.get(PREVIOUS_YEAR, 0)
    )

    expense_change = calculate_change(
        total_expenses.get(YEAR, 0),
        total_expenses.get(PREVIOUS_YEAR, 0)
    )

    # Exibir métricas em cartões modernos
    st.write("### Visão Geral")
    col1, col2 = st.columns(2)

    with col1:
        st.write("#### Receitas Totais")
        st.metric(
            label="Receitas Totais",
            value=f"R$ {total_incomes.get(YEAR, 0):,.2f}",
            delta=f"{income_change:.2f}% vs. {PREVIOUS_YEAR}",
            delta_color="inverse"
        )

    with col2:
        st.write("#### Despesas Totais")
        st.metric(
            label="Despesas Totais",
            value=f"R$ {total_expenses.get(YEAR, 0):,.2f}",
            delta=f"{expense_change:.2f}% vs. {PREVIOUS_YEAR}",
            delta_color="inverse"
        )

    # Seleção de campos
    left_col, right_col = st.columns(2)
    analysis_type = left_col.selectbox(
        label="Análise por:",
        options=["Mês", "Categoria"],
        key="analysis_type",
    )
    selected_year = right_col.selectbox("Selecione o ano:", [YEAR, PREVIOUS_YEAR])

    # Exibir o ano acima do gráfico com base na seleção
    st.write(f"**Dados para {selected_year}**")

    # Filtrar dados com base na seleção para visualização
    if analysis_type == "Categoria":
        filtered_incomes = incomes.query("year == @selected_year").groupby("category")["amount"].sum().reset_index()
        filtered_expenses = expenses.query("year == @selected_year").groupby("category")["amount"].sum().reset_index()
    else:
        filtered_incomes = incomes.query("year == @selected_year").groupby("month")["amount"].sum().reset_index()
        filtered_expenses = expenses.query("year == @selected_year").groupby("month")["amount"].sum().reset_index()
        filtered_incomes["month"] = filtered_incomes["month"].apply(lambda x: f"{x:02d}")
        filtered_expenses["month"] = filtered_expenses["month"].apply(lambda x: f"{x:02d}")

    # Exibir os dados
    st.write("### Receitas")
    st.bar_chart(filtered_incomes.set_index(filtered_incomes.columns[0])["amount"])

    st.write("### Despesas")
    st.bar_chart(filtered_expenses.set_index(filtered_expenses.columns[0])["amount"])
