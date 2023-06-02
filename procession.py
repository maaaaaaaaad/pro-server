from collections import deque


def solution(rc, operations):
  r_len, c_len = len(rc), len(rc[0])

  rows = deque(deque(row[1:-1]) for row in rc)
  out_cols = [
    deque(rc[r][0] for r in range(r_len)),
    deque(rc[r][c_len - 1] for r in range(r_len))
  ]

  for operation in operations:
    if operation[0] == "S":
      rows.appendleft(rows.pop())
      out_cols[0].appendleft(out_cols[0].pop())
      out_cols[1].appendleft(out_cols[1].pop())

    else:
      rows[r_len - 1].append(out_cols[1].pop())
      out_cols[0].append(rows[r_len - 1].popleft())
      rows[0].appendleft(out_cols[0].popleft())
      out_cols[1].appendleft(rows[0].pop())

  answer = []
  for r in range(r_len):
    answer.append([])
    answer[r].append(out_cols[0][r])
    answer[r].extend(rows[r])
    answer[r].append(out_cols[1][r])

  return answer
