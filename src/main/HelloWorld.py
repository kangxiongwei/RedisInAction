import redis

conn = redis.Redis()
conn.set("hello", "world")
res = conn.get("hello")
print res