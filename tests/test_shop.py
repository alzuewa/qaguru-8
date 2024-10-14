"""
Протестируйте классы из модуля homework/models.py
"""

import pytest

from tests.models import Product


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    @pytest.mark.parametrize('test_value', [1, 500, 999, 1000])
    def test_product_check_quantity__available_count(self, book_product, test_value):
        assert book_product.check_quantity(quantity=test_value) is True

    @pytest.mark.parametrize(
        'test_value', [1001, 20000])
    def test_product_check_quantity__unavailable_count(self, book_product, test_value):
        assert book_product.check_quantity(quantity=test_value) is False

    @pytest.mark.parametrize('test_value', [0, -1, 1.7])
    def test_product_check_quantity__unexpected_value(self, book_product, test_value):
        with pytest.raises(ValueError):
            book_product.check_quantity(quantity=test_value)

    def test_product_buy_available(self, book_product):
        book_product.buy(quantity=200)
        assert book_product.quantity == 800

    def test_product_buy_more_than_available(self, book_product):
        with pytest.raises(ValueError):
            book_product.buy(quantity=1001)

    @pytest.mark.parametrize('test_value', [0, -15, 6.0])
    def test_product_buy_unexpected_value(self, book_product, test_value):
        with pytest.raises(ValueError):
            book_product.buy(quantity=test_value)



class TestCart:

    # tests for adding to empty cart

    def test_add_product__explicitly_add_to_empty_cart(self, book_product, empty_cart):
        assert empty_cart.add_product(product=book_product, buy_count=10000) == 10000

    def test_add_product__implicitly_add_to_empty_cart(self, book_product, empty_cart):
        assert empty_cart.add_product(product=book_product) == 1

    # ===================================
    # tests for adding to non-empty cart

    def test_add_product__product_exists_in_cart(self, cart_with_one_product):
        '''
        This test will not pass if we create here absolutely the same test_product that already exists in fixture cart, i.e.:
        test_product = Product("book", 20, "A simple book", 300) --> create the same test_product
        cart_with_test_product.add_product(test_product, buy_count=50) --> add 50 items of test_product to cart

        This test_product will not be added to existing one in cart, because they have different identities.
        The new cart will contain 2 products which are both 'books':
        like {Product(book): 20, Product(book): 50}
        So, in case if we need it - TODO: write proper overriding of __hash__() and add __eq__() overriding for Product()
        '''
        test_product = list(cart_with_one_product.products.keys())[0]
        assert cart_with_one_product.add_product(product=test_product, buy_count=50) == 70
        assert len(cart_with_one_product.products) == 1

    def test_add_product__product_not_in_cart(self, cart_with_one_product):
        test_product = Product('pen', 800, 'Just a pen', 30)
        assert cart_with_one_product.add_product(product=test_product, buy_count=6) == 6
        assert len(cart_with_one_product.products) == 2

    # ===============================================
    # tests for removing from cart with test product

    @pytest.mark.parametrize('remove_count, expected_after_remove', [(1, 19), (5, 15)])
    def test_remove_some_product(self, cart_with_one_product, remove_count, expected_after_remove):
        test_product = list(cart_with_one_product.products.keys())[0]
        assert cart_with_one_product.remove_product(product=test_product,
                                                    remove_count=remove_count) == expected_after_remove

    def test_remove_product__all_explicitly(self, cart_with_one_product):
        test_product = list(cart_with_one_product.products.keys())[0]
        initial_test_product_count = cart_with_one_product.products[test_product]
        cart_with_one_product.remove_product(product=test_product, remove_count=initial_test_product_count)
        assert cart_with_one_product.products == {}

    def test_remove_product__all_implicitly(self, cart_with_one_product):
        test_product = list(cart_with_one_product.products.keys())[0]
        cart_with_one_product.remove_product(product=test_product)
        assert cart_with_one_product.products == {}

    def test_remove_product__more_than_exist_in_cart(self, cart_with_one_product):
        test_product = list(cart_with_one_product.products.keys())[0]
        cart_with_one_product.remove_product(product=test_product, remove_count=21)
        assert cart_with_one_product.products == {}

    @pytest.mark.parametrize('quantity', [0, -1, 16.9])
    def test_remove_product__unexpected_value(self, cart_with_one_product, quantity):
        test_product = list(cart_with_one_product.products.keys())[0]
        with pytest.raises(ValueError):
            cart_with_one_product.remove_product(test_product, quantity)

    # =================================================
    # tests for removing from cart without test product

    def test_remove_product__product_not_in_cart__pass_amount(self, cart_with_one_product):
        test_product = Product('pen', 800, 'Just a pen', 30)
        with pytest.raises(KeyError):
            cart_with_one_product.remove_product(product=test_product, remove_count=15)

#=============================================
# tests for clearing cart

    @pytest.mark.parametrize('cart', ['empty_cart', 'cart_with_one_product'])
    def test_clear(self, cart, request):
        assert request.getfixturevalue(cart).clear() == {}

#==============================
# tests for getting total price

    def test_get_total_price__not_empty_cart(self, cart_with_some_products):
        assert cart_with_some_products.get_total_price() == 2861.10

    def test_get_total_price__empty_cart(self, empty_cart):
            assert empty_cart.get_total_price() == 0

#======================================
# tests for purchasing products in cart

    def test_cart_buy_available_amount(self, cart_with_available_product_amount):
        cart_with_available_product_amount.buy()
        assert cart_with_available_product_amount.products == {}

    def test_cart_buy_unavailable_amount(self, cart_with_unavailable_product_amount):
        result = cart_with_unavailable_product_amount.buy()
        assert 'pen' in result
        assert len(cart_with_unavailable_product_amount.products) == 2
