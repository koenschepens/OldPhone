import json
import xbmc

def kodi_get_json(params):
    params["jsonrpc"] = "2.0"
    params["id"] = str(1)

    request = json.dumps(params)

    xbmc.log(msg="request: " + request, level=xbmc.LOGDEBUG) 

    return request

def kodi_execute_json(params):
    return json.loads(xbmc.executeJSONRPC(kodi_get_json(params)))