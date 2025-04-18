from dao import OrderDAO
from models import Order, OrderDetail

class OrderController:
    def __init__(self, dao: OrderDAO):
        self.dao = dao

    def create_order(self, data: dict, items: list[dict], safe: bool = False):
        order = Order(
            orderid=None,
            customerid=data['customerid'],
            employeeid=int(data['employeeid']),
            orderdate=data['orderdate'],
            shipperid=int(data.get('shipperid') or 0),
            freight=float(data.get('freight') or 0)
        )
        details = [OrderDetail(
            orderid=None,
            productid=int(it['productid']),
            unitprice=float(it['unitprice']),
            quantity=int(it['quantity']),
            discount=float(it.get('discount') or 0)
        ) for it in items]
        if safe:
            self.dao.insert_order(order, details)
        else:
            self.dao.insert_order_sql_injection(order, details)

    def report_order(self, order_id: int):
        return self.dao.get_order_report(order_id)

    def report_ranking(self, start_date: str, end_date: str):
        return self.dao.get_employee_ranking(start_date, end_date)