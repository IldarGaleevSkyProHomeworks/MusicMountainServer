import inspect, os.path
import logging

filename = inspect.getframeinfo(inspect.currentframe()).filename
work_path = os.path.dirname(os.path.abspath(filename))


def get_file_path(path: str):
    if os.path.isabs(path):
        return path
    return os.path.join(work_path, path)


def get_files_list(files_dir: str):
    dirs_for_scan = [files_dir]

    while dirs_for_scan:
        new_dirs = []
        for dir_path in dirs_for_scan:
            logging.info(f"Indexing dir: {dir_path}")
            for file in os.listdir(dir_path):
                file = os.path.join(dir_path, file)
                if os.path.isdir(file):
                    new_dirs.append(file)
                else:
                    yield dir_path, file.replace(files_dir, "")

            dirs_for_scan = new_dirs

