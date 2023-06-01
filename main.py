def solution(numbers):
  weight_map = [
    [1, 7, 6, 7, 5, 4, 5, 3, 2, 3],
    [7, 1, 2, 4, 2, 3, 5, 4, 5, 6],
    [6, 2, 1, 2, 3, 2, 3, 5, 4, 5],
    [7, 4, 2, 1, 5, 3, 2, 6, 5, 4],
    [5, 2, 3, 5, 1, 2, 4, 2, 3, 5],
    [4, 3, 2, 3, 2, 1, 2, 3, 2, 3],
    [5, 5, 3, 2, 4, 2, 1, 5, 3, 2],
    [3, 4, 5, 6, 2, 3, 5, 1, 2, 4],
    [2, 5, 4, 5, 3, 2, 3, 2, 1, 2],
    [3, 6, 5, 4, 5, 3, 2, 4, 2, 1],
  ]

  dictionary = [[None] * 10 for _ in range(10)]

  dictionary[4][6] = 0
  dictionary[6][4] = 0

  for number in map(int, numbers):
    newDict = [[None] * 10 for _ in range(10)]

    for idx1, row in enumerate(dictionary):
      for idx2, el in enumerate(row):
        if el is not None:
          value = el
          if idx1 == number or idx2 == number:
            resultValue = min(newDict[idx1][idx2], value +
                              1) if newDict[idx1][idx2] else value + 1
            newDict[idx1][idx2] = resultValue
            newDict[idx2][idx1] = resultValue
          else:
            weightValue1 = weight_map[idx1][number]
            weightValue2 = weight_map[idx2][number]

            resultValue1 = min(
              newDict[idx1][number], value +
              weightValue2) if newDict[idx1][number] else value + weightValue2
            resultValue2 = min(
              newDict[idx2][number], value +
              weightValue1) if newDict[idx2][number] else value + weightValue1

            newDict[idx1][number] = resultValue1
            newDict[number][idx1] = resultValue1
            newDict[number][idx2] = resultValue2
            newDict[idx2][number] = resultValue2

    dictionary = newDict
  filtered_dict = [min(filter(None, el)) for el in dictionary if any(el)]
  return min(filtered_dict) if filtered_dict else None
