import gradio as gr
import pandas as pd
import os
from datetime import datetime

ARQUIVO_CSV = "pacientes.csv"
COLUNAS = ["timestamp", "nome", "idade", "sexo", "cep", "endereco", "numero", "complemento", "bairro", "cidade", "estado", "convenio", "prioridade", "motivo"]
# Garante que o arquivo exista ao iniciar o app para o botão de download não falhar
if not os.path.exists(ARQUIVO_CSV):
    pd.DataFrame(columns=COLUNAS).to_csv(ARQUIVO_CSV, index=False)

def cadastrar_paciente(nome, idade, sexo, cep, endereco, numero, complemento, bairro, cidade, estado,convenio, prioridade, motivo):
    if not nome.strip():
        return "Erro: O nome do paciente é obrigatório.", pd.DataFrame()
        
    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome, 
        "idade": idade,
        "sexo": sexo,
        "cep": cep,
        "endereco": endereco,
        "numero": numero,
        "complemento": complemento,
        "bairro": bairro,
        "cidade": cidade,
        "estado": estado,
        "convenio": convenio, 
        "prioridade": prioridade,
        "motivo": motivo,
    }

    if not nome or not nome.strip():
        raise gr.Error("Digite o nome do paciente.")

    if idade is None:
        raise gr.Error("Digite a idade do paciente.")

    if not sexo:
        raise gr.Error("Selecione o sexo do paciente.")

    if not cep:
        raise gr.Error("Digite o CEP.")

    if not endereco or not endereco.strip():
        raise gr.Error("Digite o endereço.")

    if not numero or not numero.strip():
        raise gr.Error("Digite o número do endereço.")

    if not bairro or not bairro.strip():
        raise gr.Error("Digite o bairro.")

    if not cidade or not cidade.strip():
        raise gr.Error("Digite a cidade.")

    if not estado or not estado.strip():
        raise gr.Error("Digite o estado.")

    if not convenio:
        raise gr.Error("Selecione o convênio.")
    
    novo = pd.DataFrame([linha])
    
    # Como garantimos a criação do arquivo no início, podemos apenas dar append
    novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
        
    return "Paciente cadastrado com sucesso!", pd.read_csv(ARQUIVO_CSV).tail(5)

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🏥 Cadastro de Pacientes (Recepção)")
    
    nome = gr.Textbox(label="Nome do paciente")
    with gr.Row():
        idade = gr.Number(label="Idade", precision=0)
        sexo = gr.Dropdown(["","M","F","N.I"],label="Sexo")
    cep = gr.Textbox(label="CEP",placeholder="00000-000",max_length=9)
    with gr.Row():
        endereco = gr.Textbox(label="Endereço")
        numero = gr.Textbox(label="Número")
        complemento = gr.Textbox(label="Complemento")
    with gr.Row():
        bairro = gr.Textbox(label="Bairro")
        cidade = gr.Textbox(label="Cidade")
        estado = gr.Textbox(label="Estado")
    convenio = gr.Dropdown(
        ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Porto Seguro", "Alice", "Omint", "Amil", "Outro"],
        label="Convênio"
    )
    prioridade = gr.Slider(1, 5, step=1, label="Prioridade do atendimento (5 = Urgente)")
    motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3)
    
    botao = gr.Button("Cadastrar", variant="primary")
    saida_msg = gr.Textbox(label="Status", interactive=False)
    tabela = gr.Dataframe(label="Últimos pacientes cadastrados")
    
    # Adicionando o botão de download na interface apontando para o arquivo CSV
    botao_download = gr.DownloadButton("Baixar Planilha de Pacientes (CSV)", value=ARQUIVO_CSV)
    
    botao.click(
        cadastrar_paciente,
        inputs=[nome, idade, sexo, cep, endereco, numero, complemento, bairro, cidade, estado, convenio, prioridade, motivo],
        outputs=[saida_msg, tabela],
    )

if __name__ == "__main__":
    demo.launch()