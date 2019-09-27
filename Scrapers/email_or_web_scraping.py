#!/usr/bin/env python
# coding: utf-8

# In[1]:


import logging
import os
import pandas as pd
import re
import scrapy
import csv
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from googlesearch import search
logging.getLogger('scrapy').propagate = False


# In[2]:


def get_urls(tag, n, language):
    urls = [url for url in search(tag, stop=n, lang=language)][:n]
    return urls


# In[3]:


class MailSpider(scrapy.Spider):
    
    name = 'email'
    
    def parse(self, response):
        
        links = LxmlLinkExtractor(allow=()).extract_links(response)
        links = [str(link.url) for link in links]
        links.append(str(response.url))
        
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_link) 
            
    def parse_link(self, response):
        
        for word in self.reject:
            if word in str(response.url):
                return
            
        html_text = str(response.text)
#         mail_list = re.findall("^\w+([-+.']\w+)*@[A-Za-z\d]+\.(?:com|sg|edu)", html_text)
        mail_list = re.findall('\w+@\w+\.{1}\w+', html_text)

        dic = {'email': mail_list, 'link': str(response.url)}
        df = pd.DataFrame(dic)
        
        df.to_csv(self.path, mode='a', header=False)
        df.to_csv(self.path, mode='a', header=False)


# In[4]:


def ask_user(question):
    response = input(question + ' y/n' + '\n')
    if response == 'y':
        return True
    else:
        return False
def create_file(path):
    response = False
    if os.path.exists(path):
        response = ask_user('File already exists, replace?')
        if response == False: return 
    
    with open(path, 'wb') as file: 
        file.close()


# In[5]:


def get_info(tag, n, language, path, reject=[]):
    
    create_file(path)
    df = pd.DataFrame(columns=['email', 'link'], index=[0])
    df.to_csv(path, mode='w', header=True)
    
    print('Collecting Google urls...')
    google_urls = get_urls(tag, n, language)
#     google_urls = ['http://ecube.com.sg/']
    
    print('Searching for emails...')
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
    process.crawl(MailSpider, start_urls=google_urls, path=path, reject=reject)
    process.start()
    
    print('Cleaning emails...')
    df = pd.read_csv(path, index_col=0)
    df.columns = ['email', 'link']
    df = df.drop_duplicates(subset='email')
    df = df.reset_index(drop=True)
    df.to_csv(path, mode='w', header=True)
    
    return df


# In[6]:


def get_emails(websites, path, reject=[]):
    
    create_file(path)
    df = pd.DataFrame(columns=['email', 'link'], index=[0])
    df.to_csv(path, mode='w', header=True)
    
    print('Searching for emails...')
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
    process.crawl(MailSpider, start_urls=websites, path=path, reject=reject)
    process.start()
    
    print('Cleaning emails...')
    df = pd.read_csv(path, index_col=0)
    df.columns = ['email', 'link']
    df = df.drop_duplicates(subset='email')
    df = df.reset_index(drop=True)
    df.to_csv(path, mode='w', header=True)
    
    return df


# In[7]:


websites_list = [];

with open('tuition_websites.csv', newline='') as csvfile:
    websites = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in websites:
        websites_list.append(row[0])
        
formatted_websites = websites_list[1:]


# In[8]:


# bad_words = ['facebook', 'instagram', 'youtube', 'twitter', 'wiki']
# df = get_info('Walter Education Centre', 10, 'en', 'tuition_emails.csv', reject=bad_words)
# emails = get_emails(formatted_websites, 'tuition_emails.csv', reject=bad_words)


# In[97]:


education_centre_names = []

with open('tuition_names.csv') as csvfile:
    tuitions = csv.reader(csvfile)
    for row in tuitions:
        name = ' '.join(row)
        education_centre_names.append(name)


# In[104]:


def get_tuition_urls(list_of_keywords, path):

    create_file(path)
    tuitions = []
    length_of_keywords = len(list_of_keywords)
    for keyword in list_of_keywords[:10]:
        google_url = get_urls(keyword, 1, 'en');
        tuitions.append((keyword, google_url[0]))
        progress = 'In progress: ' + str(list_of_keywords.index(keyword) + 1) +'/'+  str(length_of_keywords);
        print(progress,  end='\r')
        
    tuition_weblinks = pd.DataFrame(tuitions, columns = ['name' , 'url'])
    tuition_weblinks.to_csv(path)


# In[105]:


get_tuition_urls(education_centre_names, 'tuition_urls.csv')


# In[ ]:




