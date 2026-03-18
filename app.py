import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times", layout="centered")

st.title("🏐 Torneio de Vôlei")

st.markdown("### Cabeças de Chave (Inserir de 2 a 6 jogadores)")
cabecas_input = st.text_area("Digite um nome por linha", height=120)

st.markdown("### Demais Jogadores")
jogadores_input = st.text_area("Digite um nome por linha", height=200)


# 🔎 Função simples de detecção de gênero
def detectar_genero(nome):
    nome = nome.lower().strip()

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
        st.warning(f"Atualmente você tem {total_atual}. Faltam {total_necessario - total_atual}.")
        st.stop()

    # Separar por gênero
    cab_h, cab_m = separar_generos(cabecas)
    jog_h, jog_m = separar_generos(jogadores)

    # Criar times
    times = {f"Time {i+1}": [] for i in range(num_times)}

    # Distribuir cabeças de chave
    cabecas_mix = cab_h + cab_m
    random.shuffle(cabecas_mix)

    for i in range(num_times):
        times[f"Time {i+1}"].append(cabecas_mix[i])

    # Embaralhar jogadores
    random.shuffle(jog_h)
    random.shuffle(jog_m)

    # 🔥 Distribuição controlada (máx 4 por time)
    def adicionar_jogadores(lista):
        i = 0
        for jogador in lista:
            tentativas = 0
            while tentativas < num_times:
                time = f"Time {(i % num_times) + 1}"

                if len(times[time]) < 4:
                    times[time].append(jogador)
                    i += 1
                    break

                i += 1
                tentativas += 1

    adicionar_jogadores(jog_h)
    adicionar_jogadores(jog_m)

    st.success("Sorteio realizado!")

    # Exibir resultado
    for time, integrantes in times.items():
        st.markdown(f"# 🏆 {time} ({len(integrantes)}/4)")
        for jogador in integrantes:
            st.write(f"• {jogador}")