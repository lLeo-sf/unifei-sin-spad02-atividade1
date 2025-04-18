from view import input_order, display_report, display_ranking
from controller import OrderController
from dao import OrderDAO

if __name__ == '__main__':
    connection_string = {
        'host':     'localhost',
        'dbname':   'northwind',
        'user':     'postgres',
        'password': '123qwe'
    }
    dao  = OrderDAO(connection_string)
    controller = OrderController(dao)

    op = input('1) Inserir (vulnerável)\n2) Inserir (safe)\n3) Relatório pedido\n4) Ranking\n> ')
    if op in ('1','2'):
        data, items = input_order()
        controller.create_order(data, items, safe=(op=='2'))
    elif op == '3':
        oid = int(input('Order ID: '))
        display_report(controller.report_order(oid))
    else:
        sd = input('Data início (YYYY-MM-DD): ')
        ed = input('Data fim (YYYY-MM-DD): ')
        display_ranking(controller.report_ranking(sd, ed))
