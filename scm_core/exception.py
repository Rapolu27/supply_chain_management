class UserException(Exception):
    def __init__(self, message="Invalid user"):
        self.message = message
        super().__init__(self.message)

class ProductException(Exception):
    def __init__(self, message="Invalid Product details"):
        self.message = message
        super().__init__(self.message)

class SupplierException(Exception):
    def __init__(self, message="Supplier details not valid"):
        self.message = message
        super().__init__(self.message)

class POException(Exception):
    def __init__(self, message="Purchase order is  invalid"):
        self.message = message
        super().__init__(self.message)