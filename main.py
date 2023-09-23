import visual
import arg_parser
import requestor
import searcher
import sys
import re
import time
import json
import requests

def get_words(args) :
    try :
        with open(args.wordlist, "r") as file :
            words = [word.rstrip('\n') for word in file.readlines()]
            return words
    except Exception as e:
        print(visual.error(str(e)))
        sys.exit()

def print_found(found) :
    retour = {}
    retour["body"] = []
    retour["headers"] = []
    if len(found["body"]) == 0 : 
        print("\t Nothing found in body")
    else :
        body = visual.green("Found") + " in Body : "
        for find in found["body"] : 
            body += " " + find
            retour["body"].append(find)
        print("\t " + body)
    if len(found["headers"]) == 0 :
        print("\t Nothing found in headers")
    else :
        headers = visual.green("Found") + " in Headers :"
        for find in found["headers"] : 
            headers += " " + find
            retour["headers"].append(find)
        print("\t " + headers)
    return retour

def print_retour_directory(args, retour):
    print("Output of " + retour["title"])
    print("GREEN CODE :")
    for key, value in retour["url"].items():
        if value["code"] < 400 :
            print("[" + visual.green(str(value["code"])) + "] " + key)
            if args.find is not None :
                if value["find"]["body"] is not None :
                    for found in value["find"]["body"] :
                        print("\t " + visual.blue("Found : ") + found)
    print("\n")
    print("RED CODE :")
    for key, value in retour["url"].items():
        if value["code"] >= 400 :
            print("[" + visual.red(str(value["code"])) + "] " + key)
    print("\n")

def prepare_url(origin, suffix) :
    if suffix.startswith(origin) :
        new_url = suffix
    elif suffix.startswith("https://") or suffix.startswith("http://") :
        new_url = suffix
    elif len(suffix) == 0 or (len(suffix) > 0 and (suffix[0] == "/" or origin[-1] == "/"))  :
        if origin.endswith("index.php") :
            origin = origin[:-9]
        if len(suffix) > 0 and suffix[0] == "/" and origin[-1] == "/" :  
            suffix = suffix[1:]
        new_url = origin + suffix  
    else :
        new_url = origin + "/" + suffix
    return new_url

def send_url(args, origin_url, words) : 
    nb_request = 0
    retour = {}
    retour["title"] = "Directory Fuzzing"
    retour["url"] = {}
    retour["ok"] = {}
    retour["sent"] = []
    current_url = origin_url
    # print("Fuzzing on " + origin_url)
    for word in words :
        if args.slow is not None :
            time.sleep(float(args.slow))
        nb_request += 1
        current_url = prepare_url(origin_url, word)
        response = requestor.send(args, current_url)
        retour["sent"].append(current_url)
        if args.silent is False :
            if response.status_code >= 400 :
                print("[" + visual.red(str(response.status_code)) + "] " + current_url)
            else :
                print("[" + visual.green(str(response.status_code)) + "] " + current_url)
        else :
            if nb_request % 100 == 0 :
                print(str(nb_request) + " requests sent")
        if response.status_code < 400 : 
            retour["ok"][current_url] = response
        retour["url"][current_url] = {} 
        retour["url"][current_url]["code"] = response.status_code
        if args.find is not None :
            found = searcher.find_response(args, response)
            retour["url"][current_url]["find"] = print_found(found)
        else :
            retour["url"][current_url]["find"] = {}
    # print(str(nb_request) + " requests sent")
    return {"retour":retour, "nb_request":nb_request}

def intelligent(args, sent_urls, words) :
    stack_urls = []
    if not args.silent : 
        print("+ STARTING INTELLIGENT SCAN OF RESPONSE")
    retour = {}
    retour["ok"] = {}
    retour["url"] = {}
    current_retour = send_url(args, args.url, [""])["retour"]
    retour["ok"].update(current_retour["ok"])
    retour["url"].update(current_retour["url"])
    stack_urls.append(current_retour["ok"])
    sent_urls.append(args.url)
    while stack_urls :
        response = stack_urls.pop()
        new_urls = searcher.search_url(response[next(iter(response))].text)
        if new_urls :
            for new_suffix in new_urls :
                new_url = prepare_url(args.url, new_suffix)
                if new_url not in sent_urls :
                    current_retour = send_url(args, new_url, [""] + words)["retour"]
                    retour["ok"].update(current_retour["ok"])
                    retour["url"].update(current_retour["url"])
                    if len(current_retour["ok"]) > 0 :
                        stack_urls.append(current_retour["ok"])
                    sent_urls.append(new_url)
    return retour

def directory(args) :
    print(visual.title("START DIRECTORY FUZZING"))
    if args.wordlist is not None :
        if not args.silent :
            print("Execution of wordlist")
        words = get_words(args)
        url_sent = send_url(args, args.url, words)
        retour = url_sent["retour"]
        sent_urls = retour["sent"]
    else :
        retour = {}
        retour["url"] = {}
        retour["intelligent"] = {}
        retour["title"] = "Directory Fuzzing"
        sent_urls = []
        words = []
        retour["ok"] = {}
    if args.intelligent :
        retour["intelligent"] = intelligent(args, sent_urls, words)
        retour["ok"].update(retour["intelligent"]["ok"])
        retour["url"].update(retour["intelligent"]["url"])
    print(visual.title("END DIRECTORY FUZZING"))
    return retour

def process_retour(retour) :
    for element in retour :
        if element == "ok" :
            for url in retour["ok"] :
                current_response = retour["ok"][url]
                response = {}
                response["code"] = current_response.status_code
                response["text"] = current_response.text

def write_output(args, retour) :
    if args.output is not None :
        try :
            with open(args.output, "w") as file :
                file.write(json.dumps(retour))
        except Exception as e:
            print(visual.error(str(e)))
            sys.exit()

def main() :
    args = arg_parser.get_args()
    retour = directory(args)
    if not args.silent :
        print("\n")
    print_retour_directory(args, retour)
    process_retour(retour)
    write_output(args, retour)

if __name__ == '__main__' : 
    main()