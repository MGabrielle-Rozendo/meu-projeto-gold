import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
from datetime import date

# 1. CONFIGURAÇÃO DA NAVE ESPACIAL
st.set_page_config(page_title="Atlas Study Gold", page_icon="🏆", layout="wide")

# Estilo para o Modo Dark e Botões
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stButton>button { border-radius: 20px; background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%); color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

arquivo = "meus_estudos.csv"

# 2. CARREGAR DADOS
if os.path.exists(arquivo):
    df = pd.read_csv(arquivo)
else:
    df = pd.DataFrame(columns=["Data", "Matéria", "Tempo (min)"])

# --- BARRA LATERAL ---
st.sidebar.title("🎮 Painel de Controle")

with st.sidebar:
    st.subheader("⏱️ Cronômetro Pomodoro")
    tempo_foco = st.number_input("Minutos de foco:", value=25)
    if st.button("Iniciar Cronômetro"):
        barra_progresso = st.progress(0)
        status_texto = st.empty()
        for i in range(tempo_foco):
            progresso = (i + 1) / tempo_foco
            barra_progresso.progress(progresso)
            status_texto.text(f"Faltam {tempo_foco - i} minutos...")
            time.sleep(60) # Aqui no teste deixamos 1 segundo para você ver rodar!
        st.success("Fim do ciclo! Hora de registrar!")
        st.balloons()

    st.divider()
    
    st.subheader("📝 Registro Manual")
    materia_input = st.selectbox("Matéria:", ["Lógica", "Python", "HTML/CSS", "Banco de Dados", "Atlas Especial"])
    tempo_input = st.number_input("Duração (min):", min_value=1, step=5)
    
    if st.button("Salvar Registro"):
        hoje = date.today().strftime("%d/%m/%Y")
        nova_linha = pd.DataFrame([[hoje, materia_input, tempo_input]], columns=["Data", "Matéria", "Tempo (min)"])
        df = pd.concat([df, nova_linha], ignore_index=True)
        df.to_csv(arquivo, index=False)
        st.sidebar.success("Registrado no Banco de Dados!")
        st.rerun()

# --- PAINEL PRINCIPAL ---
st.title("🏆 Atlas Study Gold Edition")
st.write(f"Foco total, **Maria Gabrielle**! Vamos conquistar o mundo hoje.")

# 3. MÉTRICAS E MEDALHAS
total_min = df["Tempo (min)"].sum()
horas_totais = total_min / 60

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Estudado", f"{int(total_min)} min")
with col2:
    # SISTEMA DE MEDALHAS
    if horas_totais < 2: medalha = "🌱 Bronze"
    elif horas_totais < 5: medalha = "🥈 Prata"
    else: medalha = "🥇 Ouro"
    st.metric("Seu Nível Atual", medalha)
with col3:
    meta = 300 # Meta de 5 horas
    progresso_meta = min(total_min / meta, 1.0)
    st.write(f"**Meta do Dia (5h):** {int(progresso_meta*100)}%")
    st.progress(progresso_meta)

st.divider()

# 4. GRÁFICOS E ANÁLISE
col_esq, col_dir = st.columns([2, 1])

with col_esq:
    st.subheader("📊 Gráfico de Performance")
    if not df.empty:
        fig = px.pie(df, values='Tempo (min)', names='Matéria', hole=0.5,
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aguardando seu primeiro registro para gerar o gráfico.")

with col_dir:
    st.subheader("🏅 Conquistas")
    if horas_totais >= 5: st.success("🔓 Desbloqueado: Mestra do Código!")
    if len(df) >= 5: st.warning("🔓 Desbloqueado: Disciplina de Ferro!")
    
    st.subheader("📅 Últimas Entradas")
    st.dataframe(df.tail(5), hide_index=True)