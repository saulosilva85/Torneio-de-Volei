import streamlit as st
import random
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

st.set_page_config(page_title="Torneio de Vôlei", layout="centered")

st.title("🏐 OPEN VILLAGE 18+ 🏐")

# Inputs
st.markdown("## 🔹 Cabeças de Chave (6 homens)")
cabecas_input = st.text_area("Digite 6 nomes")

st.markdown("## 🔹 Mulheres (6 obrigatórias)")
mulheres_input = st.text_area("Digite 6 nomes femininos")

st.markdown("## 🔹 Demais Jogadores")
jogadores_input = st.text_area("Digite os demais jogadores")


# -------------------------
# GERAR JOGOS DO GRUPO (3 TIMES)
# -------------------------
def gerar_jogos_grupo(times):
    return [
        (times[0], times[1]),
        (times[0], times[2]),
        (times[1], times[2])
    ]


# -------------------------
# GERAR PDF
# -------------------------
def gerar_pdf(times, nomes_times, grupoA, grupoB, jogosA, jogosB):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("OPEN VILLAGE 18+ - TORNEIO DE VÔLEI", styles["Title"]))
    elementos.append(Spacer(1, 12))

    # Times
    elementos.append(Paragraph("Times", styles["Heading2"]))
    for i, time in enumerate(times):
        elementos.append(Paragraph(f"<b>{nomes_times[i]}</b>", styles["Heading3"]))
        for jogador in time:
            elementos.append(Paragraph(f"- {jogador}", styles["Normal"]))
        elementos.append(Spacer(1, 10))

    # Grupos
    elementos.append(Paragraph("Grupos", styles["Heading2"]))

    elementos.append(Paragraph("Grupo A", styles["Heading3"]))
    for t in grupoA:
        elementos.append(Paragraph(t, styles["Normal"]))

    elementos.append(Spacer(1, 10))

    elementos.append(Paragraph("Grupo B", styles["Heading3"]))
    for t in grupoB:
        elementos.append(Paragraph(t, styles["Normal"]))

    elementos.append(Spacer(1, 10))

    # Jogos
    elementos.append(Paragraph("Jogos - Grupo A", styles["Heading2"]))
    for j in jogosA:
        elementos.append(Paragraph(f"{j[0]} vs {j[1]}", styles["Normal"]))

    elementos.append(Spacer(1, 10))

    elementos.append(Paragraph("Jogos - Grupo B", styles["Heading2"]))
    for j in jogosB:
        elementos.append(Paragraph(f"{j[0]} vs {j[1]}", styles["Normal"]))

    elementos.append(Spacer(1, 20))

    # Mata-mata
    elementos.append(Paragraph("Mata-Mata", styles["Heading2"]))
    elementos.append(Paragraph("Semi 1: 1º A vs 2º B", styles["Normal"]))
    elementos.append(Paragraph("Semi 2: 1º B vs 2º A", styles["Normal"]))
    elementos.append(Paragraph("Final: Vencedores das semis", styles["Normal"]))

    doc.build(elementos)
    buffer.seek(0)
    return buffer


# -------------------------
# BOTÃO
# -------------------------
if st.button("🎲 Sortear Torneio"):

    cabecas = [n.strip() for n in cabecas_input.split("\n") if n.strip()]
    mulheres = [n.strip() for n in mulheres_input.split("\n") if n.strip()]
    jogadores = [n.strip() for n in jogadores_input.split("\n") if n.strip()]

    # Validações
    if len(cabecas) != 6:
        st.error("Informe 6 cabeças de chave.")
        st.stop()

    if len(mulheres) != 6:
        st.error("Informe 6 mulheres.")
        st.stop()

    todos = cabecas + mulheres + jogadores
    if len(todos) != len(set(todos)):
        st.error("Existem nomes duplicados.")
        st.stop()

    random.shuffle(mulheres)
    random.shuffle(jogadores)

    # Criar times
    times = []
    nomes_times = []

    for i in range(6):
        time = [cabecas[i], mulheres[i]]
        times.append(time)
        nomes_times.append(f"Time {i+1}")

    # Distribuir jogadores
    i = 0
    while jogadores:
        times[i % 6].append(jogadores.pop(0))
        i += 1

    # Exibir times
    st.markdown("## 🏆 Times")
    for i, time in enumerate(times):
        st.markdown(f"### {nomes_times[i]}")
        for jogador in time:
            st.write(f"• {jogador}")

    # -------------------------
    # SORTEAR GRUPOS
    # -------------------------
    random.shuffle(nomes_times)

    grupoA = nomes_times[:3]
    grupoB = nomes_times[3:]

    st.markdown("## 🔵 Grupo A")
    for t in grupoA:
        st.write(t)

    st.markdown("## 🔴 Grupo B")
    for t in grupoB:
        st.write(t)

    # -------------------------
    # GERAR JOGOS DOS GRUPOS
    # -------------------------
    jogosA = gerar_jogos_grupo(grupoA)
    jogosB = gerar_jogos_grupo(grupoB)

    st.markdown("## 📅 Jogos - Grupo A")
    for j in jogosA:
        st.write(f"{j[0]} 🆚 {j[1]}")

    st.markdown("## 📅 Jogos - Grupo B")
    for j in jogosB:
        st.write(f"{j[0]} 🆚 {j[1]}")

    # -------------------------
    # MATA-MATA (ESTRUTURA)
    # -------------------------
    st.markdown("## 🏆 Mata-Mata")
    st.write("Semi 1: 1º A 🆚 2º B")
    st.write("Semi 2: 1º B 🆚 2º A")
    st.write("Final: vencedores das semifinais")

    # -------------------------
    # PDF
    # -------------------------
    pdf = gerar_pdf(times, nomes_times, grupoA, grupoB, jogosA, jogosB)

    st.download_button(
        label="📄 Baixar PDF",
        data=pdf,
        file_name="torneio_volei_grupos.pdf",
        mime="application/pdf"
    )