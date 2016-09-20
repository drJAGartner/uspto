import urllib2, re
from bs4 import BeautifulSoup

def url_to_soup(url):
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    req = urllib2.Request(url, headers=hdr)
    res = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(req, timeout=4)
    return BeautifulSoup(res.read(), "html.parser")

def main():
    soup = url_to_soup('https://www.tivo.com/legal/patents')

    products = {}
    all_ids = set()
    for p in soup.find_all('p'):
        if p.get_text().find('U.S. Pat. Nos.') != -1:
            txt = p.get_text()
            pivot = txt.find('U.S. Pat.')
            name = txt[:pivot-1]
            pivot_2 = txt[pivot+15:].find('.')
            products[name] = map(lambda x: re.sub('[^a-zA-Z0-9]','',x, flags=re.UNICODE), txt[pivot+15:pivot+15+pivot_2].split(' '))

    for k, v in products.iteritems():
        for pat in v:
            all_ids.add(pat)

    print all_ids




if __name__ == "__main__":
    main()