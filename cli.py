import os
import sys
import time
import logging

import fire
import redis


class RedisCli:
    def __init__(self, redis_host=os.environ.get('REDIS_HOST', 'localhost')):
        print(r"""
________              ________                
\______ \   _______  _\_____  \ ______  ______
 |    |  \_/ __ \  \/ //   |   \\____ \/  ___/
 |    `   \  ___/\   //    |    \  |_> >___ \ 
/_______  /\___  >\_/ \_______  /   __/____  >
        \/     \/             \/|__|       \/ 
                        """)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)
        self.redis_host = redis_host
        self.logger.info('connecting.. to redis %s:6379' % redis_host)

    def get_client(self):
        try:
            redis_client = redis.Redis(host=self.redis_host, port=6379, db=0)

            redis_info = redis_client.info()
            self.logger.info("Redis info: %s - %s | Slave: %s" % (redis_info['role'], redis_info['redis_mode'], str(redis_info.get('slave0', {}))))

            total_keys = redis_client.dbsize()
            self.logger.info('total current redis keys %d' % total_keys)
            return redis_client
        except redis.exceptions.ConnectionError:
            self.logger.error('failed to connect to redis %s:6379' % self.redis_host)
            return None

    def set_keys(self):
        self.logger.info('setting key/val to redis')
        redis_client = self.get_client()
        for x in range(10):
            redis_client.set('devops %d' % x, 'devops %d' % x)
        return True

    def get_all_keys(self):
        redis_client = self.get_client()
        keys = redis_client.keys('*')
        self.logger.info("getting all redis key/values")
        for key in keys:
            val = redis_client.get(key)
            self.logger.info("%s:%s" % (key, val))
        return keys

    def delete_all_keys(self):
        redis_client = self.get_client()
        self.logger.info("deleting all redis keys")
        redis_client.flushdb()
        return True
    
    def watch_keys(self):
        while True:
            time.sleep(1)
            self.get_all_keys()


if __name__ == '__main__':
    fire.Fire(RedisCli)