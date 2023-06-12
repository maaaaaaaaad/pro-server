import sys

sys.setrecursionlimit(10000)


def solution(k, room_number):
  rooms = dict()
  for num in room_number:
    chk_in = find_emptyroom(num, rooms)
  return list(rooms.keys())


def find_emptyroom(chk, rooms):
  if chk not in rooms.keys():
    rooms[chk] = chk + 1
    return chk
  empty = find_emptyroom(rooms[chk], rooms)
  rooms[chk] = empty + 1
  return empty
