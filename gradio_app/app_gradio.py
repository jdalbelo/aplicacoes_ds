import gradio as gr
import pandas as pd
import os
from datetime import datetime

# CONFIGURAÇÕES
ARQUIVO_CSV = "pacientes.csv"

COLUNAS = [
    "timestamp", "nome", "idade", "sexo", "cep", "endereco", 
    "numero", "complemento", "bairro", "cidade", "estado", 
    "convenio", "prioridade", "motivo"
]

ESTADOS = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", 
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", 
    "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]

CONVENIOS = [
    "Particular", "Unimed", "Bradesco Saúde", "SulAmérica", 
    "Porto Seguro", "Alice", "Omint", "Amil", "Outro"
]


# FUNÇÕES DE MANIPULAÇÃO DE ARQUIVO E DADOS
def inicializar_arquivo():
    if not os.path.exists(ARQUIVO_CSV):
        pd.DataFrame(columns=COLUNAS).to_csv(ARQUIVO_CSV, index=False, encoding="utf-8-sig")

def carregar_pacientes():
    if not os.path.exists(ARQUIVO_CSV):
        return pd.DataFrame(columns=COLUNAS)
    try:
        return pd.read_csv(ARQUIVO_CSV, encoding="utf-8-sig")
    except Exception:
        return pd.DataFrame(columns=COLUNAS)

def buscar_ultimos_pacientes():
    df = carregar_pacientes()
    if df.empty:
        return pd.DataFrame(columns=COLUNAS)
    return df.tail(5)

# NOVA FUNÇÃO: Busca por nome
def buscar_paciente_por_nome(nome_busca):
    df = carregar_pacientes()
    if df.empty or not nome_busca.strip():
        return pd.DataFrame(columns=COLUNAS)
    
    # Filtra usando contains ignorando maiúsculas e minúsculas
    mask = df["nome"].str.contains(nome_busca.strip(), case=False, na=False)
    df_filtrado = df[mask]
    return df_filtrado

def normalizar_dados(nome, cep, endereco, numero, complemento, bairro, cidade, estado, motivo):
    nome = nome.strip().title()
    cep = cep.strip().replace("-", "")

    if len(cep) == 8 and cep.isdigit():
        cep = f"{cep[:5]}-{cep[5:]}"

    endereco = endereco.strip().title()
    numero = str(numero).strip()
    complemento = str(complemento).strip()
    bairro = bairro.strip().title()
    cidade = cidade.strip().title()
    estado = estado.strip().upper() if estado else ""
    motivo = str(motivo).strip()

    return (nome, cep, endereco, numero, complemento, bairro, cidade, estado, motivo)

def validar_paciente(nome, idade, sexo, cep, endereco, numero, bairro, cidade, estado, convenio, prioridade):
    if not nome or not nome.strip():
        raise gr.Error("Digite o nome do paciente.")
    if len(nome.strip()) < 3:
        raise gr.Error("O nome deve possuir pelo menos 3 caracteres.")
    if idade is None:
        raise gr.Error("Digite a idade do paciente.")
    if idade < 0 or idade > 120:
        raise gr.Error("Digite uma idade entre 0 e 120 anos.")
    if not sexo:
        raise gr.Error("Selecione o sexo do paciente.")
    if not cep or not cep.strip():
        raise gr.Error("Digite o CEP.")
    
    cep_limpo = cep.strip().replace("-", "")
    if len(cep_limpo) != 8 or not cep_limpo.isdigit():
        raise gr.Error("Digite um CEP válido. Exemplo: 00000-000.")
        
    if not endereco or not endereco.strip():
        raise gr.Error("Digite o endereço.")
    if not numero or not str(numero).strip():
        raise gr.Error("Digite o número do endereço.")
    if not bairro or not bairro.strip():
        raise gr.Error("Digite o bairro.")
    if not cidade or not cidade.strip():
        raise gr.Error("Digite a cidade.")
    if not estado:
        raise gr.Error("Selecione o estado.")
    if not convenio:
        raise gr.Error("Selecione o convênio.")
    if prioridade is None or prioridade < 1 or prioridade > 5:
        raise gr.Error("Selecione uma prioridade entre 1 e 5.")


# CADASTRAR & EXCLUIR
def cadastrar_paciente(nome, idade, sexo, cep, endereco, numero, complemento, bairro, cidade, estado, convenio, prioridade, motivo):
    validar_paciente(nome, idade, sexo, cep, endereco, numero, bairro, cidade, estado, convenio, prioridade)

    nome, cep, endereco, numero, complemento, bairro, cidade, estado, motivo = normalizar_dados(
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

    novo = pd.DataFrame([linha])
    novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False, encoding="utf-8-sig")

    tabela = buscar_ultimos_pacientes()
    opcoes_exclusao = atualizar_opcoes_exclusao()
    
    campos_limpos = ["", None, None, "", "", "", "", "", "", None, None, 1, ""]

    return (
        "Paciente cadastrado com sucesso!", 
        tabela, 
        gr.update(choices=opcoes_exclusao), 
        *campos_limpos
    )

def excluir_paciente(selecao):
    if not selecao:
        raise gr.Error("Selecione um paciente para excluir.")
        
    timestamp = selecao.split(" - ")[-1]
    
    df = carregar_pacientes()
    if not df.empty:
        df_filtrado = df[df["timestamp"] != timestamp]
        df_filtrado.to_csv(ARQUIVO_CSV, index=False, encoding="utf-8-sig")
        
    tabela = buscar_ultimos_pacientes()
    novas_opcoes = atualizar_opcoes_exclusao()
    
    return "Registro excluído com sucesso!", tabela, gr.update(choices=novas_opcoes, value=None)

def atualizar_opcoes_exclusao():
    df = carregar_pacientes()
    if df.empty:
        return []
    return [f"{row['nome']} - {row['timestamp']}" for _, row in df.iterrows()]



# INICIALIZA O ARQUIVO
inicializar_arquivo()


# INTERFACE GRADIO
with gr.Blocks(theme=gr.themes.Ocean()) as cadastro:

    gr.Markdown("# Cadastro de Pacientes\nSistema para cadastro e controle de pacientes.")

    
    # 1. FORMULÁRIO DE CADASTRO
    
    with gr.Group():
        gr.Markdown("### Dados do paciente")
        nome = gr.Textbox(label="Nome do paciente", placeholder="Digite o nome completo")
        with gr.Row():
            idade = gr.Number(label="Idade", precision=0, minimum=0, maximum=120)
            sexo = gr.Dropdown(choices=["M", "F", "N.I"], label="Sexo", value=None)

        gr.Markdown("### Endereço")
        cep = gr.Textbox(label="CEP", placeholder="00000-000", max_length=9)
        with gr.Row():
            endereco = gr.Textbox(label="Endereço")
            numero = gr.Textbox(label="Número")
            complemento = gr.Textbox(label="Complemento")
        with gr.Row():
            bairro = gr.Textbox(label="Bairro")
            cidade = gr.Textbox(label="Cidade")
            estado = gr.Dropdown(choices=ESTADOS, label="Estado", value=None)

        gr.Markdown("### Informações do atendimento")
        convenio = gr.Dropdown(choices=CONVENIOS, label="Convênio", value=None)
        prioridade = gr.Slider(minimum=1, maximum=5, step=1, value=1, label="Prioridade do atendimento (5 = Urgente)")
        motivo = gr.Textbox(label="Motivo da consulta / observações", placeholder="Digite o motivo da consulta ou outras observações", lines=3)

        botao_cadastrar = gr.Button("Cadastrar paciente", variant="primary")
        saida_msg = gr.Textbox(label="Status do Cadastro", interactive=False)

    gr.Markdown("---")

    
    # 2. BUSCA DE PACIENTES
    gr.Markdown("## Buscar Pacientes")
    with gr.Row():
        campo_busca = gr.Textbox(label="Buscar por nome", placeholder="Digite o nome (ou parte dele) para buscar", scale=3)
        botao_busca = gr.Button("Pesquisar", scale=1)
    
    tabela_busca = gr.Dataframe(headers=COLUNAS, interactive=False, label="Resultados da Busca")

    gr.Markdown("---")

    
    # 3. GESTÃO DE REGISTROS (PARTE INFERIOR)
    gr.Markdown("## Gestão de Registros")
    
    gr.Markdown("### Últimos cadastros")
    tabela_ultimos = gr.Dataframe(value=buscar_ultimos_pacientes(), headers=COLUNAS, interactive=False)
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Exportar Dados")
            botao_download = gr.DownloadButton("Baixar CSV Completo", value=ARQUIVO_CSV)
        
        with gr.Column():
            gr.Markdown("### Excluir um paciente")
            dropdown_excluir = gr.Dropdown(choices=atualizar_opcoes_exclusao(), label="Selecione o paciente", value=None)
            botao_excluir = gr.Button("Confirmar Exclusão", variant="stop")
            saida_exclusao = gr.Textbox(label="Status da Exclusão", interactive=False)


    # Evento de Cadastro
    botao_cadastrar.click(
        fn=cadastrar_paciente,
        inputs=[nome, idade, sexo, cep, endereco, numero, complemento, bairro, cidade, estado, convenio, prioridade, motivo],
        outputs=[
            saida_msg, tabela_ultimos, dropdown_excluir, 
            nome, idade, sexo, cep, endereco, numero, complemento, bairro, cidade, estado, convenio, prioridade, motivo
        ]
    )

    # Evento de Busca (pode ser acionado clicando no botão ou apertando Enter no campo de texto)
    botao_busca.click(fn=buscar_paciente_por_nome, inputs=[campo_busca], outputs=[tabela_busca])
    campo_busca.submit(fn=buscar_paciente_por_nome, inputs=[campo_busca], outputs=[tabela_busca])

    # Evento de Exclusão
    botao_excluir.click(
        fn=excluir_paciente,
        inputs=[dropdown_excluir],
        outputs=[saida_exclusao, tabela_ultimos, dropdown_excluir]
    )

if __name__ == "__main__":
    cadastro.launch()