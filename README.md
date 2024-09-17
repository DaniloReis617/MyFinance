### Estrutura do Projeto `finance_app`
finance_app/
│
├── data/
│   └── users.parquet
│   └── goals.parquet
│   └── incomes.parquet
│   └── expenses.parquet
│
├── pages/
│   └── login.py
│   └── register.py
│   └── goals.py
│   └── incomes.py
│   └── expenses.py
│   └── dashboard.py
│   └── profile.py
│
│
├── assets/
│   └── profile_image.png
├── utils/
│   └── auth_utils.py
│   └── db_utils.py
│   └── file_utils.py
│
├── app.py
└── requirements.txt
#### Diretórios e Arquivos

- **data/**: Este diretório contém os arquivos de dados em formato Parquet. Estes arquivos armazenam informações essenciais para o funcionamento do aplicativo.
  - `users.parquet`: Armazena os dados dos usuários, incluindo `user_id`, `email` e `password`.
  - `goals.parquet`: Armazena as metas financeiras dos usuários, incluindo `goal_id`, `user_id`, `goal_name`, `goal_amount` e `date`.
  - `incomes.parquet`: Armazena as receitas dos usuários, incluindo `income_id`, `user_id`, `income_name`, `amount` e `date`.
  - `expenses.parquet`: Armazena as despesas dos usuários, incluindo `expense_id`, `user_id`, `expense_name`, `amount` e `date`.

- **pages/**: Este diretório contém os diferentes módulos de página do aplicativo, cada um representando uma funcionalidade específica.
  - `login.py`: Página de login onde os usuários podem entrar no sistema.
  - `register.py`: Página de registro para novos usuários.
  - `goals.py`: Página para cadastro e visualização de metas financeiras.
  - `incomes.py`: Página para cadastro e visualização de receitas.
  - `expenses.py`: Página para cadastro e visualização de despesas.
  - `dashboard.py`: Página principal do dashboard, onde os usuários podem visualizar um resumo das suas finanças.
  - `profile.py`: Página de perfil do usuário, onde ele pode mudar informações sobre o seu perfil e alterar a senha.

- **assets/**: Este diretório contém arquivos estáticos, como imagens.
  - `profile_image.png`: Imagem de perfil usada na página de perfil.

- **utils/**: Este diretório contém utilitários e funções auxiliares.
  - `auth_utils.py`: Funções de autenticação, como login de usuário.
  - `db_utils.py`: Funções de banco de dados, como verificação de existência de usuário e registro de novo usuário.
  - `file_utils.py`: este código garante que os arquivos Parquet necessários para armazenar dados de usuários, metas, rendas e despesas sejam criados se ainda não existirem.
- **app.py**: Arquivo principal do aplicativo que configura a navegação entre as páginas e inicializa os arquivos de dados.

- **requirements.txt**: Arquivo que lista todas as dependências necessárias para rodar o aplicativo, como `streamlit`, `pandas` e `pyarrow`.


### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
