from collections import deque, defaultdict


def solution(n, path, order):
  graph = defaultdict(list)
  order1, order2 = {}, {}
  vis = [0 for _ in range(n)]
  vis[0] = 1
  q = deque()
  q.append(0)
  for u, v in path:
    graph[u].append(v)
    graph[v].append(u)
  for u, v in order:
    order1[u] = v
    order2[v] = u
    if v == 0:
      return False
    if u == 0:
      order1[0] = 0

  while q:
    cur = q.popleft()
    if cur == order1.get(order2.get(cur)):
      vis[cur] = 2
    else:
      for node in graph[cur]:
        if vis[node] == 0:
          q.append(node)
          vis[node] = 1
          if order1.get(node):
            if vis[order1[node]] == 2:
              q.append(order1[node])
              vis[order1[node]] = 1
            order1[node] = 0
  for check in vis:
    if not check:
      return False
  return True
