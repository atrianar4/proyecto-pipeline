class Sm:
    def __init__(self,name,_id=None):
        self._id=_id
        self.name = name
        
    def toDBCollection(self):
        collection = {
            'name':self.name
        }
        if self._id is not None:
            collection['_id'] = self._id
        return collection