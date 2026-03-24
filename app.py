import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times - Vôlei", layout="centered")

st.title("🏐 Sorteio de Times - Torneio de Vôlei")

# =========================
# INPUTS
# =========================

st.markdown("### 👑 Cabeças de chave (5 homens)")
cabecas_input = st.text_area("Digite um nome por linha", height=150)

st.markdown("### 👩 Mulheres (5 jogadoras)")
mulheres_input = st.text_area("Digite um nome por linha", height=150)

st.markdown("### 👥 Demais jogadores (10 homens)")
homens_input = st.text_area("Digite um nome por linha", height=150)

# =========================
# BOTÃO
# =========================

if st.button("🎲 Sortear Times"):

    # =========================
    # PROCESSAMENTO
    # =========================

    cabecas = [c.strip() for c in cabecas_input.split("\n") if c.strip()]
    mulheres = [m.strip() for m in mulheres_input.split("\n") if m.strip()]
    homens = [h.strip() for h in homens_input.split("\n") if h.strip()]

    # 🔒 REMOVER DUPLICADOS GLOBAIS
    todos = cabecas + mulheres + homens
    if len(todos) != len(set(todos)):
        st.error("❌ Existem nomes duplicados entre as listas.")
        st.stop()

    # =========================
    # VALIDAÇÕES
    # =========================

    if len(cabecas) != 5:
        st.error("❌ Devem existir exatamente 5 cabeças de chave.")
        st.stop()

    if len(mulheres) != 5:
        st.error("❌ Devem existir exatamente 5 mulheres.")
        st.stop()

    if len(homens) != 10:
        st.error("❌ Devem existir exatamente 10 homens.")
        st.stop()

    # =========================
    # SORTEIO
    # =========================

    random.shuffle(cabecas)
    random.shuffle(mulheres)
    random.shuffle(homens)

    times = {}

    # Criar base dos times
    for i in range(5):
        times[f"Time {i+1}"] = [
            cabecas[i],   # cabeça de chave
            mulheres[i]   # 1 mulher por time
        ]

    # Distribuir homens restantes
    index = 0
    for jogador in homens:
        time = f"Time {(index % 5) + 1}"
        times[time].append(jogador)
        index += 1

    # =========================
    # RESULTADO
    # =========================

    st.success("✅ Sorteio realizado com sucesso!")

    for time, jogadores in times.items():
        st.markdown(f"## 🏐 {time}")
        for j in jogadores:
            st.write(f"• {j}")