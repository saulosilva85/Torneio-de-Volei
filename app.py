import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times", layout="centered")

st.title("🏐 Torneio de Vôlei")

st.markdown("### Cabeças de Chave (Inserir de 2 a 6 jogadores)")
cabecas_input = st.text_area("Digite um nome por linha", height=120)

st.markdown("### Demais Jogadores")
jogadores_input = st.text_area("Digite um nome por linha", height=200)


# 🔎 Detecção de gênero (agora com suporte a "?")
def detectar_genero(nome):
    nome = nome.lower().strip()

    if "?" in nome:
        return "F"

    if nome.endswith("a"):
        return "F"
    elif nome.endswith(("o", "r", "l")):
        return "M"
    else:
        return random.choice(["M", "F"])


# 🔎 Separar por gênero
def separar_generos(lista):
    homens = []
    mulheres = []

    for nome in lista:
        genero = detectar_genero(nome)
        if genero == "M":
            homens.append(nome)
        else:
            mulheres.append(nome)

    return homens, mulheres


if st.button("🎲 Sortear Times"):
    cabecas = [c.strip() for c in cabecas_input.split("\n") if c.strip()]
    jogadores = [j.strip() for j in jogadores_input.split("\n") if j.strip()]

    # Validação cabeças
    if len(cabecas) < 2 or len(cabecas) > 6:
        st.error("Você deve inserir entre 2 e 6 cabeças de chave.")
        st.stop()

    num_times = len(cabecas)

    # 🔥 Validação TOTAL de jogadores
    total_necessario = num_times * 4
    total_atual = len(cabecas) + len(jogadores)

    if total_atual != total_necessario:
        st.error(f"Você precisa de exatamente {total_necessario} jogadores no total.")
        st.stop()

    # Separar por gênero
    cab_h, cab_m = separar_generos(cabecas)
    jog_h, jog_m = separar_generos(jogadores)

    todas_mulheres = cab_m + jog_m

    # 🚨 REGRA PRINCIPAL
    if len(todas_mulheres) != num_times:
        st.error(f"Deve haver exatamente {num_times} mulheres (1 por time).")
        st.stop()

    # Criar times
    times = {f"Time {i+1}": [] for i in range(num_times)}

    # 🔥 PASSO 1 — distribuir 1 mulher por time
    random.shuffle(todas_mulheres)

    for i in range(num_times):
        times[f"Time {i+1}"].append(todas_mulheres[i])

    # 🔥 PASSO 2 — adicionar cabeças de chave (sem repetir mulheres)
    cabecas_restantes = [c for c in cabecas if c not in todas_mulheres]

    random.shuffle(cabecas_restantes)

    for i in range(num_times):
        if len(times[f"Time {i+1}"]) < 4:
            times[f"Time {i+1}"].append(cabecas_restantes[i])

    # 🔥 PASSO 3 — completar com os demais jogadores
    restantes = [j for j in jogadores if j not in todas_mulheres]

    random.shuffle(restantes)

    i = 0
    for jogador in restantes:
        while True:
            time = f"Time {(i % num_times) + 1}"
            if len(times[time]) < 4:
                times[time].append(jogador)
                i += 1
                break
            i += 1

    st.success("Sorteio realizado com 1 mulher por time!")

    # Exibir resultado
    for time, integrantes in times.items():
        st.markdown(f"# 🏆 {time} ({len(integrantes)}/4)")
        for jogador in integrantes:
            st.write(f"• {jogador}")