def getWebConfig(config_json_name):
    from requests import get
    response = get("https://data.clientnet.ml/config.json")
    data = response.json()[config_json_name]
    return data