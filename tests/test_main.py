from unittest import TestCase
from ssh.main import main


class TestMain(TestCase):
    def test_main(self):

        main()

        self.assertTrue(True)
