
MAX_POSSIBLE_PRODUCT_QUANTITY = 10000

class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        if quantity <= 0 or isinstance(quantity, float):
            raise ValueError('Requested quantity cannot be less then 1 or float value')
        return self.quantity >= quantity

    def buy(self, quantity) -> str | Exception:
        if self.check_quantity(quantity):
            self.quantity -= quantity
            return 'Success'
        else:
            raise ValueError

    def __hash__(self) -> int:
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count: int = 1) -> int:
        if buy_count <= 0 or isinstance(buy_count, float):
            raise ValueError('Can only take integer >= 1')
        elif product in self.products:
            self.products[product] += buy_count
        else:
            self.products[product] = buy_count
        return self.products[product]


    def remove_product(self, product: Product, remove_count=None):
        if product not in self.products:
            raise ValueError('No such product in cart')
        elif remove_count is None:  # do this check before next `elif`, otherwise cannot compare None to int (<= 0)
            self.products.pop(product)
        elif remove_count <= 0 or isinstance(remove_count, float):
            raise ValueError('Can only take integer >= 1')
        elif (remove_count > self.products[product] or
              self.products[product] == remove_count):
            self.products.pop(product)
        else:
            self.products[product] -= remove_count
        return self.products[product]


    def clear(self):
        self.products.clear()
        return self.products


    def get_total_price(self) -> float:
        total_price = 0
        if not len(self.products):
            pass
        else:
            for product, quantity in self.products.items():
                total_price += product.price * quantity
        return round(total_price, 2)


    def buy(self):
        for product in self.products:
            try:
                product.buy(self.products[product])
            except ValueError:
                raise
        return 'Success'
