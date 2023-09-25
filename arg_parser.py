import argparse

def add_arguments() :
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', dest='url', required=True, help='target url')
    parser.add_argument('-w', '--wordlist', dest='wordlist', required=False, help='wordlist of files that will be searched')
    parser.add_argument('-o', '--output', dest='output', required=False, help='file.txt where output is dump')
    parser.add_argument('-headers', '--headers', dest='headers', required=False, help='optional http headers on json tab format')
    parser.add_argument('-c', '--cookies', dest='cookies', required=False, help='optionnal http cookies on json tab format')
    parser.add_argument('-data', '--data', dest='data', required=False, help='optional http data on json list format')
    parser.add_argument('-p', '--post', dest='post', required=False, action='store_true', help='post request (get by default)')
    parser.add_argument('-f', '--find', dest='find', required=False, help='look for keywords in respone (-find \'[\'word1\',\'word2\']\')')
    parser.add_argument('-s', '--silent', dest='silent', required=False, action='store_true', help='silent mode, only print the output')
    parser.add_argument('-i', '--intelligent', dest='intelligent', required=False, action='store_true', help='Will search for url of the same domain in the response and searching on it')
    parser.add_argument('-slow', '--slow', dest='slow', type=float, required=False, help='time to sleep beetwen two requests')
    return parser

def error_args(parser, args) :
    if args.wordlist is None and args.intelligent is False :
        parser.error("You need to provide at least -w WORDLIST.txt or -i parameter")

def get_args() :
    parser = add_arguments()
    args = parser.parse_args()
    error_args(parser, args)
    return args

