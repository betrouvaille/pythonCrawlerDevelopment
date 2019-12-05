import redis


client = redis.StrictRedis()
client.lpush('chapter_6', 123)
print(client.llen('chapter_6'))

client.sadd('test_set', 'www.bbbaidu.com')

print(client.scard('test_set'))

