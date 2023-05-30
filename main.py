def cost(land, P, Q, height):
  total_cost = 0
  for row in land:
    for block in row:
      if block > height:
        total_cost += (block - height) * Q
      else:
        total_cost += (height - block) * P
  return total_cost


def solution(land, P, Q):
  flatten = sum(land, [])
  min_height = min(flatten)
  max_height = max(flatten)

  while min_height < max_height:
    mid_height = (min_height + max_height) // 2
    if cost(land, P, Q, mid_height) < cost(land, P, Q, mid_height + 1):
      max_height = mid_height
    else:
      min_height = mid_height + 1

  return cost(land, P, Q, min_height)
