import collections
import math


def bfs(land, height, groups, x, y, group_number):
  move = [(1, 0), (0, 1), (-1, 0), (0, -1)]
  queue = collections.deque([(x, y)])
  groups[x][y] = group_number

  while queue:
    now = queue.popleft()
    for i in range(4):
      new_x = now[0] + move[i][0]
      new_y = now[1] + move[i][1]
      if new_x < 0 or new_y < 0 or new_x >= len(groups) or new_y >= len(
          groups[0]) or groups[new_x][new_y] != 0:
        continue
      if abs(land[new_x][new_y] - land[now[0]][now[1]]) <= height:
        queue.append((new_x, new_y))
        groups[new_x][new_y] = group_number


def get_groups_wieghts(land, groups, height):
  move = [(1, 0), (0, 1), (-1, 0), (0, -1)]
  weights = collections.defaultdict(lambda: math.inf)

  for i in range(len(groups)):
    for j in range(len(groups[0])):
      now = groups[i][j]
      for dx, dy in move:
        new_x, new_y = i + dx, j + dy
        if new_x < 0 or new_y < 0 or new_x >= len(groups) or new_y >= len(
            groups[0]) or groups[new_x][new_y] == now:
          continue

        dist = abs(land[new_x][new_y] - land[i][j])
        weights[(now, groups[new_x][new_y])] = min(
          dist, weights[(now, groups[new_x][new_y])])

  return weights


def find(x, root):
  if x == root[x]:
    return x
  else:
    r = find(root[x], root)
    root[x] = r
    return r


def union(x, y, root):
  x_root = find(x, root)
  y_root = find(y, root)
  root[y_root] = x_root


def kruskal(group_weights, groups):
  sum = 0
  roots = {_: _ for _ in range(1, groups)}

  for (x, y), value in group_weights:
    if find(x, roots) != find(y, roots):
      sum += value
      union(x, y, roots)
    if len(roots.items()) == 1:
      return sum
  return sum


def solution(land, height):
  answer = 0
  row = len(land)
  col = len(land[0])

  groups = [[0 for _ in range(col)] for _ in range(row)]

  group_number = 1
  for i in range(row):
    for j in range(col):
      if groups[i][j] == 0:
        bfs(land, height, groups, i, j, group_number)
        group_number += 1

  groups_weights = get_groups_wieghts(land, groups, height)
  groups_weights = sorted(groups_weights.items(), key=lambda x: x[1])

  answer = kruskal(groups_weights, group_number)
  return answer
