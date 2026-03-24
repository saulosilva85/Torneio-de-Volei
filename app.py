import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times - Vôlei", layout="centered")

st.title("🏐 Sorteio de Times de Vôlei")

st.markdown("## 🔹 Cabeças de Chave (5 homens obrigatórios)")
cabecas_input = st.text_area("Digite 5 nomes (um por linha)")

st.markdown("## 🔹 Mulheres (5 obrigatórias - 1 por time)")
mulheres_input = st.text_area("Digite 5 nomes femininos")

st.markdown("## 🔹 Demais Jogadores")
jogadores_input = st.text_area("Digite os outros jogadores")

if st.button("🎲 Sortear Times"):

    # Processamento das listas
    cabecas = [n.strip() for n in cabecas_input.split("\n") if n.strip()]
    mulheres = [n.strip() for n in mulheres_input.split("\n") if n.strip()]
    jogadores = [n.strip() for n in jogadores_input.split("\n") if n.strip()]

    # Validações
    if len(cabecas) != 5:
        st.error("Você precisa informar exatamente 5 cabeças de chave.")
        st.stop()

    if len(mulheres) != 5:
        st.error("Você precisa informar exatamente 5 mulheres.")
        st.stop()

    # Verifica duplicidade
    todos = cabecas + mulheres + jogadores
    if len(todos) != len(set(todos)):
        st.error("Existem nomes duplicados. Corrija antes de continuar.")
        st.stop()

    # Embaralhar listas
    random.shuffle(mulheres)
    random.shuffle(jogadores)

    # Criar times com cabeça de chave + mulher
    times = []
    for i in range(5):
        time = [cabecas[i], mulheres[i]]
        times.append(time)

    # Distribuir demais jogadores
    i = 0
    while jogadores:
        times[i % 5].append(jogadores.pop(0))
        i += 1

    # Exibir resultado
    st.markdown("## 🏆 Times Sorteados")

    for i, time in enumerate(times):
        st.markdown(f"### Time {i+1}")
        for jogador in time:
            st.write(f"• {jogador}")