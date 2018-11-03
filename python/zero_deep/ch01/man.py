class Man:
    def __init__(self, name):
        self.name = name
        print('Initialized!')

    def hello(self):
        print(f'Hello {self.name}')

    def goodby(self):
        print(f'Good by ! {self.name}')


m = Man('David')
m.hello()
m.goodby()
