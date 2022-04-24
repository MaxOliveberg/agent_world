class IBoardSquare:

    def get_content(self):
        raise NotImplementedError

    def add(self, thing):
        raise NotImplementedError

    def remove(self, thing):
        raise NotImplementedError
