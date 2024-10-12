import random
import string
from typing import List

import pytest

from tests.models import MAX_POSSIBLE_PRODUCT_QUANTITY, Cart, Product


BOOK = Product("book", 100, "This is a book", 1000)
WORKBOOK = Product("workbook", 100, "This is a book", 1000)


@pytest.fixture
def book_product() -> Product:
    return BOOK

@pytest.fixture(params=[{}, {BOOK: 3}, {WORKBOOK: 5}, ])
def random_cart(request) -> Cart:
    cart = Cart()
    cart.products = request.param
    return cart

@pytest.fixture(params=[{}, {WORKBOOK: 5}])
def cart_without_book_product(request) -> Cart:
    cart = Cart()
    cart.products = request.param
    return cart

@pytest.fixture
def cart_with_book_product() -> Cart:
    cart = Cart()
    cart.products = {BOOK: 27}
    return cart

@pytest.fixture
def cart_with_products_count_max() -> Cart:
    cart = Cart()
    cart.products = {BOOK: BOOK.quantity, WORKBOOK: WORKBOOK.quantity}
    return cart

@pytest.fixture
def cart_with_products_count_over_max() -> Cart:
    cart = Cart()
    cart.products = {
        BOOK: BOOK.quantity + random.randint(1,1000),
        WORKBOOK: WORKBOOK.quantity + random.randint(1,1000)
    }
    return cart

@pytest.fixture
def empty_cart() -> Cart:
    return Cart()

@pytest.fixture
def generate_products() -> List[Product]:
    product_names = ['book', 'pen', 'workbook', 'pencil']
    products = []
    for product in product_names:
        products.append(
            Product(
                name=product,
                price=round(random.random() * random.randint(1, 1000), 2),
                description=''.join(random.choices(string.ascii_letters, k=15)),
                quantity=random.randint(0, MAX_POSSIBLE_PRODUCT_QUANTITY)
                )
        )
    return products

@pytest.fixture
def generate_carts(generate_products) -> List[Cart]:
    products_count_in_cart = range(1, len(generate_products)+1)
    carts = []
    for count in products_count_in_cart:
        cart = Cart()
        products_in_cart = random.sample(population=generate_products, k=count)
        for product in products_in_cart:
            cart.products[product] = random.randint(1, MAX_POSSIBLE_PRODUCT_QUANTITY)
        carts.append(cart)
    return carts
