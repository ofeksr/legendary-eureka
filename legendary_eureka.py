#!/usr/bin/env python3

import json
import random
import time

import requests
from bs4 import BeautifulSoup
from linkedin import linkedin


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

    # TODO
    def get_jobs(self):
        pass


class Glassdoor(Resource):
    def __init__(self):
        Resource.__init__(self, 'glassdoor')

    # TODO: wrap requests.post parts with try / except.
    def get_jobs(self, job_title: str, job_location: str = None, job_type: str = ''):
        """
        using part of code from: https://gist.github.com/scrapehero/352286d0f9dee87990cd45c3f979e7cb
        :param job_title: for example: 'python developer'
        :param job_type: optional, 'fulltime' or ___ or ___ TODO: get job_type possibilities
        :param job_location: Jerusalem (Israel), Tel Aviv-Yafo (Israel), Haifa (Israel), Ashdod (Israel),
         Bnei Brak (Israel), Netanya (Israel), Bene Beraq (Israel), Bat Yam (Israel), Ramat Gan(Israel),
         Ashqelon (Israel).
        """

        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'accept-encoding': 'gzip, deflate, sdch, br',
                   'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
                   'referer': 'https://www.glassdoor.com/',
                   'upgrade-insecure-requests': '1',
                   'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
                   'Cache-Control': 'no-cache',
                   'Connection': 'keep-alive'
                   }

        location_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.01',
            'accept-encoding': 'gzip, deflate, sdch, br',
            'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
            'referer': 'https://www.glassdoor.com/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
        data = {"term": 'Israel',
                "maxLocationsToReturn": 10}

        location_url = "https://www.glassdoor.co.in/findPopularLocationAjax.htm?"

        # Getting location id for search location
        print("Fetching location details")
        location_response = requests.post(location_url, headers=location_headers, data=data).json()

        if job_location in [dictionary['label'] for dictionary in location_response]:
            location_response = [dictionary for dictionary in location_response
                                 if job_location in dictionary['label']]
        else:
            print('Job location not found, printing jobs from all locations in Israel..')

        for i, location in enumerate(location_response):
            job_listings = {}
            place_id = location_response[i]['locationId']
            place_label = location_response[i]['label']

            if place_id:
                print("Fetching jobs for location: ", place_label)

                #  delay time for avoiding block by requests.post
                #  TODO: change delay time with better (and faster) anti-block strategy.
                if i > 0:
                    delays = [3, 2, 1]
                    delay = random.choice(delays)
                    time.sleep(delay)

                job_listing_url = 'https://www.glassdoor.com/Job/jobs.htm'

                # Form data to get job results
                data = {
                    'clickSource': 'searchBtn',
                    'sc.keyword': job_title,
                    'locT': 'C',
                    'locId': place_id,
                    'jobType': job_type
                }

                response = requests.post(job_listing_url, headers=headers, data=data)
                soup = BeautifulSoup(response.content, "html.parser")

                for a in soup.find_all('a', href=True):

                    if a['href'].startswith('/partner/'):
                        link = a['href']
                        full_link = 'https://www.glassdoor.com'+link  # TODO: shrink full links length with tiny url?
                        job_id = link.split('jobListingId=')[1]

                        if (a.string is not None) and (a.string != 'JobInfo'):

                            if place_label in job_listings:
                                if job_id not in job_listings[place_label]:
                                    job_listings[place_label].update({job_id: [a.string, full_link]})
                                else:
                                    if a.string not in job_listings[place_label][job_id]:
                                        job_listings[place_label][job_id].append(a.string)
                            else:
                                job_listings[place_label] = {job_id: [a.string, full_link]}

                print(json.dumps(job_listings, indent=4, ensure_ascii=False))
