def solution(a):
  MOD = 10**7 + 19
  R, C = len(a), len(a[0])
  pascal = [[0] * (R + 1) for _ in range(R + 1)]

  def comb(n, c):
    if n == c or c == 0:
      pascal[n][c] = 1
      return 1
    if pascal[n][c] > 0:
      return pascal[n][c] % MOD
    pascal[n][c] = (comb(n - 1, c - 1) + comb(n - 1, c)) % MOD
    return pascal[n][c]

  for i in range(R + 1):
    for j in range(i + 1):
      comb(i, j)
  cnt = []
  for j in range(C):
    o = 0
    for i in range(R):
      if a[i][j] == 1:
        o += 1
    cnt.append(o)
  dp = [[0 for _ in range(R + 1)] for _ in range(C + 1)]
  dp[1][R - cnt[0]] = pascal[R][R - cnt[0]]
  for c in range(1, C):
    for r in range(R + 1):
      if dp[c][r] == 0:
        continue
      for o in range(cnt[c] + 1):
        nxt = (r - o) + (cnt[c] - o)
        if nxt > R or r < o:
          continue
        case = (pascal[r][o] * pascal[R - r][cnt[c] - o]) % MOD
        dp[c + 1][nxt] += (dp[c][r] * case) % MOD
  return dp[C][R]
