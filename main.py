class Mock:

  def __init__(self):
    self.count = 0

  @property
  def count(self):
    return self.count

  @count.setter
  def count(self, n):
    self.count = n
