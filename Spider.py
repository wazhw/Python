from urllib import request
import requests ,re

class Spider:
    def get_content(self,page):
        self.page = page
        hd = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=4&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        #html = requests.get(url,headers = hd).text
        response = request.Request(url,headers = hd)
        html = request.urlopen(response).read()
        html = html.decode("gbk")#字符编码
        return html

    def get(self,html):
        self.html = html
        reg = re.compile(r'<p class="t1 ">.*?<a target="_blank" title="(.*?)".*?<span class="t2"><a target="_blank" title="(.*?)".*?<span class="t3">(.*?)</span>.*? <span class="t4">(.*?)</span>',re.S)
        items = re.findall(reg,self.html)
        return items
if __name__=='__main__':
    spider=Spider()
    for i in range(1,10):
        a = spider.get_content(i)
        for j in spider.get(a):
            print(j)