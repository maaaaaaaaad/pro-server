import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup


def get_kbo_ranking(start_year, end_year):
  url = f"https://ko.wikipedia.org/wiki/KBO_%EB%A6%AC%EA%B7%B8_%EC%97%B0%EB%8F%84%EB%B3%84_%ED%8C%80_%EC%88%9C%EC%9C%84"
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  table = soup.find("table", {"class": "wikitable"})
  rows = table.findAll("tr")[2:]  # 헤더 제외한 행 추출

  ranking = {}
  for row in rows:
    cols = row.findAll("td")
    team_name = cols[1].get_text().strip()
    rank = int(cols[0].get_text().strip())
    year = int(cols[2].get_text().strip())
    if year not in ranking:
      ranking[year] = {}
    ranking[year][team_name] = rank

  return {year: ranking[year] for year in range(start_year, end_year + 1)}


start_year = 2016
end_year = 2020
lotte_giants_rankings = []

kbo_rankings = get_kbo_ranking(start_year, end_year)

for year in range(start_year, end_year + 1):
  lotte_giants_rank = kbo_rankings[year]["롯데 자이언츠"]
  lotte_giants_rankings.append(lotte_giants_rank)

print(lotte_giants_rankings)


def calculate_probability(rankings, threshold):
  total_years = len(rankings)
  successful_years = sum(1 for rank in rankings if rank <= threshold)
  probability = successful_years / total_years
  return probability


threshold = 5
probability = calculate_probability(lotte_giants_rankings, threshold)

print(f"롯데 자이언츠가 가을 야구에 진출할 확률: {probability * 100:.2f}%")
