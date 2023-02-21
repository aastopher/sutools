import unittest
from unittest.mock import patch
from io import StringIO
import sutools as su

class TestCLIHandler(unittest.TestCase):
    def test_add_command(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            su.cli(['add', '2', '3'])
            self.assertEqual(fake_out.getvalue().strip(), '5')

class TestLogHandler(unittest.TestCase):
    def test_log_handler(self):
        logger = su.log()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            logger.add.info('This is a test message')
            self.assertEqual(fake_out.getvalue().strip(), 'INFO: This is a test message')

if __name__ == '__main__':
    unittest.main()