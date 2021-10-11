

# content of test_sample.py
from unittest import TestCase
from unittest.mock import Mock, MagicMock, call

from openAIgym.data_extractor import CachingExtractorDecorator

class CacheTest(TestCase):
    def test_answer(self):
        de = MagicMock()
        cached_de = CachingExtractorDecorator(de)

        cached_de.get_data(1, 3)
        cached_de.get_data(2, 3)
        cached_de.get_data(2, 3)

        self.assertEqual(2, de.get_data.call_count)


if __name__ == "__main__":
    CacheTest().test_answer()

