# -*- coding: utf_8 -*-

import sys
import time
import lxml
import xlrd

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup


def excel_read(xlsfilename, sheet_idx):
	book = xlrd.open_workbook(xlsfilename)
	sheet = book.sheet_by_index(sheet_idx)
	elems = []
	# skip the first row
	for row in range(1, sheet.nrows):
        # read A column
		elems.append(sheet.cell(row, 0).value)
	return elems

def hsk_vocab_scrape(wd, url):
    #driver = webdriver.PhantomJS(service_log_path=None)
    wd.get(url)
    
    # Get a mouse
    mouse = webdriver.ActionChains(wd)

    # element that mouse hovers 
    mh = wd.find_element_by_xpath("/html/body[@class='nomarginpadding ']/div[@id='contentarea']/table/tbody/tr/td[@class='resultswrap']/table[@class='wordresults']/tbody/tr[@class='row']/td[@class='actions']/div[@class='nonprintable']/div/div[@class='c']/img")
    mouse.move_to_element(mh).perform

    # Click "Copy this entry in plain text"
    #mc = wd.find_element_by_xpath("/html/body[@class='nomarginpadding ']/div[@id='contentarea']/table/tbody/tr/td[@class='resultswrap']/table[@class='wordresults']/tbody/tr[@class='row']/td[@class='actions']/div[@class='nonprintable']/div/div[@class='e']/div[@class='b']/a[3]")
    mc = wd.find_element_by_xpath("/html/body[@class='nomarginpadding ']/div[@id='contentarea']/table/tbody/tr/td[@class='resultswrap']/table[@class='wordresults']/tbody/tr[@class='row']/td[@class='actions']/div[@class='nonprintable']/div/div[@class='e']/div[@class='b']/a[@title='Copy this entry in plain text']")                               
    mouse.click(mc).perform()
    
    # wait until it's loaded
    #time.sleep(5)
    WebDriverWait(wd, 5).until(lambda d: d.find_element_by_xpath("/html/body[@class='nomarginpadding ']/div[@id='contentarea']/table/tbody/tr/td[@class='resultswrap']/table[@class='wordresults']/tbody/tr[2]/td/table").is_displayed())

    #driver.save_screenshot('click.png')    
    html = wd.page_source.encode('utf-8')    
    # Now scrape the targeta
    soup = BeautifulSoup(html, "lxml")
    try:
        target = soup.find("html").find("body").find("div", id='contentarea').find("td", class_="resultswrap").find("table", class_="wordresults").find("table", attrs={"cellpadding":"0", "cellspacing":"0"}).textarea.string
    except:
        target = "NOTFOUND"
    return target

if __name__ == '__main__':
    meaning_list = []
    wd = webdriver.Firefox()
    
    urlbase = 'http://www.mdbg.net/chindict/chindict.php?page=worddict&wdrst=0&wdqb={voca}'   
    vocas = excel_read("/Users/yusuke/Dropbox/Works/Python/HSK_Vocabulary_Builder/HSK_Vocabulary.xlsx", 0)

    i = 0
    for vocabulary in vocas:
        result = hsk_vocab_scrape(wd, urlbase.format(voca=vocabulary))
        meaning_list.append(result) 
        i += 1
        if i > 5:
            break

    out = open('result.txt', 'w')
    for meaning in meaning_list:
       out.write("%s\n" % (meaning))