"""
Протестируйте классы из модуля homework/models.py
"""
import random

import pytest

from tests.conftest import cart_without_book_product
from tests.models import MAX_POSSIBLE_PRODUCT_QUANTITY


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    @pytest.mark.parametrize(
        'test_value, expected_result',
        [(1, True), (500, True), (999, True), (1000, True), (1001, False)]
    )
    def test_product_check_quantity__positive(self, book_product, test_value, expected_result):
        assert book_product.check_quantity(test_value) is expected_result

    @pytest.mark.parametrize('test_value', [0, -1, 1.7])
    def test_product_check_quantity__negative(self, book_product, test_value):
        with pytest.raises(ValueError):
            book_product.check_quantity(test_value)

    def test_product_buy(self, book_product):
        initial_product_count = book_product.quantity
        requested_items_count = random.randint(1, book_product.quantity)
        assert book_product.buy(requested_items_count) == 'Success'
        assert book_product.quantity == initial_product_count - requested_items_count

    def test_product_buy_more_than_available(self, book_product):
        requested_items_count = random.randint(1001, MAX_POSSIBLE_PRODUCT_QUANTITY)
        with pytest.raises(ValueError):
            book_product.buy(requested_items_count)



class TestCart:
#=================
# tests for adding

    def test_add_product__explicitly_add_1_item(self, book_product, random_cart):
        initial_product_count = random_cart.products.get(book_product, 0)
        assert random_cart.add_product(book_product, 1) == initial_product_count + 1

    def test_add_product__implicitly_add_1_item(self, book_product, random_cart):
        initial_product_count = random_cart.products.get(book_product, 0)
        assert random_cart.add_product(book_product) == initial_product_count + 1

    def test_add_product_add__acceptable_amount(self, book_product, random_cart):
        initial_product_count = random_cart.products.get(book_product, 0)
        quantity = random.randint(2, MAX_POSSIBLE_PRODUCT_QUANTITY)
        assert random_cart.add_product(book_product, quantity) == initial_product_count + quantity

    @pytest.mark.parametrize('quantity', [-1, 0, 1.5])
    def test_add_product__unacceptable_amount(self, book_product, random_cart, quantity):
        with pytest.raises(ValueError):
            random_cart.add_product(book_product, quantity)

#=========================================
# tests for removing from cart with product

    def test_remove_product__1(self, book_product, cart_with_book_product):
        initial_product_count = cart_with_book_product.products[book_product]
        assert cart_with_book_product.remove_product(book_product, 1) == initial_product_count - 1

    def test_remove_product__not_all(self, book_product, cart_with_book_product):
        initial_product_count = cart_with_book_product.products[book_product]
        remove_product_count = random.randint(2, initial_product_count-1)
        assert cart_with_book_product.remove_product(book_product, remove_product_count) == initial_product_count - remove_product_count

    def test_remove_product__all_implicitly(self, book_product, cart_with_book_product):
        with pytest.raises(KeyError):
            cart_with_book_product.remove_product(book_product)

    def test_remove_product__all_explicitly(self, book_product, cart_with_book_product):
        initial_product_count = cart_with_book_product.products[book_product]
        remove_product_count = initial_product_count
        with pytest.raises(KeyError):
            cart_with_book_product.remove_product(book_product, remove_product_count)

    def test_remove_product__more_than_exist_in_cart(self, book_product, cart_with_book_product):
        initial_product_count = cart_with_book_product.products[book_product]
        remove_product_count = random.randint(initial_product_count + 1, MAX_POSSIBLE_PRODUCT_QUANTITY)
        with pytest.raises(KeyError):
            cart_with_book_product.remove_product(book_product, remove_product_count)

    @pytest.mark.parametrize('quantity', [0, -1, 1.7])
    def test_remove_product__unacceptable_amount(self, book_product, cart_with_book_product, quantity):
        with pytest.raises(ValueError):
            cart_with_book_product.remove_product(book_product, quantity)

#=============================================
# tests for removing from cart without product

    @pytest.mark.parametrize('quantity', [1, 10, 0, -1, 2.5])
    def test_remove_product__product_not_in_cart__pass_amount(self, book_product, cart_without_book_product, quantity):
        with pytest.raises(ValueError):
            cart_without_book_product.remove_product(book_product, quantity)

    def test_remove_product__product_not_in_cart__no_pass_amount(self, book_product, cart_without_book_product):
        with pytest.raises(ValueError):
            cart_without_book_product.remove_product(book_product)

#=============================================
# tests for clearing cart

    def test_clear(self, random_cart):
        assert random_cart.clear() == {}

#==============================
# tests for getting total price

    def test_get_total_price__not_empty_cart(self, generate_carts):
        for cart in generate_carts:
            expected_result = round(sum(product.price * cart.products[product] for product in cart.products), 2)
            assert cart.get_total_price() == expected_result

    def test_get_total_price__empty_cart(self, empty_cart):
            assert empty_cart.get_total_price() == 0

#======================================
# tests for purchasing products in cart

    def test_cart_buy_available_amount(self, cart_with_book_product):
        assert cart_with_book_product.buy() == 'Success'

    def test_cart_buy_max_available_amount(self, cart_with_products_count_max):
        assert cart_with_products_count_max.buy() == 'Success'

    def test_cart_buy_unavailable_amount(self, cart_with_products_count_over_max):
        with pytest.raises(ValueError):
            cart_with_products_count_over_max.buy()
