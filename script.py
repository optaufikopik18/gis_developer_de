import requests
import cgi

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.error import HTTPError

def get_files(link, forcast, level, variable, leftlon, rightlon, toplat, bottomlat):
    url        = link
    main_page  = [a['href'] for a in BeautifulSoup(requests.get(url).text,'html.parser').findAll('a')]
    files      = ['?file=gfs.t00z.pgrb2.0p25.f'+('00'+str(a))[-3:] for a in range(forcast)]
    levels     = ''.join(['&'+a+'=on'for a in level])
    variables  = ''.join(['&var_'+a+'=on' for a in variable])
    subset     = '&leftlon={}&rightlon={}&toplat={}&bottomlat={}'.format(leftlon,rightlon,toplat,bottomlat)
    times      = [c['href'] for b in [BeautifulSoup(requests.get(a).text,'html.parser').findAll('a') for a in main_page] for c in b if c['href'][-2:] in ('00','12')]
    fields     = [c['href'].replace(url+'?','&') for b in [BeautifulSoup(requests.get(a).text,'html.parser').findAll('a') for a in times] for c in b]
    success    = []
    fail       = []

    for file in files:
        for field in fields:
            try:
                remotefile = urlopen(url+file+levels+variables+subset+field)
                content = remotefile.info()['Content-Disposition']
                params = cgi.parse_header(content)[1]
                path = 'files/'
                filename = params['filename']
                urlretrieve(url, path+filename)
                success.append(filename)
                print(filename, 'Download successful')
            except HTTPError as err:
                fail.append(filename)
                print(filename, 'Download failed with error code '+str(err.code))

    print('Successful download '+ str(len(success)) +' file'+('s' if len(success) > 1 else ''))
    print('Failed download '+ str(len(success)) +' file'+('s' if len(success) > 1 else ''))



    

def main():
    get_files('https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl', 49, ['lev_1000_mb','lev_500_mb','lev_800_mb'], ['APCP','UGRD','VGRD'], 70, 170, 40, -25)
    

if __name__ == '__main__':
    main()
