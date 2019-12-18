#!/usr/bin/env python3

import re
import requests
import urllib.request

from bs4 import BeautifulSoup


class Resource:
    def __init__(self, name):
        self.name = name

    def get_jobs(self):
        return None


class Linkedin(Resource):
    def __init__(self):
        Resource.__init__(self, 'linkedin')

    # TODO
    def get_jobs(self):
        pass


class Indeed(Resource):
    def __init__(self):
        Resource.__init__(self, 'indeed')
    
    
    def get_page(self, what,where):
        """ Takes the query attributes - 'what' (job description) and 'where' (area for job search)
            and build the right URL string for Indeed.com job search according to the rellevant preferences.
           
            Parameters
            ----------
            whar : str
                the job description for the search
            where : str
                the area for job search
            wt : str
                the splitted string of parameter what
            url : str
                the finaly url string
        """
        
        what = str(what)
        where = str(where)
        wt = what.split()
        what = ""
        for i in range(len(wt)):   #re-build of the "what" parameter, to match the Indeed's url structure
            what+= wt[i]
            if(i<len(wt)-1):
                what+="+"
        url = "https://il.indeed.com/jobs?q="+str(what)+"&l="+str(where)+"&sort=date"
        print(url)
        return url

    def get_soup(self, url):
        """ Returns the BeautifulSoup object made from the html code of the given url
        
            Parameters
            ----------
            utl : str
                the url string of the relevant job search in Indeed.com
            page: urllib object
                the search page in a urllib object
            soup : BeautifulSoup object
                the BeautifulSoup object from the urllib page
            page_count: list
                gets all "searchCountPages" IDs to check if there are results for the search or not
        """
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
    
    def get_jobList(self, soup,url): #builds list of first 100 jobs found on indeed.com
        """
            This func goes over all job results in the page, filter the jobs published at last 30 days,
            and pharse them into a dictionary of the format- {Title: Link}.
            
            Parameters
            ----------
            jobsDict : Dict
                        the dictionary of all jobs found
            comp_lis : list
                        list of all companies of all jobs found on specific page
            title_link_lis : list
                            list of all 'a' elements of every job found on a specific page
                            from each a element the func takes the Title and the URL Link of the job
            date_lis : list
                        list of all publish dates of every job found on specific page
        """
        jobsDict ={}
        count_page = soup.find_all(id="searchCountPages")
        for cnt in count_page:
            countArr = [int(s) for s in str(cnt).split() if s.isdigit()]
        if len(countArr) > 1:
            pageN,amount_of_jobs = countArr
            loop_size = int(amount_of_jobs/10)
        for i in range(loop_size):
            url_run = url+"&start="+str(i*10)
            soup = self.get_soup(url_run)
            regex = re.compile('^company')
            comp_lis = soup.find_all('span', attrs={'class': regex})
            regex = re.compile('^jobtitle turnstileLink')
            title_link_lis = soup.find_all('a', attrs={'class': regex})
            regex = re.compile('^date')
            date_lis = soup.find_all('span', attrs={'class': regex})
            for link,company,date in zip(title_link_lis,comp_lis,date_lis):
                days = re.findall('\d+', str(date))
                if (len(days)==0 or (int(days[0])<30)):
                    jobsDict[(link.get('title')+","+company.get_text())] = ("http://il.indeed.com"+link.get('href'))
        return jobsDict
    
    def get_jobs(self, what, where):
        url = self.get_page(what,where)
        soup = self.get_soup(url)
        if soup is not None:
            jd = self.get_jobList(soup,url)
            return jd
        else:
            return None


class Glassdoor(Resource):
    def __init__(self):
        Resource.__init__(self, 'glassdoor')

    # TODO
    def get_jobs(self):
        pass
