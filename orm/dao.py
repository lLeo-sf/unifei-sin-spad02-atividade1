from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Base, Order, OrderDetail, Employee

class OrderDAO:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.bind = self.engine
        self.Session = sessionmaker(bind=self.engine)

    def insert_order(self, order_data: dict, items_data: list[dict]):
        session = self.Session()
        max_id = session.query(func.max(Order.orderid)).scalar() or 0
        order_data_with_id = dict(order_data)
        order_data_with_id['orderid'] = max_id + 1
        order = Order(**order_data_with_id)
        session.add(order)
        session.flush() 
        for item in items_data:
            od = OrderDetail(orderid=order.orderid, **item)
            session.add(od)
        session.commit()
        session.close()

    def get_order_report(self, order_id: int) -> dict:
        session = self.Session()
        order = session.query(Order).get(order_id)
        header = {
            "orderid": order.orderid,
            "orderdate": order.orderdate,
            "customer": order.customer.companyname,
            "employee": f"{order.employee.firstname} {order.employee.lastname}",
        }
        items = [
            {
                "productid": od.productid,
                "productname": od.product.productname,
                "quantity": od.quantity,
                "unitprice": od.unitprice,
            }
            for od in order.order_detailss
        ]
        session.close()
        return {"header": header, "items": items}

    def get_employee_ranking(self, start_date, end_date) -> list:
        session = self.Session()
        results = (
            session.query(
                Employee.employeeid,
                func.concat(Employee.firstname, " ", Employee.lastname).label("employee"),
                func.count(Order.orderid).label("total_orders"),
                func.sum(
                    OrderDetail.quantity * OrderDetail.unitprice * (1 - OrderDetail.discount)
                ).label("total_sales"),
            )
            .join(Order, Employee.employeeid == Order.employeeid)
            .join(OrderDetail, Order.orderid == OrderDetail.orderid)
            .filter(Order.orderdate.between(start_date, end_date))
            .group_by(Employee.employeeid, "employee")
            .order_by(func.sum(
                OrderDetail.quantity * OrderDetail.unitprice * (1 - OrderDetail.discount)
            ).desc())
            .all()
        )
        session.close()
        return results