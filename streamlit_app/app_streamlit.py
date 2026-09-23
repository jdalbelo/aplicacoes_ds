import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ============================================================
# CONFIGURAÇÕES
# ============================================================

ARQUIVO_CSV = "pacientes.csv"

COLUNAS = [
    "timestamp",
    "nome",
    "idade",
    "sexo",
    "cep",
    "endereco",
    "numero",
    "complemento",
    "bairro",
    "cidade",
    "estado",
    "convenio",
    "prioridade",
    "motivo"
]

ESTADOS = [
    "AC", "AL", "AP", "AM",
    "BA", "CE", "DF", "ES",
    "GO", "MA", "MT", "MS",
    "MG", "PA", "PB", "PR",
    "PE", "PI", "RJ", "RN",
    "RS", "RO", "RR", "SC",
    "SP", "SE", "TO"
]

CONVENIOS = [
    "Particular",
    "Unimed",
    "Bradesco Saúde",
    "SulAmérica",
    "Porto Seguro",
    "Alice",
    "Omint",
    "Amil",
    "Outro"
]


# ============================================================
# CONFIGURAÇÃO DO STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Cadastro de Pacientes",
    page_icon="🏥",
    layout="centered"
)

# ============================================================
# INICIALIZAÇÃO DO ARQUIVO
# ============================================================
def inicializar_arquivo():
    #Cria o arquivo CSV caso ele ainda não exista.
    if not os.path.exists(ARQUIVO_CSV):

        pd.DataFrame(
            columns=COLUNAS
        ).to_csv(
            ARQUIVO_CSV,
            index=False,
            encoding="utf-8-sig"
        )

# ============================================================
# LEITURA DOS DADOS
# ============================================================

def carregar_pacientes():
    #Carrega os pacientes armazenados no CSV.

    if not os.path.exists(ARQUIVO_CSV):
        return pd.DataFrame(columns=COLUNAS)

    try:

        df = pd.read_csv(
            ARQUIVO_CSV,
            encoding="utf-8-sig"
        )

        return df

    except Exception:
        return pd.DataFrame(columns=COLUNAS)


# ============================================================
# NORMALIZAÇÃO DOS DADOS
# ============================================================

def normalizar_dados(
    nome,
    cep,
    endereco,
    numero,
    complemento,
    bairro,
    cidade,
    estado,
    motivo
):
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

    return (
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


# ============================================================
# VALIDAÇÃO
# ============================================================

def validar_paciente(
    nome,
    idade,
    sexo,
    cep,
    endereco,
    numero,
    bairro,
    cidade,
    estado,
    convenio,
    prioridade
):
    #Valida os campos obrigatórios do cadastro. Retorna: True  -> dados válidos - False -> dados inválidos

    # Nome
    if not nome or not nome.strip():
        st.error("Digite o nome do paciente.")
        return False

    if len(nome.strip()) < 3:
        st.error(
            "O nome deve possuir pelo menos 3 caracteres."
        )
        return False

    # Idade
    if idade is None:
        st.error("Digite a idade do paciente.")
        return False

    if idade < 0 or idade > 120:
        st.error(
            "Digite uma idade entre 0 e 120 anos."
        )
        return False

    # Sexo
     if not sexo:
        st.error("Selecione o sexo do paciente.")
        return False

    # CEP
    if not cep or not cep.strip():
        st.error("Digite o CEP.")
        return False

    cep_tratado = cep.strip().replace("-", "")

    if len(cep_tratado) != 8 or not cep_tratado.isdigit():
        st.error(
            "Digite um CEP válido. Exemplo: 00000-000."
        )
        return False

    # Endereço
    if not endereco or not endereco.strip():
        st.error("Digite o endereço.")
        return False

    # Número
    if not numero or not numero.strip():
        st.error(
            "Digite o número do endereço."
        )
        return False

    # Bairro
    if not bairro or not bairro.strip():

        st.error("Digite o bairro.")
        return False

    # Cidade
    if not cidade or not cidade.strip():

        st.error("Digite a cidade.")
        return False

    # Estado
    if not estado:

        st.error("Selecione o estado.")
        return False

    # Convênio
     if not convenio:

        st.error("Selecione o convênio.")
        return False

    # Prioridade
    if prioridade is None or prioridade < 1 or prioridade > 5:

        st.error(
            "Selecione uma prioridade entre 1 e 5."
        )
        return False

    return True

# SALVAR PACIENTE

def salvar_dados_paciente(linha):
    #Adiciona um novo paciente ao arquivo CSV.

    novo = pd.DataFrame(
        [linha],
        columns=COLUNAS
    )

    novo.to_csv(
        ARQUIVO_CSV,
        mode="a",
        header=False,
        index=False,
        encoding="utf-8-sig"
    )

# CONSULTAR ÚLTIMOS PACIENTES

def buscar_ultimos_pacientes():
    #Retorna os últimos 5 pacientes cadastrados.

    df = carregar_pacientes()

    if df.empty:
        return pd.DataFrame(columns=COLUNAS)

    return df.tail(5)


# LIMPAR FORMULÁRIO

def limpar_formulario():

    campos = [
        "nome",
        "idade",
        "sexo",
        "cep",
        "endereco",
        "numero",
        "complemento",
        "bairro",
        "cidade",
        "estado",
        "convenio",
        "prioridade",
        "motivo"
    ]

    for campo in campos:

        if campo in st.session_state:
            del st.session_state[campo]


# CADASTRAR PACIENTE

def cadastrar_paciente(
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
):
    #Valida, normaliza e salva o paciente.

    # Validação

    valido = validar_paciente(
        nome,
        idade,
        sexo,
        cep,
        endereco,
        numero,
        bairro,
        cidade,
        estado,
        convenio,
        prioridade
    )

    if not valido:
        return False

    # Normalização

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

    # Criação do registro
 
    linha = {
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),
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

    # Salvamento
    
    salvar_dados_paciente(linha)
    return True


# INICIALIZAÇÃO
inicializar_arquivo()


# INTERFACE
st.title("🏥 Cadastro de Pacientes")

st.markdown(
    "Sistema para cadastro e controle de pacientes."
)


# FORMULÁRIO

with st.form(
    "cadastro_paciente",
    clear_on_submit=False
):

    # DADOS DO PACIENTE
    
    st.markdown("### 👤 Dados do paciente")

    nome = st.text_input(
        "Nome do paciente",
        placeholder="Digite o nome completo",
        key="nome"
    )

    col1, col2 = st.columns(2)

    with col1:

        idade = st.number_input(
            "Idade",
            min_value=0,
            max_value=120,
            step=1,
            value=None,
            placeholder="Digite a idade",
            key="idade"
        )

    with col2:

        sexo = st.selectbox(
            "Sexo",
            options=["M", "F", "N.I"],
            index=None,
            placeholder="Selecione",
            key="sexo"
        )

    # ENDEREÇO

    st.markdown("### 📍 Endereço")
    cep = st.text_input(
        "CEP",
        placeholder="00000-000",
        max_chars=9,
        key="cep"
    )

    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:

        endereco = st.text_input(
            "Endereço",
            key="endereco"
        )

    with col2:

        numero = st.text_input(
            "Número",
            key="numero"
        )

    with col3:

        complemento = st.text_input(
            "Complemento",
            key="complemento"
        )

    col1, col2, col3 = st.columns(3)

    with col1:

        bairro = st.text_input(
            "Bairro",
            key="bairro"
        )

    with col2:

        cidade = st.text_input(
            "Cidade",
            key="cidade"
        )

    with col3:

        estado = st.selectbox(
            "Estado",
            options=ESTADOS,
            index=None,
            placeholder="Selecione",
            key="estado"
        )

    # INFORMAÇÕES DO ATENDIMENTO

    st.markdown(
        "### 🏥 Informações do atendimento"
    )

    convenio = st.selectbox(
        "Convênio",
        options=CONVENIOS,
        index=None,
        placeholder="Selecione o convênio",
        key="convenio"
    )

    prioridade = st.slider(
        "Prioridade do atendimento (5 = Urgente)",
        min_value=1,
        max_value=5,
        value=1,
        step=1,
        key="prioridade"
    )

    motivo = st.text_area(
        "Motivo da consulta / observações",
        placeholder=(
            "Digite o motivo da consulta "
            "ou outras observações"
        ),
        height=100,
        key="motivo"
    )

    # BOTÃO

    enviado = st.form_submit_button(
        "Cadastrar paciente",
        type="primary",
        use_container_width=True
    )

# PROCESSAMENTO DO CADASTRO
if enviado:

    sucesso = cadastrar_paciente(
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
    )

    if sucesso:
        st.success(
            "✅ Paciente cadastrado com sucesso!"
        )
        st.rerun()


# ÚLTIMOS PACIENTES

st.markdown("### 📋 Últimos pacientes cadastrados")

df_ultimos = buscar_ultimos_pacientes()

if df_ultimos.empty:

    st.info(
        "Nenhum paciente cadastrado ainda."
    )

else:

    st.dataframe(
        df_ultimos,
        use_container_width=True,
        hide_index=True
    )


# DOWNLOAD

df_completo = carregar_pacientes()

if not df_completo.empty:

    st.markdown("### 📥 Exportação")

    csv = df_completo.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="📥 Baixar dados dos pacientes (CSV)",
        data=csv,
        file_name="pacientes.csv",
        mime="text/csv",
        use_container_width=True
    )