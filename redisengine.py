from queueengine import QueueEngine
from redis import StrictRedis


class RedisEngine(QueueEngine):
	"""docstring for RedisEngine"""
	def __init__(self):
		super(RedisEngine, self).__init__()
		self.r = None
		self.host = 'localhost'
		self.port = 6379

	def connect(self):
		self.r = StrictRedis(self.host, self.port, db=0)
		return self.is_available()

	def is_available(self):
		print('is redis available')
		if self.r is None:
			return False
		return self.r.ping() is not None

	def enqueue(self, queue, msg, timeout=0):
		self.r.rpush(queue, msg)

	def dequeue(self, queue, timeout):
		rsp = self.r.blpop(queue, timeout=0)
		return rsp[1]
