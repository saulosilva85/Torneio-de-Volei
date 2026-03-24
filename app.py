import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times - Vôlei", layout="centered")

st.title("🏐 Sorteio de Times - Torneio de Vôlei")

st.markdown("### 👑 Cabeças de chave (5 homens)")
cabecas_input = st.text_area("Digite um nome por linha", height=150)

st.markdown("### 👥 Demais jogadores (15 jogadores, sendo 5 mulheres)")
jogadores_input = st.text_area("Digite um nome por linha", height=200)

if st.button("🎲 Sortear Times"):

    cabecas = list(set([c.strip() for c in cabecas_input.split("\n") if c.strip()]))
    jogadores = list(set([j.strip() for j in jogadores_input.split("\n") if j.strip()]))

    # 🔒 Validações
    if len(cabecas) != 5:
        st.error("É necessário exatamente 5 cabeças de chave (homens).")
        st.stop()

    if len(jogadores) != 15:
        st.error("É necessário exatamente 15 jogadores adicionais.")
        st.stop()

    # 🔍 Identificar mulheres (simples: nomes com indicador)
    # Você pode adaptar para uma lista fixa se quiser mais precisão
    mulheres = []
    homens = []

    for nome in jogadores:
        if nome.lower().endswith("a"):  # heurística simples
            mulheres.append(nome)
        else:
            homens.append(nome)

    if len(mulheres) != 5:
        st.error("Devem existir exatamente 5 mulheres na lista de jogadores.")
        st.stop()

    if len(homens) != 10:
        st.error("Devem existir exatamente 10 homens restantes.")
        st.stop()

    # 🎲 Embaralhar tudo
    random.shuffle(cabecas)
    random.shuffle(mulheres)
    random.shuffle(homens)

    # 🏐 Criar times
    times = {}

    for i in range(5):
        times[f"Time {i+1}"] = [
            cabecas[i],      # cabeça de chave
            mulheres[i]      # 1 mulher por time
        ]

    # Distribuir homens restantes
    index = 0
    for jogador in homens:
        time = f"Time {(index % 5) + 1}"
        times[time].append(jogador)
        index += 1

    # 📊 Exibir resultado
    st.success("✅ Sorteio realizado com sucesso!")

    for time, jogadores in times.items():
        st.markdown(f"## 🏐 {time}")
        for j in jogadores:
            st.write(f"• {j}")