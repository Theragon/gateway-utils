from queueengine import QueueEngine
from disq import Disque


class DisqueEngine(QueueEngine):
	"""docstring for DisqueEngine"""
	def __init__(self):
		super(DisqueEngine, self).__init__()
		self.d = None
		self.host = 'localhost'
		self.port = 7711

	def connect(self):
		self.d = Disque(host=self.host, port=self.port)
		return self.is_available()

	def is_available(self):
		print('is disque available')
		if self.d is None:
			return False
		return self.d.hello() is not None

	def enqueue(self, queue, msg, timeout=0):
		self.d.addjob(queue, msg, timeout_ms=timeout)

	def dequeue(self, queue, timeout=0):
		rsp = self.d.getjob(queue, timeout_ms=timeout)
		if rsp is not None:
			self.d.ackjob(rsp[0][1])
			return rsp[0][2]
		else:
			return None

	def get_from_queues(self, queues, timeout=0):
		rsps = self.d.getjob(queues[0], timeout_ms=timeout, queues=queues[1:])

		return rsps

	def flush_all(self):
		return self.d.debug_flushall()
