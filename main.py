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


def main():
  n = 6
  r = 4

  arr = list(range(1, n + 1))
  combinations = generate_combinations(arr, r)
  result = len(combinations)

  print(f"{n}C{r}={result}")


if __name__ == "__main__":
  main()
