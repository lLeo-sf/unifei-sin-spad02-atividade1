from datetime import date


def input_order():
    data = {
        'customerid': input('Cliente ID: '),
        'employeeid': input('Vendedor ID: '),
        'orderdate':  date.today(),
        'shipperid':    input('Shipper ID: '),
        'freight':     input('Frete (0.00): ')
    }
    items = []
    while True:
        pid = input('  Produto ID (enter para sair): ')
        if not pid:
            break
        items.append({
            'productid': pid,
            'unitprice': input('  Preço unitário: '),
            'quantity':   input('  Quantidade: '),
            'discount':   input('  Desconto (0–1): ')
        })
    return data, items


def display_report(report: dict):
    hdr = report['header']
    print(f"Pedido #{hdr[0]}, data {hdr[1]}, cliente {hdr[2]}, vendedor {hdr[3]}, shipper {hdr[4]}")
    for pid, name, qty, pr in report['items']:
        print(f" - {pid} | {name}: {qty} x {pr}")


def display_ranking(rows: list):
    for emp_id, emp, tot, sales in rows:
        print(f"{emp} (#{emp_id}): {tot} pedidos, R$ {sales:.2f}")