import gradio as gr
import pandas as pd
import os
from datetime import datetime


# ============================================================
# CONFIGURAÇÕES
# ============================================================

ARQUIVO_CSV = "pacientes.csv"

COLUNAS = ["timestamp", "nome", "idade", "sexo", "cep", "endereco", "numero", "complemento", "bairro", "cidade", "estado", "convenio", "prioridade", "motivo"]

# ============================================================
# INICIALIZAÇÃO DO ARQUIVO
# ============================================================

def inicializar_arquivo():
    #Cria o arquivo CSV caso ele ainda não exista.
    if not os.path.exists(ARQUIVO_CSV):
        pd.DataFrame(columns=COLUNAS).to_csv(
            ARQUIVO_CSV,
            index=False
        )

# ============================================================
# NORMALIZAÇÃO DOS DADOS
# ============================================================

def normalizar_dados(nome, cep, endereco, numero, complemento, bairro, cidade, estado, motivo):
    #Padroniza os campos de texto antes de salvar.


    nome = nome.strip().title()

    cep = cep.strip().replace("-", "")

    if len(cep) == 8 and cep.isdigit():
        cep = f"{cep[:5]}-{cep[5:]}"

    endereco = endereco.strip().title()
    numero = numero.strip()
    complemento = complemento.strip()
    bairro = bairro.strip().title()
    cidade = cidade.strip().title()
    estado = estado.strip().upper()
    motivo = motivo.strip()

    return (nome, cep, endereco, numero, complemento, bairro, cidade, estado, motivo)


# ============================================================
# VALIDAÇÃO
# ============================================================

def validar_paciente(nome, idade, sexo, cep, endereco, numero, bairro, cidade, estado, convenio, prioridade):
    #Valida os campos obrigatórios do cadastro.

    # Nome
    if not nome or not nome.strip():
        raise gr.Error("Digite o nome do paciente.")

    if len(nome.strip()) < 3:
        raise gr.Error("O nome deve possuir pelo menos 3 caracteres.")

    # Idade
    if idade is None:
        raise gr.Error("Digite a idade do paciente.")

    if idade < 0 or idade > 120:
        raise gr.Error("Digite uma idade entre 0 e 120 anos.")

    # Sexo
    if not sexo:
        raise gr.Error("Selecione o sexo do paciente.")

    # CEP
    if not cep or not cep.strip():
        raise gr.Error("Digite o CEP.")

    cep_limpo = cep.strip().replace("-", "")

    if len(cep_limpo) != 8 or not cep_limpo.isdigit():
        raise gr.Error("Digite um CEP válido. Exemplo: 00000-000.")

    # Endereço
    if not endereco or not endereco.strip():
        raise gr.Error("Digite o endereço.")

    # Número
    if not numero or not numero.strip():
        raise gr.Error("Digite o número do endereço.")

    # Bairro
    if not bairro or not bairro.strip():
        raise gr.Error("Digite o bairro.")

    # Cidade
    if not cidade or not cidade.strip():
        raise gr.Error("Digite a cidade.")

    # Estado
    if not estado:
        raise gr.Error("Selecione o estado.")

    # Convênio
    if not convenio:
        raise gr.Error("Selecione o convênio.")

    # Prioridade
    if prioridade is None or prioridade < 1 or prioridade > 5:
        raise gr.Error("Selecione uma prioridade entre 1 e 5.")


# ============================================================
# SALVAR PACIENTE
# ============================================================

def salvar_paciente(linha):
    #Salva um novo paciente no arquivo CSV.
    novo = pd.DataFrame([linha])

    novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)


# ============================================================
# Consulta os últimos pacientes cadastrados
# ============================================================

def buscar_ultimos_pacientes():
    #Retorna os últimos 5 pacientes cadastrados.
    if not os.path.exists(ARQUIVO_CSV):
        return pd.DataFrame(columns=COLUNAS)

    df = pd.read_csv(ARQUIVO_CSV)

    return df.tail(5)


# ============================================================
# CADASTRAR PACIENTE
# ============================================================
def cadastrar_paciente(nome, idade, sexo, cep, endereco, numero, bairro, cidade, estado, convenio, prioridade):
    #Valida, normaliza e salva os dados do paciente.

    # --------------------------------------------------------
    # Validação
    # --------------------------------------------------------

    validar_paciente(nome, idade, sexo, cep, endereco, numero, bairro, cidade, estado, convenio, prioridade)

    # --------------------------------------------------------
    # Normalização
    # --------------------------------------------------------

    (
        nome,
        cep,
        endereco,
        numero,
        complemento,
        bairro,
        cidade,
        estado,
        motivo
    ) = normalizar_dados(
        nome,
        cep,
        endereco,
        numero,
        complemento,
        bairro,
        cidade,
        estado,
        motivo
    )

    # --------------------------------------------------------
    # Criação do registro
    # --------------------------------------------------------

    linha = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "nome": nome,
        "idade": int(idade),
        "sexo": sexo,
        "cep": cep,
        "endereco": endereco,
        "numero": numero,
        "complemento": complemento,
        "bairro": bairro,
        "cidade": cidade,
        "estado": estado,
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": motivo
    }

    # --------------------------------------------------------
    # Salvamento
    # --------------------------------------------------------

    salvar_paciente(linha)

    # --------------------------------------------------------
    # Consulta dos últimos registros
    # --------------------------------------------------------

    tabela = buscar_ultimos_pacientes()

    # --------------------------------------------------------
    # Limpa o formulário após o cadastro
    # --------------------------------------------------------

    campos_limpos = [
        "",
        None,
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        None,
        1,
        ""
    ]

    return (
        "Paciente cadastrado com sucesso!",
        tabela,
        *campos_limpos
    )


# ============================================================
# INICIALIZA O ARQUIVO
# ============================================================

inicializar_arquivo()


# ============================================================
# INTERFACE GRADIO
# ============================================================

with gr.Blocks(
    theme=gr.themes.Soft()
) as demo:

    gr.Markdown(
        # Cadastro de Pacientes - Sistema para cadastro e controle de pacientes.
    )

    # --------------------------------------------------------
    # DADOS DO PACIENTE
    # --------------------------------------------------------

    gr.Markdown("### Dados do paciente")

    nome = gr.Textbox(
        label="Nome do paciente",
        placeholder="Digite o nome completo"
    )

    with gr.Row():
        idade = gr.Number(
            label="Idade",
            precision=0,
            minimum=0,
            maximum=120
        )
        sexo = gr.Dropdown(
            choices=["M", "F", "N.I"],
            label="Sexo",
            value=None
        )

    # --------------------------------------------------------
    # ENDEREÇO
    # --------------------------------------------------------

    gr.Markdown("### Endereço")

    cep = gr.Textbox(
        label="CEP",
        placeholder="00000-000",
        max_length=9
    )

    with gr.Row():
        endereco = gr.Textbox(label="Endereço")
        numero = gr.Textbox(label="Número")
        complemento = gr.Textbox(label="Complemento")

    with gr.Row():
        bairro = gr.Textbox(label="Bairro")
        cidade = gr.Textbox(label="Cidade")
        estado = gr.Dropdown(
            choices=[
                "AC", "AL", "AP", "AM",
                "BA", "CE", "DF", "ES",
                "GO", "MA", "MT", "MS",
                "MG", "PA", "PB", "PR",
                "PE", "PI", "RJ", "RN",
                "RS", "RO", "RR", "SC",
                "SP", "SE", "TO"
            ],
            label="Estado",
            value=None
        )

    # --------------------------------------------------------
    # INFORMAÇÕES DO ATENDIMENTO
    # --------------------------------------------------------

    gr.Markdown("### Informações do atendimento")

    convenio = gr.Dropdown(
        choices=[
            "Particular",
            "Unimed",
            "Bradesco Saúde",
            "SulAmérica",
            "Porto Seguro",
            "Alice",
            "Omint",
            "Amil",
            "Outro"
        ],
        label="Convênio",
        value=None
    )

    prioridade = gr.Slider(
        minimum=1,
        maximum=5,
        step=1,
        value=1,
        label="Prioridade do atendimento (5 = Urgente)"
    )

    motivo = gr.Textbox(
        label="Motivo da consulta / observações",
        placeholder="Digite o motivo da consulta ou outras observações",
        lines=3
    )

    # --------------------------------------------------------
    # BOTÃO CADASTRAR
    # --------------------------------------------------------

    botao = gr.Button(
        "Cadastrar paciente",
        variant="primary"
    )

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    saida_msg = gr.Textbox(
        label="Status",
        interactive=False
    )

    tabela = gr.Dataframe(
        headers=COLUNAS,
        label="Últimos pacientes cadastrados",
        interactive=False
    )

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    botao_download = gr.DownloadButton(
        "Baixar dados dos pacientes (CSV)",
        value=ARQUIVO_CSV
    )

    # --------------------------------------------------------
    # EVENTO DO BOTÃO
    # --------------------------------------------------------

    botao.click(
        fn=cadastrar_paciente,

        inputs=[
            nome,
            idade,
            sexo,
            cep,
            endereco,
            numero,
            complemento,
            bairro,
            cidade,
            estado,
            convenio,
            prioridade,
            motivo
        ],

        outputs=[
            saida_msg,
            tabela,
            nome,
            idade,
            sexo,
            cep,
            endereco,
            numero,
            complemento,
            bairro,
            cidade,
            estado,
            convenio,
            prioridade,
            motivo
        ]
    )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    demo.launch()