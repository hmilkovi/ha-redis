[![Build Status](https://travis-ci.com/hmilkovi/ha-redis.svg?branch=master)](https://travis-ci.com/hmilkovi/ha-redis)

# HA Redis Deployement


Requirements:
1. Docker
2. docker-compose >= v1.24.1
3. Python 3.8

### There are two solutions for HA Redis

1. Master->Slave + Sentinel
This approach is fine as long as we can take possibility of some data loss due to asyc replication master->slave

2. 6 node Redis Cluster
There are 3 master nodes and 3 slave nodes

### Usage docker-compose via Makefile

I have made a Makefile to handle tipical lifting of both solutions:
```
$ cd docker-compose
$ make help
help:           Show this help.
up-sentinel:    Lift up docker-compose redis master-slave with sentinel
down-sentinel:  Down docker-compose redis master-slave with sentinel
up-cluster:     Lift up docker-compose redis 6 node cluster
down-cluster:   Down docker-compose redis 6 node cluster
```

### Where is what?
```
docker-compose:
- cluster-config-X.conf - configuration for each Redis instance in 6 node setup
- prom-cluster.yml - prometheus redis cluster conf
- prom-sentinel.yml - prometheus redis with sentinel conf
- Makefile - described above
- haproxy.cfg - haproxy config for redis with sentinel
- haproxy_6_nodes.cfg - haproxy config for 6 node redis cluster
- docker-compose.yml - docker-compose for redis with sentinel solution
- docker-compose-6-node.yml - docker-compose for redis 6 node setup
-- provisioning-grafana
---- dashboards - inital Grafana dashboards inside docker
---- datasources - default prometheus datasource setup fro Grafana in docker
```

### Python simple Redis cli tool

Before running it please lift up one of redis setups

```
Usage: cli.py - <command>
available commands:
    delete_all_keys - deletes all key/val inside redis
    get_all_keys - logs all key/val inside redis
    set_keys - sets 10 keys inside redis
    watch_keys - watch and print all keys inside redis every second

Example: python cli.py get_all_keys
```

For integration testing lift up redis master-slave + sentinel solution and ` python test.py `.


#### Notice
Python cli tool doesn't work with 6 node cluster if it's outside Docker network.

Reason is that cluster master node may send MOVED to other master node and it can't be reached.

For this reason every docker-compose deployment as ` redis-script-python ` so we demonstrate it's working
as a service.

### Monitoring
Both solutions have monitoring setup:
- redis_exporter
- prometheus
- grafana

It's implemented inside docker-compose ymls.



### Docker Compose service access local
1. 127.0.0.1:8080 - HAproxy
2. 127.0.0.1:3000 - Grafana
3. 127.0.0.1:9090 - Prometheus

### Other stuff
Docker images:
```
https://hub.docker.com/r/hrvoje6/redis-script-python
```

Docker Hub builds Docker image for Python script on commit.

Travis runs tests on commit:
```
https://travis-ci.com/hmilkovi/ha-redis
```