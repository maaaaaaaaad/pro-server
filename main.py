import heapq

INF = int(1e9)


def solution(n, start, end, roads, traps):
  graph = [[INF] * (n + 1) for _ in range(n + 1)]
  trap_dict = {trap: [] for trap in traps}
  rev_trap_dict = {trap: [] for trap in traps}
  trap_state = [0] * (n + 1)
  for road in roads:
    P, Q, S = road
    graph[P][Q] = min(graph[P][Q], S)
    if Q in traps:
      trap_dict[Q].append(P)
    if P in traps:
      rev_trap_dict[P].append(Q)

  q = []
  heapq.heappush(q, (0, start, tuple(trap_state)))
  dist = {tuple(trap_state): [INF] * (n + 1)}
  dist[tuple(trap_state)][start] = 0
  while q:
    time, now, trap_state = heapq.heappop(q)
    trap_state = list(trap_state)
    if time > dist[tuple(trap_state)][now]:
      continue
    if now in traps:
      for node in trap_dict[now]:
        graph[now][node], graph[node][now] = graph[node][now], graph[now][node]
      for node in rev_trap_dict[now]:
        graph[now][node], graph[node][now] = graph[node][now], graph[now][node]
      trap_state[now] = 1 if trap_state[now] == 0 else 0
    for i in range(1, n + 1):
      cost = time + graph[now][i]
      if cost < dist[tuple(trap_state)][i]:
        dist[tuple(trap_state)][i] = cost
        heapq.heappush(q, (cost, i, tuple(trap_state)))
  return min(dist[tuple(trap_state)][end] for trap_state in dist.values())
