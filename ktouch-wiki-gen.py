#!/usr/bin/python2.7

#    Copyright © 2010 Spencer Krum

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from urllib import FancyURLopener
from BeautifulSoup import BeautifulSoup
import re
import datetime

url = "http://en.wikipedia.com/wiki/lasers"

def doit():
    
    class MyOpener(FancyURLopener) :
        version = 'Mozilla/5.0 (Windows NT 5.1; U; en-US; rv:1.8.1) Gecko/20091102 Firefox/3.5.5'
        
    # get the wikipedia mainpage
    myopener = MyOpener()
    article = myopener.open(url).read()

    #Beautiful soup you are my hero
    soup = BeautifulSoup(''.join(article))
    #process name o file
    title = soup.title.string
    t = str(title)
    t = t.split()
    for i in range(4):
        t.pop()
    strtitle = ''
    for i in t:
        strtitle += i

    paragraphs = soup.findAll('p')
    text = []
    for i in paragraphs:
        t =  str(i)
        f = re.sub('<[a-zA-Z\/][^>]*>','',t) #parse out html
        s = re.sub('\[\d?\d?\d?\]', '', f) #parse out citations
        text.append(s)
    
    kttitle = strtitle + '.ktouch.xml'
    ktouchfile = open(kttitle, 'w')
    
    ktouchfile.write('<?xml version="1.0" ?>\n')
    ktouchfile.write('<KTouchLecture>\n')
    ktouchfile.write('\t<Title>\n')
    ktouchfile.write('\t\t%s\n' % strtitle)
    ktouchfile.write('\t</Title>\n')
    ktouchfile.write('\t<Comment>\n')
    datetoday = datetime.date.today()
    datetoday = str(datetoday)
    ktouchfile.write('\tMade by ktouch wiki gen - github.com/nibalizer/ktouch-wiki-gen, retrieved from wikipedia on %s\n' % datetoday)
    ktouchfile.write('\t<FontSuggestions>\n')
    ktouchfile.write('\t\tCourier 10 Pitch\n')
    ktouchfile.write('\t</FontSuggestions>\n')
    ktouchfile.write('\t<Levels>\n')

    linelength = 70
    levels = []

    for s in text:
        lines = []
        length = len(s)
        c = 0
        print "total length is %s" %length
        print s
        while c <= length:
            oldc = c
            c += linelength
            #from pdb import set_trace; set_trace()
            print c
            #if length == 514:
            #    from pdb import set_trace; set_trace()
            if oldc < (length - linelength):
                while s[c] != ' ' :
                    c += 1
                    #if length == 514:
                       # from pdb import set_trace; set_trace()
                    if (c == (len(s)-0)):
                        lines.append(s[oldc:len(s)])
                        break;

                    if (c == (len(s)-1)):
                        lines.append(s[oldc:len(s)])
                        break;
                lines.append(s[oldc:c])
            else:
                lines.append(s[oldc:length])
        levels.append(lines)

    for level in levels:
        ktouchfile.write('\t\t<Level>\n')
        for line in level:
            ktouchfile.write('\t\t\t<Line>\n')
            ktouchfile.write('\t\t\t\t%s\n' % line)
            ktouchfile.write('\t\t\t</Line>\n')
        ktouchfile.write('\t\t</Level>\n')
    
    ktouchfile.write('\t</Levels>\n')
    ktouchfile.write('</KTouchLecture>\n')
#<?xml version="1.0" ?>
#<KTouchLecture>
#  <Title>
#    Colemak (auto-generated)
#  </Title>
#  <Comment>
#    2005-12-15 Shai Coleman, http://colemak.com/ . Public domain. Modified by Sascha Peilicke 2008-08-07
#  </Comment>
#  <FontSuggestions>
#    Courier 10 Pitch
#  </FontSuggestions>
#  <Levels>
#
#  </Levels>
#</KTouchLecture>
    print text


doit()
