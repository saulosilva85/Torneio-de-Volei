import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times - Vôlei", layout="centered")

st.title("🏐 Sorteio de Times - Torneio de Vôlei")

st.markdown("### 👥 Lista única de jogadores (20 nomes)")
lista_input = st.text_area("Digite um nome por linha", height=300)

if st.button("🎲 Sortear Times"):

    # =========================
    # PROCESSAR LISTA
    # =========================
    jogadores = [j.strip() for j in lista_input.split("\n") if j.strip()]

    # Remover duplicados automaticamente
    jogadores_unicos = list(set(jogadores))

    if len(jogadores_unicos) != len(jogadores):
        st.error("❌ Existem nomes duplicados na lista.")
        st.stop()

    if len(jogadores) != 20:
        st.error("❌ A lista deve conter exatamente 20 jogadores.")
        st.stop()

    # =========================
    # DEFINIR MULHERES (MANUAL)
    # =========================
    # ⚠️ AJUSTE AQUI SE PRECISAR
    mulheres_nomes = ["Milena", "Mika", "Joyce", "Rê", "Isabela"]

    mulheres = [j for j in jogadores if j in mulheres_nomes]
    homens = [j for j in jogadores if j not in mulheres_nomes]

    if len(mulheres) != 5:
        st.error("❌ O sistema não encontrou exatamente 5 mulheres.")
        st.stop()

    if len(homens) != 15:
        st.error("❌ O sistema não encontrou exatamente 15 homens.")
        st.stop()

    # =========================
    # SORTEIO
    # =========================

    random.shuffle(homens)

    cabecas = homens[:5]      # 5 homens como cabeça de chave
    restantes_homens = homens[5:]

    random.shuffle(mulheres)
    random.shuffle(restantes_homens)

    times = {}

    # Criar base dos times
    for i in range(5):
        times[f"Time {i+1}"] = [
            cabecas[i],     # cabeça de chave
            mulheres[i]     # 1 mulher por time
        ]

    # Distribuir homens restantes
    index = 0
    for jogador in restantes_homens:
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