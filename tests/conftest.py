import pytest

from tests.models import Cart, Product


@pytest.fixture
def book_product() -> Product:
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def empty_cart() -> Cart:
    return Cart()

@pytest.fixture
def cart_with_one_product() -> Cart:
    cart = Cart()
    test_product = Product('book', 20, 'This is a book', 300)
    cart.add_product(test_product, buy_count=20)
    return cart

@pytest.fixture
def cart_with_some_products() -> Cart:
    cart = Cart()
    product1 = Product('book', 500, 'This is a book', 400)
    product2 = Product('pen', 15.7, 'Just a pen', 1500)
    cart.add_product(product1, buy_count=5)
    cart.add_product(product2, buy_count=23)
    return cart

@pytest.fixture
def cart_with_available_product_amount() -> Cart:
    cart = Cart()
    product1 = Product('book', 500, 'This is a book', 400)
    product2 = Product('pen', 15.7, 'Just a pen', 1500)
    cart.add_product(product1, buy_count=20)
    cart.add_product(product2, buy_count=700)
    return cart

@pytest.fixture
def cart_with_unavailable_product_amount() -> Cart:
    cart = Cart()
    product1 = Product('book', 500, 'A simple book', 400)
    product2 = Product('pen', 15.7, 'Just a pen', 1500)
    cart.add_product(product1, buy_count=2000)
    cart.add_product(product2, buy_count=7000)
    return cart
