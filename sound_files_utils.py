from datetime import timedelta
from typing import NamedTuple

import eyed3
import os.path


def is_sound_file(file_name: str) -> (bool, str, str):
    name, ext = os.path.splitext(os.path.basename(file_name))
    ext = ext.lstrip('.').lower()
    return ext in ['mp3', 'wav', 'flac'], name, ext


class SoundFileInfo(NamedTuple):
    title: str
    artist: str
    album: str
    genre: str
    year: int
    duration: timedelta


def get_file_info(file_name: str) -> SoundFileInfo | None:
    is_music, f_name, f_ext = is_sound_file(file_name)

    if is_music and f_ext == 'mp3':
        file = eyed3.load(file_name)

        title = file.tag.title
        title = title if title else f_name
        artist = file.tag.artist
        genre = file.tag.genre.name
        album = file.tag.album
        duration = timedelta(seconds=file.info.time_secs)
        year = file.tag.recording_date.year

        return SoundFileInfo(
            title=title,
            artist=artist,
            genre=genre,
            album=album,
            duration=duration,
            year=year
        )

    return None
