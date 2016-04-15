
def get_type(msg):
	return msg.iterkeys().next()


def get_guid(msg, txn_type=None):
	if txn_type is None:
		txn_type = get_type(msg)
	return msg.get(txn_type).get('guid')


def set_guid(msg, guid, txn_type=None):
	if txn_type is None:
		txn_type = get_type(msg)
	msg[txn_type]['guid'] = guid


def set_status(msg, status, txn_type=None):
	if txn_type is None:
		txn_type = get_type(msg)
	msg[txn_type]['status'] = status


def get_status(msg, txn_type=None):
	if txn_type is None:
		txn_type = get_type(msg)
	return msg.get(txn_type).get('status')


def get_route(msg, txn_type=None):
	if txn_type is None:
		txn_type = get_type(msg)
	return msg.get(txn_type).get('route')


def set_route(msg, route, txn_type=None):
	if txn_type is None:
		txn_type = get_type(msg)
	msg[txn_type]['route'] = route
