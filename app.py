import streamlit as st
import random
from openpyxl import Workbook
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
# GERAR JOGOS DO GRUPO
# -------------------------
def gerar_jogos_grupo(times):
    return [
        (times[0], times[1]),
        (times[0], times[2]),
        (times[1], times[2])
    ]


# -------------------------
# GERAR EXCEL
# -------------------------
def gerar_excel(times, nomes_times, grupoA, grupoB, jogosA, jogosB):
    wb = Workbook()

    # =========================
    # ABA 1 - TIMES
    # =========================
    ws1 = wb.active
    ws1.title = "Times"

    row = 1
    for i, time in enumerate(times):
        ws1.cell(row=row, column=1, value=nomes_times[i])
        row += 1
        for jogador in time:
            ws1.cell(row=row, column=2, value=jogador)
            row += 1
        row += 1

    # =========================
    # ABA 2 - GRUPOS
    # =========================
    ws2 = wb.create_sheet("Grupos")

    ws2["A1"] = "Grupo A"
    for i, t in enumerate(grupoA, start=2):
        ws2[f"A{i}"] = t

    ws2["C1"] = "Grupo B"
    for i, t in enumerate(grupoB, start=2):
        ws2[f"C{i}"] = t

    # =========================
    # ABA 3 - JOGOS
    # =========================
    ws3 = wb.create_sheet("Jogos")

    ws3["A1"] = "Grupo A"
    row = 2
    for j in jogosA:
        ws3.cell(row=row, column=1, value=j[0])
        ws3.cell(row=row, column=2, value="vs")
        ws3.cell(row=row, column=3, value=j[1])
        row += 1

    ws3["E1"] = "Grupo B"
    row = 2
    for j in jogosB:
        ws3.cell(row=row, column=5, value=j[0])
        ws3.cell(row=row, column=6, value="vs")
        ws3.cell(row=row, column=7, value=j[1])
        row += 1

    # =========================
    # ABA 4 - MATA-MATA
    # =========================
    ws4 = wb.create_sheet("Mata-Mata")

    ws4["A1"] = "Semi 1"
    ws4["A2"] = "1º A"
    ws4["A3"] = "2º B"

    ws4["C1"] = "Semi 2"
    ws4["C2"] = "1º B"
    ws4["C3"] = "2º A"

    ws4["E1"] = "Final"
    ws4["E2"] = "Vencedor Semi 1"
    ws4["E3"] = "Vencedor Semi 2"

    # Salvar em memória
    buffer = io.BytesIO()
    wb.save(buffer)
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

    # Sortear grupos
    random.shuffle(nomes_times)

    grupoA = nomes_times[:3]
    grupoB = nomes_times[3:]

    st.markdown("## 🔵 Grupo A")
    for t in grupoA:
        st.write(t)

    st.markdown("## 🔴 Grupo B")
    for t in grupoB:
        st.write(t)

    # Jogos
    jogosA = gerar_jogos_grupo(grupoA)
    jogosB = gerar_jogos_grupo(grupoB)

    st.markdown("## 📅 Jogos - Grupo A")
    for j in jogosA:
        st.write(f"{j[0]} 🆚 {j[1]}")

    st.markdown("## 📅 Jogos - Grupo B")
    for j in jogosB:
        st.write(f"{j[0]} 🆚 {j[1]}")

    # Mata-mata
    st.markdown("## 🏆 Mata-Mata")
    st.write("Semi 1: 1º A 🆚 2º B")
    st.write("Semi 2: 1º B 🆚 2º A")
    st.write("Final")

    # Excel
    excel = gerar_excel(times, nomes_times, grupoA, grupoB, jogosA, jogosB)

    st.download_button(
        label="📊 Baixar Excel",
        data=excel,
        file_name="torneio_volei.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )