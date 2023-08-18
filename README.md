# Музыкальная библиотека

## Endpoints
| HTTP method |           endpoint           | request                                                  | response                                                         | note                |
|:-----------:|:----------------------------:|----------------------------------------------------------|------------------------------------------------------------------|---------------------|
|    `GET`    |             `/`              |                                                          | `{"state":"ok"}`                                                 | Index               |
|    `GET`    |         `/playlists`         |                                                          | `[{"id":<playlist_id>,"name":"<playlist name>"}, ...]`           | Playlists list      |
|   `POST`    |         `/playlists`         | `{"name":"<playlist name>", "tracks":[<tracks_inices>]}` | `{"status":"ok", "playlist-id":<new_playlist_id>}`               | Create new playlist |
|    `GET`    |  `/playlists/<playlist_id>`  |                                                          | `{"name":"<playlist name>", "tracks":[<tracks_list>]}`           | Playlist info       |
|    `PUT`    |  `/playlists/<playlist_id>`  | `{"name":"<playlist name>", "tracks":[<tracks_inices>]}` | `{"status":"ok"}`                                                | Change playlist     |
|  `DELETE`   |  `/playlists/<playlist_id>`  |                                                          | `{"status":"ok"}`                                                | Remove playlist     |
|    `GET`    |    `/tracks/<track_id>`      |                                                          | `{"id":<track_id>, "name":"<track_name>", "tags":[<tags_list>]}` | Track info          |
|    `GET`    |   `/play/track/<track_id>`   |                                                          | `:FILE:`                                                         | Play track          |
|    `GET`    | `/download/track/<track_id>` |                                                          | `:FILE:`                                                         | Download track      |
