#!/usr/bin/python3

import urllib.request

rawplayers = "http://www.multirpg.net/rawplayers3.php"
myrawplayers = urllib.request.urlopen(rawplayers).read().decode('UTF-8')
allplayers = {}

for player in myrawplayers.splitlines():
    playerstats = dict([(x, y) for x, y in zip(player.split()[::2], player.split()[1::2])])
    allplayers[playerstats['rank']] = playerstats

for player in allplayers:
    thisplayer = allplayers[player]
    if thisplayer['char'] == "horseshoecrab":
        print(thisplayer)
