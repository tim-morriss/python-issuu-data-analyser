import argparse
import sys

from task_manager import TaskManager


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_name", type=str, help="Name of input .json file.a")
    parser.add_argument("-d", "--doc_uuid", type=str, help="Document uuid to search for.")
    parser.add_argument("-u", "--user_uuid", type=str, help="User uuid for 'also like' functionality.")
    parser.add_argument("-t", "--task_id", type=str, help="Specify the task to implement (2a, 2b, 3a, 3b, 4, 5d, 6).")

    args = parser.parse_args()

    if len(sys.argv) <= 1:
        TaskManager(task_id='7')
    else:
        TaskManager(args.file_name, args.doc_uuid, args.user_uuid, args.task_id)


if __name__ == "__main__":
    main()
