# Issuu Data Analyser

This project includes the design and implementation of a python 3.8 application for data analysis of the document tracking site issuu.com.\
The input data format uses JSON and counts the views by country/continent; counts the views by browser; displays the readers with the highest read times; and ‘also likes’ a function that returns related documents based on what other viewers of a document also read.\
The program can be run from either the command line interface or through a graphical user interface (GUI).

Program can be run from the command line using the main.py file.\
Options for the CLI are:
```bash
usage: main.py [-h] [-f FILE_NAME] [-d DOC_UUID] [-u USER_UUID] [-t TASK_ID]
optional arguments:
  -h, --help            show this help message and exit
  -f FILE_NAME, --file_name FILE_NAME
                        Name of input .json file
  -d DOC_UUID, --doc_uuid DOC_UUID
                        Document uuid to search for
  -u USER_UUID, --user_uuid USER_UUID
                        User uuid for 'also like' functionality
  -t TASK_ID, --task_id TASK_ID
                        Specify the task to implement (2a, 2b, 3a, 3b, 4, 5d, 6).
```
The tasks used by the program are:
- Task 2(a): views by country
- Task 2(b): views by continent
- Task 3(a): views by browser (verbose)
- Task 3(b): views by browser (shorthand)
- Task 4: reader profiles
- Task 5(a): return readers of document
- Task 5(b): return documents read by user
- Task 5(c): return ‘also likes’
- Task 5(d): return top ‘also likes’
- Task 6: ‘also likes’ graph
- Task 7: GUI
- Task 8: command line usage

The GUI can be called by calling the main.py file without arguments:
```bash
python main.py
```
The GUI has the exact same functionality as the CLI:
