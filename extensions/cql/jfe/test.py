from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError
import unittest
import json
import glob

valid_fixtures = glob.glob("fixtures/valid/*.json")
invalid_fixtures = glob.glob("fixtures/invalid/*.json")


class TestSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("schema.json", "r") as f:
            cls.schema = json.load(f)
            Draft7Validator.check_schema(cls.schema)
            cls.validator = Draft7Validator(cls.schema)

    def test_valid(self):
        for path in valid_fixtures:
            with self.subTest(path=path):
                with open(path) as f:
                    fixture = json.load(f)
                self.validator.validate(fixture)

    def test_invalid(self):
        for path in invalid_fixtures:
            with self.subTest(path=path):
                with open(path) as f:
                    fixture = json.load(f)
                with self.assertRaises(ValidationError):
                    self.validator.validate(fixture)

    def test_examples(self):
        definitions = self.schema["definitions"]
        for id, entry in definitions.items():
            examples = entry.get("examples")
            if not examples:
                continue
            with self.subTest(id=id):
                for example in examples:
                    self.validator.validate(example)

    def test_title_matches_operator(self):
        definitions = self.schema["definitions"]
        for id, entry in definitions.items():
            title = entry.get("title")
            if not title:
                continue
            with self.subTest(id=id):
                items = entry.get("items")
                self.assertIsNotNone(items)
                self.assertGreater(len(items), 0)

                enum = items[0].get("enum")
                self.assertIsNotNone(enum)
                self.assertEqual(len(enum), 1)

                self.assertEqual(enum[0], title)


if __name__ == "__main__":
    unittest.main()

