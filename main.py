import visual
import arg_parser
import requestor
import searcher
import sys
import re
import time

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

def print_retour_directory(retour):
    print("Output of " + retour["title"])
    print("GREEN CODE :")
    for key, value in retour["url"].items():
        if value["code"] < 400 :
            print("[" + visual.green(str(value["code"])) + "] " + key)
    print("Forbidden Code :")
    for key, value in retour["url"].items():
        if value["code"] == 403 :
            print("[" + visual.red(str(value["code"])) + "] " + key)

def prepare_url(origin, suffix) :
    if suffix.startswith(origin) :
        new_url = suffix
    elif len(suffix) == 0 or len(suffix) > 0 and (suffix[0] == "/" or suffix[-1] == "/")  :
        if origin.endswith("index.php") :
            origin = origin[:-9]
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
    print("Fuzzing on " + origin_url)
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
                retour["ok"][current_url] = response
        else :
            if nb_request % 100 == 0 :
                print(str(nb_request) + " requests sent")
        retour["url"][current_url] = {} 
        retour["url"][current_url]["code"] = response.status_code
        if args.find is not None :
            found = searcher.find_response(args, response)
            retour["url"][current_url]["find"] = print_found(found)
        else :
            retour["url"][current_url]["find"] = {}
    print(str(nb_request) + " requests sent")
    return {"retour":retour, "nb_request":nb_request}

def deep(args, urls, words, sent_urls) :
    retour = {}
    retour["sent"] = []
    retour["ok"] = {}
    retour["url"] = {}
    for url in urls :
        if not re.search(r"\.[a-zA-Z0-9]+$", url) and url != args.url and url not in sent_urls :
            print("+ STARTING NEW FUZZING ON " + url)
            sent = send_url(args, url, words)
            retour["sent"].append(url)
            retour["ok"].update(sent["retour"]["ok"])
            retour["url"].update(sent["retour"]["url"])
            retour[url] = sent["retour"]
    return retour

def intelligent(args, urls, sent_urls, words) :
    stack_urls = urls
    print("+ STARTING INTELLIGENT SCAN OF RESPONSE")
    retour = {}
    retour["ok"] = {}
    retour["url"] = {}
    while stack_urls :
        url, response = stack_urls.popitem()
        new_urls = searcher.search_url(response.text)
        if new_urls :
            for new_url in new_urls :
                new_url = prepare_url(args.url, new_url)
                if new_url not in sent_urls :
                    current_retour = send_url(args, new_url, words)["retour"]
                    retour["ok"].update(current_retour["ok"])
                    retour["url"].update(current_retour["url"])
                    stack_urls.update(current_retour["ok"])
                    sent_urls.append(new_url)
    return retour

def directory(args) :
    print("\n")
    print(visual.title("START DIRECTORY FUZZING"))
    if args.silent :
        print("Execution of wordlist")
    words = get_words(args)
    url_sent = send_url(args, args.url, words)
    retour = url_sent["retour"]
    sent_urls = retour["sent"]
    if args.deep :
        retour["deep"] = deep(args, retour["ok"], words, sent_urls)
        sent_urls.append(retour["deep"]["sent"])
        retour["ok"].update(retour["deep"]["ok"])
        retour["url"].update(retour["deep"]["url"])
    if args.intelligent :
        retour["intelligent"] = intelligent(args, retour["ok"], sent_urls, words)
        retour["ok"].update(retour["intelligent"]["ok"])
        retour["url"].update(retour["intelligent"]["url"])
        print(visual.title("END DIRECTORY FUZZING"))
    return retour
        

def main() :
    args = arg_parser.get_args()
    retour = directory(args)
    if not args.silent :
        print("\n")
    print_retour_directory(retour)

if __name__ == '__main__' : 
    main()