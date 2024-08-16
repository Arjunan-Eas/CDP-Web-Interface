import redis
from time import time
from redis.exceptions import ConnectionError, DataError, NoScriptError, RedisError, ResponseError

redis_host = "localhost"
stream_key = "mystream"

r=redis.Redis(host="localhost",port=6379) 
print(r.ping())

for x in range(4):
    r.xadd( stream_key, {'CDP_WEB':f'SDUID:MAMA000{x}\0TOPIC:Status\0DATA:Test message {x}\0'} )
