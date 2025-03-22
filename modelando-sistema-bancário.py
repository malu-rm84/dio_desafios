import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

# Configuração dos tipos de conta
TIPOS_DE_CONTA = {
    "Amethist": {
        "limite_saques": 3,  # limite de saques diários
        "limite_saque": 150,  # valor máximo de saque
        "pode_exceder_saldo": False,
        "limite_negativo": 0,  # não pode ficar negativo
        "beneficio": "Sem benefícios adicionais.",
        "taxa_saque": 0.02  # valor da taxa em cima do saque
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

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, tipo_conta):
        super().__init__(numero, cliente)
        self._tipo_conta = tipo_conta
        self._limite = TIPOS_DE_CONTA[tipo_conta]["limite_saque"]
        self._limite_saques = TIPOS_DE_CONTA[tipo_conta]["limite_saques"]
        self._pode_exceder_saldo = TIPOS_DE_CONTA[tipo_conta]["pode_exceder_saldo"]
        self._limite_negativo = TIPOS_DE_CONTA[tipo_conta]["limite_negativo"]
        self._taxa_saque = TIPOS_DE_CONTA[tipo_conta]["taxa_saque"]

    @classmethod
    def nova_conta(cls, cliente, numero, tipo_conta):
        return cls(numero, cliente, tipo_conta)

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques
        saldo_futuro = self.saldo - valor - (valor * self._taxa_saque)
        excedeu_limite_negativo = saldo_futuro < -self._limite_negativo

        if excedeu_limite:
            print(f"\n@@@ Operação falhou! O valor do saque excede o limite de R$ {self._limite:.2f}. @@@")

        elif excedeu_saques:
            print(f"\n@@@ Operação falhou! Número máximo de saques ({self._limite_saques}) excedido. @@@")

        elif not self._pode_exceder_saldo and valor > self.saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif excedeu_limite_negativo:
            print(f"\n@@@ Operação falhou! O saque excede o limite negativo permitido de R$ {-self._limite_negativo:.2f}. @@@")

        elif valor > 0:
            taxa = valor * self._taxa_saque if self._taxa_saque > 0 else 0

            if taxa > 0:
                print(f"Taxa de saque ({self._taxa_saque * 100:.0f}%): R$ {taxa:.2f}")
                self._saldo -= taxa
                self.historico.adicionar_transacao(Saque(taxa))

            self._saldo -= valor
            self.historico.adicionar_transacao(Saque(valor))
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            Tipo de Conta:\t{self._tipo_conta}
            Benefício:\t{TIPOS_DE_CONTA[self._tipo_conta]['beneficio']}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """\n
    ================ OBSIDIAN BANK ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def depositar(contas):
    numero_conta = int(input("Informe o número da conta: "))
    conta = next((conta for conta in contas if conta.numero == numero_conta), None)

    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    cliente = conta.cliente
    cliente.realizar_transacao(conta, transacao)

def sacar(contas):
    numero_conta = int(input("Informe o número da conta: "))
    conta = next((conta for conta in contas if conta.numero == numero_conta), None)

    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    cliente = conta.cliente
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(contas):
    numero_conta = int(input("Informe o número da conta: "))
    conta = next((conta for conta in contas if conta.numero == numero_conta), None)

    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n=== Usuário criado com sucesso! Bem vindo ao Obsidian Bank! ===")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    print("\nEscolha o tipo de conta:")
    print("[1] Conta Amethist")
    print("[2] Conta Sapphire")
    print("[3] Conta Ruby")

    opcao = input("=> ")

    tipos_conta = {"1": "Amethist", "2": "Sapphire", "3": "Ruby"}
    tipo_conta = tipos_conta.get(opcao)

    if not tipo_conta:
        print("\n@@@ Opção inválida. Conta não criada. @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta, tipo_conta=tipo_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")
    print(f"Número da Conta: {numero_conta}")
    print(f"Tipo de Conta: {tipo_conta}")
    print(f"Benefício: {TIPOS_DE_CONTA[tipo_conta]['beneficio']}")

def listar_contas(contas):
    for conta in contas:
        config = TIPOS_DE_CONTA[conta._tipo_conta]
        linha = f"""\
            Agência:\t{conta.agencia}
            Nº da Conta:\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Tipo:\t{conta._tipo_conta}
            Benefício:\t{config['beneficio']}
            Saldo:\t{conta.saldo:.2f}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(contas)

        elif opcao == "s":
            sacar(contas)

        elif opcao == "e":
            exibir_extrato(contas)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Obrigado por confiar no Obsidian Bank. Até logo!")
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

main()
