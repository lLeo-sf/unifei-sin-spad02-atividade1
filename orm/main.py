from view import input_order, display_report, display_ranking
from controller import OrderController
from dao import OrderDAO


def main():
    db_url = "postgresql://postgres:123qwe@localhost:5432/northwind"
    dao = OrderDAO(db_url)
    ctrl = OrderController(dao)

    op = input("1) Inserir pedido\n2) Relatório pedido\n3) Ranking funcionários\n> ")
    if op == "1":
        data, items = input_order()
        ctrl.create_order(data, items)
    elif op == "2":
        oid = int(input("Order ID: "))
        report = ctrl.report_order(oid)
        display_report(report)
    else:
        sd = input("Data início (YYYY-MM-DD): ")
        ed = input("Data fim (YYYY-MM-DD): ")
        rows = ctrl.report_ranking(sd, ed)
        display_ranking(rows)


if __name__ == "__main__":
    main()
