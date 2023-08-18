import json
import os.path

import config
import database_model as db
from aiohttp import web
import logging

routes = web.RouteTableDef()


@routes.get(r'/')
async def index(request):
    return web.json_response({"state": "ok"})


@routes.get(r'/track/{track_id:\d+}')
async def get_track_by_id(request):
    track_id = request.match_info['track_id']

    with db.db.atomic():
        track = db.Track.get_or_none(db.Track.id == int(track_id))
        if track:
            return web.json_response({
                "id": track.id,
                "name": track.name,
                "tags": [{"id": tag.id, "name": tag.tag} for tag in track.tags]})

    raise web.HTTPNotFound()


@routes.get(r'/{action:\w+}/track/{track_id:\d+}')
async def get_track_file_by_id(request):
    track_id = request.match_info['track_id']
    action = request.match_info['action'].lower()

    match action:
        case 'download':
            disposition = 'attachment'
        case 'play':
            disposition = 'inline'
        case _:
            raise web.HTTPBadRequest

    with db.db.atomic():
        track = db.Track.get_or_none(db.Track.id == int(track_id))
        file_name = os.path.join(config.DATA_FILE_PATH, track.file_name)
        if os.path.exists(file_name):
            base_name = os.path.basename(file_name)
            return web.FileResponse(
                file_name,
                headers={
                    'Content-Type': 'audio/mpeg',
                    'Content-Disposition': f'{disposition}; filename="' + base_name + '"'
                })

    raise web.HTTPNotFound()


@routes.get(r'/playlists')
async def get_playlists(request):
    with db.db.atomic():
        playlists = db.Playlist.select(db.Playlist.playlist_name, db.Playlist.id)
        tracks = []
        for playlist in playlists:
            tracks.append({
                "id": playlist.id,
                "name": playlist.playlist_name
            })
        return web.json_response(tracks)


@routes.get(r'/playlists/{playlist_id:\d+}')
async def get_playlist_by_id(request):
    playlist_id = request.match_info['playlist_id']

    with db.db.atomic():
        playlist = db.Playlist.get_or_none(db.Playlist.id == int(playlist_id))
        if playlist:
            return web.json_response({
                "name": playlist.playlist_name,
                "tracks": [
                    {
                        "id": track.id,
                        "name": track.name
                    } for track in playlist.tracks]})

    raise web.HTTPNotFound()


@routes.put(r'/playlists/{playlist_id:\d+}')
async def update_playlist_by_id(request):
    playlist_id = request.match_info['playlist_id']

    try:
        playlist_info = await request.json()

        new_name = playlist_info.get('name', None)
        tracks_id = playlist_info.get('tracks', [])

        with db.db.atomic():
            playlist = db.Playlist.get_or_none(db.Playlist.id == int(playlist_id))

            if playlist is None:
                raise web.HTTPNotFound()

            if new_name:
                playlist.playlist_name = new_name

            if tracks_id:
                new_tracks = [db.Track.get_or_none(db.Track.id == track_id) for track_id in tracks_id]

                playlist.tracks.add([track for track in new_tracks if track])

            playlist.save()
            return web.json_response({"status": "ok"})

    except json.decoder.JSONDecodeError:
        raise web.HTTPBadRequest


@routes.delete(r'/playlists/{playlist_id:\d+}')
async def delete_playlist_by_id(request):
    playlist_id = request.match_info['playlist_id']

    with db.db.atomic():
        playlist = db.Playlist.get_or_none(db.Playlist.id == int(playlist_id))
        if playlist:
            playlist.delete_instance()
            return web.json_response({"status": "ok"})
    raise web.HTTPNotFound()


@routes.post(r'/playlists')
async def create_playlist(request):
    try:
        playlist_info = await request.json()

        name = playlist_info.get('name', None)
        tracks_id = playlist_info.get('tracks', [])

        with db.db.atomic():
            tracks = [db.Track.get_or_none(db.Track.id == track_id) for track_id in tracks_id]

            new_playlist = db.Playlist(playlist_name=name)
            new_playlist.save()

            new_playlist.tracks.add([track for track in tracks if track])
            new_playlist.save()
            return web.json_response({"status": "ok", "playlist-id": new_playlist.id})

    except json.decoder.JSONDecodeError:
        raise web.HTTPBadRequest


logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)

app = web.Application()
app.add_routes(routes)
web.run_app(app, host=config.SERVER_HOST, port=config.SERVER_PORT)
