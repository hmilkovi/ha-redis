import os
import sys
import time
import logging

import fire
import redis
import rediscluster


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

        self.redis_setup = os.environ.get('REDIS_HA', 'SENTINEL')

    def get_cluster_client(self):
        startup_nodes = []
        try:
            for entry in self.redis_host.split(','):
                port = entry.split(':')[1]
                addr = entry.split(':')[0]
                startup_nodes.append({"host": addr, "port": port})
            self.logger.info('connecting.. to redis %s' % str(startup_nodes))
            redis_client = rediscluster.RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
            return redis_client
        except Exception as e:
            self.logger.error(e)
            self.logger.error('failed to connect to redis %s:6379' % self.redis_host)
            time.sleep(1)
            return self.get_cluster_client()

    def get_client_sentinel(self):
        try:
            redis_client = redis.Redis(host=self.redis_host, port=6379, db=0)

            total_keys = redis_client.dbsize()
            self.logger.info('total current redis keys %d' % total_keys)

            return redis_client
        except redis.exceptions.ConnectionError as e:
            self.logger.error(e)
            self.logger.error('failed to connect to redis %s:6379' % self.redis_host)
            time.sleep(1)
            return self.get_client()

    def get_client(self):
        if 'CLUSTER' in self.redis_setup:
            return self.get_cluster_client()
        else:
            return self.get_client_sentinel()

    def set_keys(self):
        self.logger.info('setting key/val to redis')
        redis_client = self.get_client()
        try:
            for x in range(10):
                redis_client.set('devops %d' % x, 'devops %d' % x)
            return True
        except Exception as e:
            self.logger.error(e)
            if 'CLUSTER' in self.redis_setup:
                time.sleep(1)
                return self.set_keys()
        return False

    def get_all_keys(self):
        try:
            redis_client = self.get_client()
            keys = redis_client.keys('*')
            self.logger.info("getting all redis key/values")
            for key in keys:
                val = redis_client.get(key)
                self.logger.info("%s:%s" % (key, val))
            return keys
        except Exception as e:
           self.logger.error(e)
           return []

    def delete_all_keys(self):
        try:
            redis_client = self.get_client()
            self.logger.info("deleting all redis keys")
            redis_client.flushdb()
        except Exception as e:
           self.logger.error(e)
           return False
        return True
    
    def watch_keys(self):
        while True:
            time.sleep(1)
            try:
                self.get_all_keys()
            except AttributeError:
                self.logger.error('redis is current down or not ready %s:6379' % self.redis_host)


if __name__ == '__main__':
    fire.Fire(RedisCli)