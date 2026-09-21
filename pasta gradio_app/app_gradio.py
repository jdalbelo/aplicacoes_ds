import gradio as gr
import pandas as pd
import os
from datetime import datetime

ARQUIVO_CSV = "pacientes.csv"
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]

def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    if not nome.strip():
        return "Erro: O nome do paciente é obrigatório.", pd.DataFrame()
        
    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome, 
        "idade": idade,
        "convenio": convenio, 
        "prioridade": prioridade,
        "motivo": motivo,
    }
    
    novo = pd.DataFrame([linha])
    
    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)
        
    return "Paciente cadastrado com sucesso!", pd.read_csv(ARQUIVO_CSV).tail(5)

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🏥 Cadastro de Pacientes (Recepção)")
    
    nome = gr.Textbox(label="Nome do paciente")
    idade = gr.Number(label="Idade", precision=0)
    convenio = gr.Dropdown(
        ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"],
        label="Convênio",
    )
    prioridade = gr.Slider(1, 5, step=1, label="Prioridade do atendimento (5 = Urgente)")
    motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3)
    
    botao = gr.Button("Cadastrar", variant="primary")
    saida_msg = gr.Textbox(label="Status", interactive=False)
    tabela = gr.Dataframe(label="Últimos pacientes cadastrados")
    
    botao.click(
        cadastrar_paciente,
        inputs=[nome, idade, convenio, prioridade, motivo],
        outputs=[saida_msg, tabela],
    )

if __name__ == "__main__":
    demo.launch()