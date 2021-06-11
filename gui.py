# Based on tkinter example from lectures
import pathlib
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


class GUI:

    def __init__(self, task_manager):
        """GUI for issuu data application

        Parameters
        ----------
        task_manager : TaskManager
            Task manager object
        """
        self.tm = task_manager

        self.root = Tk()
        self.root.title("Issuu Explorer ver. 0.00000001")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        mainframe = ttk.Frame(self.root, padding=12)
        mainframe.grid(column=0, row=0, sticky='NSEW')
        mainframe.grid_columnconfigure(0, weight=1)

        self.doc_id = StringVar()
        self.doc_id.set(self.tm.doc_id)
        if self.doc_id.get() == 'None':
            self.doc_id.set('')
        self.user_id = StringVar()
        self.user_id.set(self.tm.user_id)
        if self.user_id.get() == 'None':
            self.user_id.set('')
        self.orientation = IntVar()
        self.graph_text = StringVar()
        self.file_path = StringVar()
        self.file_path.set(self.tm.json_loader.filename)
        if self.file_path.get() == 'None':
            self.file_path.set('')

        self.browse_frame(mainframe, 0)
        self.sep(mainframe, 1)
        self.uuid_frame(mainframe, 2)
        self.sep(mainframe, 3)
        self.task_frame(mainframe, 4)
        self.sep(mainframe, 5)
        self.options_frame(mainframe, 6)

        self.root.mainloop()

    def browse_frame(self, frame, row):
        browse_frame = ttk.Frame(frame, padding=1)
        browse_frame.grid(row=row, sticky='NSEW')
        browse_frame.grid_columnconfigure(1, weight=1)

        browse = ttk.Button(browse_frame, text='Browse for json file', command=self.file_dialog)
        browse.grid(row=0, column=1)
        browse_label = ttk.Label(browse_frame, textvariable=self.file_path)
        browse_label.grid(row=1, column=1)

    def uuid_frame(self, frame, row):
        uuid_frame = ttk.Frame(frame, padding=1)
        uuid_frame.grid(row=row, sticky='NSEW')

        uuid_frame.grid_columnconfigure(1, weight=1)

        doc_label = ttk.Label(uuid_frame, text='Document UUID')
        doc_label.grid(column=0, row=0, sticky='E')
        doc_entry = Entry(uuid_frame, textvariable=self.doc_id)
        doc_entry.grid(column=1, row=0, sticky='EW')

        user_label = ttk.Label(uuid_frame, text='User UUID')
        user_label.grid(column=0, row=1, sticky='E')
        user_entry = Entry(uuid_frame, textvariable=self.user_id)
        user_entry.grid(column=1, row=1, sticky='EW')

    def task_frame(self, frame, row):
        ttk.Style().configure("TButton", justify=CENTER)

        task_frame = ttk.Frame(frame, padding=1)
        task_frame.grid(row=row, sticky='NSEW')
        task_frame.grid_columnconfigure((0, 1), weight=1)

        countries = ttk.Button(task_frame, text='Document readers by country \n(Task 2a)', command=self.readers_by_country)
        countries.grid(column=0, row=0, sticky='EW')
        continents = ttk.Button(task_frame, text='Document readers by continent \n(Task 2b)', command=self.readers_by_continent)
        continents.grid(column=1, row=0, sticky='EW')

        devices_verbose = ttk.Button(task_frame, text='Show verbose devices \n(Task 3a)', command=self.show_devices_verbose)
        devices_verbose.grid(column=0, row=1, sticky='EW')
        devices = ttk.Button(task_frame, text='Show devices \n(Task 3b)', command=self.show_devices)
        devices.grid(column=1, row=1, sticky='EW')

        readers = ttk.Button(task_frame, text='Show most avid readers \n(Task 4)', command=self.active_readers)
        readers.grid(column=0, row=2, sticky='EW')
        also_likes = ttk.Button(task_frame, text='Show docs readers also like \n (Task 5d)', command=self.also_likes)
        also_likes.grid(column=1, row=2, sticky='EW')

    def options_frame(self, frame, row):
        options_frame = ttk.Frame(frame, padding=1)
        options_frame.grid(row=row, sticky='NSEW')
        options_frame.grid_columnconfigure((0, 1), weight=1)

        self.graph_text.set('Horizontal')
        graph_pos_label = ttk.Label(options_frame, text='Set graph orientation:')
        graph_pos_label.grid(column=0, row=0, sticky='EW')
        graph_position = ttk.Checkbutton(options_frame, text='Graph Orientation', textvariable=self.graph_text, variable=self.orientation, command=self.graph_orientation)
        graph_position.grid(column=0, row=1, sticky='EW')

        also_likes_graph = ttk.Button(options_frame, text='Generate also likes graph', command=self.confirm)
        also_likes_graph.grid(column=1, row=1, sticky='EW')

    def sep(self, frame, row):
        ttk.Separator(frame, orient=HORIZONTAL).grid(row=row, sticky='EW')

    def file_dialog(self):
        # adapted from https://stackoverflow.com/a/3430395
        parent_dir = pathlib.Path(__file__).parent.absolute()
        filename = filedialog.askopenfilename(initialdir=parent_dir, title="Select A File", filetypes=[("json files", "*.json"), ("all files", "*.*")])
        self.tm.update_filename(filename)
        self.file_path.set(filename)

    def readers_by_country(self):
        self.tm.task_2a(self.doc_id.get())

    def readers_by_continent(self):
        self.tm.task_2b(self.doc_id.get())

    def show_devices_verbose(self):
        self.tm.task_3a()

    def show_devices(self):
        self.tm.task_3b()

    def active_readers(self):
        self.tm.task_4()

    def also_likes(self):
        self.tm.task_5d(self.doc_id.get(), self.user_id.get())

    def graph_orientation(self):
        if self.orientation.get() == 0:
            self.tm.orientation = 'h'
            self.graph_text.set('Horizontal')
        else:
            self.tm.orientation = 'v'
            self.graph_text.set('Vertical')

    def confirm(self):
        result = messagebox.askquestion("Generate graph?", "Are you sure?", icon='warning')
        if result == 'yes':
            self.tm.task_6(self.doc_id.get(), self.user_id.get())
