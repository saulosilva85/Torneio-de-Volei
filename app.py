import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times", layout="centered")

st.title("🏐 Open Village 18+ 🏐")

st.markdown("### Cabeças de Chave (Inserir exatamente 5 jogadores - TODOS HOMENS)")
cabecas_input = st.text_area("Digite um nome por linha", height=120)

st.markdown("### Demais Jogadores")
jogadores_input = st.text_area("Digite um nome por linha", height=200)


# 🔎 Função de detecção de gênero (somente para jogadores)
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

    num_times = 5

    # ✅ Validação cabeças
    if len(cabecas) != num_times:
        st.error("Você deve inserir exatamente 5 cabeças de chave.")
        st.stop()

    # ✅ Validação total jogadores
    total_necessario = num_times * 4
    total_atual = len(cabecas) + len(jogadores)

    if total_atual != total_necessario:
        st.error(f"Você precisa de exatamente {total_necessario} jogadores no total.")
        st.stop()

    # 🚨 Validação duplicados
    todos_nomes = cabecas + jogadores
    if len(set(todos_nomes)) != len(todos_nomes):
        st.error("Existem nomes duplicados. Corrija antes de sortear.")
        st.stop()

    # 🔥 Mulheres APENAS dos jogadores
    mulheres_jogadores = [n for n in jogadores if detectar_genero(n) == "F"]

    # 🚨 Regra obrigatória
    if len(mulheres_jogadores) < num_times:
        st.error(f"É necessário pelo menos {num_times} mulheres nos jogadores.")
        st.stop()

    # 🔥 Criar times com cabeças (todos homens)
    times = {f"Time {i+1}": [cabecas[i]] for i in range(num_times)}

    # 🔥 PASSO 1 — colocar 1 mulher em cada time (obrigatório)
    random.shuffle(mulheres_jogadores)

    for i in range(num_times):
        time = f"Time {i+1}"
        mulher = mulheres_jogadores.pop()
        times[time].append(mulher)

    # 🔥 PASSO 2 — preencher restante
    usados = set()
    for jogadores_time in times.values():
        usados.update(jogadores_time)

    restantes = [j for j in jogadores if j not in usados]
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

    # 🔒 VALIDAÇÃO FINAL (garantia absoluta)
    for time, integrantes in times.items():
        if not any(detectar_genero(j) == "F" for j in integrantes):
            st.error(f"{time} ficou sem mulher. Revise os dados.")
            st.stop()

    st.success("Sorteio realizado com sucesso!")

    # 📊 Exibir resultado
    for time, integrantes in times.items():
        st.markdown(f"# 🏆 {time} ({len(integrantes)}/4)")
        for jogador in integrantes:
            st.write(f"• {jogador}")