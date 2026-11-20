# Projeto-Global_Solution---Neighborhood-Action-Dashboard
Projeto criado pelos alunos da FIAP para o desafio Neighborhood Action Dashboard que pede que criássemos uma plataforma que registra diversos tipos de ocorrências de infraestrutura em uma vizinhança hipotética ou com consentimento de pessoas reais.

README ProjetoGS

Integrantes: 
Felipe Barone Morales – RM 574357 
Thiago Simões – RM 576405
Manuela Mateus – RM 576139
Rafael de Almeida Irineu – RM 574613

Esse projeto foi criado com a mentalidade de realizar um CRUD, que consiste nas nomenclaturas CREATE, READ, UPDATE e DELETE. Sendo o básico para o estudante de computação que deseja criar seu primeiro banco de dados. Utilizamos essa inspiração dado ao fato que o pedido do projeto solicitava que criássemos chamados, lêssemos e atualizássemos o mesmo.

O código pode ser divido em três estruturas para compreende-lo de forma mais simples:

Começamos importando as bibliotecas para criação do diretório e listas necessários para que o programa tenha sua base criada, em seguida, temos a criação de funções e, por fim, a execução principal do código.

Primeira estrutura – Bibliotecas:

from pathlib import Path
From datetime import datetime
Import csv

Escolhemos o formato CSV pois é o mais universal para leituras de tabelas, CSV significa comma separeted value, ou seja, cada um dos valores é separado por vírgula e inserido em uma linha, formando assim uma matriz entre o cabeçalho de valores e os chamados que iremos armazenar nesse programa.

Ao utilizar o CSV, podemos utilizar o método .open() para ler o mesmo, adicionar ou reescrever. Como encoding utilizamos o latin-1 para conseguir utilizar ç, tio e acentuações comuns da língua portuguesa para facilitar leitura.

Form pathlib importPath:

A primeira biblioteca é a pathlib, basicamente ela é o nosso mapa e guia o programa através do computador do usuário que roda o mesmo.

ao utilizar o método Path.home(), basicamente indicamos para o programa onde fica a basta do usuário e, a partir disso, podemos construir o programa.

pasta.mkdir(parents=True, exist_ok=True), parents garante que o diretório tenha o caminho construído até ele e o exist_ok verifica se o arquivo foi criado, caso contrário, ele o cria sem sobrescrever sempre que o programa roda.

Arquivo.touch faz basicamente a mesma coisa que o mkdir, porém criando um arquivo.csv.

Após isso, para facilitar futuras buscas e referências, cria-se três listas:

Colunas, Categorias Válidas e Status Validos:

Colunas = ["Categoria", "Protocolo", "Pessoa", "CPF","Descrição", "Local", "Data", "Status"]
STATUS_VALIDOS = ("Aberto", "Andamento", "Concluído")
E, posteriormente 
Lista_Categorias = {'Água': [],
 'Infraestrutura': [],
  'Saneamento': []
  }

Esse último dicionário existe para separar cada chamado em sua respectiva categoria, basicamente adicionando um dicionário dentro de outro dicionário. Ele também é utilizado em funções como:
“ for cat_nome in Lista_Categorias.keys():
print(f"- {cat_nome}") ”

Cada coluna será posteriormente constantemente utilizada para comparar os valores dentro da planilha ou que o usuário deseja verificar dependendo da função chamada, como criar, ler ou atualizar chamado.

Segunda estrutura – Funções:

Cada função do programa é fundamentalmente dependente do arquivo.csv para seu funcionamento:

def protocolo_existe(protocolo)
Essa função primeiramente valida se o arquivo existe, caso contrário, retorna false.
Posteriormente, utilizamos a função de abrir o arquivo, ler, imprimir as linhas em uma variável chamada leitor e, com um for loop in leitor, verificamos se a coluna “Protocolo” é equivalente ao protocolo que inserimos como valor nessa função, caso seja, a função retorna True.

def criar_chamado(categoria, protocolo, pessoa, cpf, desc, local, data, status
)

É uma das funções principais do código, da qual chama a função protocolo existe, formata os valores de dentro da mesma comparando com a lista de categorias criadas na primeira estrutura e cria o dicionário “chamado” para ser agregado no dicionário de lista de categorias.
Realizamos mais uma verificação se o arquivo esta vazio ou se o bitesize dele esta nulo para a possibilidade do arquivo ter sido deletado enquanto o código roda e, posteriormente abrimos o arquivo, realizamos a função de append para não sobrescrever nenhuma linha, apenas adicionar e, caso o arquivo esteja vazio, escrevermos o cabeçalho dele novamente.

def ler_chamado():
A função mais extensa do código, ela primeiramente abre o arquivo, lê e armazena todos os valores de dentro do arquivo em uma lista chamada “linhas”.
Caso a lista esteja vazia, ele retorna que nenhum cadastro esta no arquivo ainda.
Nessa função, criamos um menu com o print(“\nQual valor deseja consultar?”) essa que pegamos o tamanho do número de colunas e adicionamos mais um para caso o usuário queira verificar a opção adicional de colunas, que são todas.
Posteriormente enumeramos a colunas e retornamos o valor do número e nome para leitura do usuário.

Com isso, “escolha_ler = input(f"Escolha uma opção acima (1 a {opcao_todas_col}): ").strip()” é um input do qual o usuário escolhe qual opção de leitura ele deseja verificar, se a escolha não for um dígito ou não estiver no range estipulado para leitura, o código retorna como inválido.

Caso o usuário selecione a última opção, o código apenas imprime todas as colunas, caso contrário, armazenamos o valor digitado nesse input, subtraímos um e pegamos o resultado para retornar como o index da lista “Colunas”, transformando assim o número selecionado em uma string representando as Keys da list Colunas.

Com isso, entramos em nosso primeiro Match Case para a variável leitura_escolhida:

Caso leitura_escolhida retorne “Categoria”, listamos as categorias, imprimimos uma lógica parecida com a da seleção de colunas e, ao validar se a coluna existe e, caso o usuário não selecione apenas a opção “todas as categorias”, que imprime todos os chamados novamente, podemos assim armazenar a categoria a nossa variável “busca”.

A variável busca será utilizada para comparar os valores da lista com os valores do input e, ao verificar que esse valor esta dentro ou é igual ao valor fornecido, nos retorna os chamados desejados.

Para case "Protocolo" | "Data" | "Status" e "Pessoa" | "Descrição" | "Local" | "CPF" a lógica é basicamente a mesma, a única coisa que muda é o input da variável “busca” para fazer um melhor sentido semântico.
Caso busca esteja vazia, o programa retorna um erro.
Criamos uma variável condição que segue duas lógicas: “in” para nomes, descrições e opções mais extensas que seria contraprodutivo escrever por completo, retornando assim apenas o valor dentro da string parcialmente. E também a lógica “==” que apenas verifica se a condição em caixa baixa é equivalente a leitura escolhida pelo usuário.

def atualizar_chamado():

Nessa função, primeiramente perguntamos pro usuário se ele deseja fazer uma consulta e, caso afirmativo, apenas puxamos a função ler_chamado() novamente.
Seguindo com isso, fazemos o usuário escolher exatamente o protocolo que deseja atualizar.
Ao selecionar o protocolo, o usuário escolhe uma lista de qual coluna exatamente ele deseja atualizar e armazena esses valores em uma variável chamada “novo_valor”.

Após validações de categoria e status para evitar erros, o programa armazena todos os chamados anteriores em uma lista temporária, procura o protocolo atual e substitui essa linha pelo novo valor e, posteriormente, reescreve o programa completamente com as mudanças realizadas nessa lista temporária.

def deletar_chamado():
Essa função é a mais simples, armazena todos os valores em uma lista temporária, pede pro usuário um protocolo específico, pergunta por validação e depois reescreve o programa do zero com exceção do protocolo específico do qual o usuário inseriu.

def gerar_proximo_protocolo():
Para gerar uma sensação de continuidade, essa função apenas lê o código, compara os valores da coluna protocolo e retorna o maior valor de protocolo mais um.

Posteriormente temos as funções:

def _validar_categoria(valor): Essa função valida se a formatação sem acento é valida e depois verifica se o valor formatado esta dentro da lista de categorias.

def _validar_cpf(valor): Essa função apenas limpa a variável valor removendo pontuações e traços de um CPF, verifica seu tamanho e se apenas dígitos foram fornecidos e depois retorna o CPF formatado corretamente.

def _validar_data(valor): Igual a função CPF, porém valida o tamanho da data e compara com o import datetime para verificar se a data é um formato válido e não, por exemplo, 99/99/9999.

def _validar_status(valor): Apenas verifica se o valor fornecido esta dentro da lista de status como Concluído, Aberto e Andamento.
Todas essas funções existiam em uma única função maior e não eficiente, com a ajuda do gemini para formata-la, conseguimos deixar os funcionamentos do programa mais dinâmico.

def validar_entrada(coluna, valor): Essa função une todas as validações anteriores em um dicionário criado: 
“VALIDADORES = {
    "Categoria": _validar_categoria,
    "CPF": _validar_cpf,
    "Data": _validar_data,
    "Status": _validar_status,
}”
Esse dicionário é chamado nessa função, pegamos os valores de cada um com a função .get() e, caso o validador retorne verdadeiro, a função segue sem problemas.

Por fim, a nossa última função:

def primeira_vez(): Essa função verifica se o arquivo existe no computador do usuário ao executar o programa pela primeira vez, após essa verificação, caso o arquivo exista ela apenas retorna e nada ocorre.
Caso o arquivo não exista ou tenha sido deletado, ela cria os cenários necessários pedidos no exercício:

Cenários Pré-definidos:
    
    #Cenários de Água
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

Esses cenários também foram criados com auxílio do Gemini.

Terceira Estrutura - __name__ == ‘__main__’

Por fim, realizamos uma verificação __name__ == ‘__main__’ para esse arquivo, assim rodando os programas principais, utilizamos essa comparação pois em um protótipo utilizando o Gemini, diferente do programa original, queríamos implementar uma versão desse código utilizando a biblioteca Customtkinter para criar uma interface “user-friendly”.
Essas interfaces user-friendly que são criadas usando VIBECODING, não pertencem a nossa proposta original do projeto e são apenas protótipos que gostaríamos de apresentar a faculdade.

Na verificação __main__, rodamos a função primeira vez e criamos um menu de interface que fica em looping até o usuário sair da mesma. Criamos um Match Menu_Interação para o case escolhido pelo usuário, onde:
1 - Cria um novo chamado que o usuário manualmente seleciona qual deseja; 
2 – invoca a função ler chamado;
3 – Invoca a função atualizar chamado;
4 – Invoca a função deletar chamado
‘_’ – case else, que retorna inválido.

e, se o usuário escolher “S” ou “5”, ele encerra o programa.




