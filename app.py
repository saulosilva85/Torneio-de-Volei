import streamlit as st
import random

st.set_page_config(page_title="Sorteio de Times", layout="centered")

st.title("🏐 Open Village 18+ 🏐")

st.markdown("### Cabeças de Chave (Inserir exatamente 5 jogadores homens)")
cabecas_input = st.text_area("Digite um nome por linha", height=120)

st.markdown("### Demais Jogadores")
jogadores_input = st.text_area("Digite um nome por linha", height=200)


# 🔎 Função de detecção de gênero (apenas para os demais jogadores)
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

    # ✅ Validação cabeças
    if len(cabecas) != 5:
        st.error("Você deve inserir exatamente 5 cabeças de chave (homens).")
        st.stop()

    num_times = 5

    # ✅ Validação total jogadores
    total_necessario = num_times * 4
    total_atual = len(cabecas) + len(jogadores)

    if total_atual != total_necessario:
        st.error(f"Você precisa de exatamente {total_necessario} jogadores no total (20).")
        st.stop()

    # 🚨 Validação de nomes duplicados
    todos_nomes = cabecas + jogadores
    if len(set(todos_nomes)) != len(todos_nomes):
        st.error("Existem nomes duplicados. Corrija antes de sortear.")
        st.stop()

    # 🔥 Separar mulheres e homens
    mulheres_jogadores = [n for n in jogadores if detectar_genero(n) == "F"]
    homens_jogadores = [n for n in jogadores if detectar_genero(n) == "M"]

    # 🚨 Regra obrigatória
    if len(mulheres_jogadores) < num_times:
        st.error("É necessário pelo menos 5 mulheres (1 por time).")
        st.stop()

    # 🔥 Criar times com cabeças fixos
    times = {f"Time {i+1}": [cabecas[i]] for i in range(num_times)}

    # 🔥 PASSO 1 — Garantir uma mulher em cada time
    random.shuffle(mulheres_jogadores)
    mulheres_selecionadas = mulheres_jogadores[:num_times]  # exatamente 5 mulheres
    restantes = homens_jogadores + mulheres_jogadores[num_times:]  # sobra de homens + mulheres excedentes
    random.shuffle(restantes)

    for i in range(num_times):
        time = f"Time {i+1}"
        times[time].append(mulheres_selecionadas[i])

    # 🔥 PASSO 2 — Preencher restantes sem duplicar
    idx = 0
    for time in times:
        while len(times[time]) < 4 and idx < len(restantes):
            times[time].append(restantes[idx])
            idx += 1

    # 🚨 Garantia final: nenhum nome duplicado
    usados = []
    for integrantes in times.values():
        usados.extend(integrantes)
    if len(usados) != len(set(usados)):
        st.error("Erro interno: houve duplicação de nomes. Verifique os dados inseridos.")
        st.stop()

    st.success("Sorteio realizado com sucesso!")

    # 📊 Exibir resultado
    for time, integrantes in times.items():
        st.markdown(f"# 🏆 {time} ({len(integrantes)}/4)")
        for jogador in integrantes:
            st.write(f"• {jogador}")