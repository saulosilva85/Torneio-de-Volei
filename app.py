if st.button("🎲 Sortear Times"):
    cabecas = [c.strip() for c in cabecas_input.split("\n") if c.strip()]
    jogadores = [j.strip() for j in jogadores_input.split("\n") if j.strip()]

    # ✅ Validação cabeças
    if len(cabecas) < 2 or len(cabecas) > 6:
        st.error("Você deve inserir entre 2 e 6 cabeças de chave.")
        st.stop()

    num_times = len(cabecas)

    # ✅ Validação total jogadores
    total_necessario = num_times * 4
    total_atual = len(cabecas) + len(jogadores)

    if total_atual != total_necessario:
        st.error(f"Você precisa de exatamente {total_necessario} jogadores no total.")
        st.stop()

    # 🔥 Separar todos
    todos = cabecas + jogadores

    mulheres = [n for n in todos if detectar_genero(n) == "F"]
    homens = [n for n in todos if detectar_genero(n) == "M"]

    # 🚨 REGRA OBRIGATÓRIA
    if len(mulheres) < num_times:
        st.error(f"É necessário pelo menos {num_times} mulheres (1 por time).")
        st.stop()

    random.shuffle(mulheres)
    random.shuffle(homens)

    # 🔥 Criar times
    times = {f"Time {i+1}": [] for i in range(num_times)}

    # 🔥 PASSO 1 — garantir 1 mulher por time (OBRIGATÓRIO)
    for i in range(num_times):
        time = f"Time {i+1}"
        mulher = mulheres.pop()
        times[time].append(mulher)

    # 🔥 PASSO 2 — adicionar cabeças de chave
    for i, cabeca in enumerate(cabecas):
        time = f"Time {i+1}"

        # evita duplicar se cabeça já foi usada como mulher
        if cabeca not in times[time]:
            times[time].append(cabeca)

    # 🔥 PASSO 3 — juntar restantes
    restantes = mulheres + homens

    # remover duplicados já usados
    usados = set(sum(times.values(), []))
    restantes = [j for j in restantes if j not in usados]

    random.shuffle(restantes)

    # 🔥 PASSO 4 — completar times até 4 jogadores
    for jogador in restantes:
        for time in times:
            if len(times[time]) < 4:
                times[time].append(jogador)
                break

    # 🚨 VALIDAÇÃO FINAL (garantia absoluta)
    for time, integrantes in times.items():
        if not any(detectar_genero(j) == "F" for j in integrantes):
            st.error(f"Erro: {time} ficou sem mulher. Refazer sorteio.")
            st.stop()

    st.success("Sorteio realizado com sucesso!")

    # 📊 Exibir resultado
    for time, integrantes in times.items():
        st.markdown(f"# 🏆 {time} ({len(integrantes)}/4)")
        for jogador in integrantes:
            st.write(f"• {jogador}")