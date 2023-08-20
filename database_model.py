import os.path
import config
import logging

import peewee
import config

db = peewee.SqliteDatabase(config.DATABASE_PATH)
logger = logging.getLogger('Database Context')


class BaseModel(peewee.Model):
    class Meta:
        database = db


TrackTagThroughDeferred = peewee.DeferredThroughModel()
PlaylistsThroughDeferred = peewee.DeferredThroughModel()
AlbumThroughDeferred = peewee.DeferredThroughModel()


class Artist(BaseModel):
    id = peewee.AutoField(column_name='id')
    name = peewee.TextField(column_name='name')

    class Meta:
        table_name = 'Artists'


class Track(BaseModel):
    id = peewee.AutoField(column_name='id')
    artist = peewee.ForeignKeyField(Artist, backref='tracks')
    name = peewee.TextField(column_name='name')
    file_name = peewee.TextField(column_name='file_name')

    class Meta:
        table_name = 'Tracks'


class Album(BaseModel):
    id = peewee.AutoField(column_name='id')
    name = peewee.TextField(column_name='name')
    artist = peewee.ForeignKeyField(Artist, backref='albums')
    tracks = peewee.ManyToManyField(Track, backref='tags', through_model=AlbumThroughDeferred)

    class Meta:
        table_name = 'Albums'


class TrackTag(BaseModel):
    id = peewee.AutoField(column_name='id')
    tag = peewee.TextField(column_name='tag')
    tracks = peewee.ManyToManyField(Track, backref='tags', through_model=TrackTagThroughDeferred)

    class Meta:
        table_name = 'Tags'


class Playlist(BaseModel):
    id = peewee.AutoField(column_name='id')
    playlist_name = peewee.TextField(column_name='playlist_name')
    tracks = peewee.ManyToManyField(Track, backref='playlists', through_model=PlaylistsThroughDeferred)

    class Meta:
        table_name = 'Playlists'


class TrackAlbumsAssign(BaseModel):
    id = peewee.AutoField(column_name='id')
    track = peewee.ForeignKeyField(Track, on_delete='CASCADE')
    album = peewee.ForeignKeyField(Album, on_delete='CASCADE')

    class Meta:
        table_name = 'TrackAlbums'


AlbumThroughDeferred.set_model(TrackAlbumsAssign)


class TrackTagAssign(BaseModel):
    track = peewee.ForeignKeyField(Track, on_delete='CASCADE')
    tag = peewee.ForeignKeyField(TrackTag, on_delete='CASCADE')

    class Meta:
        table_name = 'TrackTags'


TrackTagThroughDeferred.set_model(TrackTagAssign)


class TrackPlaylistAssign(BaseModel):
    id = peewee.AutoField(column_name='id')
    track = peewee.ForeignKeyField(Track, on_delete='CASCADE')
    playlist = peewee.ForeignKeyField(Playlist, on_delete='CASCADE')

    class Meta:
        table_name = 'TrackPlaylists'


PlaylistsThroughDeferred.set_model(TrackPlaylistAssign)

dir_name = os.path.dirname(config.DATABASE_PATH)
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

if not os.path.exists(config.DATABASE_PATH):
    try:
        logger.info("Database file init")

        db.create_tables([
            Track,
            Artist,
            Playlist,
            TrackTag,
            Album,
            TrackAlbumsAssign,
            TrackPlaylistAssign,
            TrackTagAssign
        ])
    except Exception as ex:
        logger.fatal(f"Database init error: {ex}")
        raise ex
