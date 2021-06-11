# Class to control the different parts of section 3

import json

from data_analyser import DataAnalyser
from histogram_plot import HistogramPlot
from likes_graph import LikesGraph
from json_loader import JsonLoader
from gui import GUI


class TaskManager:
    """
    Links the DataAnalyser class with each of the tasks specified in the coursework.

    Attributes
    ----------
    filename : str
        path to JSON file
    doc_id : str
        document uuid
    user_id : str
        user uuid
    task_id : str
        which task function to run
    """
    def __init__(self, filename=None, doc_id=None, user_id=None, task_id=None):
        self.doc_id = doc_id
        self.user_id = user_id
        self.json_loader = JsonLoader(filename)
        self.da = DataAnalyser(self.json_loader)
        self.hp = HistogramPlot()
        self.likes_graph = LikesGraph()
        self.orientation = 'h'
        self.tasks = {
            '2a': self.task_2a,
            '2b': self.task_2b,
            '3a': self.task_3a,
            '3b': self.task_3b,
            '4': self.task_4,
            '5a': self.task_5a,
            '5b': self.task_5b,
            '5c': self.task_5c,
            '5d': self.task_5d,
            '6': self.task_6,
            '7': self.gui
        }
        if task_id not in self.tasks:
            print('Please choose a task id from one of the following:'
                  '\n 2a, 2b, 3a, 3b, 4, 5d, 6, 7')
        else:
            self.tasks[task_id]()

    # Return a histogram of countries of viewers
    def task_2a(self, doc_id=None):
        if doc_id is not None:
            self.doc_id = doc_id
        output = self.da.views_by_country(self.doc_id)
        self.hp.show_histo(output, orient=self.orientation, xlabel='Number of readers', title='Views by country')

    # Return a histogram of continent of viewers
    def task_2b(self, doc_id=None):
        if doc_id is not None:
            self.doc_id = doc_id
        output = self.da.group_by_continent(self.doc_id)
        self.hp.show_histo(output, orient=self.orientation, xlabel='Number of readers', title='Views by continent')

    # Return a histogram of all browser identities of viewers
    def task_3a(self):
        output = self.da.count_devices_verbose()
        self.hp.show_histo(output, orient=self.orientation, xlabel='Number of devices', title='Counts of user devices')

    # Return a histogram of shortened browser identities of viewers
    def task_3b(self):
        self.da.count_devices()
        self.hp.show_histo(self.da.devices, orient=self.orientation, xlabel='Number of devices', title='Counts of user devices (shorthand)')

    # Return the top 10 readers based on read time
    def task_4(self):
        output = self.da.most_active_readers()
        print(json.dumps(output, indent=4))
        self.hp.show_histo(output, orient=self.orientation, xlabel='Read times (milliseconds)', title='Top user read times')

    # Return all the readers of a document
    def task_5a(self, doc_id=None):
        if doc_id is not None:
            self.doc_id = doc_id
        output = self.da.return_document_visitors(self.doc_id)
        print(json.dumps(output, indent=4))

    # Return all the documents read by a visitor
    def task_5b(self, user_id=None):
        if user_id is not None:
            self.user_id = user_id
        output = self.da.return_user_read(self.user_id)
        print(json.dumps(output, indent=4))

    # Returns an 'also like' list of documents
    def task_5c(self, doc_id, sorting_func=None):
        if doc_id is not None:
            self.doc_id = doc_id
        output = self.da.also_likes(self.doc_id, sorting_func)
        print(json.dumps(output, indent=4))

    # Returns a top 10 'also like' list of documents
    def task_5d(self, doc_id=None, user_id=None):
        if doc_id is not None:
            self.doc_id = doc_id
        if user_id is not None:
            self.user_id = user_id
        output = self.da.top_also_like(self.doc_id, 10, self.user_id)
        print(json.dumps(output, indent=4))

    # Generate a graph of the 'also likes' documents
    def task_6(self, doc_id=None, user_id=None):
        if doc_id is not None:
            self.doc_id = doc_id
        if user_id is not None:
            self.user_id = user_id
        self.likes_graph.draw_likes_graph(self.user_id, self.doc_id, self.da)

    # updates the filename stored in the object
    def update_filename(self, filename):
        self.json_loader.filename = filename
        self.da.empty()

    # calls the gui
    def gui(self):
        GUI(self)
