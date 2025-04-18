from datetime import date


def input_order():
    data = {
        "customerid": input("Cliente ID: "),
        "employeeid": input("Vendedor ID: "),
        "orderdate": date.today(),
        "shipperid": input("Shipper ID: "),
    }
    items = []
    while True:
        pid = input("  Produto ID (enter para sair): ")
        if not pid:
            break
        items.append({
            "productid": pid,
            "unitprice": float(input("  Preço unitário: ")),
            "quantity": int(input("  Quantidade: ")),
            "discount": float(input("  Desconto (0–1): ")),
        })
    return data, items


def display_report(report: dict):
    hdr = report["header"]
    print(
        f"Pedido #{hdr['orderid']}, data {hdr['orderdate']}, "
        f"cliente {hdr['customer']}, vendedor {hdr['employee']}"
    )
    for item in report["items"]:
        print(f" - {item['productid']} | {item['productname']}: {item['quantity']} x {item['unitprice']}")


def display_ranking(rows: list):
    for emp_id, emp, total, sales in rows:
        print(f"{emp} (#{emp_id}): {total} pedidos, R$ {sales:.2f}")