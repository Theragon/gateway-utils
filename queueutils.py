from redis import StrictRedis
from disq import Disque

DEFAULT_ENGINE = 'redis'
CURRENT_ENGINE = 'disque'

DISQUE = 'disque'
REDIS = 'redis'

d = None
r = None

engines = {
	'disque': {'host': 'localhost', 'port': 7711},
	'redis': {'host': 'localhost', 'port': 6379}
}


def connect(engine=None):
	return init_engine(engine)


def init_engine(engine=None):
	if engine is None:
		engine = CURRENT_ENGINE
	host = engines[engine]['host']
	port = engines[engine]['port']
	return init_funcs[engine](host, port)


def init_disque(host, port):
	global d
	d = Disque(host=host, port=port)
	return is_disque_available()


def init_redis(host, port):
	global r
	r = StrictRedis(host=host, port=port, db=0)
	return is_redis_available()


init_funcs = {
		DISQUE: init_disque,
		REDIS: init_redis
	}


def switch_to_engine(engine):
	if engine in engines:
		global CURRENT_ENGINE
		CURRENT_ENGINE = engine
		print('switching to ' + CURRENT_ENGINE)
		return init_engine(CURRENT_ENGINE)


def is_available(engine=None):
	if engine is None:
		engine = CURRENT_ENGINE
	print('current engine: ' + engine)
	return availability_funcs[engine]()


def is_disque_available():
	print('is disque available')
	if d is None:
		return False
	return d.hello() is not None


def is_redis_available():
	print('is redis available')
	if r is None:
		return False
	return r.ping() is not None


availability_funcs = {
		DISQUE: is_disque_available,
		REDIS: is_redis_available
	}


def enqueue(queue, msg, timeout=0):
	return {
		DISQUE: enqueue_disque,
		REDIS: enqueue_redis
	}[CURRENT_ENGINE](queue, msg, timeout)


def enqueue_disque(queue, msg, timeout=0):
	d.addjob(queue, msg)


def enqueue_redis(queue, msg, timeout=0):
	r.rpush(queue, msg)


def dequeue(queue, timeout=None):
	return {
		DISQUE: dequeue_disque,
		REDIS: dequeue_redis
	}[CURRENT_ENGINE](queue, timeout)


def dequeue_disque(queue, timeout=0):
	rsp = d.getjob(queue)
	d.ackjob(rsp[0][1])
	return rsp[0][2]


def dequeue_redis(queue, timeout):
	rsp = r.blpop(queue, timeout=0)
	return rsp[1]
