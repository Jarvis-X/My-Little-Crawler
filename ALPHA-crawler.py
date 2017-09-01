import requests
import time
import os
from bs4 import BeautifulSoup
import re
import bs4

################################################################################
## functions
################################################################################
'''''''''''''''''''''''''''
get robots.txt info about the HTML page
'''''''''''''''''''''''''''
def getrobot(url):
    try:
        useragent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0"}
        # act as a Mozilla Browser   
        urlrobot = url + "/robots.txt"
        # access the robots.txt file under the root of the page
        robots = requests.get(urlrobot, headers = useragent)
        robots.encoding = robots.apparent_encoding
        text = robots.text
        if "User-agent" in text:
            print(text)
            return text
        else:
            print("No valid robots.txt found.")
    except:
        print("An error occurs!")

'''''''''''''''''''''''''''
search the whole internet via search engines
'''''''''''''''''''''''''''
def search(keyword, engine="google", start_time_refresh=True):
    useragent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0"}
    # pretending to act like a Mozilla Browser
    global start
    if start_time_refresh:
        start = time.time()
    # the whole process cannot be too long
    
    # BEGIN google search needs to change'''
    if engine.lower() == "google":
        # default searching engine is google
        url = "https://www.google.com/search"
        try:
            print("Googling...")
            r = requests.get(url, params={'q':keyword}, headers = useragent, timeout=1)
            ''' This format seems not working'''
            print(r.request.url)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            print("Google succeeded.")
            print("Length of the searching result: {}".format(len(r.text)))
            print("Returning results...")
            return r
        except:
            end = time.time()
            if end - start >= 5:
                print("Search failed.")
                return None
            else:
                try:
                    print("Google failed. Trying Baidu...")
                    return search(keyword, engine="baidu", start_time_refresh=False)
                # if google failed to load search results
                # trying Baidu recursively
                except:
                    print("Baidu failed. Trying Bing...")
                    return search(keyword, engine="bing", start_time_refresh=False)
                # if Baidu failed to load search results
                # trying Bing recursively            
    # END google search needs to change'''
    
    elif engine.lower() == "baidu":
        # user can choose to use baidu as search engine
        url = "http://www.baidu.com/s"
        try:
            print("Baiduing...")
            r = requests.get(url, params = {"wd":keyword}, headers = useragent, timeout=1)
            print(r.request.url)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            print("Baidu succeeded.")
            print("Length of the searching result: {}".format(len(r.text)))
            print("Returning results..")
            return r
        except:
            end = time.time()
            if end - start >= 5:
                print("Search failed.")
                return None
            else:            
                try:
                    # if Baidu failed to load search results
                    # trying Bing recursively                
                    print("Baidu failed. Trying Bing...")
                    return search(keyword, engine="bing", start_time_refresh=False)
                except:
                    # if Bing failed to load search results
                    # trying google recursively
                    print("Google failed. Trying Google...")
                    return search(keyword, engine="google", start_time_refresh=False)
            
    elif engine.lower() == "bing":
        # user can choose to use bing as search engine
        url = "https://www.bing.com/search"
        try:
            print("Binnnng...")
            r = requests.get(url, params = {'q':keyword}, headers = useragent, timeout=1)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            print(r.request.url)
            print("Bing succeeded.")
            print("Length of the searching result: {}".format(len(r.text)))
            print("Returning results...")
            return r
        except:
            end = time.time()
            if end - start >= 5:
                print("Search failed.")
                return None
            else:            
                try:
                    # if Bing failed to load search results
                    # trying google recursively                
                    print("Bing failed. Trying Google...")
                    return search(keyword, engine="google", start_time_refresh=False)
                except:
                    # if google failed to load search results
                    # trying Baidu recursively                
                    print("Google failed. Trying Baidu...")
                    return search(keyword, engine="baidu", start_time_refresh=False)    

'''''''''''''''''''''''''''
Download binary resources, i.e., pictures, videos.
'''''''''''''''''''''''''''
def DLbin(rcsurl, pathroot, rename=None):
    # user is required to enter the url for the picture
    # and where to download the picture
    try:
        useragent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0"}
        print("Downloading...")
        if not os.path.exists(pathroot):
            os.mkdir(pathroot)
            # if the path does not exist, create the path
        if not rename:
            path = pathroot + rcsurl.split('/')[-1]
        else:
            path = pathroot + rename
        if not os.path.exists(path):
            # if the picture does not exist, save it
            r = requests.get(rcsurl, headers=useragent)
            r.raise_for_status()            
            with open(path, "wb") as f:
                f.write(r.content) 
            print("Download succeeded!")
        else:
            print("File already exists.")
            print("Download aborted.")
    except:
        print("Download failed.")

'''''''''''''''''''''''''''
looking for location of an IP address, default for current internet environment
'''''''''''''''''''''''''''
def IP2lct(ipaddr=None):
    try:
        url = "http://whatismyipaddress.com/ip/"
        if not ipaddr:
            ipaddr = requests.get("http://bot.whatismyipaddress.com/").text
        r = requests.get(url+ipaddr)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "lxml")
        tagoflocation = str(soup.find(name="script", string=re.compile("Location")))
        location = tagoflocation[tagoflocation.rfind("General Location"):tagoflocation.rfind("<br>")].split("<br>")[1]
        x, y = tuple(tagoflocation[tagoflocation.find("[")+1:tagoflocation.find(']')].split(','))
        x, y = float(x),float(y)
        if x<0:
            x = str(-x) + 'S'
        else:
            x = str(x) + 'N'
        if y<0:
            y = str(-y) + 'W'
        else:
            y = str(y) + 'E'
        print(location)
        print("{}, {}".format(x, y))
    except:
        print("IP to Geolocation conversion failed.")
            
'''''''''''''''''''''''''''
extract links in an HTML document
'''''''''''''''''''''''''''
def getlinks(url):
    useragent = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0"}
    try:
        r = requests.get(url, headers=useragent)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "lxml")
        links = []
        for link in soup.find_all('a'):
            # in the list of tags of links
            link_real = link.get("href")
            if "http" in str(link_real):
                # store all links
                links.append(link_real)
        return links
    except:
        print("Failing to get the links.")

'''''''''''''''''''''''''''
login websites with cookies
'''''''''''''''''''''''''''
def login_cookie(websitelogin, captchaurl, username, password):
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0"}
    with requests.session() as s:
        mode = {"mode":"imagecaptcha"}  # may change according to different websites
        r = s.get(websitelogin, params = mode)
        r.encoding = r.apparent_encoding
        cookie = r.cookies  # save the cookies
        soup = BeautifulSoup(r.text, "lxml")
        rnd = str(soup.find(name="img", id="captcha_img").get("src")).split('?')[-1].split('=')[-1] # find out rnd number for the cap-picture
        param = {"rnd" : rnd}
        r = s.get(captchaurl, params=param, headers=head)
        pathroot = "F:/00000_testfiles/"    # the location on my computer saving the captcha pics
        print("Downloading...")
        if not os.path.exists(pathroot):
            os.mkdir(pathroot)
        path = pathroot + "captcha.jpg"
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content) 
        print("Download succeeded!")
        word = input("type in the captcha:\t")
        postdata = {"action":"login", "name":username, "pass":password, "use_old_captcha":1, "captcha":word}    # vary for different sites
        s.post("https://www.furaffinity.net/login/", data=postdata, cookies=cookie)
        r = s.get(websitelogin)
        soup = BeautifulSoup(r.text, "lxml")
        if soup.find(name='b', string="Please log in!"):
            print("login failed.\n\n\n\n\n\n\n")
        print(soup.prettify())  # check if successful
################################################################################
## functions end
################################################################################
        
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''#
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''#

################################################################################
## main function below
################################################################################
if __name__ == "__main__":
    #picurl = "http://image.nationalgeographic.com.cn/userpic/58536/2017/0505120115585368605.jpeg"
    #path = "F:/00002_Files/"
    #DLbin(picurl, path,"1234.jpeg")
    
    #ip = "4.237.2.60"
    #IP2lct()
    #links = getlinks("http://www.baidu.com")
