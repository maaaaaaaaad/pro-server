class Mock:

  def __init__(self):
    self.__count = 0

  @property
  def count(self):
    return self.__count

  @count.setter
  def count(self, n):
    self.__count = n


mock = Mock()
get = mock.count
print(get)

mock.count = 100
print(get)
