import os.path

import progressbar
import logging
import config
import utils
import sound_files_utils
import database_model as db

PROGRESS_BAR_MARKER = '█'


def add_to_database(root_dir: str, file_name: str):
    sound_file = sound_files_utils.get_file_info(os.path.join(root_dir, file_name))

    if sound_file:
        with db.db.atomic():

            if sound_file.artist:
                artist, _ = db.Artist.get_or_create(name=sound_file.artist)

            if sound_file.album:
                album, _ = db.Album.get_or_create(name=sound_file.album, artist=artist)

            db.Track.create(
                name=sound_file.title,
                file_name=file_name,
                artist=artist,
                album=album
            )


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


def add_files_to_database(root_dir: str, files_list: list[str]):
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
            add_to_database(root_dir, files_list[i])
            bar.update(i)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='file_indexing.log', encoding='utf-8')

    files_path = utils.get_file_path(config.DATA_FILE_PATH)

    files_list = indexing_files(files_path)
    add_files_to_database(files_path, files_list)
    print("Done!")
