import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times", layout="centered")

st.title("🏐 Torneio de Vôlei")

st.markdown("### Cabeças de Chave (Inserir de 2 a 6 jogadores)")
cabecas_input = st.text_area("Digite um nome por linha", height=120)

st.markdown("### Demais Jogadores")
jogadores_input = st.text_area("Digite um nome por linha", height=200)


# 🔎 Detecção simples (mantida)
def detectar_genero(nome):
    nome = nome.lower().strip()

    if nome.endswith("a"):
        return "F"
    elif nome.endswith(("o", "r", "l")):
        return "M"
    else:
        return random.choice(["M", "F"])


if st.button("🎲 Sortear Times"):
    cabecas = [c.strip() for c in cabecas_input.split("\n") if c.strip()]
    jogadores = [j.strip() for j in jogadores_input.split("\n") if j.strip()]

    # Validação cabeças
    if len(cabecas) < 2 or len(cabecas) > 6:
        st.error("Você deve inserir entre 2 e 6 cabeças de chave.")
        st.stop()

    num_times = len(cabecas)

    # Validação total jogadores
    total_necessario = num_times * 4
    total_atual = len(cabecas) + len(jogadores)

    if total_atual != total_necessario:
        st.error(f"Você precisa de exatamente {total_necessario} jogadores no total.")
        st.stop()

    # Separar todos
    todos = cabecas + jogadores

    mulheres = [n for n in todos if detectar_genero(n) == "F"]
    homens = [n for n in todos if detectar_genero(n) == "M"]

    # 🚨 REGRA: precisa ter pelo menos 1 mulher por time
    if len(mulheres) < num_times:
        st.error(f"É necessário pelo menos {num_times} mulheres (1 por time).")
        st.stop()

    # Criar times com cabeça fixa
    times = {f"Time {i+1}": [cabecas[i]] for i in range(num_times)}

    # 🔥 PASSO 1 — garantir 1 mulher por time
    mulheres_disponiveis = mulheres.copy()

    # Se cabeça já for mulher, conta
    for i in range(num_times):
        time = f"Time {i+1}"
        cabeca = cabecas[i]

        if detectar_genero(cabeca) == "F":
            mulheres_disponiveis.remove(cabeca)

    random.shuffle(mulheres_disponiveis)

    for i in range(num_times):
        time = f"Time {i+1}"
        cabeca = cabecas[i]

        # Se cabeça NÃO for mulher → adiciona uma
        if detectar_genero(cabeca) != "F":
            times[time].append(mulheres_disponiveis.pop())

    # 🔥 PASSO 2 — completar com restantes
    usados = set(sum(times.values(), []))
    restantes = [j for j in todos if j not in usados]

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

    st.success("Sorteio realizado!")

    # Exibir resultado
    for time, integrantes in times.items():
        st.markdown(f"# 🏆 {time} ({len(integrantes)}/4)")
        for jogador in integrantes:
            st.write(f"• {jogador}")