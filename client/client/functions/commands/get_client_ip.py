def getClientIp():
    from requests import get
    ip = get('https://api.ipify.org').text
    return ip