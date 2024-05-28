import os.path
import unittest
import app
import sys


class portTestCase(unittest.TestCase):
    def test_check_invalid_path_return_exception(self):
        #app.read_comport("xxx.json")
        self.assertRaises(TypeError, 'app.read_comport' "xxx.json")

    def test_check_valid_path_return_dictionary(self):
        data = app.read_comport_preferences("preferences.json")
        self.assertIsNotNone(data)

    def test_crc8_return_valid_byte(self):
        ###b'\x0\x0\x0a\x29\x0\x0\x0\x1\x0\x0' length 10
        return '\xc0'
        ###
    def test_check_convert_reponse_return_valid_response(self):
        pass

    def test_check_create_undefine_command_return_exception(self):
        self.assertRaises(TypeError, 'app.read_comport' "xxx.json")


if __name__ == '__main__':
    unittest.main()
