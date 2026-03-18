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

    # 🔥 Base grande de nomes femininos (Brasil)
    nomes_femininos = {
        "maria","ana","julia","fernanda","patricia","camila","beatriz",
        "larissa","amanda","juliana","carla","paula","mariana","aline",
        "bruna","renata","leticia","sabrina","bianca","priscila","simone",
        "elaine","cristina","raquel","daniela","monica","luana","caroline",
        "karina","tatiane","fabiana","rosana","claudia","viviane","sheila",
        "sandra","andreia","debora","erika","flavia","gisele","helena",
        "isabela","joana","katia","luciana","michelle","natalia","olivia",
        "pamela","regina","silvia","tania","valeria","yasmin","luiza",
        "eduarda","gabriela","rafaela","milena","nicole","laura","alice",
        "manuela","heloisa","cecília","clarice","lorena","marcela","samara",
        "talita","vanessa","yara","zilda","bia","Re"
    }

    # 🔥 Regra forte: prioridade total
    if primeiro_nome in nomes_femininos:
        return "F"

    # 🔥 Heurística forte (Brasil)
    if nome.endswith(("a", "e")):
        return "F"

    if nome.endswith(("o", "r", "l", "s", "m")):
        return "M"

    # fallback seguro
    return "M"

    if primeiro_nome in nomes_femininos:
        return "F"

    if nome.endswith("a"):
        return "F"

    if nome.endswith(("o", "r", "l")):
        return "M"

    return "M"  # fallback seguro


if st.button("🎲 Sortear Times"):
    cabecas = [c.strip() for c in cabecas_input.split("\n") if c.strip()]
    jogadores = [j.strip() for j in jogadores_input.split("\n") if j.strip()]

    # Validação cabeças
    if len(cabecas) < 2 or len(cabecas) > 6:
        st.error("Você deve inserir entre 2 e 6 cabeças de chave.")
        st.stop()

    num_times = len(cabecas)

    # 🔥 Validação total jogadores
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
        st.error(f"É necessário pelo menos {num_times} mulheres para garantir 1 por time.")
        st.stop()

    # Criar times com cabeça fixa
    times = {f"Time {i+1}": [cabecas[i]] for i in range(num_times)}

    # 🔥 PASSO 1 — garantir 1 mulher por time (sem remover cabeça)
    mulheres_disponiveis = [m for m in mulheres if m not in cabecas]

    # Se alguma cabeça já for mulher, conta ela
    mulheres_por_time = {}

    for i in range(num_times):
        time = f"Time {i+1}"
        cabeca = cabecas[i]

        if detectar_genero(cabeca) == "F":
            mulheres_por_time[time] = 1
        else:
            mulheres_por_time[time] = 0

    random.shuffle(mulheres_disponiveis)

    for i in range(num_times):
        time = f"Time {i+1}"

        if mulheres_por_time[time] == 0:
            if not mulheres_disponiveis:
                st.error("Erro: não há mulheres suficientes para distribuir.")
                st.stop()

            times[time].append(mulheres_disponiveis.pop())

    # 🔥 PASSO 2 — adicionar restantes (sem duplicar)
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

    st.success("Sorteio realizado com 1 mulher por time e cabeça fixa!")

    # Exibir resultado
    for time, integrantes in times.items():
        st.markdown(f"# 🏆 {time} ({len(integrantes)}/4)")
        for jogador in integrantes:
            st.write(f"• {jogador}")