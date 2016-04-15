class QueueEngine(object):
	"""Base clas for IPC message queue system"""
	def __init__(self):
		super(QueueEngine, self).__init__()

	def connect():
		raise NotImplementedError("Queue engine must implement this")

	def is_available():
		raise NotImplementedError("Queue engine must implement this")

	def enqueue():
		raise NotImplementedError("Queue engine must implement this")

	def dequeue():
		raise NotImplementedError("Queue engine must implement this")
