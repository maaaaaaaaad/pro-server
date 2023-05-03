class Animal:

  def __init__(self, name):
    self.name = name

  def make_sound(self):
    pass


class Dog(Animal):

  def __init__(self, name):
    super().__init__(name)

  def make_sound(self):
    print("ziral!")


class Cat(Animal):

  def __init__(self, name):
    super().__init__(name)

  def make_sound(self):
    print("ny~")


d = Dog("b")
c = Cat("n")

d.make_sound()
c.make_sound()
