import unittest

from tython.src.main.path.path import InternalPath


class TestPath(unittest.TestCase):

    def setUp(self):
        self.non_existent_path = InternalPath("non_existent_path.txt")

        self.write_path = InternalPath("tython/src/test/resources/paths/write_path.txt")
        self.read_path = InternalPath("tython/src/test/resources/paths/read_path.txt")

        self.read_json_path = InternalPath("tython/src/test/resources/paths/read_json.json")
        self.write_json_path = InternalPath("tython/src/test/resources/paths/write_json.json")

    def test_read_text(self):
        self.assertEqual(self.read_path.read_text(), "Read text test")

    def test_read_json(self):
        self.assertEqual(self.read_json_path.read_json(), {"read": "json"})

    def test_write_text(self):
        self.write_path.write_text("Write text test")
        self.assertEqual(self.write_path.read_text(), "Write text test")
        self.write_path.delete()

    def test_write_json(self):
        self.write_json_path.write_json({"write": "json"})
        self.assertEqual(self.write_json_path.read_json(), {"write": "json"})
        self.write_json_path.delete()

    def test_read_non_existent_path(self):
        self.assertIsNone(self.non_existent_path.read_text())

    def test_delete(self):
        self.write_path.write_text("Write text test")
        self.write_path.delete()
        self.assertIsNone(self.write_path.read_text())

        self.write_json_path.write_json({"write": "json"})
        self.write_json_path.delete()
        self.assertIsNone(self.write_json_path.read_json())
