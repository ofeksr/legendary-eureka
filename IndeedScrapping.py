# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 23:43:20 2019

@author: barjan
"""

from bs4 import BeautifulSoup
import urllib.request
import re

#this func builds the right query for the users job-defenition input
def get_page(what,where):
    wt = what.split()
    what = ""
    for i in range(len(wt)):   #re-build of the "what" parameter, to match the Indeed's url structure
        what+= wt[i]
        if(i<len(wt)-1):
            what+="+"
    url = "https://il.indeed.com/jobs?q="+str(what)+"&l="+str(where)
    print(url)
    return url

def get_soup(url):
    try:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        page_count = soup.find_all(id="searchCountPages")
        if (len(page_count)>0):   #if there's no id named "searchCountPages" that means there is no result for the search
            return soup
        else:
            print("No results for your search.")
    except:
        print("An error occured.")

def get_jobList(soup,url): #builds list of first 100 jobs found on indeed.com
    jobsList = []
    count_page = soup.find_all(id="searchCountPages")
    print (len(count_page))
    for cnt in count_page:
        countArr = [int(s) for s in str(cnt).split() if s.isdigit()]
    loop_size = 11
    if len(countArr) > 1:
        pageN,amount_of_jobs = countArr
        if amount_of_jobs < 100:
            loop_size = int(amount_of_jobs/10)
        print(amount_of_jobs)
    for i in range(loop_size):
        print(i)
        url_run = url+"&start="+str(i*10)
        soup = get_soup(url_run)
        regex = re.compile('^company')
        comp_lis = soup.find_all('span', attrs={'class': regex})
        regex = re.compile('^jobtitle turnstileLink')
        title_lis = soup.find_all('a', attrs={'class': regex})
        regex = re.compile('^p_')
        link_lis = soup.find_all(id=regex)
        for title,company,link in zip(title_lis,comp_lis,link_lis):
            jobsList.append(title.get('title')+","+company.get_text()+","+url_run+"&vjk="+link.get('data-jk'))
    return jobsList

def searchResults(jobsList):
        for job in jobsList:
            print(job)

def find_job(what,where):
    if not ((type(what) is str) and (type(where) is str)):    #checking input type
        print("Bad syntax.")
    else:
        url = get_page(what,where)
        soup = get_soup(url)
        if soup is not None:
            jl = get_jobList(soup,url)
            searchResults(jl)

find_job("software","haifa")