import json
import xbmc

def kodi_get_json(params):
    params["jsonrpc"] = "2.0"
    params["id"] = str(1)
    xbmc.log(msg="request: " + json.dumps(params), level=xbmc.LOGDEBUG) 

    return json.dumps(params)

def kodi_execute_json(params):
    return json.loads(xbmc.executeJSONRPC(kodi_get_json(params)))