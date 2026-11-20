from pathlib import Path
from datetime import datetime
import csv

''' Criação do Arquivo:
    Nessa sessão o diretório é definido, criado (mkdir= make directory), criamos um caminho para o arquivo e criamos um sem sobrescrever utilizando o "exist_ok"
    O encoding="latin-1" é para garantir que o conteúdo do arquivo não seja corrompido ao ter seus bites decodificados por outros sistemas
    '''

#define o caminho baseado no Path.home() que retorna o local do usuário que esta rodando este arquivo, busca uma pasta chamada "Registro de Ocorrencias" e salva esse valor na variável Pasta
pasta = Path.home() / "Registro de Ocorrencias"
#cria a pasta da variável pasta caso não exista e o exist_ok=True evita erros caso ela ja exista
pasta.mkdir(parents=True, exist_ok=True)
#Monta o caminho para o arquivo
arquivo = pasta/"Ocorrencias.csv"
#Cria o arquivo vazio sem sobrescrever um ja existente
arquivo.touch(exist_ok=True)

Colunas = ["Categoria", "Protocolo", "Pessoa", "CPF","Descrição", "Local", "Data", "Status"]
CATEGORIAS_VALIDAS = ("Água", "Infraestrutura", "Saneamento")
STATUS_VALIDOS = ("Aberto", "Andamento", "Concluído")

''' 
Função que checa se o protocolo já existe dentro do arquivo 
'''
def protocolo_existe(protocolo):
    if not arquivo.exists():
        return False
    
    with arquivo.open("r", newline="", encoding="latin-1") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            if linha["Protocolo"] == str(protocolo):
                return True
    return False


'''
Função que cria um dicionário 'chamado' e escreve ele no arquivo

'''

Lista_Categorias = {'Água': [],
 'Infraestrutura': [],
  'Saneamento': []
  }

def criar_chamado(categoria, protocolo, pessoa, cpf, desc, local, data, status):

    if protocolo_existe(protocolo):
        return print(f"O chamado com o protocolo {protocolo} já existe!")
    
    categoria_formatada = categoria.strip().capitalize() #formata a chave categoria do dict chamado para que não tenha espaços e sempre com a primeira letra capitalizada.

    if categoria_formatada not in Lista_Categorias:
        print(f"Categoria '{categoria}' inválida!")
        return

    chamado = {
        "Categoria": categoria_formatada,
        "Protocolo": protocolo,
        "Pessoa": pessoa,
        "CPF": cpf, 
        "Descrição": desc, 
        "Local": local,
        "Data": data, 
        "Status": status
     }

    Lista_Categorias[categoria_formatada].append(chamado)

    #Checa na função se o arquivo existe ou se não tem nenhum byte para evitar cabeçalho duplicado
    arquivo_vazio = not arquivo.exists() or arquivo.stat().st_size == 0

    #Abre o arquivo de forma livre, o "a" significa append
    with arquivo.open("a", newline="", encoding="latin-1") as f:
        escritor = csv.DictWriter(f, fieldnames= Colunas)
        if arquivo_vazio:
            escritor.writeheader()
        escritor.writerow(chamado)

     
    return chamado

'''
Função para ler chamado, onde selecionamos o tipo de categoria que gostariamos de listar
'''

def ler_chamado():
    with arquivo.open("r", newline="", encoding="latin-1") as csvfile:
        linhas = list(csv.DictReader(csvfile))
    
    if not linhas:
        print("\nNenhum chamado cadastrado no arquivo ainda.")
        return

    print("\nQual valor deseja consultar?")
    opcao_todas_col = len(Colunas) + 1
    for numero_coluna, nome_coluna in enumerate(Colunas, start=1):
        print(f"[{numero_coluna}] - {nome_coluna}")
    print(f"[{opcao_todas_col}] - Todos os valores")

    escolha_ler = input(f"Escolha uma opção acima (1 a {opcao_todas_col}): ").strip()

    if not escolha_ler.isdigit() or not (1 <= int(escolha_ler) <= int(opcao_todas_col)):
        print(f"Opção {escolha_ler} é inválida.")
        return
    if escolha_ler == str(opcao_todas_col):
        for row in linhas:
            print("-" * 20)
            for chave, valor in row.items():
                print(f"{chave}: {valor}")
        return

    else:
        leitura_escolhida = Colunas[int(escolha_ler) - 1]
    encontrou = False

    match leitura_escolhida:
        case "Categoria":
            categorias = list(Lista_Categorias.keys())
            opcao_todas_cat = len(categorias) + 1

            print("\nQual Categoria gostaria de ler?")
            for num_cat, nome_cat in enumerate(categorias, start=1):
                print(f"[{num_cat}] - {nome_cat}")
            print(f"[{opcao_todas_cat}] - Todas as Categorias")

            ler_cat = input(f"Escolha um número acima (1 a {opcao_todas_cat}): ").strip()

            if ler_cat == str(opcao_todas_cat):
                for row in linhas:
                    print("-" * 20)
                    for chave, valor in row.items():
                        print(f"{chave}: {valor}")
                return

            elif ler_cat.isdigit() and 1 <= int(ler_cat) <= len(categorias):
                busca = categorias[int(ler_cat) - 1]

            else:
                print("Opção de categoria inválida!")
                return

    # Em versões anteriores, eu tinha feito mais de 8 cases, cada case com mais uns 4 switch. Ao limpar o código, notei que protocolo, CPF, Data e Status seguiam basicamente a mesma lógica
    # Então, juntei todos em um único case, retornando o valor de busca e futuramente, em um for loop que analiso linha por linha, busco qual valor que quero analisar e comparo com a busca que puxamos
    # quando condição se prova verdadeiro através da lógica booleana de que busca esta presente no valor da linha ou é exatemente igual ao valor da linha, printamos a fila/linha (row)            

        case "Protocolo" | "Data" | "Status": 
            # dict.fromkeys remove valores duplicados na listagem mantendo a ordem
            valores_disponiveis = list(dict.fromkeys(row[leitura_escolhida] for row in linhas if row[leitura_escolhida]))
            print(f"\nOpções disponíveis para {leitura_escolhida}:")
            for valor in valores_disponiveis:
                print(f"- {valor}")
            
            busca = input(f"\nDigite o(a) {leitura_escolhida} que deseja buscar: ").strip()

        case "Pessoa" | "Descrição" | "Local" | "CPF":
            valores_disponiveis = list(dict.fromkeys(row[leitura_escolhida] for row in linhas if row[leitura_escolhida]))
            print(f"\nRegistros atuais em {leitura_escolhida}: ")
            for valor in valores_disponiveis:
                print(f"- {valor}")

            busca = input(f"\nDigite parte ou nome completo de {leitura_escolhida}: ").strip()

    if not busca:
        print("\nA busca não pode ficar vazia.")
        return

    print(f"\nResultados para {leitura_escolhida}: '{busca}'")

    for row in linhas:
        valor_linha = str(row[leitura_escolhida]).strip().lower()

        if leitura_escolhida in ("Pessoa", "Descrição", "Local", "CPF"): #Isso faz com que busque o valor que esta presenta em leitura escolhida como uma busca parcial em pessoa, descrição e local, não sendo necessário digitar o nome completo
            condicao = busca.lower() in valor_linha
        else:
            condicao = busca.lower() == valor_linha

        if condicao:
            print("-" * 35)
            for chave, valor in row.items():
                print(f"{chave}: {valor}")
            encontrou = True

    if not encontrou:
        print(f"Nenhum chamado encontrado para {leitura_escolhida} = '{busca}'.")
        return
    return


def atualizar_chamado():

    consultar = input("\nDeseja consultar um chamado antes de seguirmos com a atualização?\n[1] - Sim\n[2]- Não, ja sei o protocolo\n")

    if consultar == "1":
        ler_chamado()
    
    protocolo = input("\nQual o protocolo que deseja atualizar?\nDigite o número do protocolo por extenso: ")

    if not protocolo_existe(protocolo):
        return print(f"O protocolo '{protocolo}' não existe!")

    print("\nQual coluna atualizaremos?")
    for numero_coluna, nome_coluna in enumerate(Colunas, start=1):
        print(f"[{numero_coluna}] - {nome_coluna}")
    
    escolha = input("Escolha uma opção acima (1 a 8): ").strip()

    if not escolha.isdigit() or not (1 <= int(escolha) <= len(Colunas)):
        print("Opção de ocorrência inválida!")
        return

    coluna_escolhida = Colunas[int(escolha) - 1]
    novo_valor = input(f"Atualize a coluna '{coluna_escolhida}': ").strip()

    if coluna_escolhida == "Categoria":
        novo_valor = novo_valor.capitalize()
        if novo_valor not in Lista_Categorias:
            print(f"Categoria '{novo_valor}' inválida!")
            return

    if coluna_escolhida == "Status":
        novo_valor = novo_valor.capitalize()
        if novo_valor not in ("Concluído", "Aberto", "Andamento"):
            print(f"Status '{novo_valor}' inválido!")
            return

    with arquivo.open("r", newline="", encoding="latin-1") as csvfile:
        reader = csv.DictReader(csvfile)
        linhas = list(reader)
        for row in linhas:
            if row["Protocolo"] == str(protocolo):
                row[coluna_escolhida] = novo_valor
                print(f'\nChamado {protocolo} atualizado com sucesso!')
                print("Dados atualizados: ", row)
                break

    with arquivo.open("w", newline="", encoding="latin-1") as csvfile:
        updater = csv.DictWriter(csvfile, fieldnames= Colunas)
        updater.writeheader()
        updater.writerows(linhas)


def deletar_chamado():
    with arquivo.open("r", newline="", encoding="latin-1") as csvfile:
        linhas = list(csv.DictReader(csvfile))

    if not linhas:
        print("\nO arquivo esta vazio. Não há chamados para deletar.")
        return

    print("\nProtocolos cadastrados:")
    for row in linhas:
        print(f" - {row['Protocolo']}: ({row['Pessoa']} - {row['Categoria']})")

    protocolo_alvo = input("\nDigite o Protocolo que deseja deletar: ").strip()

    confirmar = input(f"\nTem certeza que deseja deletar o protocolo {protocolo_alvo}? \n[S] - Sim\n[N] - Não\n").strip().capitalize()

    if confirmar == "N":
        print("\nNenhum protocolo foi deletado")
        return

    linhas_mantidas = [row for row in linhas if str(row["Protocolo"]).strip() != protocolo_alvo]

    if len(linhas_mantidas) == len(linhas):
        print(f"\nO protocolo {protocolo_alvo} não foi encontrado!")
        return

    with arquivo.open("w", newline="", encoding="latin-1") as csvfile:
        escritor = csv.DictWriter(csvfile, fieldnames=Colunas)
        escritor.writeheader()
        escritor.writerows(linhas_mantidas)

    print(f"\nO chamado de protocolo {protocolo_alvo} foi deletado com sucesso!")

    return

def gerar_proximo_protocolo():
    #Percorre todos os chamados nas categorias, encontra o maior protocolo e soma 1
    maior_protocolo = 0

    with arquivo.open("r", newline="", encoding="latin-1") as csvfile:
        reader = csv.DictReader(csvfile)
        lista_chamados = list(reader)
        for row in lista_chamados:
            #converte para int caso esteja salvo em string
            protocolo_atual = int(row["Protocolo"])
            if protocolo_atual > maior_protocolo:
                maior_protocolo = protocolo_atual
    
    return maior_protocolo + 1

def _validar_categoria(valor):
    cat_formatada = valor.capitalize()

    if cat_formatada == "Agua":
        cat_formatada = "Água"
        return True, cat_formatada

    if cat_formatada not in Lista_Categorias.keys():
        opcoes = ", ".join(Lista_Categorias.keys())
        return False, f"Categoria inválida. Escolha entre: {opcoes}."
    return True, cat_formatada


def _validar_cpf(valor):
    cpf_limpo = valor.replace(".", "").replace("-", "")
    if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
        return False, f"O CPF '{valor}' é inválido. Digite exatamente 11 números."
    cpf_formatado = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    return True, cpf_formatado


def _validar_data(valor):
    data_limpa = valor.replace("/", "")
    if not data_limpa.isdigit() or len(data_limpa) != 8:
        return False, f"'{valor}' é uma data inválida. Use o formato DD/MM/AAAA."
    data_formatada = f"{data_limpa[:2]}/{data_limpa[2:4]}/{data_limpa[4:]}"
    try:
        datetime.strptime(data_formatada, "%d/%m/%Y")
    except ValueError:
        return False, f"A data '{data_formatada}' não existe no calendário."
    return True, data_formatada


def _validar_status(valor):
    status_formatado = valor.capitalize()
    if status_formatado not in STATUS_VALIDOS:
        opcoes = ", ".join(STATUS_VALIDOS)
        return False, f"Status inválido. Escolha entre: {opcoes}."
    return True, status_formatado

VALIDADORES = {
    "Categoria": _validar_categoria,
    "CPF": _validar_cpf,
    "Data": _validar_data,
    "Status": _validar_status,
}


def validar_entrada(coluna, valor):
    valor = valor.strip()
    if not valor:
        return False, "O campo não pode ficar vazio."

    validador = VALIDADORES.get(coluna)
    if validador:
        return validador(valor)

    return True, valor

# TESTE CRIAÇÃO PREDEFINIDOS

def primeira_vez():

    arquivo_vazio = not arquivo.exists() or arquivo.stat().st_size == 0

    if not arquivo_vazio:
        return

    # Cenários de Água
    criar_chamado("Água", 123458, "Carlos Eduardo", "333.444.555-67", "Vazamento de água limpa na calçada", "Tatuapé", "12/11/2026", "Aberto")
    criar_chamado("Água", 123459, "Fernanda Lima", "444.555.666-78", "Baixa pressão de água nas torneiras", "Ipiranga", "13/11/2026", "Andamento")
    criar_chamado("Água", 123460, "Roberto Alves", "555.666.777-89", "Água saindo com coloração turva", "Santana", "13/11/2026", "Aberto")
    criar_chamado("Água", 123461, "Juliana Costa", "666.777.888-90", "Hidrômetro danificado vazando na rua", "Pinheiros", "14/11/2026", "Concluído")

    # Cenários de Infraestrutura
    criar_chamado("Infraestrutura", 123462, "Marcos Paulo", "777.888.999-01", "Calçada cedendo próximo ao ponto de ônibus", "Belém", "14/11/2026", "Aberto")
    criar_chamado("Infraestrutura", 123463, "Patrícia Souza", "888.999.000-12", "Poste de iluminação pública apagado", "Vila Mariana", "14/11/2026", "Andamento")
    criar_chamado("Infraestrutura", 123464, "Lucas Mendes", "999.000.111-23", "Asfalto afundando no cruzamento", "Penha", "15/11/2026", "Aberto")
    criar_chamado("Infraestrutura", 123465, "Aline Rocha", "101.202.303-44", "Sinalização de trânsito caída na via", "Lapa", "15/11/2026", "Concluído")

    # Cenários de Saneamento
    criar_chamado("Saneamento", 123466, "Ricardo Gomes", "202.303.404-55", "Bueiro entupido causando alagamento", "Itaquera", "15/11/2026", "Aberto")
    criar_chamado("Saneamento", 123467, "Camila Dias", "303.404.505-66", "Vazamento de esgoto a céu aberto", "Jabaquara", "15/11/2026", "Andamento")
    criar_chamado("Saneamento", 123468, "Felipe Nascimento", "404.505.606-77", "Mau cheiro forte vindo da galeria pluvial", "Casa Verde", "16/11/2026", "Aberto")
    criar_chamado("Saneamento", 123469, "Beatriz Martins", "505.606.707-88", "Tampa de poço de visita deslocada", "Butantã", "16/11/2026", "Concluído")


if __name__ == '__main__':

    primeira_vez()
    while True:
        Menu_Interação = input("\nEscolha uma operação para realizar:"
        "\n[1] - Criar chamado"
        "\n[2] - Ler Chamado"
        "\n[3] - Atualizar Chamado"
        "\n[4] - Deletar Chamado"
        "\n[5] - Sair do programa"
        "\nEscolha uma opção acima [1-5] ou [S] para sair: ").strip().upper()

        if Menu_Interação in ("S", "5"):
            print("Encerrando o programa.")
            break
        match Menu_Interação:
            case '1':
                valores_chamado = []
                for coluna in Colunas:
                    if coluna == "Protocolo":
                        novo_protocolo = gerar_proximo_protocolo()
                        print(f"\nProtocolo gerado automaticamente: {novo_protocolo}")
                        valores_chamado.append(novo_protocolo)
                        continue

                    if coluna == "Categoria":
                        print("\nOpções para Categorias:")
                        for cat_nome in Lista_Categorias.keys():
                            print(f"- {cat_nome}")

                    if coluna == "Status":
                        print("\nOpções para Status:")
                        for status_nome in STATUS_VALIDOS:
                            print(f"- {status_nome}")

                    while True:
                        entrada = input(f"\nInsira um valor para {coluna}: ")
                        valido, resultado = validar_entrada(coluna, entrada)
                        if valido:
                            valores_chamado.append(resultado)
                            break
                        print(f"\nErro: {resultado} Tente novamente.")

                chamado_criado = criar_chamado(*valores_chamado)
                if chamado_criado:
                    print("\nChamado registrado com sucesso:\n")
                    for chave, valor in chamado_criado.items():
                        print(f"{chave}: {valor}")
                continue

            case '2':
                ler_chamado()
                continue
            case '3':
                atualizar_chamado()
                continue
            case '4':
                deletar_chamado()
                continue
            case _:
                print("Opção inválida. Tente novamente.")
                continue