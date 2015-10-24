import json
import sys
try:
    import xbmc, xbmcgui
except:
    try:
        sys.path.append('/usr/share/pyshared/xbmc')
        import xbmc, xbmcgui
    except:
        pass

def kodi_get_json(params):
    params["jsonrpc"] = "2.0"
    params["id"] = str(1)

    request = json.dumps(params)

    print("request: " + request) 

    return request

def kodi_execute_json(params):
    return json.loads(xbmc.executeJSONRPC(kodi_get_json(params)))
