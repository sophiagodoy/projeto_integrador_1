# MENU
import sys # o que faz o código ser executado
import time # define funções de tempo
import pandas as pd # facilita a análise e manipulação de dados (planilhas, tabelas SQL)
import oracledb # permite a conexão com o banco de dados oracle 
import numpy as np # permite estruturas os dados em tabelas (linhas e colunas)

# CONEXÃO COM O ORACLE 
conexao = oracledb.connect( # estabelece a conexão com o banco de dados oracle 
    user="sys", # nome do usuário do banco de dados
    password="743274", # senha do banco de dados
    dsn="localhost/XEPDB1", # nome do banco de dados
    mode = oracledb.SYSDBA) # modo de conexão com o banco de dados
cursor = conexao.cursor() 
# utilizado para que os dados que foram adicionados diretamente no banco de dados possam ser mostrados no terminal do python, isso é feito através da variável 'cursor'   

# INÍCIO LOADING BAR 
def loading_bar():
    toolbar_width = 10
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1))
    for i in range(toolbar_width):
        time.sleep(0.10)  
        sys.stdout.write(".")
        sys.stdout.flush()
    sys.stdout.write("\n")
# FIM LOADING BAR

# DEFININDO A FUNÇÃO DA TABELA DO BANCO DE DADOS 
def data_bank ():
    cursor.execute("SELECT CÓDIGO_PRODUTO, NOME, DESCRICAO, CP, CF, CV, IV, ML FROM CADASTRO_PRODUTO")
    # esse comando, pede para o banco de dados selecionar algumas colunas da tabela cadastro_produto
    linhas = cursor.fetchall() 
    # usado para obter todas as linhas resultantes do comando executado no sql  
    # as linhas são armazenadas na variável 'linhas'

    # EXIBIR OS DADOS COM A COLUNA DESCRIPTOGRAFADA 
    for linha in linhas: # vê cada linha das colunas selecionadas 
        CÓDIGO_PRODUTO, NOME, DESCRICAO, CP, CF, CV, IV, ML = linha # cada elemento da tupla linha é atribuído a uma variável (um valor)
        info_descriptografada = descripto(DESCRICAO) # chama a função descripto
        print(f"ID: {CÓDIGO_PRODUTO}, Nome: {NOME}, Descricao: {info_descriptografada}, CP: {CP}, CF: {CF}, CV: {CV}, IV: {IV}, ML: {ML}")

# DEFININDO A CRIPTOGRAFIA E DESCRIPTOGRAFIA 
alfabeto = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 0}
# um dicionário que mapeia cada letra do alfabeto a um número específico

def criptografando(desc): # esta função recebe uma string desc como entrada e retorna a versão criptografada dessa string
    pal = desc.upper() # converte todas as letras da string desc para maiúscula
    matriz_pal = np.array([[],[]]) # inicializa uma matriz vazia
    main_matriz = np.array([[4,3],[1,2]]) # define a matriz principal
    if len(pal) %2 !=0:
        pal+='A' # se o comprimento da variável 'pal' for ímpar, adiciona 'A' ao final  
    matriz_pal = pal_em_matriz(pal) # chama a fução 
    pal = pal[:-1] # remove o último caractere adicionado ('A')
    pal_cripto = np.dot(main_matriz, matriz_pal) % 26 # multiplica as matrizes e aplica o módulo 26
    palavra_cripto = formando_palavra(pal_cripto) # converte a matriz criptografada de volta para palavra
    return palavra_cripto # retorna a palavra criptografada 
    
def descripto(a): # recebe uma string a como entrada, que é assumida como a string criptografada, e retorna a versão descriptografada dessa string
  pal_cripto = a.upper() # coverte a string para maiúsculo 
  matriz_pal_num= pal_em_matriz(pal_cripto) # chama a função
  determinante= 4*2-3*1 # calcula o determinante da matriz de criptografia
  chave_m_i = np.array([[2,-3],[-1,4]]) # define a matriz inversa da matriz de criptografia

  det_inversas = {1: 1, 3: 9, 5: 21, 7: 15, 9: 3, 11: 19, 15: 7, 17: 23, 19: 11, 21: 5, 23: 17, 25: 25}
  for chave, valor in det_inversas.items():
      if determinante == chave:
          determinante = valor
          break
  # este bloco verifica se o determinante da matriz de criptografia está presente no dicionário det_inversas e substitui o determinante pelo seu inverso modular correspondente

  chave_m_i *= determinante # multiplica a matriz inversa pelo determinante modificado
  matriz_pal_num = np.dot(chave_m_i, matriz_pal_num) # aplica a multiplicação da matriz inversa (chave_m_i) pela matriz numérica da string criptografada (matriz_pal_num)
  palavra_descripto = formando_palavra(matriz_pal_num) # chama a função
  return palavra_descripto # retorna a palavra descriptografada 
  
def pal_em_matriz(pal):
        letras = []
        matriz_pal_num = np.array([[], []]) # cria uma matriz vazia
        pal=pal.replace(" ", "") # remove todos os espaços em branco da string 'pal'
        for letra in range(len(pal)): # integra sobre cada caractere da string 'pal'
            for chave, valor in alfabeto.items():
                if pal[letra] == chave:
                    letras.append(valor) # se um caractere de pal corresponder a uma chave no dicionário alfabeto, seu valor correspondente é adicionado à lista letras
        for i in range(0, len(pal)-1, 2): # itera sobre a string pal em passos de dois caracteres 
            novaColuna = np.array([[letras[i]], [letras[i+1]]]) # para cada par de caracteres, cria uma nova coluna 
            matriz_pal_num = np.append(matriz_pal_num, novaColuna, axis=1) #  para adicionar essa nova coluna à matriz_pal_num
        return matriz_pal_num 

def formando_palavra(matriz_pal_num):
    palavra = '' # inicializa uma string vazia para armazenar a palavra descriptografada
    for i in range(matriz_pal_num.shape[1]): # itera sobre o número de colunas da matriz
        for j in range(matriz_pal_num.shape[0]): # itera sobre o número de linhas da matriz
            valor = matriz_pal_num[j, i] % 26 # obtém o valor na posição (j, i) da matriz e aplica mod 26
            for chave, val in alfabeto.items(): # itera sobre o dicionário 'alfabeto'
                if val == valor: # verifica se o valor do dicionário é igual ao valor obtido da matriz
                    palavra += chave # # concatena a chave (letra) correspondente à matriz na variável 'palavra'
    return palavra # retorna a palavra descriptografada

# COMEÇO DO PROGRAMA 
print(f"<--------------------CADASTRO DE PRODUTO-------------------->")
x = int(input('[1] Para cadastrar um novo produto: \n[2] Para alterar um produto: \n[3] Para apagar um produto: \n[4] Listar os produtos já cadastrados: \n[5] Sair:  '))
print("-"*61)     
if (x == 1):
    cod=int(input("\nDigite o código do produto: ")) 
    loading_bar()
    print("\nRegistrado com sucesso!")

    prod=str(input("\nDigite o nome do produto: "))
    loading_bar()
    print("\nRegistrado com sucesso!")

    desc=input("\nDigite a descrição do produto: ")
    loading_bar()
    print("\nRegistrado com sucesso!")

    CP=float(input("\nDigite o custo do produto em reais: "))
    loading_bar()
    print("\nRegistrado com sucesso!")

    CF=float(input("\nDigite o custo fixo em %: "))
    loading_bar()
    print("\nRegistrado com sucesso!")

    CV=float(input("\nDigite a comissão de venda em %: "))
    loading_bar()
    print("\nRegistrado com sucesso!")

    IV=float(input("\nDigite o valor dos impostos em %: "))
    loading_bar()
    print("\nRegistrado com sucesso!")

    ML=float(input("\nDigite o valor da rentabilidade em %: "))
    loading_bar()
    print("\nRegistrado com sucesso!")

    # CÁLCULOS FINANCEIROS
    PV=0 # preço de venda 
    PV=CP/(1-((CF+CV+IV+ML)/(100)))
    CA=(CP*100)/PV # custo de aquisição
    RB=PV-CP # receita bruta
    RBB=(RB*100)/PV # procentagem da receita bruta
    CFF=(PV/100)*CF # custos fixos
    CVV=(PV/100)*CV # custos variáveis 
    IVV=(PV/100)*IV # impostos variáveis 
    OC=((CFF)+(CVV)+(IVV)) # outros custos
    OCC=((CF)+(CV)+(IV)) # outros custos cumulativos
    ML=((RBB)-(OCC)) 
    MLL=((RB)-(OC)) # margem de lucro líquida 

    # CRIANDO A TABELA 
    df=pd.DataFrame({"Descrição":["Preco de venda","Custo de aquisicao(fornecedor)",
    "Receita bruta (A-B)","Custo fixo/Administrativo","Comissao de vendas","Impostos","Outros custos (D + E + F)",
    "Rentabilidade", ],
                    "Valor":[PV,CP,RB,CFF,CVV,IVV,OC,MLL],
                    "%":["100%",CA,RBB,CF,CV,IV,OCC,ML]})
    print(df)
    # o código cria um DataFrame (é um tipo de tabela de dados, onde os dados são organizados em linhas e colunas) utilizando a biblioteca Pandas em Python
    # essa DataFrame é construído a partir de um dicionário onde as chaves são os nomes das colunas e os valores são listas que representam os dados das colunas
    # -> na chave ‘descrição’ contém descrições das variáveis ou cálculos realizados
    # -> na chave ‘valor’ contém os valores correspondestes às variáveis ou cálculos que foram atribuídos anteriormente
    # -> na chave ‘%’ representa a porcentagem ou unidade associada a cada valor
    
    # DEFININDO A RENTABILIDADE 
    if ML > 20 and ML < 100:
        print("\nO produto se encontra na faixa de lucro ALTO.")
    elif ML > 10 and ML < 20:
        print("\nO produto se encontra na faixa de lucro MÉDIO.")
    elif ML > 0 and ML < 10:
        print("\nO produto se encontra na faixa de lucro BAIXO.")
    elif ML == 0:
        print("\nO produto se encontra em EQUILÍBRIO.")
    elif ML < 0:
        print("\nO produto se encontra em PREJUÍZO.")
    elif ML > 100:
        print("\nErro.")

    # CONFIRMANDO O REGISTRO DO NOVO PRODUTO
    y = int(input("Para registrar esse produto em definitivo digite [1]. Caso contrário, digite [2]: "))
    loading_bar()
    if (y == 1):
        palavra_cripto = criptografando(desc) # chama a função criptografando(desc)
        cursor.execute (f"INSERT INTO CADASTRO_PRODUTO (Código_produto,Nome,Descricao,cp,cf,cv,iv,ml) VALUES ({cod},'{prod}','{palavra_cripto}',{CP},{CF},{CV},{IV},{ML})")
        # executa um comando sql para inserir os dados do novo produto na tabela ‘cadastro_produto’
        conexao.commit()
        # confirma a transação para o banco de dados 
        print(f"\n\tO produto foi registrado!")
        loading_bar()
        data_bank() # chama a função para mostrar a tabela nova (tabela alterada)
    elif (y == 2):
        print(f"\n\tNenhum produto foi registrado.")

# ALTERAR PRODUTO 
elif (x == 2):
    loading_bar()
    data_bank()
    loading_bar()
    print(f"<----------------------------------------------------------->")
    z = int(input("[1] Para alterar o código: \n[2] Para alterar o nome: \n[3] Para alterar a descrição: \n[4] Para alterar o preço: \n[5] Para alterar o custo fixo: \n[6] Para alterar comissão de vendas: \n[7] Para alterar os impostos: \n[8] Para alterar a rentabilidade: "))
    print(f"<----------------------------------------------------------->")
    if (z == 1):
        loading_bar()
        y = int(input("Digite o código do produto que se quer alterar: "))
        loading_bar()
        cod = int(input("Digite o novo código do produto: "))
        cursor.execute (f"UPDATE CADASTRO_PRODUTO SET Código_produto = {cod} WHERE Código_Produto = {y}")
        conexao.commit()
        loading_bar()
        data_bank()
    elif(z == 2):
        loading_bar()
        y = int(input("Digite o código do produto que se quer alterar: "))
        loading_bar()
        prod = str(input("Digite o novo nome do produto: "))
        cursor.execute (f"UPDATE CADASTRO_PRODUTO SET Nome = '{prod}' WHERE Código_Produto = {y}")
        conexao.commit()
        loading_bar()
        data_bank()
    elif(z == 3):
        loading_bar()
        y = int(input("Digite o código do produto que se quer alterar: "))
        loading_bar()
        desc = str(input("Digite a nova descrição do produto: "))
        palavra_cripto = criptografando(desc)
        cursor.execute (f"UPDATE CADASTRO_PRODUTO SET Descricao = '{palavra_cripto}' WHERE Código_Produto = {y}")
        conexao.commit()
        loading_bar()
        data_bank()
    elif(z == 4):
        loading_bar()
        y = int(input("Digite o código do produto que se quer alterar: "))
        loading_bar()
        CP=float(input("Digite o novo custo do produto em reais: ")) 
        cursor.execute (f"UPDATE CADASTRO_PRODUTO SET cp = {CP} WHERE Código_Produto = {y}")
        conexao.commit()
        loading_bar()
        data_bank()
    elif(z == 5):
        loading_bar()
        y = int(input("Digite o código do produto que se quer alterar: "))
        loading_bar()
        CF=float(input("\nDigite o novo custo fixo em %: "))
        cursor.execute (f"UPDATE CADASTRO_PRODUTO SET cf = {CF} WHERE Código_Produto = {y}")
        conexao.commit()
        loading_bar()
        data_bank()
    elif(z == 6):
        loading_bar()
        y = int(input("Digite o código do produto que se quer alterar: "))
        loading_bar()
        CV=float(input("Digite a nova comissão de venda em %: "))
        cursor.execute (f"UPDATE CADASTRO_PRODUTO SET cf = {CV} WHERE Código_Produto = {y}")
        conexao.commit()
        loading_bar()
        data_bank()
    elif(z == 7):
        loading_bar()
        y = int(input("Digite o código do produto que se quer alterar: "))
        loading_bar()
        IV=float(input("Digite o novo valor dos impostos em %: "))
        cursor.execute (f"UPDATE CADASTRO_PRODUTO SET cf = {IV} WHERE Código_Produto = {y}")
        conexao.commit()
        loading_bar()
        data_bank()
    elif(z == 8):
        loading_bar()
        y = int(input("Digite o código do produto que se quer alterar: "))
        loading_bar()
        ML=float(input("Digite o novo valor da rentabilidade em %: "))
        cursor.execute (f"UPDATE CADASTRO_PRODUTO SET cf = {ML} WHERE Código_Produto = {y}")
        conexao.commit()
        loading_bar()
        data_bank()

# DELETAR PRODUTO
elif(x == 3):
    print(f"<----------------------------------------------------------->")
    data_bank()
    print(f"<----------------------------------------------------------->")
    cod=int(input("\nDigite o código do produto que se deseja deletar: ")) 
    pergunta = int(input(f"TEM CERTEZA QUE DESEJA APAGAR O PRODUTO DE CÓDIGO {cod}? SIM: [1] \nNÃO [2]: "))
    if(pergunta == 1):
        cursor.execute (f"DELETE FROM CADASTRO_PRODUTO WHERE Código_produto = {cod}")
        conexao.commit()
        loading_bar()
        data_bank()
    elif(pergunta == 2):
        sys.exit()

# PRODUTOS JÁ CADASTRADOS 
elif (x == 4):
    cursor = conexao.cursor()
    # # a variável cursor (que foi cria na conexão com o banco de dados) é utilizada para executar comandos no banco de dados e ser mostrada no python
    cursor.execute("SELECT * FROM CADASTRO_PRODUTO") # executada no banco de dados o comando que deseja, nesse caso, exibir a tabela
    var = cursor.fetchall() # vai guardar através da variável ‘var’ todos os elementos da tabela 
    conexao.commit() # confirma as alterações feitas 

    # CÁLCULOS FINANCEIROS 
    for i in var :
            cod, prod, desc, CP, CF, CV, IV, ML = i
            desc = descripto(desc) # chama a função descripto(desc)
            PV=0
            PV=CP/(1-((CF+CV+IV+ML)/(100)))
            CA=(CP*100)/PV
            RB=PV-CP
            RBB=(RB*100)/PV
            CFF=(PV/100)*CF
            CVV=(PV/100)*CV
            IVV=(PV/100)*IV
            OC=((CFF)+(CVV)+(IVV))
            OCC=((CF)+(CV)+(IV))
            ML=((RBB)-(OCC))
            MLL=((RB)-(OC))

            # CRIANDO A TABELA 
            df=pd.DataFrame({"Descrição":["Preco de venda","Custo de aquisicao(fornecedor)",
            "Receita bruta (A-B)","Custo fixo/Administrativo","Comissao de vendas","Impostos","Outros custos (D + E + F)",
            "Rentabilidade", ],
                            "Valor":[PV,CP,RB,CFF,CVV,IVV,OC,MLL],
                            "%":["100%",CA,RBB,CF,CV,IV,OCC,ML]})
            print(f"<----------------------------------------------------------->")
            print(f"\n{cod}             {prod}                {desc}\n\t{df}")

            # DEFININDO A RENTABILIDADE 
            if ML > 20 and ML < 100:
                print("\nO produto se encontra na faixa de lucro ALTO.")
            elif ML > 10 and ML < 20:
                print("\nO produto se encontra na faixa de lucro MÉDIO.")
            elif ML > 0 and ML < 10:
                print("\nO produto se encontra na faixa de lucro BAIXO.")
            elif ML == 0:
                print("\nO produto se encontra em EQUILÍBRIO.")
            elif ML < 0:
                print("\nO produto se encontra em PREJUÍZO.")
            elif ML > 100:
                print("\nErro.")
    print(f"<----------------------------------------------------------->")

# SAIR DO PROGRAMA 
elif(x == 5):
    sys.exit()