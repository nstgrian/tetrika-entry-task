import unittest
from unittest.mock import patch
import tempfile
from collections import Counter
from pathlib import Path
from solution import WikipediaCategoryFetcher


class TestWikipediaCategoryFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = WikipediaCategoryFetcher(
            api_url="https://ru.wikipedia.org/w/api.php",
            category="Категория:Животные_по_алфавиту",
            title_storage_file="beasts.txt",
            output_file="beasts.csv"
        )

    @patch('requests.Session.get')
    def test_fetch_category_members(self, mock_get):
        sample_response = {
            'batchcomplete': "",
            'continue': {
                'cmcontinue': "page|12345",
                'continue': "-||"
            },
            'query': {
                'categorymembers': [
                    {'pageid': 1, 'ns': 0, 'title': "Акула"},
                    {'pageid': 2, 'ns': 0, 'title': "Белка"}
                ]
            }
        }
        mock_get.return_value.json.return_value = sample_response
        mock_get.return_value.raise_for_status = lambda: None

        result = self.fetcher.fetch_category_members()
        self.assertEqual(result, sample_response)

    def test_save_to_file(self):
        with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8') as tmpfile:
            self.fetcher.title_storage_file = Path(tmpfile.name)
            titles = ["Акула", "Белка"]
            self.fetcher.save_to_file(titles)
            tmpfile.seek(0)
            content = tmpfile.read()
            self.assertEqual(content, "Акула\nБелка\n")

    def test_count_entries(self):
        with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8') as tmpfile:
            tmpfile.write("Акула\nБелка\nБизон\nВолк\n")
            tmpfile.flush()
            self.fetcher.title_storage_file = Path(tmpfile.name)

            counter = self.fetcher.count_entries()
            self.assertEqual(counter['А'], 1)
            self.assertEqual(counter['Б'], 2)
            self.assertEqual(counter['В'], 1)

    @patch.object(WikipediaCategoryFetcher, 'count_entries')
    def test_export_results(self, mock_count_entries):
        counter = Counter({'А': 1, 'Б': 2})
        mock_count_entries.return_value = counter
        with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8') as tmpfile:
            self.fetcher.output_file = Path(tmpfile.name)
            self.fetcher.export_results()
            tmpfile.seek(0)
            content = tmpfile.read()
            expected = "Letter,Count\nА,1\nБ,2\n"
            self.assertEqual(content, expected)


if __name__ == '__main__':
    unittest.main()
