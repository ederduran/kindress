#-*- coding: utf-8 -*-
import feedparser
import BeautifulSoup, markdown2, html2text, readability
import time, urllib2, codecs, os, sys, getopt, sh

from sendemail import sendemail
from future import Future
from datetime import date, datetime, timedelta
from helper import strip_tags

class KindressCore:
  def __init__(self):
    self.data = Data()
    self.path = '/home/varl/projects/kindress'

  def start(filename, user):
    filename = filename+'_'+date.today().isoformat()
    self.data.prettyname = 'Toilet Literature, '+date.today().isoformat()
    self.data.name = filename
    self.data.filename = filename+'.html'
    with open(os.path.join(self.path, 'database.flat')) as f:
      urls = f.readlines()

    feeds = self.get_feed(urls)
    article = codecs.open(os.path.join(self.path,'html',filename+'.html'),'w+',encoding='utf-8')
    article.write(self.content(feeds).decode('utf-8'))
    article.close()

    welcome = codecs.open(os.path.join(self.path, 'html','welcome.html'),'w+',encoding='utf-8')
    welcome.write(self.welcome())
    welcome.close()

    toc = codecs.open(os.path.join(self.path, 'html','toc.html'),'w+',encoding='utf-8')
    toc.write(self.toc(feeds).decode('utf-8'))
    toc.close()

    ncx = codecs.open(os.path.join(self.path, 'html',filename+'.ncx'), 'w+',encoding='utf-8')
    ncx.write(self.ncx(feeds))
    ncx.close()

    opf = codecs.open(os.path.join(self.path, 'html',filename+'.opf'), 'w+',encoding='utf-8')
    opf.write(self.opf().decode('utf-8'))

    kindlegen = sh.Command(os.path.join(self.path, 'bin', 'kindlegen'))
    kindlegen(os.path.join(opf.name), '-gif',_ok_code=[0,1])
    opf.close()

    sender = user.email
    password = user.email_password
    recipient = user.kindle_device
    subject = 'Daily Digest '+date.today().isoformat()
    message = 'Sir, your daily digest. xoxo --Kindress'

    sendemail(sender, password, recipient, subject, message)

  def welcome(self):
    # returns a quote of the day between the cover and the toc
    return '<html><head><meta http-equiv="content-type" content="text/html; charset=utf-8"/><link rel="stylesheet" type="text/css" href="base.css"/></head><body><div class="break"><center><blockquote>A great idea can often be found in the combination of two existing ideas.</blockquote><em>-A friend</em></center></div></body></html>'

  def get_feed(self, urls):
    future_calls = [Future(feedparser.parse, url.strip('\n')) for url in urls]
    feeds = [future_obj() for future_obj in future_calls]

    entries = []
    for feed in feeds:
      entries.extend(feed.entries)

    sorted_entries = filter(todays_catch, sorted(entries, key=lambda entry: entry.published_parsed))

    print len(sorted_entries)
    return sorted_entries[::-1]

  def content(self, entries):
    html_content = ['<html><head><meta http-equiv="content-type" content="text/html; charset=utf-8"/><style type="text/css">'+self.style()+'</style></head><body>']
    for idx, entry in enumerate(entries):
      div = []
      div.extend('<div class="break">')
      div.extend('<a name="article_'+str(idx)+'"></a>')
      div.extend('<div class="titlediv"><h1 class="kindresstitle"><center>'+entry.title+'</center></h1><hr/></div>')
      if ('description' in entry and len(entry.description) > 200):
        div.extend(entry.description)
      elif ('content' in entry and len(entry.content) > 200):
        for stuff in entry.content:
          div.extend(stuff.value)
      else:
        div.extend(readability.readability.Document(urllib2.urlopen(entry.link).read()).summary(True))
      div.extend('</div>')

      foo = BeautifulSoup.BeautifulSoup(''.join(div))
      alltags = foo.findAll("img")
      counter = 0
      for imgidx, img in enumerate(alltags):
        filename, fileext = os.path.splitext(img['src'])
        if fileext.lower() in ['.jpg', '.jpeg', '.gif']:
          if counter == 0:
            name = 'image_'+str(idx)+'_'+str(imgidx)+fileext.lower()
            imgurl = img['src']            
            print 'creating/saving image: '+os.path.join('html', name)
            try:
              f = codecs.open(os.path.join('html', name),'w+')
              f.write(urllib2.urlopen(imgurl).read())
              f.close()
              title = foo.find('div', {'class': 'titlediv'})
              title.insert(2, BeautifulSoup.BeautifulSoup('<center><img class="title-image" src="'+name+'"/></center>'))
              counter = counter+1
            except urllib2.HTTPError:
              print 'image save failed.. skipping to next'
              counter = 0
          img.extract()
          img['src'] = name
        else:
          img.extract()
      html_content.extend(foo.prettify())
    html_content.extend('</body></html>')
    html = BeautifulSoup.BeautifulSoup(''.join(html_content))
    return html.prettify()

  def toc(self, entries):
    toc = []
    toc.extend('<html><head><meta http-equiv="content-type" content="text/html; charset=utf-8"/><style stype="text/css">'+self.style()+'</style></head><body>')
    toc.extend('<div>')
    toc.extend('<h1 class="kindresstitle"><center><b>/!\</b> <em>table of contents</em> <b>/!\</b></center></h1>')
    for idx, entry in enumerate(entries):
      toc.extend('<div>')
      toc.extend(str(idx+1)+'. <a href="'+self.data.filename+'#article_'+str(idx)+'">'+entry.title+'</a>')
      toc.extend('</div>')
    toc.extend('<h1 class="kindresstitle"><center><em>~* ~* ~* ~* ~* ~*</em></center></h1>')
    toc.extend('</div>')
    toc.extend('</body></html>')
    return BeautifulSoup.BeautifulSoup(''.join(toc)).prettify()

  def ncx(self, entries):
    ncx = []
    ncx.extend("""<?xml version="1.0" encoding="UTF-8"?>
       <!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
        "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
        <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en-US">
        <head>
        """)
    ncx.extend('<meta name="dtb:uid" content="'+self.data.name+'"/>')
    ncx.extend("""<meta name="dtb:depth" content="2"/>
        <meta name="dtb:totalPageCount" content="0"/>
        <meta name="dtb:maxPageNumber" content="0"/>
        </head>
        """)
    ncx.extend('<docTitle><text>'+self.data.name+'</text></docTitle>')
    ncx.extend('<docAuthor><text>Viktor Varland, viktor@vardevs.se</text></docAuthor>')
    ncx.extend('<navMap>')
    ncx.extend("""
    <navPoint class="welcome" id="welcome" playOrder="2">
      <navLabel>
        <text>Welcome</text>
      </navLabel>
      <content src="welcome.html"/>
    </navPoint>    
    """)
    ncx.extend("""
    <navPoint class="toc" id="toc" playOrder="2">
      <navLabel>
        <text>Table of Contents</text>
      </navLabel>
      <content src="toc.html"/>
    </navPoint>    
    """)
    for idx, entry in enumerate(entries):
      ncx.extend('<navPoint id="article_'+str(idx)+'" playOrder="'+str(idx+3)+'">')
      ncx.extend('<navLabel><text>'+entry.title+'</text></navLabel>')
      ncx.extend('<content src="'+self.data.filename+'#article_'+str(idx)+'"/>')
      ncx.extend('</navPoint>')
    ncx.extend('</navMap></ncx>')

    return ''.join(ncx)

  def opf(self):
    opf = []
    opf.extend('<?xml version="1.0" encoding="utf-8"?>')
    opf.extend('<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="'+self.data.name+'">')
    opf.extend('<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">')
    opf.extend('<dc:title>'+self.data.prettyname+'</dc:title>')
    opf.extend('<dc:language>en-us</dc:language>')
    opf.extend('<meta name="cover" content="cover"/>')
    opf.extend('<dc:creator>Kindress</dc:creator>')
    opf.extend('<dc:publisher>vardevs</dc:publisher>')
    opf.extend('<dc:subject>Reference</dc:subject>')
    opf.extend('<dc:date>'+date.today().isoformat()+'</dc:date>')
    opf.extend('<dc:description>A custom set of RSS articles in a convenient e-book format.</dc:description>')
    opf.extend('</metadata>\n')
    opf.extend('<manifest>')
    opf.extend('<item id="item" media-type="application/xhtml+xml" href="'+self.data.filename+'"/>')
    opf.extend('<item id="welcome" media-type="application/xhtml+xml" href="welcome.html"/>')
    opf.extend('<item id="toc" media-type="application/xhtml+xml" href="toc.html"/>')
    opf.extend('<item id="ncx" media-type="application/x-dtbncx+xml" href="'+self.data.name+'.ncx"/>')
    opf.extend('<item id="cover" media-type="image/gif" href="img/cover.gif"/>')
    opf.extend('</manifest>\n')
    opf.extend('<spine toc="ncx">')
    opf.extend('<itemref idref="welcome"/>')
    opf.extend('<itemref idref="toc"/>')
    opf.extend('<itemref idref="item"/>')
    opf.extend('</spine>\n')
    opf.extend('<guide>\n')
    opf.extend('<reference type="welcome" title="Welcome" href="welcome.html"/>')
    opf.extend('<reference type="toc" title="Table of Contents" href="toc.html"/>')
    opf.extend('<reference type="text" title="Articles" href="'+self.data.filename+'"/>')
    opf.extend('\n</guide>')
    opf.extend('</package>')
    return ''.join(opf)
            
  def style(self):
    css = codecs.open(os.path.join('html','base.css'), 'r')
    return css.read()

class Data:
  pass

def todays_catch(x):
  published = time.mktime(x.published_parsed)
  if datetime.now() - datetime.fromtimestamp(published) < timedelta(days=1):
    return True
  else:
    return False
