import unittest
import connector


# test on create com port
class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.valid_preferences_path = "../preferences.json"
        self.invalid_preferences_path = "pref.json"

    def test_create_connector_with_valid_path_return_serial_object(self):
        serial = connector.connector(self.valid_preferences_path)
        self.assertIsNotNone(serial)  # add assertion here

    def test_create_connector_with_invalid_path_return_exception(self):
        with self.assertRaises(Exception) as context:
            connector.connector(self.invalid_preferences_path)


if __name__ == '__main__':
    unittest.main()
