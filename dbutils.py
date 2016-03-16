#!/usr/bin/env python

import redis
import json

host = 'localhost'
port = 6379
db = 0

red = redis.StrictRedis(host=host, port=port, db=db)
pubsub = red.pubsub()


def add_to_queue(queue, item):
	if isinstance(item, dict):
		item = json.dumps(item)
	try:
		red.rpush(queue, item)
	except Exception, e:
		raise e


def listen(msg):
	while True:
		m = red.get_message()
	return m


def get_value(key):
	return red.get(key)


def set(key, value):
	red.set(key, value)


def send_to_core(msg):
	add_to_queue('incoming', msg)


#def wait_for_rsp2(guid, timeout=None):
#	print('waiting for guid ' + str(guid))
#	rsp = None
#	start = now()
#	while rsp is None:
#		rsp = get_value(guid)
#		diff = now() - start
#		if timeout and diff > timeout:
#			raise GatewayTimeoutException('Operation timed out')
#
#	red.delete(guid)
#	return json.loads(rsp)


def wait_for_rsp(guid, timeout=0):
	rsp = red.blpop(guid, timeout=timeout)
	return json.loads(rsp[1])


def get_msg():
	"""
	Pop message from message queue and return its payload
	"""
	msg = red.blpop('incoming', timeout=0)
	payload = msg[1]
	return payload


def delete(item):
	red.delete(item)


def flushdb():
	red.flushdb()


def client_side_incr(pipe):
	current_value = pipe.get('OUR-SEQUENCE-KEY')
	next_value = int(current_value) + 1
	pipe.multi()
	pipe.set('OUR-SEQUENCE-KEY', next_value)


def incr():
	red.transaction(client_side_incr, 'OUR-SEQUENCE-KEY')


def subscribe_to_channel(channel, callback):
	pubsub.subscribe(**{channel: callback})
