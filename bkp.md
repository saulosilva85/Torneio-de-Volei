import streamlit as st
import random
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

st.set_page_config(page_title="Torneio de Vôlei", layout="centered")

st.title("🏐 OPEN VILLAGE 30+ 🏐")

# Inputs
st.markdown("## 🔹 Cabeças de Chave (5 homens)")
cabecas_input = st.text_area("Digite 5 nomes")

st.markdown("## 🔹 Mulheres (5 obrigatórias)")
mulheres_input = st.text_area("Digite 5 nomes femininos")

st.markdown("## 🔹 Demais Jogadores")
jogadores_input = st.text_area("Digite os demais jogadores")


def gerar_tabela(times):
    lista = times[:]
    lista.append("FOLGA")

    n = len(lista)
    rodadas = []

    for rodada in range(n - 1):
        jogos = []
        for i in range(n // 2):
            t1 = lista[i]
            t2 = lista[n - 1 - i]

            if t1 != "FOLGA" and t2 != "FOLGA":
                jogos.append((t1, t2))

        rodadas.append(jogos)
        lista = [lista[0]] + [lista[-1]] + lista[1:-1]

    return rodadas


def gerar_pdf(times, nomes_times, tabela):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elementos = []

    # Título
    elementos.append(Paragraph("OPEN VILLAGE 18+ - TORNEIO DE VÔLEI", styles["Title"]))
    elementos.append(Spacer(1, 12))

    # Times
    elementos.append(Paragraph("Times Sorteados", styles["Heading2"]))

    for i, time in enumerate(times):
        elementos.append(Paragraph(f"<b>{nomes_times[i]}</b>", styles["Heading3"]))
        for jogador in time:
            elementos.append(Paragraph(f"- {jogador}", styles["Normal"]))
        elementos.append(Spacer(1, 10))

    # Jogos
    elementos.append(Paragraph("Tabela de Jogos", styles["Heading2"]))

    for i, rodada in enumerate(tabela):
        elementos.append(Paragraph(f"<b>Rodada {i+1}</b>", styles["Heading3"]))
        for jogo in rodada:
            elementos.append(Paragraph(f"{jogo[0]} vs {jogo[1]}", styles["Normal"]))
        elementos.append(Spacer(1, 10))

    doc.build(elementos)
    buffer.seek(0)

    return buffer


if st.button("🎲 Sortear e Gerar Tabela"):

    cabecas = [n.strip() for n in cabecas_input.split("\n") if n.strip()]
    mulheres = [n.strip() for n in mulheres_input.split("\n") if n.strip()]
    jogadores = [n.strip() for n in jogadores_input.split("\n") if n.strip()]

    # Validações
    if len(cabecas) != 5:
        st.error("Informe 5 cabeças de chave.")
        st.stop()

    if len(mulheres) != 5:
        st.error("Informe 5 mulheres.")
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

    for i in range(5):
        time = [cabecas[i], mulheres[i]]
        times.append(time)
        nomes_times.append(f"Time {i+1}")

    # Distribuir jogadores
    i = 0
    while jogadores:
        times[i % 5].append(jogadores.pop(0))
        i += 1

    # Exibir times
    st.markdown("## 🏆 Times")
    for i, time in enumerate(times):
        st.markdown(f"### {nomes_times[i]}")
        for jogador in time:
            st.write(f"• {jogador}")

    # Gerar tabela
    tabela = gerar_tabela(nomes_times)

    st.markdown("## 📅 Tabela de Jogos (Pontos Corridos)")
    for i, rodada in enumerate(tabela):
        st.markdown(f"### Rodada {i+1}")
        for jogo in rodada:
            st.write(f"{jogo[0]} 🆚 {jogo[1]}")

    # Gerar PDF
    pdf = gerar_pdf(times, nomes_times, tabela)

    # Botão de download
    st.download_button(
        label="📄 Baixar PDF",
        data=pdf,
        file_name="tabela_torneio_volei.pdf",
        mime="application/pdf"
    )