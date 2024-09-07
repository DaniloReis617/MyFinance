import streamlit as st
from utils.file_utils import initialize_data_files

# Inicializar arquivos de dados
initialize_data_files()

# Configuração da página deve ser feita apenas uma vez
st.set_page_config(page_title="Finance App", page_icon="📊", layout="wide")

# Verificar se o usuário está logado
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Função para carregar a página dinamicamente
def load_page(page_name):
    module = __import__(f'pages.{page_name}', fromlist=['app'])
    return module.app

# Navegação entre páginas
if st.session_state.logged_in:
    pages = {
        "Dashboard": "dashboard",
        "Metas": "goals",
        "Receitas": "incomes",
        "Despesas": "expenses",
        "Perfil": "profile",
        "Chatbot": "chatbot",
        "Redefinir Senha": "reset_password",
    }
else:
    pages = {
        "Login": "login",
        "Cadastro": "register",
    }

st.sidebar.title("Menu")
selection = st.sidebar.radio("Ir para", list(pages.keys()))

# Carregar e exibir a página selecionada
page_app = load_page(pages[selection])
page_app()
