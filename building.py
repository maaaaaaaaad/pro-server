import sys

sys.setrecursionlimit(1000000)
cache = {(1, 1): 1}


def solve(i, j):
  if i == 0 or j == 0:
    return 0

  if (i, j) in cache:
    return cache[(i, j)]

  v = solve(i - 1, j - 1) + solve(i - 1, j) * 2 * (i - 1)
  cache[(i, j)] = v % 1000000007

  return cache[(i, j)]


def solution(n, count):
  return solve(n, count)
