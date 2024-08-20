"""
Use this for testing the redis_web_process. I used Docker to run redis-server, which is 
required to make this work on Windows.

This code just represents another user interacting with the Redis stream, so you can send
messages back and forth.
"""

import redis
from time import time

redis_host = "localhost"
stream_key = "mystream"

r=redis.Redis(host="localhost",port=6379) 
print(r.ping())

for x in range(4):
    r.xadd( stream_key, {'CDP_WEB':f'SDUID:MAMA000{x}\0TOPIC:Status\0DATA:Test message {x}\0'} )
