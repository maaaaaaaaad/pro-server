from heapq import heappop, heappush


def solution(n, start, end, roads, traps):
  INF = int(1e9)
  start -= 1
  end -= 1
  graph = [[[] for _ in range(n)] for _ in range(2)]
  trap_set = set(traps)

  for x, y, cost in roads:
    x -= 1
    y -= 1
    graph[0][x].append((y, cost))
    graph[1][y].append((x, cost))
    if x + 1 in trap_set:
      graph[1][x].append((y, cost))
    if y + 1 in trap_set:
      graph[0][y].append((x, cost))

  dist = [[INF] * n for _ in range(1 << len(trap_set))]
  trap_dict = {trap - 1: i for i, trap in enumerate(traps)}
  state = sum(1 << trap_dict[trap - 1] for trap in traps if trap - 1 < start)
  dist[state][start] = 0
  queue = [(0, start, state)]

  while queue:
    time, node, state = heappop(queue)
    if node == end:
      return time
    trap_here = (1 << trap_dict[node]) if node + 1 in trap_set else 0
    for next_node, cost in graph[state >> trap_dict[node]
                                 & 1 if trap_here else state & 1 ^ 1][node]:
      next_state = (state ^ trap_here) if (next_node +
                                           1 in trap_set) else state
      if time + cost < dist[next_state][next_node]:
        dist[next_state][next_node] = time + cost
        heappush(queue, (time + cost, next_node, next_state))
  return -1
