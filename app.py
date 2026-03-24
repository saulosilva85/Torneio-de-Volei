import random
import os

# ============================
# CONFIGURAÇÃO DE JOGADORES
# ============================

# Cabeças de chave (homens)
cabecas = ["João", "Carlos", "Marcos", "Roberto", "Alexandre"]

# Mulheres (não são cabeças de chave, mas devem ser distribuídas)
mulheres = ["Maria", "Ana", "Juliana", "Fernanda", "Camila"]

# Demais homens
homens_restantes = [
    "Pedro", "Lucas", "Rafael", "Tiago", "Bruno",
    "Felipe", "André", "Paulo", "Daniel", "Gustavo"
]

# ============================
# FUNÇÃO DE SORTEIO
# ============================

def sortear_times():
    # Cria 5 times vazios
    times = [[] for _ in range(5)]

    # Adiciona cabeças de chave (homens)
    for i in range(5):
        times[i].append(cabecas[i])

    # Embaralha mulheres e distribui (uma por time)
    mulheres_embaralhadas = random.sample(mulheres, len(mulheres))
    for i in range(5):
        times[i].append(mulheres_embaralhadas[i])

    # Embaralha homens restantes e distribui
    homens_embaralhados = random.sample(homens_restantes, len(homens_restantes))
    idx = 0
    for i in range(5):
        while len(times[i]) < 5:
            times[i].append(homens_embaralhados[idx])
            idx += 1

    return times

# ============================
# INTERFACE SIMPLES
# ============================

def mostrar_times(times):
    os.system("cls" if os.name == "nt" else "clear")
    print("===== TORNEIO DE VÔLEI - SORTEIO =====\n")
    for i, time in enumerate(times, start=1):
        print(f"Time {i}: {', '.join(time)}")
    print("\n======================================")

def main():
    while True:
        times = sortear_times()
        mostrar_times(times)

        opcao = input("\nDeseja refazer o sorteio? (s/n): ").strip().lower()
        if opcao != "s":
            print("\nBoa sorte aos times!")
            break

if __name__ == "__main__":
    main()