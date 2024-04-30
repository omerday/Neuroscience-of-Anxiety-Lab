import unittest
from medoc_api.Utilities import converters, temp_converter


class converterTestCase(unittest.TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)

    def setUp(self):
        self.case1 = [0x37, 0x00, 0x15, 0x25]
        self.case2 = [0xff, 0xee, 0xdd, 0xaa]
        self.case32 = [0x61, 0x20, 0x00, 0x30, 0x23]
        self.get_version_response = [0x37, 0x00, 0x15, 0x25, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x0b, 0x56, 0x53, 0x41,
                                     0x20, 0x32, 0x2e, 0x30, 0x2e, 0x30, 0x2e, 0x37]
        self.short = 3700
        self.ushort = 30000
        self.int = 2000000
        self.m_temperature = 32

    def test_check_convert_response_return_valid_response1(self):
        self.assertEqual(0x3700, converters.to_u_int_16_ex(self.case1, 0))
        self.assertEqual(0x0015, converters.to_u_int_16_ex(self.case1, 1))
        self.assertEqual(0x1525, converters.to_u_int_16_ex(self.case1, 2))
        # self.assertRaises(Main.to_u_int_16_ex(self.case1, 4),
        with self.assertRaises(IndexError) as context:
            converters.to_u_int_16_ex(self.case1, 4)

    def test_byte_converter_to_int_16_return_valid(self):
        self.assertEqual(0x3700, converters.to_int_16(self.case1, 0))
        self.assertEqual(0x0015, converters.to_int_16(self.case1, 1))
        self.assertEqual(0x1525, converters.to_int_16(self.case1, 2))
        # self.assertRaises(Main.to_u_int_16_ex(self.case1, 4),
        with self.assertRaises(IndexError) as context:
            converters.to_int_16(self.case1, 3)
        with self.assertRaises(IndexError) as context:
            converters.to_int_16(self.case1, 4)

    def test_byte_converter_to_uint_16_return_valid(self):
        """
        Testing ByteConverter.ToUInt16
        :return:
        """
        self.assertEqual(0xFFEE, converters.to_uint_16(self.case2, 0))
        self.assertEqual(0xEEDD, converters.to_uint_16(self.case2, 1))
        self.assertEqual(0xDDAA, converters.to_uint_16(self.case2, 2))
        # self.assertRaises(Main.to_u_int_16_ex(self.case1, 4),
        with self.assertRaises(IndexError) as context:
            converters.to_int_16(self.case1, 3)
        with self.assertRaises(IndexError) as context:
            converters.to_int_16(self.case1, 4)

    def test_byte_converter_to_uint_32_return_valid(self):
        """
        Testing ByteConverter.ToUInt32
        :return:
        """
        self.assertEqual(0x61200030,
                         converters.to_uint_32(self.case32, 0))  # [0x61, 0x20, 0x00, 0x30, 0x23] -> 0x61200030
        self.assertEqual(0x20003023,
                         converters.to_uint_32(self.case32, 1))  # [0x61, 0x20, 0x00, 0x30, 0x23] ->0x20003023
        # self.assertRaises(Main.to_u_int_16_ex(self.case1, 4),
        with self.assertRaises(IndexError) as context:
            converters.to_uint_32(self.case32, 2)
        with self.assertRaises(IndexError) as context:
            converters.to_uint_32(self.case32, 3)

    def test_byte_converter_to_string_return_valid_string(self):
        """
        #TODO need realize
        :return:
        """

    def test_get_bytes_return_valid(self):
        self.assertEqual([0x74, 0x0e], list(converters.get_bytes16(self.short)))
        self.assertEqual([0x30, 0x75], list(converters.get_bytes16(self.ushort)))
        self.assertEqual([0x80, 0x84, 0x1e, 0x00], list(converters.get_bytes32(self.int)))

    def test_pc2tcu_return_valid_short(self):
        self.assertEqual(3200, temp_converter.pc2tcu(self.m_temperature))


if __name__ == '__main__':
    unittest.main()
