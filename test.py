class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show_name(self):
        print(self.name)

    def show_age(self):
        print(self.age)

man = Person("Guido", 61)
man.show_name()
man.show_age()
