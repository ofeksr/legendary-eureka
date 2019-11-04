#!/usr/bin/env python3

import requests
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

    # TODO
    def get_jobs(self):
        pass
