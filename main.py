import visual
import arg_parser
import requestor
import searcher
import sys

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

def send_url(args, origin_url, words) : 
    nb_request = 0
    retour = {}
    retour["title"] = "Fuzzing Directory"
    retour["url"] = {}
    retour["ok"] = {}
    current_url = origin_url
    for word in words :
        nb_request += 1
        if word[0] == "/" :
            current_url = origin_url + word  
        else :
            current_url = origin_url + "/" + word
        response = requestor.send(args, current_url)
        if args.silent is False :
            if response.status_code >= 400 :
                print("[" + visual.red(str(response.status_code)) + "] " + current_url)
            else :
                print("[" + visual.green(str(response.status_code)) + "] " + current_url)
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
    return {"retour":retour, "nb_request":nb_request}

def directory(args) :
    print(visual.title("START DIRECTORY FUZZING"))
    if args.silent :
        print("Execution of wordlist")
    words = get_words(args)
    url_sent = send_url(args, args.url, words)
    retour = url_sent["retour"]
    nb_request = url_sent["nb_request"]
    print(str(nb_request) + "requests sent")
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