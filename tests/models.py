
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

    def buy(self, quantity) -> None:
        if self.check_quantity(quantity):
            self.quantity -= quantity
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
            raise KeyError('No such product in cart')
        elif remove_count is None:  # do this check before next `elif`, otherwise cannot compare None to int (<= 0)
            self.products.pop(product)
            return
        elif remove_count <= 0 or isinstance(remove_count, float):
            raise ValueError('Can only take integer >= 1')
        elif (remove_count > self.products[product] or
              self.products[product] == remove_count):
            self.products.pop(product)
            return
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
        is_purchase_possible = all(product.check_quantity(self.products[product]) for product in self.products)
        if is_purchase_possible:
            for product in self.products:
                product.buy(self.products[product])
            self.products.clear()
        else:
            not_enough_products = []
            for product in self.products:
                check_result = product.check_quantity(self.products[product])
                if check_result is False:
                    not_enough_products.append(product.name)
            output_str = ', '.join(not_enough_products)
            return f'Not enough products: {output_str}'
