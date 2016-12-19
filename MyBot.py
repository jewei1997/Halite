from hlt import *
from networking import *
import logging

logging.basicConfig(filename='output.log',level=logging.DEBUG)

myID, gameMap = getInit()
sendInit("MyPythonBot")

def findNearestEnemyDirection(loc):
    direction = NORTH
    maxDistance = min(gameMap.height, gameMap.width) / 2
    for d in CARDINALS:
        distance = 0
        current = loc
        site = gameMap.getSite(current, d)
        while (site.owner == myID and distance < maxDistance):
            distance += 1
            current = gameMap.getLocation(current, d)
            site = gameMap.getSite(current)

        if distance < maxDistance:
            direction = d
            maxDistance = distance
    return direction

def move(location):
    site = gameMap.getSite(location)
    border = False
    for d in CARDINALS:
        neighbour_site = gameMap.getSite(location, d)
        if neighbour_site.owner != myID:
            border = True
            if neighbour_site.strength < site.strength:
                return Move(location, d)
    if site.strength < site.production * 10:
        return Move(location, STILL)
    if not border:
        return Move(location, findNearestEnemyDirection(location))
    return Move(location, STILL)
i = 0
while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            location = Location(x, y)
            if gameMap.getSite(location).owner == myID:
                moves.append(move(location))
    i += 1
    sendFrame(moves)
