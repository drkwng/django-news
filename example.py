from time import time


def timelog(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Work time: {round(t2-t1), 10} sec')
        return result
    return wrapper


class Product:

    product = 'Abstract product'

    __meta = 'Analytics signal'

    def __init__(self, name):
        self.product = name

    def add_to_cart(self, count):
        print(f'Add {count} products [{self.product}] to cart')

    def add_description(self):
        print(f'Add Description')

    def add_review(self, text):
        print(f'Add review: {text}')


class Book(Product):

    def __init__(self, name, author, pages):
        super().__init__(name=name)
        self.name = self.product = name
        self.author = author
        self.pages = pages

    def __add__(self, other):
        return Book(
            name=f'{self.name}|{other.name}',
            author=f'{self.author}|{other.author}',
            pages=self.pages + other.pages
        )

    def __str__(self):
        return f'puk puk {self.author}'

    @timelog
    def get_pages_count(self):
        print(f'pages count {self.pages}')

    @timelog
    def add_to_cart(self, count):
        super().add_to_cart(count)
        print(f'Add {count} products1111 [{self.product}] to cart')