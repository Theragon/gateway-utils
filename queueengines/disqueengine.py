import os
import imp
import logging
from disq import Disque
base_path = os.path.dirname(__file__)
full_path = base_path + '/queueengine.py'
base = imp.load_source('queueengine', full_path)
QueueEngine = getattr(base, 'QueueEngine')

log = logging.getLogger(__name__)


class DisqueEngine(QueueEngine):
	"""docstring for DisqueEngine"""
	def __init__(self):
		super(DisqueEngine, self).__init__()
		self.d = None

	def connect(self, host='localhost', port=7711):
		self.d = Disque(host=host, port=port)
		return self.is_available()

	def is_available(self):
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
