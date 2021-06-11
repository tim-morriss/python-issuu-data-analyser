import itertools

from user_agents import parse

import continent_converter as cc
import country_converter as pc
from json_loader import JsonLoader


class DataAnalyser:
    """
    Contains various data analysis methods for issuu json files.

    Attributes
    ----------
    json_loader : JsonLoader
    countries : dict
        k: alpha2 country code
        v: number of readers
    continents : dict
        k: alpha2 continent code
        v: number of readers
    devices : dict
        k: shorthand device name
        v: number of those devices
    devices_verbose : dict
        k: full user agent string
        v: number of those devices
    read_times : dict
        k: visitor UUID
        v: their total read time in milliseconds
    likes : dict
        two dimensional dictionary
        k: user uuid of reader
            k: document uuid that they read
            v: how many times they read it
    doc_id : str
        string to keep doc_id
        used to check if process has already run
    """

    def __init__(self, json_loader):
        self.json_loader = json_loader
        self.countries = {}
        self.continents = {}
        self.devices = {}
        self.devices_verbose = {}
        self.read_times = {}
        self.likes = {}
        self.doc_id = ''

    def empty(self):
        """Function to empty all object variables."""
        self.countries = {}
        self.continents = {}
        self.devices = {}
        self.devices_verbose = {}
        self.read_times = {}
        self.likes = {}
        self.doc_id = ''

    # task 2a
    def views_by_country(self, doc_id):
        """Counts the number of readers per country.

        Method takes .json file and writes to self.countries.
        Only looks at the 'subject_doc_id', 'visitor_country' and 'event_type' fields.
        Only counts it as being read if 'event_type' is 'read'.

        Parameters
        ----------
        doc_id : str
            subject_doc_id of issuu document

        Returns
        -------
        dict
        """
        if self.doc_id == doc_id and self.countries:
            return self.countries
        else:
            self.doc_id = doc_id
            for line in self.json_loader.read_json():
                if 'subject_doc_id' in line and 'visitor_country' in line and 'event_type' in line:
                    if line['subject_doc_id'] == doc_id and line['event_type'] == 'read':
                        country = pc.convert_country_alpha2_to_country_name(line['visitor_country']) + "\n(%s)" % line['visitor_country']
                        # adapted from https://stackoverflow.com/a/473344
                        self.countries[country] = self.countries.get(country, 0) + 1
            return self.countries

    # task 2b
    def group_by_continent(self, doc_id, flag=True):
        """Groups entries in self.countries as continents

        Parameters
        ----------
        doc_id : str
            subject_doc_id of issuu document
        flag : bool
            True = generate views by country first
            False = use values stored in self.countries

        Returns
        -------
        dict
        """
        if not self.countries and flag:
            self.views_by_country(doc_id)
            return self.group_by_continent(doc_id, False)
        elif self.doc_id == doc_id and self.continents:
            return self.continents
        else:
            self.doc_id = doc_id
            for country in self.countries:
                continent = cc.convert_country_alpha2_to_continent(country.split(')')[0].split('(')[1])
                self.continents[continent] = self.continents.get(continent, self.countries[country]) + 1
            return self.continents

    # task 3a
    def count_devices_verbose(self):
        """Returns dictionary with key of verbose device name and value of the number present in the json file.

        e.g. "Mozilla/5.0 (BB10; Touch) AppleWebKit/537.10+ (KHTML, like Gecko) Version/10.1.0.2050 Mobile Safari/537.10+": 1

        Returns
        -------
        dict
        """
        if self.devices_verbose:
            return self.devices_verbose
        else:
            for line in self.json_loader.read_json():
                if 'visitor_useragent' in line and 'event_type' in line:
                    if line['event_type'] == 'read':
                        browser = line['visitor_useragent']
                        self.devices_verbose[browser] = self.devices_verbose.get(browser, 0) + 1
            return self.devices_verbose

    # task 3b
    def count_devices(self):
        """Returns dictionary with key of short device name and value of the number present in the json file.

        e.g. "Chrome": 1

        Returns
        -------
        dict
        """
        if self.devices:
            return self.devices
        else:
            for line in self.json_loader.read_json():
                if 'visitor_useragent' in line and 'event_type' in line:
                    if line['event_type'] == 'read':
                        browser = line['visitor_useragent']
                        # browser_short = browser.split('/')[0] + "-" + parse(browser).browser.family
                        browser_short = parse(browser).browser.family
                        self.devices[browser_short] = self.devices.get(browser_short, 0) + 1

    # task 4
    def most_active_readers(self, n=10):
        """Returns n amount of the most active readers based on 'event_readtime'.


        Parameters
        ---------
        n : int
            The number of most active readers to return

        Returns
        -------
        dict
        """
        if self.read_times:
            return self.read_times
        else:
            for line in self.json_loader.read_json():
                if 'event_readtime' in line:
                    self.read_times[line['visitor_uuid']] = self.read_times.get(line['visitor_uuid'], 0) + line['event_readtime']
            # adapted from https://stackoverflow.com/a/613218
            ordered_read_times = dict(sorted(self.read_times.items(), key=lambda item: item[1], reverse=True))
            # adapted from https://stackoverflow.com/a/7971660
            return dict(itertools.islice(ordered_read_times.items(), n))

    # part 5a
    def return_document_visitors(self, doc_id):
        """Returns the readers of a document

        Parameters
        ---------
        doc_id : str
            uuid of issuu document

        Returns
        -------
        dict
        """
        readers = {}
        for line in self.json_loader.read_json():
            if 'subject_doc_id' in line and 'visitor_uuid' in line and 'event_type' in line:
                if line['subject_doc_id'] == doc_id and line['event_type'] == 'read':
                    readers[line['visitor_uuid']] = readers.get(line['visitor_uuid'], 0) + 1
        return readers

    # part 5b
    def return_user_read(self, user_id):
        """Returns all documents read by user and how many times they read it

        Parameters
        ---------
        user_id : str
            uuid of user

        Returns
        -------
        dict
        """
        docs = {}
        for line in self.json_loader.read_json():
            if 'subject_doc_id' in line and 'visitor_uuid' in line and 'event_type' in line:
                if line['visitor_uuid'] == user_id and line['event_type'] == 'read':
                    docs[line['subject_doc_id']] = docs.get(line['subject_doc_id'], 0) + 1
        return docs

    # part 5c
    def also_likes(self, doc_id, user_id=None, sorting_func=None):
        """Returns a dictionary of other documents read by the readers of current document

        Parameters
        ---------
        doc_id : str
            uuid of document
        user_id : str
            the user_id to avoid
        sorting_func : function
            optional sorting function

        Returns
        -------
        dict
        """
        if doc_id is None:
            print('Please input a doc id!')
        if self.likes and self.doc_id == doc_id:
            return self.likes
        else:
            readers = self.return_document_visitors(doc_id)
            self.likes = {}
            for reader in readers:
                if reader == user_id:
                    # if the reader is the one supplied then skip
                    continue
                else:
                    # add to output dict
                    if reader not in self.likes:
                        self.likes[reader] = {}
                    # find the documents they also read
                    also_read = self.return_user_read(reader)
                    # count these documents
                    for read in also_read:
                        if read in self.likes[reader]:
                            # print("+1 for: %s" % str(read))
                            self.likes[reader][read] += 1
                        else:
                            self.likes[reader][read] = 0
            if sorting_func is None:
                self.doc_id = doc_id
                return self.likes
            else:
                return sorting_func(self.likes)

    # part 5d
    def top_also_like(self, doc_id, n=10, user_id=None, sorting_func=None):
        """ Returns the top n documents that show up in the also likes dictionary

        Parameters
        ----------
        doc_id : str
            document ID
        n : int
            number of results to return
        user_id : str
            user ID
        sorting_func
            optional sorting function

        Returns
        -------
        dict
        """
        if self.likes and self.doc_id == doc_id:
            readers = self.likes
            sorted_docs = {}
            for reader in readers:
                for doc in readers[reader]:
                    sorted_docs[doc] = sorted_docs.get(doc, 0) + 1
            sorted_docs = dict(sorted(sorted_docs.items(), key=lambda item: item[1], reverse=True))
            return dict(itertools.islice(sorted_docs.items(), n))
        else:
            readers = self.also_likes(doc_id, user_id, sorting_func)
            sorted_docs = {}
            for reader in readers:
                for doc in readers[reader]:
                    sorted_docs[doc] = sorted_docs.get(doc, 0) + 1
            sorted_docs = dict(sorted(sorted_docs.items(), key=lambda item: item[1], reverse=True))
            return dict(itertools.islice(sorted_docs.items(), n))
