import redis
from time import time
from redis.exceptions import ConnectionError, DataError, NoScriptError, RedisError, ResponseError

redis_host = "localhost"
stream_key = "mystream"

r=redis.Redis(host="localhost",port=6379) 
print(r.ping())

for x in range(4):
    r.xadd( stream_key, {'CDP_WEB':f'SDUID:MAMA000{x}\x00TOPIC:Status\x00DATA:Test message {x}\x00'} )
