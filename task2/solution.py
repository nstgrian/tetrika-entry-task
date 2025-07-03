import logging
import time
import requests
from requests.exceptions import RequestException
from collections import Counter
from pathlib import Path

LETTERS_SORTED = "АаБбВвГгЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя" + \
                 "AaBbCcDdEeFfGgHhIiGgKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("fetcher.log"), logging.StreamHandler()]
)


class WikipediaCategoryFetcher:
    def __init__(self, api_url: str, category: str, title_storage_file: str, output_file: str):
        self.api_url = api_url
        self.category = category
        self.title_storage_file = Path(title_storage_file)
        self.output_file = Path(output_file)
        self.session = requests.Session()

    def fetch_category_members(self, cmcontinue: str = None) -> dict | None:
        params = {
            "action": "query",
            "cmtitle": self.category,
            "cmlimit": 500,
            "list": "categorymembers",
            "format": "json",
            "cmtype": "page"
        }
        if cmcontinue:
            params["cmcontinue"] = cmcontinue

        try:
            response = self.session.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            logging.error(f"Failed to fetch API data: {e}")
            return None

    def save_to_file(self, titles: list[str]) -> None:
        try:
            with self.title_storage_file.open('a', encoding='utf-8') as file:
                for title in titles:
                    file.write(f"{title}\n")
            logging.info(f"Saved {len(titles)} titles to {self.title_storage_file}")
        except IOError as e:
            logging.error(f"Failed to write to {self.title_storage_file}: {e}")

    def count_entries(self) -> Counter | None:
        if not self.title_storage_file.exists():
            logging.warning(f"Storage file {self.title_storage_file} does not exist.")
            return Counter()
        try:
            with self.title_storage_file.open('r', encoding='utf-8') as file:
                counter = Counter()
                for line in file:
                    if line.strip():
                        counter.update(line[0])
                return counter
        except IOError as e:
            logging.error(f"Failed to read file {self.title_storage_file}: {e}")
            return None

    def export_results(self) -> None:
        counter = self.count_entries()
        if counter is None:
            logging.error("No counter data to export.")
            return
        try:
            with self.output_file.open('w', encoding='utf-8') as file:
                file.write("Letter,Count\n")
                for letter in LETTERS_SORTED:
                    if letter in counter:
                        file.write(f"{letter},{counter[letter]}\n")
            logging.info(f"Results exported to {self.output_file}")
        except IOError as e:
            logging.error(f"Failed to write to file {self.output_file}: {e}")

    def fetch(self) -> None:
        cmcontinue = None
        total_pages = 0
        try:
            with self.title_storage_file.open('w', encoding='utf-8') as file:
                file.write("")
            logging.info(f"Title storage file {self.title_storage_file} cleared")
        except IOError as e:
            logging.error(f"Failed to clear {self.title_storage_file}: {e}")
            return

        while True:
            logging.info(f"Fetching batch (cmcontinue: {cmcontinue or 'initial'})")
            data = self.fetch_category_members(cmcontinue)
            if not data or 'query' not in data or 'categorymembers' not in data['query']:
                logging.error("Invalid API response or no results.")
                break

            pages = data['query']['categorymembers']
            titles = [page['title'] for page in pages if 'title' in page]
            self.save_to_file(titles)
            total_pages += len(titles)
            logging.info(f"Processed {len(titles)} pages (total: {total_pages})")

            if 'continue' not in data or 'cmcontinue' not in data['continue']:
                logging.info("No more pages to fetch.")
                break

            cmcontinue = data['continue']['cmcontinue']
            time.sleep(0.1)

        logging.info(f"Fetching completed. Total page titles retrieved: {total_pages}")


if __name__ == '__main__':
    fetcher = WikipediaCategoryFetcher(
        api_url="https://ru.wikipedia.org/w/api.php",
        category="Категория:Животные_по_алфавиту",
        title_storage_file="beasts.txt",
        output_file="beasts.csv"
    )
    fetcher.fetch()
    fetcher.export_results()
