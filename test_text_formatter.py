import unittest
from text_formatter import format_text_sentence, format_text_upper, format_text_lower, format_text_title, format_text

class TestTextFormatter(unittest.TestCase):
    def test_format_text_sentence(self):
        input_text = "       this is an example       sentence!     previous sentence is an example sentence.          "
        expected = "This is an example sentence! Previous sentence is an example sentence."
        result = format_text_sentence(input_text)
        self.assertEqual(result, expected)

    def test_format_text_upper(self):
        input_text = "       this is an example        sentence?     previous sentence is an example sentence.          "
        expected = "THIS IS AN EXAMPLE SENTENCE? PREVIOUS SENTENCE IS AN EXAMPLE SENTENCE."
        result = format_text_upper(input_text)
        self.assertEqual(result, expected)

    def test_format_text_lower(self):
        input_text = "      THIS IS AN EXAMPLE SENTENCE.    PREVIOUS SENTENCE IS AN EXAMPLE SENTENCE.     "
        expected = "this is an example sentence. previous sentence is an example sentence."
        result = format_text_lower(input_text)
        self.assertEqual(result, expected)

    def test_format_text_title(self):
        input_text = "       this is an example       sentence.     previous sentence is an example sentence!          "
        expected = "This Is An Example Sentence. Previous Sentence Is An Example Sentence!"
        result = format_text_title(input_text)
        self.assertEqual(result, expected)

    def test_format_text_valid(self):
        input_text = "       this is an example       sentence!     previous sentence is an example sentence.          "
        format_type = "" # no format_type provided = defaults to sentence type
        expected = "This is an example sentence! Previous sentence is an example sentence.", None
        result = format_text(input_text, format_type)
        self.assertEqual(result, expected)

    def test_format_text_invalid(self):
        input_text = "       this is an example       sentence!     previous sentence is an example sentence.          "
        format_type = "emojis" # invalid format_type
        expected = "", "Invalid format_type: 'emojis'. Valid options: 'sentence', 'upper', 'lower', 'title'"
        result = format_text(input_text, format_type)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()