# Missao Certificao 1 - Turma 2023.3 - Grupo 4

Desenvolvedores:
-
- LUCA MIGLIACCIO, 202307065765;
  
- RAFAEL SANTOS CARNEIRO, 202307152374;


# Objetivo:

Desenvolver uma aplicação para gerenciamento da Matriz SoD (“Segregation of Duties”), que tem como objetivo indicar os perfis de acesso conflitantes e que possam representar risco de fraude.

O Projeto deve conter o cadastro e consultar: 
-

1 - Os Sistemas;

2 - Os Perfis; 

3 - A Matriz SoD; 

4 - Os Usuários;


# Descrição :

O projeto consiste em uma aplicação GUI (Interface Gráfica do Usuário) desenvolvida em Python, utilizando o ambiente de desenvolvimento Visual Studio Code (VS Code). A interface foi construída com a biblioteca Tkinter. O código-fonte foi organizado em diferentes módulos para facilitar a manutenção e compreensão.

# Funcionalidades Principais:

Login e Autenticação:
-

Os usuários devem fornecer credenciais (usuário e senha) para acessar diferentes perfis da aplicação.
Credenciais de exemplo: "Admin" com senha "Admin123" e "Host" com senha "Host123".

Página Inicial:
-

Exibe uma mensagem de bem vindos.


Perfis e Abas Diferenciadas:
-


A aplicação oferece perfis distintos para "Admin" e "Host", cada um com acesso a abas específicas.
O perfil "Admin" possui acesso total, enquanto o perfil "Host" possui acesso limitado a algumas abas.


Abas e Funcionalidades:
-

Home: Página inicial com informações gerais.

Sistemas: Gerenciamento de sistemas.

Perfis: Gerenciamento de perfis associados a diferentes sistemas.

Matriz SoD: Gerenciamento dos conflitos.

Usuários: Gerenciamento de informações de usuários, incluindo CPF, sistema associado e perfil correspondente.

Desenvolvedores: Inclui um botão que, quando clicado, abre uma janela dedicada aos desenvolvedores envolvidos no projeto.


# Bibliotecas Necessárias:

pandas: Facilita a manipulação de dados e a interação com arquivos CSV.

tkinter: Uma biblioteca padrão do Python para construção de interfaces gráficas.

messagebox: Para visualizar as mensegns.

watchdog: Utilizado para monitorar alterações em arquivos, permitindo a atualização em tempo real da aplicação.

# Instruções para Execução:

Execute o Prompt de comando e baixe as bibliotecas digitando "pip install" + nome das bibliotecas, baixe o arquivo e inicie o arquivo "main.py". 
