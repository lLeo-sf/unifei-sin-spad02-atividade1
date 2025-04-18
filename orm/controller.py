from dao import OrderDAO

class OrderController:
    def __init__(self, dao: OrderDAO):
        self.dao = dao

    def create_order(self, data: dict, items: list[dict]):
        self.dao.insert_order(data, items)

    def report_order(self, order_id: int) -> dict:
        return self.dao.get_order_report(order_id)

    def report_ranking(self, start_date: str, end_date: str) -> list:
        return self.dao.get_employee_ranking(start_date, end_date)


