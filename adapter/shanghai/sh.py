#coding=utf-8
import urllib
import cookielib
import urllib2
import ocr
import html
import StringIO


class Shanghai(object):
    query_url = 'http://www.shjtaq.com/2012/dzjc2012.asp'
    vcode_url = 'http://www.shjtaq.com/2012/validatecode.asp'
    headers = {
        "Referer": "http://www.shjtaq.com/2012/dzjc2012.asp",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
                "Accept": "text/plain"}

    def query(self, pn='', pn_type='', en=''):
        cookie, code = self._get_code()
        data = dict(
                cardqz=pn.decode('utf8')[0].encode('gb2312'),
                carnumber=pn.decode('utf8')[1:].encode('gb2312'),
                type1=pn_type.decode('utf8').encode('gb2312'),
                fdjh=en,
                verify=code,
                submit=u' 提 交 '.encode('gb2312'),
                act='search'
                )
        data = urllib.urlencode(data)
        req = urllib2.Request(self.query_url, headers=self.headers)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        response = opener.open(req, data)
        return html.html.clean(response.read())

    def _get_code(self):
        req = urllib2.Request(self.vcode_url, headers=self.headers)
        cookie=cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        response = opener.open(req)
        code = ocr.read(StringIO.StringIO(response.read()))
        return cookie, code

shanghai = Shanghai()

if __name__ == '__main__':
    tickets = shanghai.query(
            pn='苏A12345',
            pn_type='02/小型汽车号牌',
            en='0123456')
    print tickets
