import requests
import logging
from bs4 import BeautifulSoup as BS  # type: ignore
import json

# Конфигурация
OUTPUT_FILE = "tasks.json"
TIMEOUT = 10

# URL для парсинга
URL = "https://freelance.habr.com/tasks?q=python"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_soup(url):
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return BS(response.text, "html.parser")
    except requests.RequestException as e:
        logging.error(f"Ошибка при получении страницы {url}: {e}")
        return None


def get_pagination(soup):
    if not soup:
        return None
    pagination = soup.find("div", class_="pagination")
    if pagination:
        pages = pagination.find_all("a")
        if pages:
            try:
                last_page = int(pages[-2].text)
                return last_page
            except (ValueError, IndexError):
                return None
    return None


def get_tasks(soup):
    if not soup:
        return

    try:
        articles = soup.find_all("article")

        for article in articles:
            try:
                a = article.find("a")
                if not a:
                    continue

                title = a.text.strip()
                url = URL.rsplit("/", 1)[0] + a.get("href", "")
                price_count = article.find("span", class_="count")
                price = price_count.text.strip() if price_count else "договорная"
                tasks.append({"title": title, "url": url, "price": price})
            except AttributeError as e:
                logging.warning(f"Ошибка при обработке задания: {e}")
    except Exception as e:
        logging.error(f"Ошибка при получении заданий: {e}")


def save_data(data):
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logging.info(f"Данные сохранены в {OUTPUT_FILE}")
    except IOError as e:
        logging.error(f"Ошибка при сохранении файла: {e}")


def main():
    global tasks
    tasks = []
    base_url = URL
    soup = get_soup(url=base_url)
    if soup:
        pagination = get_pagination(soup)
        if pagination:
            for page in range(1, pagination + 1):
                page_url = f"{base_url}?page={page}"
                page_soup = get_soup(url=page_url)
                get_tasks(page_soup)
        else:
            get_tasks(soup)
    save_data(tasks)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Bot остановлен")
