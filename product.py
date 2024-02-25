class Product:
    def __init__(self,area, prob, type,did_serv,sm,hw_impact,customer,proyect_name,book_date2,book_period,bcs_months,tcv_00,rev_fy22q3,rev_fy22q4,columna1):
        self.area = area
        self.prob = prob
        self.type = type
        self.did_serv = did_serv
        self.sm = sm
        self.hw_impact = hw_impact
        self.customer = customer
        self.proyect_name = proyect_name
        self.book_date2 = book_date2
        self.book_period = book_period
        self.bcs_months = bcs_months
        self.tcv_00 = tcv_00
        self.rev_fy22q3 = rev_fy22q3
        self.rev_fy22q4 = rev_fy22q4
        self.columna1 = columna1
        




    def toDBCollection(self):
        return {
            'area': self.area,
            'prob': self.prob,
            'type': self.type,
            'did_serv': self.did_serv,
            'sm': self.sm,
            'hw_impact': self.hw_impact,
            'customer': self.customer,
            'proyect_name': self.proyect_name,
            'book_date2': self.book_date2,
            'book_period': self.book_period,
            'bcs_months': self.bcs_months,
            'tcv_00': self.tcv_00,
            'rev_fy22q3': self.rev_fy22q3,
            'rev_fy22q4': self.rev_fy22q4,
            'columna1': self.columna1
        }