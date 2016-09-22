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

def get_dicts():
    tivo_prods = url_to_soup('https://www.tivo.com/legal/patents')

    products = {}
    all_ids = set()
    for p in tivo_prods.find_all('p'):
        if p.get_text().find('U.S. Pat. Nos.') != -1:
            txt = p.get_text()
            pivot = txt.find('U.S. Pat.')
            name = txt[:pivot-1]
            pivot_2 = txt[pivot+15:].find('.')
            products[name] = filter(lambda x: len(x) > 3, map(lambda x: re.sub('[^a-zA-Z0-9]','',x, flags=re.UNICODE), txt[pivot+15:pivot+15+pivot_2].split(' ')))

    for k, v in products.iteritems():
        for pat in v:
            all_ids.add(pat)

    patents = {}
    for idd in list(all_ids):
        print "Getting soup for ", idd
        url = 'http://patents.com/us-' + idd + '.html'
        pp = url_to_soup(url)
        patents[idd] = {}

        l_d = pp.find_all('div')
        i = 0
        for _d in l_d:
            if i == 20:
                ii = 0
                for _ch in _d.findChildren():
                    if ii == 50:
                        iii = 0
                        for _ch2 in _ch.findChildren():
                            if iii==0:
                                txt = re.sub('\n     ', ' ', _ch2.text)
                                txt = re.sub('\n', ' ', txt)
                                patents[idd]['Title'] = txt
                            if iii==5:
                                txt = re.sub('\n     ', ' ', _ch2.text)
                                txt = re.sub('\n', ' ', txt)
                                patents[idd]['Abstract'] = txt
                            iii += 1
                        break
                    ii += 1
                break
            i += 1

    return (products, patents)


if __name__ == "__main__":
    (products, patents) = get_dicts()

    for k, v in patents.iteritems():
        print "Patent", k
        for kk, vv in v.iteritems():
            print kk, ":", vv