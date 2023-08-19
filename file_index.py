import progressbar
import logging
import config
import utils

PROGRESS_BAR_MARKER = '█'


def indexing_files(files_dir: str):
    progress_bar_unknown_widgets = [
        '[ Indexing files ]',
        progressbar.BouncingBar(marker=PROGRESS_BAR_MARKER),
        ' ',
        progressbar.Timer()
    ]

    files_list = []

    with progressbar.ProgressBar(max_value=progressbar.UnknownLength,
                                 widgets=progress_bar_unknown_widgets,
                                 redirect_stdout=True) as bar:
        for file_info in utils.get_files_list(files_dir):
            file_name = file_info[1]
            files_list.append(file_name)
            bar.update()

    return files_list


def add_files_to_database(files_list: list[str]):
    progress_bar_widgets = [
        '[ Add files to DB - ',
        progressbar.Percentage(),
        ']',
        progressbar.Bar(marker=PROGRESS_BAR_MARKER),
        ' ',
        progressbar.Timer()
    ]

    files_count = len(files_list)
    with progressbar.ProgressBar(min_value=0,
                                 max_value=files_count,
                                 widgets=progress_bar_widgets,
                                 redirect_stdout=True) as bar:
        for i in range(files_count):
            bar.update(i)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='file_indexing.log', encoding='utf-8')

    files_path = utils.get_file_path(config.DATA_FILE_PATH)

    files_list = indexing_files(files_path)
    add_files_to_database(files_list)
    print("Done!")
