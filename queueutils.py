# A wrapper module for different queue systems

import os
import imp
import logging
import parseutils as pu

log = logging.getLogger(__name__)

DISQUE = 'disque'
REDIS = 'redis'

DEFAULT_ENGINE = DISQUE
CURRENT_ENGINE = DISQUE

q = None

engines = {
	DISQUE: {'host': 'localhost', 'port': 7711},
	REDIS: {'host': 'localhost', 'port': 6379}
}


def connect(engine=None, host='localhost', port=7711):
	global q
	global CURRENT_ENGINE
	if engine is None:
		engine = DEFAULT_ENGINE
	CURRENT_ENGINE = engine
	module_name = engine + 'engine.py'
	engine_name = engine + '_engine'
	constructor = engine.title() + 'Engine'
	base_path = os.path.dirname(__file__)
	module_path = base_path + '/queueengines/' + module_name
	queue_module = imp.load_source(engine_name, module_path)
	q = getattr(queue_module, constructor)()
	return q.connect(host, port)


def switch_to_engine(engine):
	if engine in engines:
		#global CURRENT_ENGINE
		#CURRENT_ENGINE = engine
		#print('switching to ' + engine)
		log.info('switching to ' + engine)
		return connect(engine)


def is_available(engine=None):
	if engine is None:
		engine = CURRENT_ENGINE
	return q.is_available()


def enqueue(queue, msg, timeout=0):
	return q.enqueue(queue, msg, timeout)


def enqueue_d(queue, msg, timeout=0):
	if isinstance(msg, dict):
		msg = pu.dict_to_json(msg)
	return q.enqueue(queue, msg, timeout)


def dequeue(queue, timeout=0):
	return q.dequeue(queue, timeout)


def dequeue_d(queue, timeout=0):
	msg = q.dequeue(queue, timeout)
	if msg and not isinstance(msg, dict):
		msg = pu.json_to_dict(msg)
	return msg


def get_from_queues(queues, timeout=0):
	return q.get_from_queues(queues, timeout)


def flush_all():
	return q.flush_all()
