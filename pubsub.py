import redis

red = redis.StrictRedis(host='localhost', port=6379, db=0)
ps = red.pubsub()


def subscribe(*args, **kwargs):
	return ps.subscribe(*args, **kwargs)


def publish(channel, msg):
	return red.publish(channel, msg)


def run_in_thread(sleep_time=0.001):
	return ps.run_in_thread(sleep_time=sleep_time)
