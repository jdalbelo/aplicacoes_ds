import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Cadastro de Pacientes", page_icon="🏥", layout="centered")

st.title("🏥 Cadastro de Pacientes")

if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(
        columns=["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
    )

with st.form("cadastro", clear_on_submit=True):
    nome = st.text_input("Nome do paciente")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    convenio = st.selectbox(
        "Convênio",
        ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"],
    )
    prioridade = st.slider("Prioridade do atendimento (5 = Urgente)", 1, 5)
    motivo = st.text_area("Motivo da consulta / observações")
    enviado = st.form_submit_button("Cadastrar", type="primary")

if enviado:
    if not nome.strip():
        st.error("Erro: O nome do paciente é obrigatório.")
    else:
        nova_linha = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nome": nome, 
            "idade": idade,
            "convenio": convenio, 
            "prioridade": prioridade,
            "motivo": motivo,
        }
        st.session_state.pacientes = pd.concat(
            [st.session_state.pacientes, pd.DataFrame([nova_linha])],
            ignore_index=True,
        )
        st.success("Paciente cadastrado com sucesso!")

# Exibição e Download
if not st.session_state.pacientes.empty:
    st.markdown("### Últimos pacientes cadastrados")
    st.dataframe(st.session_state.pacientes.tail(5))
    
    csv = st.session_state.pacientes.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Baixar CSV de Pacientes",
        data=csv,
        file_name="pacientes.csv",
        mime="text/csv"
    )