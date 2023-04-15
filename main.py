def generate_combinations(arr, r):
  if r == 0:
    return [[]]

  if not arr:
    return []

  head = arr[0]
  tail = arr[1:]

  without_head = generate_combinations(tail, r)
  with_head = [[head] + subset
               for subset in generate_combinations(tail, r - 1)]

  return with_head + without_head
