from lyricsgenius import Genius
import time
import json
from pathlib import Path

genius = Genius("O5Z7YpNcp1jSMxnuv8Jsboo4CHUpz_51A7kQ1fczrNAQFzyX3mrVH8oRnECy9q6j",
                timeout=15,
                retries=3)
genius.excluded_terms = [
  "(Remix)", "(Live)", "(Taylor's Version)", 'Edition', 'Greatest Hits'
]
genius.skip_non_songs = True

excluded_terms = [
  'Demo', '(Remix)', '(Live)', '(Taylor’s Version)',
  'Greatest Hits', 'Instrumentals', 'Exclusive', 'Live at',
  'Live from', 'Bonus Disc', 'Live!', '(Deluxe)',
  '(The Remixes)', 'Edition', 'Spotify', 'Bonus', '(UK)',
  'The Greatest', 'motion picture soundtrack', '[Remastered]',
  '(Remixes)', '(Deluxe Version)', 'The Remixes', '(US)',
  'Reissue', '(Single)', '- Single', '- EP'
]

def check_exclusion(dict_album):
  if any(excluded.lower() in dict_album['name'].lower() for excluded in excluded_terms):
    return True

def download_albums_json(str_artist, artist_id=None):
  print(f"==Getting album json files for {str_artist}==")
  if artist_id:
    artist = genius.artist(artist_id)['artist']
  else:
    artist = genius.search_artist(str_artist, max_songs=0, allow_name_change=False, get_full_info=False).to_dict()
  req = genius.artist_albums(artist['id'])
  albums = req['albums']

  while req['next_page']:
    req = genius.artist_albums(artist['id'], page=req['next_page'])
    albums.extend(req['albums'])

  # download the json files
  for album_meta in albums:
    if check_exclusion(album_meta):
      print(f"Skipped {album_meta['name']} because it contains an excluded term")
      continue
    print(f"Saving {album_meta['name']}")
    album = genius.album(album_meta['id'])
    tracklist = genius.album_tracks(album_meta['id'])
    filedir = f"json/{artist['name']}/{album_meta['name']}/"

    Path(filedir).mkdir(parents=True, exist_ok=True)
    with open(f'{filedir}/album.json', 'w+') as outfile:
      json.dump(album, outfile, indent=4)
    with open(f'{filedir}/tracks.json', 'w+') as outfile:
      json.dump(tracklist, outfile, indent=4)

def download_album_tracks_from_dict(album_tracklist):
  song = genius.song(album_tracklist['tracks'][0]['song']['id'])['song']
  artist_name = song['primary_artist']['name']
  album_name = song['album']['name']

  for track in album_tracklist['tracks']:
    print(f"-Saving {track['song']['title']}")
    filedir = f"text/{artist_name}/{album_name}/"
    Path(filedir).mkdir(parents=True, exist_ok=True)
    #     with open("text/" + title.replace(" ", "") + album + ".txt", "w") as f:
    #       f.write(lyrics)
    with open(f"{filedir}/{track['song']['title'].replace(' ', '')}" +
              f"{album_name.replace(' ', '')}.txt",
              'w+') as outfile:
      req = genius.lyrics(track['song']['id'], remove_section_headers=True)
      if req:
        req = req[req.find('\n')+1: ]
        outfile.write(req)

if __name__ == "__main__":
  # import artist names from text file
  artists_names = []
  with open("artists.txt") as file:
    artist_names = [line.rstrip() for line in file]

  for name in artist_names:
    download_albums_json(name)
    # first get artist object

# for album in albums:
#   al = genius.search_album(album, artist)
#   with open("json/" + album + ".json", "w") as outfile:
#     json.dump(al.to_json(), outfile)

#   for song in al.tracks:
#     song_dict = song.to_dict()['song']
#     title = song_dict['title']
#     lyrics = song_dict['lyrics']

#     print("-Saving " + title)
#     with open("text/" + title.replace(" ", "") + album + ".txt", "w") as f:
#       f.write(lyrics)
      # f.write(lyrics[lyrics.find('['): ])


# page = 1
# songs = []
# while page:
#     request = genius.artist_songs(1177,
#                                   sort='popularity',
#                                   page=page)
# songs.extend(request['songs'])
# page = request['next_page']

# [ print(song['title']) for song in songs ]

# with open("swift_songs.json", "w") as outfile:
#   json.dump(artist.save_lyrics(), outfile)

# with open("Lyrics_Midnights.json", "r") as f:
#   tracks = json.load(f)['tracks']

# for track in tracks:
#   title = track['song']['title']
#   lyrics = track['song']['lyrics']
#   with open("lyrics_text/" + title.replace(" ","") + "Midnights.txt", 'w') as f:
#     f.write(lyrics[lyrics.find('['):])

# page = 1
# while page:
#   request = genius.
# artist = genius.search_artist("Taylor Swift")
# artist.save_lyrics("tswift_lyrics", "txt")
