from django.http import HttpRequest, HttpResponse


class Cart:
    def __init__(self, request: HttpRequest) -> HttpResponse:
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id: int, quantity: int = 1) -> None:
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
        self.save()

    def remove(self, product_id: int) -> None:
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self) -> None:
        self.session.modified = True

    def clear(self) -> None:
        self.session['cart'] = {}
        self.save()

    def items(self) -> None:
        return self.cart.items()
