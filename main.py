import bisect


def solution(land, P, Q):
  flatten = sorted(h for row in land for h in row)
  N = len(flatten)
  prefix_sum = [0] * (N + 1)
  for i in range(N):
    prefix_sum[i + 1] = prefix_sum[i] + flatten[i]

  left, right = flatten[0], flatten[-1]
  answer = float('inf')

  def calculate_cost(mid):
    idx = bisect.bisect_right(flatten, mid)
    inc = prefix_sum[-1] - prefix_sum[idx] - (N - idx) * mid
    dec = idx * mid - prefix_sum[idx]
    return inc * Q + dec * P

  while left <= right:
    mid = (left + right) // 2
    cost = calculate_cost(mid)
    if cost <= calculate_cost(mid + 1):
      answer = min(answer, cost)
      right = mid - 1
    else:
      left = mid + 1

  return answer
