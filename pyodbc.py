# importando bibliotecas, caso não tenha use pip install pelo terminal e o nome da biblioteca.
import time as t
from click import clear
import pyodbc as p

# conexão com o banco de dados, sem autenticação

server = 'DESKTOP-J0U7P4K\SQLEXPRESS'
database = 'modelagem'

cnx = p.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_connection=yes;')
cursor = cnx.cursor()

# funcoes:

def valores():
    valor = '''
        SELECT * FROM vw_valor_final_oficina
    '''
    cursor.execute(valor)
    # executa o comando no SQL
    for linha in cursor.fetchall():
        print(linha)
    # quebra a linha para ficar mais organizado
    

def lista_clientes():
    cliente = '''
        SELECT * FROM cliente_oficina
    '''
    cursor.execute(cliente)
    for linha in cursor.fetchall():
        print(linha)


def lista_carro():
    carro = '''
        SELECT * FROM carro_oficina
    '''
    cursor.execute(carro)
    for linha in cursor.fetchall():
        print(linha)


def lista_cl_cr():
    cl_cr = '''
        SELECT * FROM vw_cliente_carro_oficina
    '''
    cursor.execute(cl_cr)
    for linha in cursor.fetchall():
        print(linha)


def lista_pedido():
    pedido = '''
        SELECT * FROM vw_pedido_oficina
    '''
    cursor.execute(pedido)
    for linha in cursor.fetchall():
        print(linha)


def lista_orcamento():
    lista = '''
        select * from vw_orcamento_oficina
    '''
    cursor.execute(lista)
    for linha in cursor.fetchall():
        print(linha)


def lista_peca():
    lista = '''
        select * from peca_oficina order by id_peca desc;
    '''
    cursor.execute(lista)
    for linha in cursor.fetchall():
        print(linha)


def cadastro_cliente():
    print('-' * 25, 'CADASTRO CLIENTE', '-' * 25)
    nomecl = str(input('Digite o Nome do(a) Cliente: '))
    sobrenomecl = str(input('Digite o Sobrenome do(a) Cliente: '))
    cep = str(input('Digite o CEP do(a) Cliente: '))
    
    # variaveis para executar um store procedure nalinha seguinte
    
    inserircl = '''
       exec sp_cadastro_cliente_oficina '{}', '{}', '{}';
    '''.format(nomecl, sobrenomecl, cep)
    cursor.execute(inserircl)
    cursor.commit()
    clear()   
    print('cliente cadastrado!')
    t.sleep(2)


def cadastro_carro():
    print('-' * 25, 'CADASTRO AUTOMÓVEL', '-' * 25)
    placa = str(input('Digite a placa do automóvel:'))
    modelo = str(input('Digite o modelo do automóvel:'))
    marca = str(input('Digite a marca do automóvel:'))
    ano = str(input('Digite a data do automóvel:'))
    if ano == '':
        ano = 'n/a'
    inserir_aut = '''
        EXEC sp_cadastro_carro_oficina '{}','{}','{}','{}'
    '''.format(placa, modelo, marca, ano)
    cursor.execute(inserir_aut)
    cursor.commit()
    print('Atuomóvel inserido.')
    t.sleep(2)


def cadastro_cr_cl():
    cliente = '''
        SELECT id_cliente, nome, sobrenome FROM cliente_oficina
    '''
    cursor.execute(cliente)
    for linha in cursor.fetchall():
        print(linha)
    print('\nId do CLiente - Nome do Cliente.')
    input('\nAperte Enter para continuar: ')
    carro = '''
        SELECT id_carro, placa, modelo FROM carro_oficina
    '''
    cursor.execute(carro)
    for linha in cursor.fetchall():
        print(linha)
    print('\nId do Carro - Placa - Modelo.')
    input('\nAperte Enter para continuar: ')
    idcliente = int(input('\n digite o id do(a) cliente:'))
    idcarro = int(input('\n digite o id do carro:'))
    inserir = '''
        insert into cliente_carro values({},{})
    '''.format(idcliente, idcarro)
    cursor.execute(inserir)
    cursor.commit()
    clear()
    print('Dados inseridos!')
    t.sleep(2)


def cadastro():

    cadastro_cliente()
    clear()
    cadastro_carro()
    clear()
    cadastro_cr_cl()


def cadastro_orcamento():
    resp = "s"
    while resp != "n":
        clear()
        print('-' * 25, 'CADASTRO ORÇAMENTO', '-' * 25)
        id_carro = int(input('Digite o Id do carro para orçamento: '))
        id_peca = int(input('Digite o Código da peça: '))
        qty = int(input('Digite a quantidade desta peça: '))
        lista = '''
            exec sp_cadastro_orcamento_oficina {},{},{};
        '''.format(id_carro, id_peca, qty)
        cursor.execute(lista)
        cursor.commit()
        clear()
        print('\nOrçamento inserido')
        resp = input('Deseja inserir novamente(s/n):')


def cadastro_peca():
    resp = "s"
    while resp != "n":
        clear()
        print('-' * 50, 'CADASTRO PEÇA', '-' * 50)
        nome = input('Digite o nome da peça: ')
        valor = float(input('Digite o Valor unitário: '))
        inserir = '''
            exec sp_cadastro_peca_oficina {},{}
        '''.format(nome, valor)
        cursor.execute(inserir)
        cursor.commit()
        clear()
        print('\nPeça inserida!')
        resp = str(input('Deseja inserir outra peça(s/n): '))


def cadastro_pedido():
    print('-' * 50, 'CADASTRO PEDIDO', '-' * 50)
    id_cliente = int(input('Digite o id do cliente: '))
    id_carro = int(input('Digite o id do carro: '))
    inserir = '''
        exec sp_cadastro_pedido_oficina {},{};
    '''.format(id_cliente, id_carro)
    cursor.execute(inserir)
    cursor.commit()
    clear()
    print('Pedido Cadastrado!')
    t.sleep(2)


def cadastro_venda():
    resp = 's'
    while resp != 'n':
        clear()
        id_pedido = int(input('Digite o número do pedido: '))
        id_orcamento = int(input('Digite o id do orçamento: '))
        inserir = '''
           insert into venda_oficina values ({}, {});
        '''.format(id_pedido, id_orcamento)
        cursor.execute(inserir)
        cursor.commit()
        clear()
        print('\n Relação feita!')
        resp = str(input('Deseja adicionar outro orçamento neste pedido(s/n): '))


# menu via terminal:
op = -1
up = -1
while op != 0 or up != 0:

    logo = '''
  ______    _______  __    ______  __  .__   __.      ___      
 /  __  \  |   ____||  |  /      ||  | |  \ |  |     /   \     
|  |  |  | |  |__   |  | |  ,----'|  | |   \|  |    /  ^  \    
|  |  |  | |   __|  |  | |  |     |  | |  . `  |   /  /_\  \   
|  `--'  | |  |     |  | |  `----.|  | |  |\   |  /  _____  \  
 \______/  |__|     |__|  \______||__| |__| \__| /__/     \__\ 
                                                               
    '''
    menu = '''
    {}
    Selecione uma opção para continuar:
        
        0 - Encerrar.
        1 - Listar Vendas.
        2 - Listar Clientes.
        3 - Listar Carros.
        4 - Listar Clientes x Carro.
        5 - Listar Pedidos.
        6 - Listar Orçamento.
        7 - Listar Peças.
    '''.format(logo)
    menu_cadastro = '''
    {}
    Selecione uma opção para continuar:
        
        0 - Encerrar.
        1 - Cadastrar Cliente.
        2 - Cadastrar Carro.
        3 - Cadastrar Cliente e o Carro.
        4 - Relacionar Cliente e o Carro.
        5 - Cadastrar Orçamento[loop]
        6 - Cadastrar Peças.
        7 - Cadastrar Pedido.
        8 - Relacionar Pedido e o Orçamento. 
    '''.format(logo)

    clear()

    print('{}Selecione uma opção:\n(1-listar / 2-Cadastrar / 0 - Sair)'.format(logo))
    print('\nDica: cadastre cliente e carro, faça a relação, orçamento, pedido e relacione pedido e orçamento.\n')
    resposta = int(input('Digite sua opção: '))

    if resposta == 1:
        clear()
        print(menu)
        op = int(input('Digite sua opção: '))

    if resposta == 2:
        clear()
        print(menu_cadastro)
        up = int(input('Digite sua opção:'))

   # Sessão de Condições:
    if op == 0 or up == 0 or resposta == 0:
        clear()
        print('Sistema Finalizado!')
        t.sleep(2)
        break

    # Lista:
    if op == 1:
        clear()
        valores()
        print('\n Id Pedido - Nome - Placa - Valor Total')
        input('\nAperte Enter para continuar: ')

    if op == 2:
        clear()
        lista_clientes()
        print('\n Id Cliente - Nome - CEP')
        input('\nAperte Enter para continuar: ')

    if op == 3:
        clear()
        lista_carro()
        print('\n Id Carro - Modelo - Marca - Ano')
        input('\nAperte Enter para continuar: ')

    if op == 4:
        clear()
        lista_cl_cr()
        print('\n Id Cliente - Nome - Id Carro - Placa - Modelo')
        input('\nAperte Enter para continuar: ')

    if op == 5:
        clear()
        lista_pedido()
        print('\n Id Pedido - Nome - Placa.')
        input('\nAperte Enter para continuar: ')

    if op == 6:
        clear()
        lista_orcamento()
        print('\nId orçamento - Placa - Peça - Quantidade')
        input('\nAperte Enter para continuar: ')

    if op == 7:
        clear()
        lista_peca()
        print('\n ID Peça - Nome - Valor unidade.')
        input('\nAperte Enter para continuar: ')

    # Cadastro a finalizar ainda:
    if up == 1:
        clear()
        cadastro_cliente()

    if up == 2:
        clear()
        cadastro_carro()

    if up == 3:
        clear()
        cadastro()

    if up == 4:
        clear()
        cadastro_cr_cl()

    if up == 5:
        clear()
        cadastro_orcamento()

    if up == 6:
        clear()
        cadastro_peca()

    if up == 7:
        clear()
        cadastro_pedido()

    if up == 8:
        clear()
        cadastro_venda()

    t.sleep(1)
    clear()
