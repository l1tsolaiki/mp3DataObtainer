import requests

from constants import *


def searchRequest(track, limit):
    METHODNAME = 'track.search'
    payload = {'method': METHODNAME, 'track': track, 'api_key': TOKEN, 'limit': limit, 'format': 'json'}
    r = requests.get(URL, params=payload)
    return r.json()


def searchTrack(track, limit=30, askConfirmation=True):
    searchResult = searchRequest(track, limit=limit)

    if not askConfirmation:
        trackFound = searchResult['results']['trackmatches']['track'][0]['name']
        artistFound = searchResult['results']['trackmatches']['track'][0]['artist']
        return trackFound, artistFound

    for i in range(len(searchResult['results']['trackmatches']['track'])):
        trackFound = searchResult['results']['trackmatches']['track'][i]['name']
        artistFound = searchResult['results']['trackmatches']['track'][i]['artist']

        if input('Did you search for {} by {} (y/n)? '.format(trackFound, artistFound)) in ('y', ''):
            # allow just pressing 'enter' instead of pressing 'y' every time
            return trackFound, artistFound

    # todo make last attempt to find the song by searching for it with the name of the band

    print('Sorry, looks like last.fm does not have {}\n'
          'Try increasing number of results shown or use other services =/'.format(track))
    return tuple()


def getInfoRequest(track, artist):
    METHODNAME = 'track.getInfo'
    payload = {'method': METHODNAME, 'api_key': TOKEN, 'artist': artist, 'track': track, 'format': 'json'}
    r = requests.get(URL, params=payload)
    return r.json()


def searchInfo(track, limit=10, askConfirmation=True):
    data = searchTrack(track, limit=limit, askConfirmation=askConfirmation)

    if data:
        # because there might be nothing found
        track, artist = data
        info = getInfoRequest(track, artist)
    else:
        print('Song name and band name were not found!')
        return str(), str(), str()

    try:
        # because there might be no info about album in the response
        album = info['track']['album']['title']
    except KeyError:
        # todo make attempt to find album with help from user
        album = ''

    if input('Is {} from {} (y/n)? '.format(track, album)) != 'y':
        album = ''

    if album:
        # we are guaranteed to have track and artist by now
        return track, album, artist
    else:
        # todo make attempt to find album with help from user
        pass

    return str(), str(), str()
