import requests
from bs4 import BeautifulSoup as BS # type: ignore

def get_soup(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_doc = response.text

        soup = BS(html_doc, "html.parser")
    return soup


def get_pagination(soup):
    pagination = soup.find("div", class_="pagination")
    if pagination:
        last_page = pagination.find_all("a")[-2].text
        return last_page


def get_tasks(soup):
    articles = soup.find_all("article")

    for article in articles:
        a = article.find("a")
        title = a.text
        url = f"https://freelance.habr.com{a['href']}"
        price_count = article.find("span", class_="count")
        price = price_count.text if price_count else "договорная"
        tasks.append({"title": title, "url": url, "price": price})


if __name__ == "__main__":

    url = "https://freelance.habr.com/tasks?q=python"

    tasks = []

    soup = get_soup(url=url)
    if soup:
        pagination = get_pagination(soup)
        if pagination:
            for page in range(int(pagination)):
                url = f"https://freelance.habr.com/tasks?q=python"
                soup = get_soup(url=url)
                get_tasks(soup)
        else:
            get_tasks(soup)
    with open("tasks.json", "w", encoding="utf-8") as f:
        import json

        json.dump(tasks, f, indent=4, ensure_ascii=False)
