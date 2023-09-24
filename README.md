# Deep_Crawler

Depp_Crawler is a powerful website crawling tool. With a command, you will have the list of URLs reachable on the domain. You can also search for keywords in the web response.

## Insallation
```bash
pip3 install requests
```

```bash
git clone https://github.com/Thomas97460/Deep_Crawler.git
```


## Usage
### URL parameter
The program takes a URL as a parameter and queries the website to find other URLs.
```bash
python3 main.py -u https://example.com
```

### Bruteforce
The -w WORDLIST.txt parameter allows searching for URLs by bruteforce. The program appends each entry in the wordlist to the end of the -u URL parameter
```bash
python3 main.py -u URL -w WORDLIST.txt
```

### Intelligent
The -i parameter instructs the program to search the web response for URLs. The URLs found are then queried. The program works recursively and will continue to query as long as there are URLs in the responses.
The URLs found must belong to the same domain as that of the -u parameter.
```bash
python3 main.py -u https://example.com -i
```
It can also be used with the -w WORDLIST.txt argument. The wordlist will be applied to each new URL found.

```bash
python3 main.py -u https://example.com -i -w WORDLIST.txt
```

**__WARNING__**: Intelligent mode is very powerful and intrusive. Only use it on sites where you have the right. This will cause a massive request sending.

### Keyword search
The -f parameter ` -f '["keyword1","keyword2"]'` searches the response for keywords from the JSON list.

```bash
python3 main.py -u http://challenge01.root-me.org/web-serveur/ch19/ -i -f '["a","baa"]' -w tiny_fuzz.txt
```

Can be used in combination with -i and -w

### Output
You can write the raw output of the program to a file. The output is in JSON form.

```bash
python3 main.py -u http://challenge01.root-me.org/web-serveur/ch19/ -i -o OUTPUT.txt
```

### Optional https headers
`-headers '{"field1":"data1","field2":"data2"}'`

`-cookies '{"cookie1":"data1","cookie2":"data2"}'`

`-data '{"key1":"data1","key2":"data2"}'`

### Silent mode 
Silent mode will notify you every 100 requests of program continuity `-s`

### Slow mode
Slow mode will impose a cooldown of X seconds between each request. `-slow 10`