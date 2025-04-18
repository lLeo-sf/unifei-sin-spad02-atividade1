import psycopg2
from psycopg2 import sql
from models import Order, OrderDetail

class OrderDAO:
    def __init__(self, conn_params):
        self.conn_params = conn_params

    def _connect(self):
        return psycopg2.connect(**self.conn_params)

    def insert_order_sql_injection(self, order: Order, items: list[OrderDetail]):
        """
        Insere pedido e detalhes vulnerável a SQL Injection e gera manualmente o order_id.
        """
        conn = self._connect()
        cur = conn.cursor()
        # Gera próximo order_id manualmente
        cur.execute("SELECT COALESCE(MAX(orderid), 0) + 1 FROM northwind.orders;")
        new_id = cur.fetchone()[0]
        # Vulnerável: concatenação direta incluindo order_id
        cur.execute(f"""
            INSERT INTO  northwind.orders(orderid, customerid, employeeid, orderdate, shipperid, freight)
            VALUES ({new_id}, '{order.customerid}', {order.employeeid}, '{order.orderdate}', {order.shipperid}, {order.freight});
        """)
        for it in items:
            cur.execute(f"""
                INSERT INTO  northwind.order_details(orderid, productid, unitprice, quantity, discount)
                VALUES ({new_id}, {it.productid}, {it.unitprice}, {it.quantity}, {it.discount});
            """)
        conn.commit()
        cur.close()
        conn.close()

    def insert_order(self, order: Order, items: list[OrderDetail]):
        """
        Insere pedido e detalhes usando prepared statements e gera manualmente o order_id.
        """
        conn = self._connect()
        cur = conn.cursor()
        # Gera próximo order_id manualmente
        cur.execute("SELECT COALESCE(MAX(orderid), 0) + 1 FROM northwind.orders;")
        new_id = cur.fetchone()[0]
        # Parametrizado incluindo order_id
        cur.execute(
            """
            INSERT INTO northwind.orders(orderid, customerid, employeeid, orderdate, shipperid, freight)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (new_id, order.customerid, order.employeeid, order.orderdate, order.shipperid, order.freight)
        )
        for it in items:
            cur.execute(
                """
                INSERT INTO  northwind.order_details(orderid, productid, unitprice, quantity, discount)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (new_id, it.productid, it.unitprice, it.quantity, it.discount)
            )
        conn.commit()
        cur.close()
        conn.close()

    def get_order_report(self, order_id: int) -> dict:
        conn = self._connect()
        cur  = conn.cursor()
        # Cabeçalho do pedido
        cur.execute(
            """
            SELECT o.orderid, o.orderdate,
                   c.companyname AS customer,
                   e.firstname || ' ' || e.lastname AS employee,
                   s.companyname AS shipper
              FROM northwind.orders o
              JOIN northwind.customers c ON o.customerid = c.customerid
              JOIN northwind.employees e ON o.employeeid = e.employeeid
              LEFT JOIN northwind.shippers s ON o.shipperid = s.shipperid
             WHERE o.orderid = %s;
            """,
            (order_id,)
        )
        header = cur.fetchone()
        # Itens do pedido
        cur.execute(
            """
            SELECT od.productid, p.productname, od.quantity, od.unitprice
              FROM northwind.order_details od
              JOIN northwind.products p ON od.productid = p.productid
             WHERE od.orderid = %s;
            """,
            (order_id,)
        )
        items = cur.fetchall()
        cur.close()
        conn.close()
        return {"header": header, "items": items}

    def get_employee_ranking(self, start_date: str, end_date: str) -> list:
        conn = self._connect()
        cur  = conn.cursor()
        cur.execute(
            """
            SELECT e.employeeid,
                   e.firstname || ' ' || e.lastname AS employee,
                   COUNT(o.orderid) AS total_orders,
                   SUM(od.quantity * od.unitprice * (1 - od.discount)) AS total_sales
              FROM northwind.employees e
              JOIN northwind.orders o ON e.employeeid = o.employeeid
              JOIN northwind.order_details od ON o.orderid = od.orderid
             WHERE o.orderdate BETWEEN %s AND %s
             GROUP BY e.employeeid, employee
             ORDER BY total_sales DESC;
            """,
            (start_date, end_date)
        )
        ranking = cur.fetchall()
        cur.close()
        conn.close()
        return ranking