import time as t
from turtle import update
from click import clear
import pyodbc as p

# conexão com o banco de dados, sem autenticação
server = 'DESKTOP-J0U7P4K\SQLEXPRESS'
database = 'modelagem'
cnx = p.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_connection=yes;')
cursor = cnx.cursor()

# funcoes:

# Lista


def valores():
    valor = '''
        SELECT * FROM vw_valor_final_oficina
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
# Fim Lista


# Cadastro
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
# Fim Cadastro


# Atualizar
def atualizar_cliente():
    clear()
    print('-' * 25, 'ATUALIZAR CLIENTE', '-' * 25)
    opcao = int(
        input('\n 0 - Encerrar\n 1 - Atualizar Nome\n 2 - Atualizar CEP\n 3 - Atualizar tudo\n Digite a sua opção: '))

    if opcao == 1:

        idcliente = int(input('Digite o id do cliente que deseja trocar: '))
        lista = '''
            select * from cliente_oficina where id_cliente = {}
        '''.format(idcliente)
        cursor.execute(lista)

        for linha in cursor.fetchall():
            print(linha)

        check = input('\nEste cliente que deseja modificar(s/n)?')

        if check == 's':
            clear()
            print('-' * 25, 'ATUALIZAR CLIENTE', '-' * 25)
            nome = str(input('\nDigite o Primeiro nome do(a) cliente: '))
            sobrenome = str(input('\nDigite o Sobrenome do(a) cliente: '))
            update = '''
                update cliente_oficina set nome = '{}', sobrenome = '{}' where id_cliente = {};
            '''.format(nome, sobrenome, idcliente)
            cursor.execute(update)
            cursor.commit()
            print('Nome alterado!')
            cursor.execute(lista)

        else:
            clear()
            atualizar_cliente()

    if opcao == 2:
        clear()
        idcliente = int(input('Digite o id do cliente que deseja trocar: '))
        lista = '''
            select * from cliente_oficina where id_cliente = {}
        '''.format(idcliente)
        cursor.execute(lista)

        for linha in cursor.fetchall():
            print(linha)

        check = input('\nEste cliente que deseja modificar(s/n)?')
        if check == 's':
            clear()
            print('-' * 25, 'ATUALIZAR CLIENTE', '-' * 25)
            cep = str(input('\nDigite o novo CEP: '))
            update = '''
                update cliente_oficina set cep = '{}'where id_cliente = {};
            '''.format(cep, idcliente)
            cursor.execute(update)
            cursor.commit()
            print('CEP alterado!')
            cursor.execute(lista)

        if opcao == 3:
            clear()
            idcliente = int(
                input('Digite o id do cliente que deseja trocar: '))
            lista = '''
                select * from cliente_oficina where id_cliente = {}
            '''.format(idcliente)
            cursor.execute(lista)

            for linha in cursor.fetchall():
                print(linha)

            check = input('\nEste cliente que deseja modificar(s/n)?')

            if check == 's':
                clear()
                print('-' * 25, 'ATUALIZAR CLIENTE', '-' * 25)
                nome = str(input('\nDigite o Primeiro nome do(a) cliente: '))
                sobrenome = str(input('\nDigite o Sobrenome do(a) cliente: '))
                cep = str(input('\nDigite o novo CEP: '))
                update = '''
                    update cliente_oficina set nome = '{}', sobrenome = '{}', cep ='{}' where id_cliente = {};
                '''.format(nome, sobrenome, cep, idcliente)
                cursor.execute(update)
                cursor.commit()
                print('Cliente alterado!')
                cursor.execute(lista)

            else:
                clear()
                atualizar_cliente()

        else:
            clear()
            atualizar_cliente()
    else:
        clear()


def atualizar_veiculo():
    clear()
    print('-' * 25, 'ATUALIZAR VEICULO', '-' * 25)
    opcao = int(
        input(' 0 - Encerrar\n 1 - Atualizar Placa\n 2 - Atualizar Modelo e Marca\n 3 - Atualizar Ano:\n 4 - Atualizar tudo\n Digite a sua opção: '))

    if opcao == 1:
        clear()
        print('-' * 25, 'ATUALIZAR VEICULO', '-' * 25)
        idcarro = int(input('Digite o id do veiculo que deseja trocar: '))
        lista = '''
            select * from carro_oficina where id_carro = {}
        '''.format(idcarro)
        cursor.execute(lista)

        for linha in cursor.fetchall():
            print(linha)

        check = input('\nEste veiculo que deseja modificar(s/n)?')

        if check == 's':
            clear()
            print('-' * 25, 'ATUALIZAR VEICULO', '-' * 25)
            placa = str(input('\n Digite a nova Placa:'))
            update = '''
                update carro_oficina set placa = '{}' where id_carro = {}
            '''.format(placa, idcarro)
            cursor.execute(update)
            cursor.commit()
            cursor.execute(lista)
            for linha in cursor.fetchall():
                print(linha)

            print('\nPlaca Atualizada!')

        else:
            clear()
            atualizar_veiculo()


def atualizar_peca():
    clear()
    print('-' * 25, 'ATUALIZAR PEÇA', '-' * 25)
    opcao = int(
        input(' 0 - Encerrar\n 1 - Atualizar Nome\n 2 - Atualizar Preço\n 3 - Atualizar Tudo\n Digite a sua opção: '))

    if opcao == 1:
        clear()
        print('-' * 25, 'ATUALIZAR PEÇA', '-' * 25)
        idpeca = int(input('Digite o id da peça: '))
        lista = '''
            select * from peca_oficina where id_peca = {}
        '''.format(idpeca)
        cursor.execute(lista)
        for linha in cursor.fetchall():
            print(linha)

        check = str(input('\nEssa peça que deseja atualizar(s/n)? '))

        if check == 's':
            clear()
            print('-' * 25, 'ATUALIZAR PEÇA', '-' * 25)
            nome = str(input('Digite o novo nome da peça: '))
            update = '''
                update peca_oficina set nome = '{}' where id_peca = {}
            '''.format(nome, idpeca)
            cursor.execute(update)
            cursor.commit()
            clear()
            cursor.execute(lista)
            print('\n Nome alterado!')
        else:
            clear()
            atualizar_peca()
    if opcao == 2:
        clear()
        print('-' * 25, 'ATUALIZAR PEÇA', '-' * 25)
        idpeca = int(input('Digite o id da peça: '))
        lista = '''
            select * from peca_oficina where id_peca = {}
        '''.format(idpeca)
        cursor.execute(lista)
        for linha in cursor.fetchall():
            print(linha)

        check = str(input('\nEssa peça que deseja atualizar(s/n)? '))

        if check == 's':
            clear()
            print('-' * 25, 'ATUALIZAR PEÇA', '-' * 25)
            preco = float(input('Digite o novo preço da peça: '))
            update = '''
                update peca_oficina set valor_unidade = {} where id_peca = {}
            '''.format(preco, idpeca)
            cursor.execute(update)
            cursor.commit()
            clear()
            cursor.execute(lista)
            print('\n Valor alterado!')

        else:
            clear()
            atualizar_peca()

    if opcao == 3:
        clear()
        print('-' * 25, 'ATUALIZAR PEÇA', '-' * 25)
        idpeca = int(input('Digite o id da peça: '))
        lista = '''
            select * from peca_oficina where id_peca = {}
        '''.format(idpeca)
        cursor.execute(lista)
        for linha in cursor.fetchall():
            print(linha)

        check = str(input('\nEssa peça que deseja atualizar(s/n)? '))

        if check == 's':
            clear()
            print('-' * 25, 'ATUALIZAR PEÇA', '-' * 25)
            nome = str(input('Digite o novo nome da peça: '))
            preco = float(input('Digite o novo preço da peça: '))
            update = '''
                update peca_oficina set nome = '{}', preco = {} where id_peca = {}
            '''.format(nome, preco, idpeca)
            cursor.execute(update)
            cursor.commit()
            clear()
            cursor.execute(lista)
            print('\n Peça alterado!')
        else:
            clear()
            atualizar_peca()


def atualizar_orcamento():
    clear()
    print('-' * 25, 'ATUALIZAR ORÇAMENTO', '-' * 25)
    opcao = int(
        input(' 0 - Encerrar\n 1 - Atualizar Veiculo\n 2 - Atualizar Peça\n 3 - Atualizar Quantidade\n Digite a sua opção: '))

    if opcao == 1:
        clear()
        print('-' * 25, 'ATUALIZAR ORÇAMENTO', '-' * 25)
        idorcamento = int(input('Digite o id do orcamento: '))
        lista = '''
            select * from vw_orcamento_oficina where id_orcamento = {}
        '''.format(idorcamento)
        cursor.execute(lista)
        for linha in cursor.fetchall():
            print(linha)

        check = str(input('Este orçamento que deseja alterar(s/n)?'))

        if check == 's':
            clear()
            print('-' * 25, 'ATUALIZAR ORÇAMENTO', '-' * 25)
            idveiculo = int(input('Digite o novo id do veiculo:'))
            update = '''
                update orcamento_oficina set id_carro = {} where id_orcamento = {}
            '''.format(idveiculo, idorcamento)
            cursor.execute(update)
            cursor.commit()
            clear()
            cursor.execute(lista)
            for linha in cursor.fetchall():
                print(linha)

            print('\nVeiculo Atualizado!')

        else:
            clear()
            atualizar_orcamento()

    if opcao == 2:
        clear()
        print('-' * 25, 'ATUALIZAR ORÇAMENTO', '-' * 25)
        idorcamento = int(input('Digite o id do orcamento: '))
        lista = '''
            select * from vw_orcamento_oficina where id_orcamento = {}
        '''.format(idorcamento)
        cursor.execute(lista)
        for linha in cursor.fetchall():
            print(linha)

        check = str(input('Este orçamento que deseja alterar(s/n)?'))

        if check == 's':
            clear()
            print('-' * 25, 'ATUALIZAR ORÇAMENTO', '-' * 25)
            idpeca = int(input('\nDigite o id da peça: '))
            update = '''
                update orcamento_oficina set id_carro = {} where id_orcamento = {}
            '''.format(idpeca, idpeca)
            cursor.execute(update)
            cursor.commit()
            clear()
            cursor.execute(lista)
            for linha in cursor.fetchall():
                print(linha)

            print('\n Peça Atualizada!')

        else:
            clear()
            atualizar_orcamento()

    if opcao == 3:
        clear()
        idorcamento = int(input('Digite o id do orcamento: '))
        lista = '''
            select * from vw_orcamento_oficina where id_orcamento = {}
        '''.format(idorcamento)
        cursor.execute(lista)
        for linha in cursor.fetchall():
            print(linha)

        check = str(input('Este orçamento que deseja alterar(s/n)? '))
        if check == 's':
            print('-' * 25, 'ATUALIZAR ORÇAMENTO', '-' * 25)
            qty = int(input('\nDigite a nova Quantidade: '))
            update = '''
                    update orcamento_oficina set quantidade = {} where id_orcamento = {}
                '''.format(qty, idorcamento)
            cursor.execute(update)
            cursor.commit()
            clear()
            cursor.execute(lista)
            for linha in cursor.fetchall():
                print(linha)

            print('\n Quantidade Atualizada!')
        else:
            clear()
            atualizar_orcamento()
    else:
        clear()


# menu via terminal:
while True:
    # valores default para as var
    op = -1
    cd = -1
    up = -1
    dl = -1

    # menu
    logo = '''
  ______    _______  __    ______  __  .__   __.      ___
 /  __  \  |   ____||  |  /      ||  | |  \ |  |     /   \.
|  |  |  | |  |__   |  | |  ,----'|  | |   \|  |    /  ^  \.
|  |  |  | |   __|  |  | |  |     |  | |  . `  |   /  /_\  \.
|  `--'  | |  |     |  | |  `----.|  | |  |\   |  /  _____  \.
 \______/  |__|     |__|  \______||__| |__| \__| /__/     \__\.

    '''
    # lista
    menu = '''
    {}
    Selecione uma opção para continuar:

        0 - Encerrar.
        1 - Listar Vendas.
        2 - Listar Clientes.
        3 - Listar Veiculos.
        4 - Listar Clientes x Veiculos.
        5 - Listar Pedidos.
        6 - Listar Orçamento.
        7 - Listar Peças.
    '''.format(logo)
    # cadastro
    menu_cadastro = '''
    {}
    Selecione uma opção para continuar:

        0 - Encerrar.
        1 - Cadastrar Cliente.
        2 - Cadastrar Veiuclo.
        3 - Cadastrar Cliente e o Veiculo.
        4 - Relacionar Cliente e o Veiculo.
        5 - Cadastrar Orçamento.
        6 - Cadastrar Peças.
        7 - Cadastrar Pedido.
        8 - Relacionar Pedido e o Orçamento.
    '''.format(logo)
    # update
    menu_update = '''
    {}
    Selecione uma opção para continuar:

        0 - Encerrar.
        1 - Atualizar dados do(a) Cliente.
        2 - Atualizar dados do Veículo.
        3 - Atualizar Peça.
        4 - Atualizar Orçamento.
        5 x Atualizar Pedido.
    '''.format(logo)
    # delete
    menu_delete = '''
    {}
    Selecione uma opção para continuar:

        0 - Encerrar.
        1 - A fazer ainda.
    '''.format(logo)
    # fim dos menus

    clear()

    # tela inicial

    print('{}Selecione uma opção:\n( 1-listar / 2-Cadastrar / 3 - Atualizar / 4 - Deletar / 0 - Sair )'.format(logo))
    print('\nDica de cadastro: cadastre cliente e carro, faça a relação, orçamento, pedido e relacione pedido e orçamento e veja na lista o valor final.\n')
    resposta = int(input('Digite sua opção: '))

    if resposta == 1:
        clear()
        print(menu)
        op = int(input('Digite sua opção: '))

    if resposta == 2:
        clear()
        print(menu_cadastro)
        cd = int(input('Digite sua opção: '))

    if resposta == 3:
        clear()
        print(menu_update)
        up = int(input('Digite sua opção: '))

    if resposta == 4:
        clear()
        print(menu_delete)
        dl = int(input('Digite sua opção: '))

    # Sessão de Condições:
    if op == 0 or cd == 0 or up == 0 or dl == 0 or resposta == 0:
        clear()
        print('Sistema Finalizado!')
        t.sleep(2)
        break

    # select:
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

    # Cadastro:
    if cd == 1:
        clear()
        cadastro_cliente()

    if cd == 2:
        clear()
        cadastro_carro()

    if cd == 3:
        clear()
        cadastro()

    if cd == 4:
        clear()
        cadastro_cr_cl()

    if cd == 5:
        clear()
        cadastro_orcamento()

    if cd == 6:
        clear()
        cadastro_peca()

    if cd == 7:
        clear()
        cadastro_pedido()

    if cd == 8:
        clear()
        cadastro_venda()

    # Update
    if up == 1:
        atualizar_cliente()
        input('\nAperte Enter para continuar: ')
    if up == 2:
        atualizar_veiculo()
        input('\nAperte Enter para continuar: ')
    if up == 3:
        atualizar_peca()
        input('\nAperte Enter para continuar: ')
    if up == 4:
        atualizar_orcamento()
        input('\nAperte Enter para continuar: ')
    if up == 5:
        input('\nAperte Enter para continuar: ')

    t.sleep(1)
    clear()
