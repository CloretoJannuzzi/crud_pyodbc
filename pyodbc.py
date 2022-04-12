import time as t
from click import clear
import pyodbc as p

# Em desenvolvimento.
# [] criar uma view para a tabela cliente_x_carro para ser mais legivel.

# conexão com o banco de dados, sem autenticação
server = 'DESKTOP-J0U7P4K\SQLEXPRESS'
database = 'modelagem'
cnx = p.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_connection=yes;')
cursor = cnx.cursor()

# funcoes:


def valores():
    valor = '''
        SELECT * FROM vw_valor_oficina
    '''
    cursor.execute(valor)
    for linha in cursor.fetchall():
        print(linha)


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
        SELECT * FROM cliente_carro
    '''
    cursor.execute(cl_cr)
    for linha in cursor.fetchall():
        print(linha)


def lista_pedido():
    pedido = '''
        SELECT * FROM pedido_oficina
    '''
    cursor.execute(pedido)
    for linha in cursor.fetchall():
        print(linha)


def lista_orcamento():
    lista = '''
        select * from orcamento_oficina order by id_orcamento desc;
    '''
    cursor.execute(lista)
    for linha in cursor.fetchall():
        print(linha)


def cadastro_cliente():
    print('-' * 25, 'CADASTRO CLIENTE', '-' * 25)
    nomecl = str(input('Digite o Nome do(a) Cliente: '))
    sobrenomecl = str(input('Digite o Sobrenome do(a) Cliente: '))
    cep = str(input('Digite o CEP do(a) Cliente: '))
    inserircl = '''
       exec sp_cadastro_cliente_oficina '{}', '{}', '{}';
    '''.format(nomecl, sobrenomecl, cep)
    cursor.execute(inserircl)
    cursor.commit()


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
    input(':')


def cadastro_cr_cl():
    cliente = '''
        SELECT id_cliente, nome, sobrenome FROM cliente_oficina order by id_cliente desc;
    '''
    cursor.execute(cliente)
    for linha in cursor.fetchall():
        print(linha)
    print('Id do CLiente; Nome do Cliente.')
    input(':')
    carro = '''
        SELECT id_carro, placa, modelo FROM carro_oficina ORDER BY id_carro DESC
    '''
    cursor.execute(carro)
    for linha in cursor.fetchall():
        print(linha)
    print('Id do Carro; Placa; Modelo.')
    input(':')
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


# menu via terminal:
op = -1
up = -1
while op != 0 or up != 0:

    menu = '''
-------------------------OFICINA-------------------------
    Selecione uma opção para continuar:
        
        0 - Encerrar.
        1 - Listar Vendas.
        2 - Listar Clientes.
        3 - Listar Carros.
        4 - Listar Clientes x Carro.
        5 - Listar Pedidos.
        6 x Listar Orçamento.
        7 x Listar Peças.
    '''
    menu_cadastro = '''
-------------------------OFICINA-------------------------
    Selecione uma opção para continuar:
        
        0 - Encerrar.
        1 - Cadastrar Cliente.
        2 - Cadastrar Carro.
        3 - Cadastrar Cliente e o Carro.
        4 - Relacionar Cliente e o Carro.
        5 x Cadastrar Orçamento[loop]
        6 x Cadastrar Peças.
        8 x Relacionar pedido e o Orçamento. 
    '''

    clear()

    print('Selecione uma opção:\n(1-listar / 2-Cadastrar / 0 - Sair)')
    resposta = int(input('Digite sua opção: '))

    if resposta == 1:
        clear()
        print(menu)
        op = int(input('Digite sua opção: '))

    if resposta == 2:
        clear()
        print(menu_cadastro)
        up = int(input('Digite sua opção:'))

   # Casos:
    if op == 0 or up == 0 or resposta == 0:
        clear()
        print('Sistema Finalizado!')
        t.sleep(2)
        break

    if op == 1:
        clear()
        valores()
        input(':')

    if op == 2:
        clear()
        lista_clientes()
        input(':')

    if op == 3:
        clear()
        lista_carro()
        input(':')

    if op == 4:
        clear()
        lista_cl_cr()
        input(':')

    if op == 5:
        clear()
        lista_pedido()
        print('\n Id Pedido; Id Cliente; Id Carro.')
        input(':')

    if op == 6:
        clear()
        lista_orcamento()
        print('\nId orçamento: id Carro; id Peça; Quantidade')
        input(':')

    if up == 1:
        clear()
        cadastro_cliente()

    if up == 2:
        clear()
        cadastro_carro()

    if up == 3:
        clear()
        cadastro_cliente()
        clear()
        cadastro_carro()
        clear()
        cadastro_cr_cl()

    if up == 4:
        clear()
        cadastro_cr_cl()

    t.sleep(2)
    clear()
