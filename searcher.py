import json
import visual
import sys
import re

def find_response(args, response) :
    retour = {}
    retour["body"] = []
    retour["headers"] = []
    try :
        words = json.loads(args.find)
    except Exception as e :
        print(visual.error("find argument need to be a json list"))
        sys.exit()
    for word in words :
        if word in response.text :
            retour["body"].append(word)
        if word in response.headers :
            retour["headers"].append(word)
    return retour

def search_url(text) : 
    urls = re.findall(r'(?<=href=")([^"]+)(?=")', text)
    return urls