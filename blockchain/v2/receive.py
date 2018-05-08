"""This module corresponds to functionality documented
at https://blockchain.info/api/api_receive
"""

from .. import util
import json


class ReceiveResponse:

    def __init__(self, address, index, callback):
        self.address = address
        self.index = index
        self.callback_url = callback


class BalanceUpdateResponse:

    def __init__(self, id, addr, op, confs, callback, onNotification):
        self.id = id
        self.addr = addr
        self.op = op
        self.confs = confs
        self.callback = callback
        self.onNotification = onNotification


class LogEntry:

    def __init__(self, callback_url, called_at, raw_response, response_code):
        self.callback_url = callback_url
        self.called_at = called_at
        self.raw_response = raw_response
        self.response_code = response_code


def receive(xpub, callback, api_key):
    """Call the '/v2/receive' endpoint and create a forwarding address.
    
    :param str xpub: extended public key to generate payment address
    :param str callback: callback URI that will be called upon payment
    :param str api_key: Blockchain.info API V2 key
    :return: an instance of :class:`ReceiveResponse` class
    """

    params = {'xpub': xpub, 'key': api_key, 'callback': callback}
    resource = 'v2/receive?' + util.urlencode(params)
    resp = util.call_api(resource, base_url='https://api.blockchain.info/')
    json_resp = json.loads(resp)
    payment_response = ReceiveResponse(json_resp['address'],
                                       json_resp['index'],
                                       json_resp['callback'])
    return payment_response


def balance_update(address, callback, key, onNotification='KEEP', confs=3, op='ALL'):
    """Call the '/v2/receive/balance_update' to monitors an address of your choice
     for received and / or spent payments

    :param str address: The address you would like to monitor
    :param str callback: The callback URL to be notified when a payment is received
    :param str key: Your blockchain.info receive payments v2 api key
    :param str onNotification: The request notification behaviour ('KEEP' | 'DELETE)
    :param int confs: Optional (Default 3). The number of confirmations the transaction needs to have before a notification is sent.
    :param str op: Optional (Default 'ALL'). The operation type you would like to receive notifications for ('SPEND' | 'RECEIVE' | 'ALL')
    :return: an instance of :class: `BalanceUpdateResponse` class
    """

    params = {
        'address': address,
        'key': key,
        'callback': callback,
        'onNotification': onNotification,
        'confs': confs,
        'op': op
    }
    resource = 'v2/receive/balance_update'
    resp = util.call_api(resource, data=params, base_url='https://api.blockchain.info/')
    json_resp = json.loads(resp)
    balance_update_response = BalanceUpdateResponse(
        id=json_resp['id'],
        addr=json_resp['addr'],
        op=json_resp['op'],
        confs=json_resp['confs'],
        callback=json_resp['callback'],
        onNotification=json_resp['onNotification'])
    return balance_update_response


def callback_log(callback, api_key):
    """Call the 'v2/receive/callback_log' endpoint and returns the callback log
    for a given callback URI with parameters.

    :param callback: callback URI
    :param api_key: Blockchain.info API V2 key
    :return: a list of :class:`LogEntry` objects
    """
    params = {'key': api_key, 'callback': callback}
    resource = 'v2/receive/callback_log?' + util.urlencode(params)
    resp = util.call_api(resource, base_url='https://api.blockchain.info/')
    json_resp = json.loads(resp)
    return [LogEntry(e['callback'], e['called_at'], e['raw_response'], e['response_code']) for e in json_resp]


def check_gap(xpub, api_key):
    """Call the 'v2/receive/checkgap' endpoint and returns the callback log
    for a given callback URI with parameters.

    :param str xpub: extended public key
    :param str api_key: Blockchain.info API V2 key
    :return: an int
    """
    params = {'key': api_key, 'xpub': xpub}
    resource = 'v2/receive/checkgap?' + util.urlencode(params)
    resp = util.call_api(resource, base_url='https://api.blockchain.info/')
    json_resp = json.loads(resp)
    return json_resp['gap']
