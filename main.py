class ListNode:

  def __init__(self, data):
    self.data = data
    self.next = None


class LinkedList:

  def __init__(self):
    self.head = None

  def insert(self, data):
    new_node = ListNode(data)
    new_node.next = self.head
    self.head = new_node

  def delete(self, data):
    current = self.head
    prev = None

    while current is not None:
      if current.data == data:
        break

      prev = current
      current = current.next

    if current is None:
      return "Value not found in the list."

    if prev is None:
      self.head = current.next
    else:
      prev.next = current.next

  def search(self, data):
    current = self.head
    while current is not None:
      if current.data == data:
        return True
      current = current.next
    return False

  def print_list(self):
    current = self.head
    while current is not None:
      print(current.data, end=" -> ")
      current = current.next
    print("None")


linked_list = LinkedList()
linked_list.insert(5)
linked_list.insert(10)
linked_list.insert(15)

linked_list.print_list()

print(linked_list.search(10))
print(linked_list.search(20))

linked_list.delete(10)
linked_list.print_list()
