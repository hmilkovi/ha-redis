import unittest
import redis
import os
import time

from cli import RedisCli

class IntegrationTestRedis(unittest.TestCase):

    def test_set_keys(self):
        cli = RedisCli()
        self.assertTrue(cli.set_keys())

    def test_get_all_keys(self):
        cli = RedisCli()
        cli.delete_all_keys()
        for x in range(10):
            cli.set_keys()
        all_keys = cli.get_all_keys()
        self.assertEqual(len(all_keys), 10)
        self.assertEqual(type(all_keys), list)

    def test_delete_all_keys(self):
        cli = RedisCli()
        self.assertTrue(cli.delete_all_keys())
        self.assertEqual(len(cli.get_all_keys()), 0)
    
    def test_fail_connect(self):
        cli = RedisCli(redis_host="devops.devops")
        self.assertEqual(cli.get_client(), None)

if __name__ == '__main__':
    time.sleep(4)
    unittest.main()