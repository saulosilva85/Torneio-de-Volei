import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times", layout="centered")

st.title("🏐 Torneio de Vôlei")

st.markdown("### Cabeças de Chave (Inserir de 2 a 6 jogadores)")
cabecas_input = st.text_area("Digite um nome por linha", height=120)

st.markdown("### Demais Jogadores")
jogadores_input = st.text_area("Digite um nome por linha", height=200)


# 🔎 Detecção MELHORADA
def detectar_genero(nome):
    nome = nome.lower().strip()
    primeiro_nome = nome.split()[0]

    # PRIORIDADE TOTAL
    if "?" in nome:
        return "F"

    # Base de nomes femininos comuns (expandida)
    nomes_femininos = {
        "maria","ana","julia","fernanda","patricia","camila",
        "beatriz","larissa","amanda","juliana","carla","paula",
        "mariana","aline","bruna","renata","leticia","sabrina",
        "Re","bia","biazinha"
    }

    if primeiro_nome in nomes_femininos:
        return "F"

    # Heurística
    if nome.endswith("a"):
        return "F"
    elif nome.endswith(("o", "r", "l")):
        return "M"
    else:
        return "M"  # fallback mais seguro


if st.button("🎲 Sortear Times"):
    cabecas = [c.strip() for c in cabecas_input.split("\n") if c.strip()]
    jogadores = [j.strip() for j in jogadores_input.split("\n") if j.strip()]

    if len(cabecas) < 2 or len(cabecas) > 6:
        st.error("Você deve inserir entre 2 e 6 cabeças de chave.")
        st.stop()

    num_times = len(cabecas)

    total_necessario = num_times * 4
    total_atual = len(cabecas) + len(jogadores)

    if total_atual != total_necessario:
        st.error(f"Você precisa de exatamente {total_necessario} jogadores no total.")
        st.stop()

    # 🔥 Separar por gênero
    todos = cabecas + jogadores

    mulheres = [n for n in todos if detectar_genero(n) == "F"]
    homens = [n for n in todos if detectar_genero(n) == "M"]

    # Criar times
    times = {f"Time {i+1}": [] for i in range(num_times)}

    # 🔥 REGRA PRINCIPAL → 1 mulher por time (se possível)
    random.shuffle(mulheres)

    if len(mulheres) >= num_times:
        for i in range(num_times):
            times[f"Time {i+1}"].append(mulheres[i])
        mulheres_restantes = mulheres[num_times:]
    else:
        # não tem mulheres suficientes
        for i in range(len(mulheres)):
            times[f"Time {i+1}"].append(mulheres[i])
        mulheres_restantes = []

    # 🔥 Adicionar cabeças restantes
    cabecas_restantes = [c for c in cabecas if c not in mulheres]
    random.shuffle(cabecas_restantes)

    for i, jogador in enumerate(cabecas_restantes):
        time = f"Time {(i % num_times) + 1}"
        if len(times[time]) < 4:
            times[time].append(jogador)

    # 🔥 Completar com todos os restantes
    restantes = [j for j in jogadores if j not in mulheres]
    restantes += mulheres_restantes

    random.shuffle(restantes)

    i = 0
    for jogador in restantes:
        tentativas = 0
        while tentativas < num_times:
            time = f"Time {(i % num_times) + 1}"

            if len(times[time]) < 4:
                times[time].append(jogador)
                i += 1
                break

            i += 1
            tentativas += 1

    st.success("Sorteio realizado com distribuição inteligente!")

    # Exibir resultado
    for time, integrantes in times.items():
        st.markdown(f"# 🏆 {time} ({len(integrantes)}/4)")
        for jogador in integrantes:
            st.write(f"• {jogador}")