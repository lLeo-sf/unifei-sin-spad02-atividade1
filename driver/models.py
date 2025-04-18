class Order:
    def __init__(self, orderid, customerid, employeeid, orderdate, shipperid=None, freight=None, **kwargs):
        self.orderid    = orderid
        self.customerid = customerid
        self.employeeid = employeeid
        self.orderdate  = orderdate
        self.shipperid    = shipperid
        self.freight     = freight

class OrderDetail:
    def __init__(self, orderid, productid, unitprice, quantity, discount=0):
        self.orderid   = orderid
        self.productid = productid
        self.unitprice = unitprice
        self.quantity   = quantity
        self.discount   = discount