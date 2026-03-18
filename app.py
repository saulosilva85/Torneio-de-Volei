import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times", layout="centered")

st.title("🏐 Torneio de Vôlei")

st.markdown("### Cabeças de Chave (Inserir de 2 a 6 jogadores)")
cabecas_input = st.text_area("Digite um nome por linha", height=120)

st.markdown("### Demais Jogadores")
jogadores_input = st.text_area("Digite um nome por linha", height=200)

if st.button("🎲 Sortear Times"):
    cabecas = [c.strip() for c in cabecas_input.split("\n") if c.strip()]
    jogadores = [j.strip() for j in jogadores_input.split("\n") if j.strip()]

    # Validação
    if len(cabecas) < 2 or len(cabecas) > 6:
        st.error("Você deve inserir entre 2 e 6 cabeças de chave.")
    else:
        num_times = len(cabecas)

        # Criar times com cabeças de chave
        times = {f"Time {i+1}": [cabecas[i]] for i in range(num_times)}

        random.shuffle(jogadores)

        # Distribuir jogadores
        for i, jogador in enumerate(jogadores):
            time = f"Time {(i % num_times) + 1}"
            times[time].append(jogador)

        st.success("Sorteio realizado!")

        # Exibir resultado
        for time, integrantes in times.items():
            st.markdown(f"## 🏆 {time}")
            for jogador in integrantes:
                st.write(f"• {jogador}")