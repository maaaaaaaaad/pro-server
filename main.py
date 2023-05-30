import sys


def solution(land, P, Q):

  def calculate_cost(height):
    inc = sum(max(0, h - height) for h in flatten) * Q
    dec = sum(max(0, height - h) for h in flatten) * P
    return inc + dec

  flatten = [h for row in land for h in row]
  flatten.sort()

  left, right = flatten[0], flatten[-1]
  answer = sys.maxsize

  while left <= right:
    mid = (left + right) // 2
    cost = calculate_cost(mid)
    if cost <= calculate_cost(mid + 1):
      answer = min(answer, cost)
      right = mid - 1
    else:
      left = mid + 1

  return answer
