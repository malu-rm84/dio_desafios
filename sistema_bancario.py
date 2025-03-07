# Função para exibir o menu principal e escolher o tipo de conta
def menu_principal():
    print("\n=== Obsidian Bank ===")
    print("Escolha o tipo de conta:")
    print("[1] Conta Amethist")
    print("[2] Conta Sapphire")
    print("[3] Conta Ruby")
    print("[q] Sair")
    return input("=> ")

# Função para exibir o menu de operações
def menu_operacoes():
    print("\n=== Menu de Operações ===")
    print("[d] Depositar")
    print("[s] Sacar")
    print("[e] Extrato")
    print("[q] Voltar ao menu anterior")
    return input("=> ")

# Função para escolher o tipo de conta
def escolher_tipo_conta():
    while True:
        opcao = menu_principal()
        if opcao == "1":
            return "Amethist"
        elif opcao == "2":
            return "Sapphire"
        elif opcao == "3":
            return "Ruby"
        elif opcao == "q":
            print("Obrigado por confiar no Obsidian Bank. Até logo!")
            exit()
        else:
            print("Opção inválida. Tente novamente.")

# Função para configurar cada tipo de conta
def configurar_conta(tipo_conta):
    if tipo_conta == "Amethist":
        return {
            "limite_saques": 3,
            "limite_saque": 150,
            "pode_exceder_saldo": False,  # Não pode ficar negativo
            "limite_negativo": 0,  # Saldo mínimo é 0
            "beneficio": "Sem benefícios adicionais.",
            "taxa_saque": 0.02  # Taxa de 2% sobre o valor sacado
        }
    elif tipo_conta == "Sapphire":
        return {
            "limite_saques": 5,
            "limite_saque": 500,
            "pode_exceder_saldo": True,  # Pode ficar negativo
            "limite_negativo": 100,  # Saldo mínimo é -100
            "beneficio": "Saque excedente de até R$ 100.",
            "taxa_saque": 0.01  # Taxa de 1% sobre o valor sacado
        }
    elif tipo_conta == "Ruby":
        return {
            "limite_saques": 10,
            "limite_saque": 1000,
            "pode_exceder_saldo": True,  # Pode ficar negativo
            "limite_negativo": 500,  # Saldo mínimo é -500
            "beneficio": "Isenção de taxas em saques.",  
            "taxa_saque": 0
        }

# Função principal
def main():
    print("Bem-vindo ao Obsidian Bank!")
    tipo_conta = escolher_tipo_conta()  # Escolhe o tipo de conta
    config = configurar_conta(tipo_conta)  # Configura as regras da conta
    saldo = 0
    extrato_entradas = ""  # Armazena as entradas (depósitos)
    extrato_saidas = ""    # Armazena as saídas (saques e taxas)
    numero_saques = 0

    print(f"\nVocê escolheu a Conta {tipo_conta}.")
    print(f"Benefício da conta: {config['beneficio']}")

    while True:
        opcao = menu_operacoes()  # Exibe o menu de operações

        # Depósito
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            if valor > 0:
                saldo += valor
                extrato_entradas += f"Depósito: R$ {valor:.2f}\n"
                print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
            else:
                print("Operação falhou! O valor informado é inválido.")

        # Saque
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            # Verifica se o saque excede o saldo (dependendo do tipo de conta)
            excedeu_saldo = valor > saldo and not config["pode_exceder_saldo"]
            # Verifica se o saque excede o limite por saque
            excedeu_limite = valor > config["limite_saque"]
            # Verifica se o número máximo de saques foi atingido
            excedeu_saques = numero_saques >= config["limite_saques"]
            # Verifica se o saldo ficará abaixo do limite negativo permitido
            saldo_futuro = saldo - valor - (valor * config["taxa_saque"])
            excedeu_limite_negativo = saldo_futuro < -config["limite_negativo"]

            if excedeu_saldo:
                print("Operação falhou! Você não tem saldo suficiente.")
            elif excedeu_limite:
                print(f"Operação falhou! O valor do saque excede o limite de R$ {config['limite_saque']:.2f}.")
            elif excedeu_saques:
                print(f"Operação falhou! Número máximo de saques ({config['limite_saques']}) excedido.")
            elif excedeu_limite_negativo:
                print(f"Operação falhou! O saque excede o limite negativo permitido de R$ {-config['limite_negativo']:.2f}.")
            elif valor > 0:
                # Calcula a taxa de saque (porcentagem sobre o valor sacado)
                taxa = valor * config["taxa_saque"]
                if config["taxa_saque"] > 0:
                    print(f"Taxa de saque ({config['taxa_saque'] * 100:.0f}%): R$ {taxa:.2f}")
                    saldo -= taxa
                    extrato_saidas += f"Taxa de saque: R$ {taxa:.2f}\n"

                saldo -= valor
                extrato_saidas += f"Saque: R$ {valor:.2f}\n"
                numero_saques += 1
                print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
            else:
                print("Operação falhou! O valor informado é inválido.")

        # Extrato
        elif opcao == "e":
            print("\n================ EXTRATO ================")
            print("Entradas (Depósitos):")
            print("Não houve entradas." if not extrato_entradas else extrato_entradas)
            print("\nSaídas (Saques e Taxas):")
            print("Não houve saídas." if not extrato_saidas else extrato_saidas)
            print(f"\nSaldo: R$ {saldo:.2f}")
            print("==========================================")

        # Voltar ao menu anterior
        elif opcao == "q":
            print("Voltando ao menu anterior...")
            break

        # Opção inválida
        else:
            print("Operação inválida. Por favor, selecione novamente a operação desejada.")

# Loop infinito
if __name__ == "__main__":
    while True:
        main()
