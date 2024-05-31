# pylint: disable=global-statement

import oslo_messaging as messaging


from oslo_config import cfg

TRANSPORT = None
NOTIFICATION_TRANSPORT = None
NOTIFIER = None


def init():
    global TRANSPORT, NOTIFICATION_TRANSPORT, NOTIFIER
    TRANSPORT = create_transport(get_transport_url())
    NOTIFICATION_TRANSPORT = messaging.get_notification_transport(cfg.CONF)
    NOTIFIER = messaging.Notifier(NOTIFICATION_TRANSPORT)


def cleanup():
    global TRANSPORT, NOTIFICATION_TRANSPORT, NOTIFIER
    if TRANSPORT is not None:
        TRANSPORT.cleanup()
    if NOTIFICATION_TRANSPORT is not None:
        NOTIFICATION_TRANSPORT.cleanup()
    TRANSPORT = NOTIFICATION_TRANSPORT = NOTIFIER = None


def get_transport_url(url_str=None):
    return messaging.TransportURL.parse(cfg.CONF, url_str)


def get_client(target):

    assert TRANSPORT is not None, "'TRANSPORT' must not be None"

    return messaging.get_rpc_client(
        TRANSPORT,
        target,
    )


def get_server(
    target,
    endpoints,
    executor="threading",
):
    assert TRANSPORT is not None, "'TRANSPORT' must not be None"

    return messaging.get_rpc_server(
        TRANSPORT,
        target,
        endpoints,
        executor=executor,
    )


def get_notifier(
    service=None, host=None, publisher_id=None
):  # pylint: disable=unused-argument
    assert NOTIFIER is not None, "'NOTIFIER' must not be None"

    return NOTIFIER.prepare()


def create_transport(url):
    return messaging.get_rpc_transport(cfg.CONF, url=url)
