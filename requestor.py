import visual
import sys
import json

try :
    import requests
except Exception as e :
    print(visual.error("You need to install requests module with 'pip install requests' : " + str(e)))
    sys.exit()

def get_headers_dict(args) :
    try :
        with open(args.headers, "r") as file :
            headers_json = file.read()
            headers = json.loads(headers_json)
            return headers
    except Exception as e :
        print(visual.error("HEADERS HTTP : " + str(e)))
        sys.exit()

def set_headers_http(args) :
    if args.headers is not None :
        try : 
            cookies = json.loads(args.headers)
        except Exception as e :
            print(visual.error("COOKIES HTTP : " + str(e)))
            sys.exit()
    else :
        headers = {}
    if args.cookies is not None :
        try : 
            cookies = json.loads(args.cookies)
        except Exception as e :
            print(visual.error("COOKIES HTTP : " + str(e)))
            sys.exit()
    else :
        cookies = {}
    if args.data is not None :
        try :
            data = json.loads(args.data)
        except Exception as e :
            print(visual.error("Data : " + str(e)))
            sys.exit()
    else :
        data = {}
    return {"headers" : headers, "cookies" : cookies, "data" : data}   

def request_get(args, url) :
    try :
        http_headers = set_headers_http(args)
        headers = http_headers["headers"]
        cookies = http_headers["cookies"]
        data = http_headers["data"]
        response = requests.get(url, headers=headers, cookies=cookies, data=data)
        return response
    except Exception as e :
        print(visual.error("Request GET : " + str(e)))
        sys.exit()

def request_post(args, url) :
    try :
        http_headers = set_headers_http(args)
        headers = http_headers["headers"]
        cookies = http_headers["cookies"]
        data = http_headers["data"]
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        return response
    except Exception as e :
        print(visual.error("Request POST : " + str(e)))
        sys.exit()
    
def send(args, url) :
    if args.post :
        return request_post(args, url)
    return request_get(args, url)