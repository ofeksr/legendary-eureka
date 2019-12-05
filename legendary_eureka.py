#!/usr/bin/env python3

import requests
import urllib.request
import re
from bs4 import BeautifulSoup


class Resource:
    def __init__(self, name):
        self.name = name

    def get_jobs(self):
        return None


class Linkedin(Resource):
    def __init__(self):
        Resource.__init__(self, 'linkedin')

    def scrap(self, jobsURL):
        try:
            # parsing jobs URL with
            page = urllib.request.urlopen(jobsURL)
            soup = BeautifulSoup(page, 'html.parser')
            if soup is not None:
                return soup
            else:
                return None
        except NameError:
            print('Error while scraping information from LinkedIn')

    def get_jobs(self, url):
        soup = self.scrap(url)
        jobs = self.extractJobs(soup)
        return jobs

    def extractJobs(self, soup):
        if soup is not None:
            jobTitleRegex = re.compile('^result-card__full-card-link')
            jobsList = soup.find_all('a', attrs={'class': jobTitleRegex})
            companyTitleRegex = re.compile('COMPANY-*')
            companysList = soup.find_all('label', attrs={'for': companyTitleRegex})
            linksList = []
            for link in jobsList:
                linksList.append(link.get('href'))
            finalList = []
            for job, company, link in zip(jobsList, companysList, linksList):
                finalList.append(
                    'Job Title: ' + str(job.getText()) + ',Comapny: ' + str(company.getText()) + ', Link:' + link)
            # Converting final list into dict
            finalDict = {i: finalList[i] for i in range(0, len(finalList))}
            return finalDict
        else:
            return None


class Indeed(Resource):
    def __init__(self):
        Resource.__init__(self, 'indeed')

    # TODO
    def get_jobs(self):
        pass


class Glassdoor(Resource):
    def __init__(self):
        Resource.__init__(self, 'glassdoor')

    # TODO
    def get_jobs(self):
        pass