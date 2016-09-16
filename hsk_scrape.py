# -*- coding: utf_8 -*-

import sys
import time
import lxml
from lxml import etree

from selenium import webdriver
from bs4 import BeautifulSoup

def hsk_vocab_scrape(url):
    #driver = webdriver.PhantomJS(service_log_path=None)
    wd = webdriver.Firefox()
    wd.get(url)
    
    # Get a mouse
    mouse = webdriver.ActionChains(wd)

    # element that mouse hovers 
    mh = wd.find_element_by_xpath("/html/body[@class='nomarginpadding ']/div[@id='contentarea']/table/tbody/tr/td[@class='resultswrap']/table[@class='wordresults']/tbody/tr[@class='row']/td[@class='actions']/div[@class='nonprintable']/div/div[@class='c']/img")
    mouse.move_to_element(mh).perform

    
    mc = wd.find_element_by_xpath("/html/body[@class='nomarginpadding ']/div[@id='contentarea']/table/tbody/tr/td[@class='resultswrap']/table[@class='wordresults']/tbody/tr[@class='row']/td[@class='actions']/div[@class='nonprintable']/div/div[@class='e']/div[@class='b']/a[3]")
    
    mouse.click(mc).perform()
    
    # wait until it's loaded
    time.sleep(5)    
    
    #print(wd.page_source)
    html = wd.page_source.encode('utf-8')
    

    #print(html)

    #elem = driver.find_element_by_id("section_word_simple")
    #element.click()
    #driver.save_screenshot('click.png')

    #mouse = webdriver.ActionChains(self.webdriver)
    #element = wd.find_element_by_xpath("//a[@name=\"buy_button_link> \"]")
    #mouse.move_to_element(element).perform()

    soup = BeautifulSoup(html, "lxml")
    #header = soup.find('//*[@id="contentarea"]/table/tbody/tr/td/table/tbody/tr[2]/td/')
    target = soup.find("html").find("body").find("div", id='contentarea').find("td", class_="resultswrap").find("table", class_="wordresults").find("table", attrs={"cellpadding":"0", "cellspacing":"0"}).textarea.string
    print(target)


    

    #htmlparser = etree.HTMLParser()
    #tree = etree.parse(html, htmlparser)
    #tree.xpath('//*[@id="contentarea"]/table/tbody/tr/td/table/tbody/tr[2]/td/')

    

if __name__ == '__main__':
    url = 'http://www.mdbg.net/chindict/chindict.php?page=worddict&wdrst=0&wdqb=%E4%BB%B7%E9%92%B1'
    #print(url)
    hsk_vocab_scrape(url)