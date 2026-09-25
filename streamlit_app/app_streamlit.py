import streamlit as st
import pandas as pd
import os
from datetime import datetime

# CONFIGURAÇÕES
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

# CONFIG. STREAMLIT
st.set_page_config(
    page_title="Cadastro de Pacientes",
    page_icon="",
    layout="centered"
)

# INICIALIZAÇÃO DO ARQUIVO
def inicializar_arquivo():
    if not os.path.exists(ARQUIVO_CSV):
        pd.DataFrame(columns=COLUNAS).to_csv(
            ARQUIVO_CSV, index=False, encoding="utf-8-sig"
        )

# LEITURA DOS DADOS
def carregar_pacientes():
    if not os.path.exists(ARQUIVO_CSV):
        return pd.DataFrame(columns=COLUNAS)
    try:
        df = pd.read_csv(ARQUIVO_CSV, encoding="utf-8-sig")
        return df
    except Exception:
        return pd.DataFrame(columns=COLUNAS)

# NORMALIZAÇÃO DOS DADOS
def normalizar_dados(nome, cep, endereco, numero, complemento, bairro, cidade, estado, motivo):
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

# VALIDAÇÃO
def validar_paciente(nome, idade, sexo, cep, endereco, numero, bairro, cidade, estado, convenio, prioridade):
    if not nome or not nome.strip():
        st.error("Digite o nome do paciente.")
        return False
    if len(nome.strip()) < 3:
        st.error("O nome deve possuir pelo menos 3 caracteres.")
        return False
    if idade is None:
        st.error("Digite a idade do paciente.")
        return False
    if idade < 0 or idade > 120:
        st.error("Digite uma idade entre 0 e 120 anos.")
        return False
    if not sexo:
        st.error("Selecione o sexo do paciente.")
        return False
    if not cep or not cep.strip():
        st.error("Digite o CEP.")
        return False

    cep_tratado = cep.strip().replace("-", "")
    if len(cep_tratado) != 8 or not cep_tratado.isdigit():
        st.error("Digite um CEP válido. Exemplo: 00000-000.")
        return False

    if not endereco or not endereco.strip():
        st.error("Digite o endereço.")
        return False
    if not numero or not numero.strip():
        st.error("Digite o número do endereço.")
        return False
    if not bairro or not bairro.strip():
        st.error("Digite o bairro.")
        return False
    if not cidade or not cidade.strip():
        st.error("Digite a cidade.")
        return False
    if not estado:
        st.error("Selecione o estado.")
        return False
    if not convenio:
        st.error("Selecione o convênio.")
        return False
    if prioridade is None or prioridade < 1 or prioridade > 5:
        st.error("Selecione uma prioridade entre 1 e 5.")
        return False

    return True

# SALVAR PACIENTE
def salvar_dados_paciente(linha):
    novo = pd.DataFrame([linha], columns=COLUNAS)
    novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False, encoding="utf-8-sig")

# EXCLUIR PACIENTE
def excluir_paciente(timestamp):
    df = carregar_pacientes()
    if not df.empty:
        df_filtrado = df[df["timestamp"] != timestamp]
        df_filtrado.to_csv(ARQUIVO_CSV, index=False, encoding="utf-8-sig")
        return True
    return False

# CONSULTAR ÚLTIMOS PACIENTES
def buscar_ultimos_pacientes():
    df = carregar_pacientes()
    if df.empty:
        return pd.DataFrame(columns=COLUNAS)
    return df.tail(5)

# LIMPAR FORMULÁRIO
def limpar_formulario():
    # Definimos os valores explícitos de vazio/padrão.
    # IMPORTANTE: isso só pode ser chamado ANTES de os widgets com essas
    # keys serem instanciados no script (ou dentro de um callback on_click/
    # on_submit, que roda antes do rerender). Nunca chame isso depois que
    # os widgets já foram desenhados na mesma execução do script.
    st.session_state["nome"] = ""
    st.session_state["idade"] = None
    st.session_state["sexo"] = None
    st.session_state["cep"] = ""
    st.session_state["endereco"] = ""
    st.session_state["numero"] = ""
    st.session_state["complemento"] = ""
    st.session_state["bairro"] = ""
    st.session_state["cidade"] = ""
    st.session_state["estado"] = None
    st.session_state["convenio"] = None
    st.session_state["prioridade"] = 1
    st.session_state["motivo"] = ""

# CADASTRAR PACIENTE
def cadastrar_paciente(nome, idade, sexo, cep, endereco, numero, complemento, bairro, cidade, estado, convenio, prioridade, motivo):
    valido = validar_paciente(nome, idade, sexo, cep, endereco, numero, bairro, cidade, estado, convenio, prioridade)
    if not valido:
        return False

    (nome, cep, endereco, numero, complemento, bairro, cidade, estado, motivo) = normalizar_dados(
        nome, cep, endereco, numero, complemento, bairro, cidade, estado, motivo
    )

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

    salvar_dados_paciente(linha)
    return True


# INICIALIZAÇÃO
inicializar_arquivo()

# LIMPEZA PENDENTE (deve rodar ANTES de qualquer widget do formulário ser criado)
# Isso evita o StreamlitWidgetAlreadyInstantiatedError: em vez de limpar o
# session_state depois que os widgets já foram desenhados, marcamos uma
# flag e limpamos no início do próximo rerun, antes de o formulário existir.
if st.session_state.get("_limpar_apos_sucesso", False):
    limpar_formulario()
    st.session_state["_limpar_apos_sucesso"] = False

# INTERFACE
st.title("Cadastro de Pacientes")
st.markdown("Sistema para cadastro e controle de pacientes.")

# FORMULÁRIO
with st.form("cadastro_paciente", clear_on_submit=False):
    st.markdown("### Dados do paciente")
    nome = st.text_input("Nome do paciente", placeholder="Digite o nome completo", key="nome")

    col1, col2 = st.columns(2)
    with col1:
        idade = st.number_input("Idade", min_value=0, max_value=120, step=1, value=None, placeholder="Digite a idade", key="idade")
    with col2:
        sexo = st.selectbox("Sexo", options=["M", "F", "N.I"], index=None, placeholder="Selecione", key="sexo")

    st.markdown("### Endereço")
    cep = st.text_input("CEP", placeholder="00000-000", max_chars=9, key="cep")

    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        endereco = st.text_input("Endereço", key="endereco")
    with col2:
        numero = st.text_input("Número", key="numero")
    with col3:
        complemento = st.text_input("Complemento", key="complemento")

    col1, col2, col3 = st.columns(3)
    with col1:
        bairro = st.text_input("Bairro", key="bairro")
    with col2:
        cidade = st.text_input("Cidade", key="cidade")
    with col3:
        estado = st.selectbox("Estado", options=ESTADOS, index=None, placeholder="Selecione", key="estado")

    st.markdown("### Informações do atendimento")
    convenio = st.selectbox("Convênio", options=CONVENIOS, index=None, placeholder="Selecione o convênio", key="convenio")
    prioridade = st.slider("Prioridade do atendimento (5 = Urgente)", min_value=1, max_value=5, value=1, step=1, key="prioridade")
    motivo = st.text_area("Motivo da consulta / observações", placeholder="Digite o motivo da consulta ou outras observações", height=100, key="motivo")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        enviado = st.form_submit_button("Cadastrar paciente", type="primary", use_container_width=True)
    with col_btn2:
        # on_click roda ANTES do rerender, então chamar limpar_formulario()
        # aqui é seguro.
        st.form_submit_button("Limpar Formulário", use_container_width=True, on_click=limpar_formulario)

# PROCESSAMENTO DO CADASTRO 
if enviado:
    sucesso = cadastrar_paciente(nome, idade, sexo, cep, endereco, numero, complemento, bairro, cidade, estado, convenio, prioridade, motivo)
    if sucesso:
        st.success("Paciente cadastrado com sucesso!")
        # Não chamamos limpar_formulario() diretamente aqui, pois os widgets
        # do formulário já foram instanciados nesta execução do script.
        # Em vez disso, marcamos uma flag e disparamos um rerun: na próxima
        # execução, a flag é verificada e o formulário é limpo ANTES de os
        # widgets serem criados novamente.
        st.session_state["_limpar_apos_sucesso"] = True
        st.rerun()

st.divider()

# ÚLTIMOS PACIENTES
st.markdown("### Últimos pacientes cadastrados")
df_ultimos = buscar_ultimos_pacientes()

if df_ultimos.empty:
    st.info("Nenhum paciente cadastrado ainda.")
else:
    st.dataframe(df_ultimos, use_container_width=True, hide_index=True)


# GESTÃO DOS DADOS: EXCLUIR E EXPORTAR
df_completo = carregar_pacientes()
if not df_completo.empty:
    st.divider()
    st.markdown("### Gestão de Registros")

    col_export, col_delete = st.columns(2)

    # Coluna 1: Download
    with col_export:
        csv = df_completo.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="Baixar dados cadastrados (CSV)",
            data=csv,
            file_name="pacientes.csv",
            mime="text/csv",
            use_container_width=True
        )

    # Coluna 2: Exclusão (Expander)
    with col_delete:
        with st.expander("Excluir um paciente"):
            opcoes_exclusao = {}
            for idx, row in df_completo.iterrows():
                try:
                    data_formatada = datetime.fromisoformat(row['timestamp']).strftime("%d/%m/%Y %H:%M:%S")
                except:
                    data_formatada = row['timestamp']

                texto_exibicao = f"{row['nome']} - {data_formatada}"
                opcoes_exclusao[texto_exibicao] = row['timestamp']

            selecao_exclusao = st.selectbox(
                "Selecione o paciente",
                options=list(opcoes_exclusao.keys()),
                index=None,
                placeholder="Escolha para excluir..."
            )

            if st.button("Confirmar Exclusão", type="primary", use_container_width=True):
                if selecao_exclusao:
                    timestamp_alvo = opcoes_exclusao[selecao_exclusao]
                    if excluir_paciente(timestamp_alvo):
                        st.success("Registro excluído com sucesso!")
                        st.rerun()
                else:
                    st.warning("Selecione um paciente para excluir.")