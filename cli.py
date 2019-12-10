import os
import sys
import logging

import fire
import redis


class RedisCli:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        redis_host = os.environ.get('REDIS_HOST', 'localhost')
        self.logger.info('connecting to redis %s:6379' % redis_host)
        self.redis_client = redis.Redis(host=redis_host, port=6379, db=0)
        redis_info = self.redis_client.info()
        self.logger.info("Redis info: %s - %s | Slave: %s" % (redis_info['role'], redis_info['redis_mode'], str(redis_info.get('slave0', {}))))
        total_keys = self.redis_client.dbsize()
        self.logger.info('total current redis keys %d' % total_keys)

    def set_keys(self):
        self.logger.info('setting key/val to redis')
        for x in range(10):
            self.redis_client.set('devops %d' % x, 'devops %d' % x)

    def get_all_keys(self):
        keys = self.redis_client.keys('*')
        self.logger.info("getting all redis key/values")
        for key in keys:
            val = self.redis_client.get(key)
            self.logger.info("%s:%s" % (key, val))

    def delete_all_keys(self):
        self.logger.info("deleting all redis keys")
        self.redis_client.flushdb()


if __name__ == '__main__':
    fire.Fire(RedisCli)