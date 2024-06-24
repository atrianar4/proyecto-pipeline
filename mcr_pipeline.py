class McrPipeline:
    def __init__(self, area, prob, type, did_serv, sm, customer, project_name, book_date2, book_period, bcs_months, tcv_00, rev_fy22q3, rev_fy22q4, columna1, _id=None):
        self.area = area
        self.prob = prob
        self.type = type
        self.did_serv = did_serv
        self.sm = sm
        self.customer = customer
        self.project_name = project_name
        self.book_date2 = book_date2
        self.book_period = book_period
        self.bcs_months = bcs_months
        self.tcv_00 = tcv_00
        self.rev_fy22q3 = rev_fy22q3
        self.rev_fy22q4 = rev_fy22q4
        self.columna1 = columna1
        self._id = _id  # Agregar el ID como atributo de la instancia
    
    def toDBCollection(self):
        collection = {
            'area': self.area,
            'prob': self.prob,
            'type': self.type,
            'did_serv': self.did_serv,
            'sm': self.sm,
            'customer': self.customer,
            'project_name': self.project_name,
            'book_date2': self.book_date2,
            'book_period': self.book_period,
            'bcs_months': self.bcs_months,
            'tcv_00': self.tcv_00,
            'rev_fy22q3': self.rev_fy22q3,
            'rev_fy22q4': self.rev_fy22q4,
            'columna1': self.columna1
        }
        if self._id is not None:  # Solo incluir _id si no es None
            collection['_id'] = self._id
        return collection