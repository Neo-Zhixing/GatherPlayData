from .. import redis, mongo, memcached

def dummy_encoder_decoder(value):
    return value

class Cached:
    enable_redis = False
    enable_memcached = True
    enable_mongodb = True

    def __init__(self, prefix, ttl=3600, encoder=dummy_encoder_decoder, decoder=dummy_encoder_decoder):
        self.prefix = prefix
        self.ttl = ttl
        self.encode = encoder
        self.decode = decoder
    
    @property
    def db(self):
        return mongo[self.prefix]

    def key(self, key):
        return self.prefix + ':' + key

    def set(self, key, value):
        if self.enable_redis:
            redis.setex(self.key(key), self.ttl, self.encode(value))
        if self.enable_memcached:
            memcached.set(self.key(key), self.encode(value), time=self.ttl)
        if self.enable_mongodb:
            self.db.update(
                { 'id': key }, # query
                { 'id': key, 'value': value},
                True # upsert
            )

    
    def get(self, key):
        if self.enable_redis:
            theData = redis.pipeline().get(self.key(key)).expire(self.key(key), self.ttl).execute()[0]
            if theData:
                return self.decode(theData.decode())
        elif self.enable_memcached:
            theData = memcached.get(self.key(key))
            if theData:
                return self.decode(theData)
        if self.enable_mongodb:
            theData = self.db.find_one({ 'id': key })
            if theData:
                theData = theData['value']
                if self.enable_redis:
                    redis.setex(self.key(key), self.ttl, self.encode(theData))
                if self.enable_memcached:
                    memcached.set(self.key(key), self.encode(theData), time=self.ttl)
                return theData
        return None
