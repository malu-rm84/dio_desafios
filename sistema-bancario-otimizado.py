import textwrap

# Configuração dos tipos de conta
TIPOS_DE_CONTA = {
    "Amethist": {
        "limite_saques": 3, # limite de saques diários
        "limite_saque": 150, # valor máximo de saque
        "pode_exceder_saldo": False,
        "limite_negativo": 0, # não pode ficar negativo
        "beneficio": "Sem benefícios adicionais.",
        "taxa_saque": 0.02 # valor da taxa em cima do saque
    },
    "Sapphire": {
        "limite_saques": 5,
        "limite_saque": 500,
        "pode_exceder_saldo": True,
        "limite_negativo": 100,
        "beneficio": "Saque excedente de até R$ 100.",
        "taxa_saque": 0.01
    },
    "Ruby": {
        "limite_saques": 10,
        "limite_saque": 1000,
        "pode_exceder_saldo": True,
        "limite_negativo": 500,
        "beneficio": "Isenção de taxas em saques.",
        "taxa_saque": 0
    }
}

# Configuração menu inicial
def menu():
    menu = """\n
    ================  Obsidian Bank ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

# Configuração função depositar
def depositar(conta, valor):
    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n*** Operação falhou! O valor informado é inválido. ***")

# Configuração função sacar
def sacar(conta, valor):
    config = TIPOS_DE_CONTA[conta["tipo_conta"]]
    limite_saques = config["limite_saques"]
    limite_saque = config["limite_saque"]
    pode_exceder_saldo = config["pode_exceder_saldo"]
    limite_negativo = config["limite_negativo"]
    taxa_saque = config["taxa_saque"]

    excedeu_saldo = valor > conta["saldo"] and not pode_exceder_saldo
    excedeu_limite = valor > limite_saque
    excedeu_saques = conta["numero_saques"] >= limite_saques
    saldo_futuro = conta["saldo"] - valor - (valor * taxa_saque)
    excedeu_limite_negativo = saldo_futuro < -limite_negativo

    if excedeu_saldo:
        print("\n*** Operação falhou! Você não tem saldo suficiente. ***")
    elif excedeu_limite:
        print(f"\n*** Operação falhou! O valor do saque excede o limite de R$ {limite_saque:.2f}. ***")
    elif excedeu_saques:
        print(f"\n*** Operação falhou! Número máximo de saques ({limite_saques}) excedido. ***")
    elif excedeu_limite_negativo:
        print(f"\n*** Operação falhou! O saque excede o limite negativo permitido de R$ {-limite_negativo:.2f}. ***")
    elif valor > 0:
        taxa = valor * taxa_saque if taxa_saque > 0 else 0

        if taxa > 0:
            print(f"Taxa de saque ({taxa_saque * 100:.0f}%): R$ {taxa:.2f}")
            conta["saldo"] -= taxa
            conta["extrato"] += f"Taxa de saque: R$ {taxa:.2f}\n"

        conta["saldo"] -= valor
        conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
        conta["numero_saques"] += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n*** Operação falhou! O valor informado é inválido. ***")

# Configuração função extrato
def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not conta["extrato"] else conta["extrato"])
    print(f"\nSaldo:\tR$ {conta['saldo']:.2f}")
    print("==========================================")

# Configuração para criar usuário
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n*** Já existe usuário com esse CPF! ***")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\n=== Usuário criado com sucesso! Bem vindo ao Obsidian Bank! ===")


def filtrar_usuario(cpf, usuarios):
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)

# Configuração para vincular usuário à conta
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\n*** Usuário não encontrado! Fluxo de criação de conta encerrado. ***")
        return

    print("\nEscolha o tipo de conta:")
    print("[1] Conta Amethist")
    print("[2] Conta Sapphire")
    print("[3] Conta Ruby")

    opcao = input("=> ")

    tipos_conta = {"1": "Amethist", "2": "Sapphire", "3": "Ruby"}
    tipo_conta = tipos_conta.get(opcao)

    if not tipo_conta:
        print("\n*** Opção inválida. Conta não criada. ***")
        return

    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario,
        "tipo_conta": tipo_conta,
        "saldo": 0,
        "extrato": "",
        "numero_saques": 0
    }

    print("\n=== Conta criada com sucesso! ===")
    print(f"Número da Conta: {numero_conta}")
    print(f"Tipo de Conta: {tipo_conta}")
    print(f"Benefício: {TIPOS_DE_CONTA[tipo_conta]['beneficio']}")

    return conta


def listar_contas(contas):
    for conta in contas:
        config = TIPOS_DE_CONTA[conta["tipo_conta"]]
        linha = f"""\   
            Agência:\t{conta['agencia']}
            Nº da Conta:\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            Tipo:\t{conta['tipo_conta']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

# Configuração menu ações
def main():
    AGENCIA = "0001"

    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            if not contas:
                print("\n*** Nenhuma conta cadastrada. Crie uma conta primeiro. ***")
                continue

            numero_conta = int(input("Informe o número da conta: "))
            conta = next((conta for conta in contas if conta["numero_conta"] == numero_conta), None)

            if not conta:
                print("\n*** Conta não encontrada. ***")
                continue

            valor = float(input("Informe o valor do depósito: "))
            depositar(conta, valor)

        elif opcao == "s":
            if not contas:
                print("\n*** Nenhuma conta cadastrada. Crie uma conta primeiro. ***")
                continue

            numero_conta = int(input("Informe o número da conta: "))
            conta = next((conta for conta in contas if conta["numero_conta"] == numero_conta), None)

            if not conta:
                print("\n*** Conta não encontrada. ***")
                continue

            valor = float(input("Informe o valor do saque: "))
            sacar(conta, valor)

        elif opcao == "e":
            if not contas:
                print("\n*** Nenhuma conta cadastrada. Crie uma conta primeiro. ***")
                continue

            numero_conta = int(input("Informe o número da conta: "))
            conta = next((conta for conta in contas if conta["numero_conta"] == numero_conta), None)

            if not conta:
                print("\n*** Conta não encontrada. ***")
                continue

            exibir_extrato(conta)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Obrigado por confiar no Obsidian Bank. Até logo!")
            break


main()
