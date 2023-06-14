import os


def disableProxy(proxy):
    del os.environ['http_proxy']
    del os.environ['HTTP_PROXY']
    del os.environ['https_proxy']
    del os.environ['HTTPS_PROXY']


def enableProxy(proxy):
    os.environ['http_proxy'] = proxy
    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy