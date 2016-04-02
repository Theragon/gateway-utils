# A wrapper module for different queue systems
from redisengine import RedisEngine as redis
from disqueengine import DisqueEngine as disque

DISQUE = 'disque'
REDIS = 'redis'

DEFAULT_ENGINE = DISQUE
CURRENT_ENGINE = DISQUE

q = None

engines = {
	DISQUE: {'host': 'localhost', 'port': 7711},
	REDIS: {'host': 'localhost', 'port': 6379}
}


def connect(engine=None):
	global q
	global CURRENT_ENGINE
	if engine is None:
		engine = DEFAULT_ENGINE
	CURRENT_ENGINE = engine
	constructor = globals()[engine]
	q = constructor()
	return q.connect()


def switch_to_engine(engine):
	if engine in engines:
		#global CURRENT_ENGINE
		#CURRENT_ENGINE = engine
		print('switching to ' + engine)
		return connect(engine)


def is_available(engine=None):
	if engine is None:
		engine = CURRENT_ENGINE
	print('current engine: ' + engine)
	return q.is_available()


def enqueue(queue, msg, timeout=0):
	return q.enqueue(queue, msg, timeout)


def dequeue(queue, timeout=0):
	return q.dequeue(queue, timeout)


def get_from_queues(queues, timeout=0):
	return q.get_from_queues(queues, timeout)


def flush_all():
	return q.flush_all()
