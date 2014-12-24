#coding=utf8
import re
from bs4 import BeautifulSoup
class Html(object):
    def clean(self, html_doc):
        regex = u"(?:.*?)车牌号：(.*?)号牌类型：(?:.*?)违法时间：(.*?)凭证编号：(.*?)违法地点：(.*?)采集机关：(.*?)违法内容：(.*?)违反条款：(.*?)状态：(.*?).*"
        soup = BeautifulSoup(html_doc)
        t = soup.find_all(attrs={'bgcolor':re.compile("#6B654D$"),
            'class':re.compile("chinses1$")})
        tickets = []
        for elm in t:
            tds = elm.find_all('td')
            ticket = []
            for td in tds:
                ticket.append("".join(td.stripped_strings))
            content = "".join(ticket)
            pattern = re.compile(regex, re.IGNORECASE)
            targets_matched = pattern.findall(content)
            for target in targets_matched:
                (pn, when, sn, addr, w, c, rules, status) = target
                tickets.append(dict(
                    pn=pn,
                    when=when,
                    sn=sn,
                    addr=addr,
                    w=w,
                    c=c,
                    rules=rules,
                    status=status
                    ))
        return tickets



html = Html()

if __name__ == '__main__':
    with open('data.html', 'r') as f:
        res = html.clean(f.read())

    print res
