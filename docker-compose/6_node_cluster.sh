#!/bin/bash
docker-compose -f docker-compose-6-node.yml down &&  docker-compose -f docker-compose-6-node.yml up -d
docker exec -it docker-compose_redis-0_1 redis-cli -h 10.0.0.2 -p 7000 --cluster create 10.0.0.2:7000 10.0.0.3:7001 10.0.0.4:7002 10.0.0.5:7003 10.0.0.6:7004 10.0.0.7:7005 --cluster-replicas 1