import streamlit as st
import pandas as pd
import requests

# =========================================================
# CONFIGURAÇÃO - COLOQUE SEUS DADOS AQUI
# =========================================================
# Clique entre as aspas e cole o código que o BotFather te deu
TOKEN_TELEGRAM = "COLE_SEU_TOKEN_AQUI" 

# Clique entre as aspas e cole o número que o UserInfoBot te deu
MEU_CHAT_ID = "COLE_SEU_ID_AQUI"
# =========================================================

def enviar_mensagem(texto):
    """Função que faz a mágica de mandar o aviso pro celular"""
    # O .strip() remove espaços vazios que podem causar erro
    token = TOKEN_TELEGRAM.strip()
    chat_id = MEU_CHAT_ID.strip()
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": texto, "parse_mode": "Markdown"}
    
    try:
        resposta = requests.post(url, data=payload)
        return resposta.json()
    except Exception as e:
        return {"ok": False, "description": str(e)}

# Configurações visuais do App
st.set_page_config(page_title="Barber Top", page_icon="✂️")
st.title("✂️ Agendamento Online")

# Criar a lista de agendamentos na memória
if 'agenda' not in st.session_state:
    st.session_state.agenda = []

# Formulário de agendamento
with st.form("form_corte"):
    st.subheader("Preencha seus dados:")
    nome = st.text_input("Nome do Cliente")
    servico = st.selectbox("O que vamos fazer?", ["Corte", "Barba", "Combo"])
    data = st.date_input("Data")
    hora = st.time_input("Hora")
    
    botao = st.form_submit_button("Confirmar Agendamento")

if botao:
    if nome and "COLE" not in TOKEN_TELEGRAM:
        # 1. Salva no site
        st.session_state.agenda.append({"Cliente": nome, "Serviço": servico, "Hora": str(hora)})
        
        # 2. Envia pro Telegram
        texto_notificacao = f"🚀 *NOVO CLIENTE!*\n\n👤 {nome}\n💇‍♂️ {servico}\n⏰ {hora}"
        resultado = enviar_mensagem(texto_notificacao)
        
        if resultado.get("ok"):
            st.success("✅ Agendado! O barbeiro já recebeu o aviso no celular.")
            st.balloons()
        else:
            erro = resultado.get("description", "Erro desconhecido")
            st.error(f"O agendamento foi feito, mas o Telegram deu erro: {erro}")
    else:
        st.warning("⚠️ Verifique se você preencheu o Nome e se configurou o Token/ID no código!")

# Exibição dos horários
st.divider()
st.subheader("📅 Próximos de Hoje")
if st.session_state.agenda:
    st.table(pd.DataFrame(st.session_state.agenda))
