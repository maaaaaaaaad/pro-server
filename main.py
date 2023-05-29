import heapq

INF = int(1e9)


def dijkstra(start, graph, distance):
  q = []
  heapq.heappush(q, (0, start, 0))
  distance[start][0] = 0
  while q:
    dist, now, trap_state = heapq.heappop(q)
    if distance[now][trap_state] < dist:
      continue
    for i in graph[now][trap_state]:
      cost = dist + i[1]
      if cost < distance[i[0]][i[2]]:
        distance[i[0]][i[2]] = cost
        heapq.heappush(q, (cost, i[0], i[2]))


def solution(n, start, end, roads, traps):
  start -= 1
  end -= 1
  traps = [x - 1 for x in traps]

  graph = [[[], []] for _ in range(n)]
  for road in roads:
    x, y, cost = road
    x -= 1
    y -= 1

    graph[x][0].append((y, cost, [0, 1][y in traps]))
    graph[y][1].append((x, cost, [0, 1][x in traps]))
    graph[y][0].append((x, cost, [0, 1][x in traps]))
    graph[x][1].append((y, cost, [0, 1][y in traps]))

  distance = [[INF] * 2 for _ in range(n)]

  dijkstra(start, graph, distance)

  return min(distance[end])
