# Sistema de Cadastro de Pacientes (Aplicações DS)

Este repositório contém um sistema de cadastro e gestão de pacientes desenvolvido em Python. O projeto implementa a mesma solução utilizando dois frameworks de criação de interfaces web (Gradio e Streamlit), permitindo a comparação e o uso de diferentes abordagens para aplicações de Data Science.

## Funcionalidades

O sistema foi desenhado para facilitar a entrada, controle e gestão de pacientes, oferecendo as seguintes capacidades:
*   **Cadastro Completo**: Formulário para inserção de dados do paciente (nome, idade, sexo), endereço completo com CEP, e informações do atendimento (convênio, prioridade de 1 a 5, motivo).
*   **Validação e Normalização**: Tratamento automático de entradas, como a formatação correta de CEP (ex: 00000-000), capitalização de nomes e validação de campos obrigatórios.
*   **Gestão de Registros**: Exibição em tabela dos últimos cinco pacientes cadastrados no sistema.
*   **Exclusão de Pacientes**: Interface para selecionar e remover registros específicos baseados no momento do cadastro (timestamp).
*   **Exportação de Dados**: Botão para download de toda a base de pacientes em um arquivo CSV.
*   **Busca por Nome**: Ferramenta de pesquisa para encontrar pacientes específicos utilizando seu nome ou parte dele (recurso exclusivo da interface Gradio).

## Estrutura de Arquivos

*   **`gradio_app/app_gradio.py`**: Aplicação construída com o framework Gradio. Apresenta os recursos divididos por blocos e inclui uma aba dedicada para a busca textual de pacientes cadastrados.
*   **`streamlit_app/app_streamlit.py`**: Aplicação construída com o framework Streamlit. Utiliza o recurso de gerenciamento de estado da sessão (`session_state`) para limpar o formulário e apresenta as funções de exportação e exclusão organizadas na parte inferior da tela em colunas.

## Armazenamento de Dados

Ambos os scripts operam de forma local e armazenam os registros de atendimento em um arquivo chamado `pacientes.csv`. Se o arquivo não existir no momento da execução, ele será inicializado automaticamente com as colunas corretas.
