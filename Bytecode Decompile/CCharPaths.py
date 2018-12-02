from Point3 import *
from Vec3 import *
import copy
__mickeyPaths = {'a': (Point3(17, -17, 4.025), ('b', 'e')), 'b': (Point3(17.5, 7.6, 4.025), ('c', 'e')), 'c': (Point3(85, 11.5, 4.025), ('d',)), 'd': (Point3(85, -13, 4.025), ('a',)), 'e': (Point3(-27.5, -5.25, 0.0), ('a', 'b', 'f')), 'f': (Point3(-106.15, -4.0, -2.5), ('e', 'g', 'h', 'i')), 'g': (Point3(-89.5, 93.5, 0.5), ('f', 'h')), 'h': (Point3(-139.95, 1.69, 0.5), ('f', 'g', 'i')), 'i': (Point3(-110.95, -68.57, 0.5), ('f', 'h'))}
__mickeyWaypoints = (
 (
  'a', 'e', 1, []), ('b', 'e', 1, []), ('e', 'f', 1, [Point3(-76.87, -7.85, -1.85), Point3(-80.57, -4.0, -1.85)]), ('f', 'g', 1, [Point3(-106.62, 28.65, -1.5)]), ('g', 'h', 1, [Point3(-134.96, 60.34, 0.5)]), ('h', 'f', 1, []), ('h', 'i', 1, [Point3(-137.13, -42.79, 0.5)]), ('i', 'f', 1, []))
__minniePaths = {'a': (Point3(53.334, 71.057, 6.525), ('b', 'r')), 'b': (Point3(127.756, 58.665, -11.75), ('a', 's', 'c')), 'c': (Point3(130.325, 15.174, -2.003), ('b', 'd')), 'd': (Point3(126.173, 7.057, 0.522), ('c', 'e')), 'e': (Point3(133.843, -6.618, 4.71), ('d', 'f', 'g', 'h')), 'f': (Point3(116.876, 1.119, 3.304), 'e'), 'g': (Point3(116.271, -41.568, 3.304), ('e', 'h')), 'h': (Point3(128.983, -49.656, -0.231), ('e', 'g', 'i', 'j')), 'i': (Point3(106.024, -75.249, -4.498), 'h'), 'j': (Point3(135.016, -93.072, -13.376), ('h', 'k', 'y')), 'k': (Point3(123.966, -100.242, -10.879), ('j', 'l')), 'l': (Point3(52.859, -109.081, 6.525), ('k', 'm')), 'm': (Point3(-32.071, -107.049, 6.525), ('l', 'n')), 'n': (Point3(-40.519, -99.685, 6.525), ('m', 'o')), 'o': (Point3(-42.389, -91.257, 6.525), ('n', 'p')), 'p': (Point3(-69.782, -62.394, 6.525), ('o', 'q')), 'q': (Point3(-61.366, 27.12, 6.525), ('p', 'r')), 'r': (Point3(-18.344, 69.532, 6.525), ('q', 'a')), 's': (Point3(91.357, 44.546, -13.475), ('b', 't')), 't': (Point3(64.256, 18.879, -13.475), ('s', 'u')), 'u': (Point3(-13.765, 42.362, -13.475), ('t', 'v')), 'v': (Point3(-52.627, 7.428, -13.475), ('u', 'w')), 'w': (Point3(-50.654, -54.879, -13.475), ('v', 'x')), 'x': (Point3(-3.711, -81.819, -13.475), ('w', 'y')), 'y': (Point3(68.536, -68.591, -13.475), ('j', 'x'))}
__minnieWaypoints = (
 (
  'a', 'b', 1, []), ('k', 'l', 1, []), ('b', 'c', 1, []), ('c', 'd', 1, []), ('d', 'e', 1, []), ('e', 'f', 1, []), ('e', 'g', 1, []), ('e', 'h', 1, []), ('g', 'h', 1, []), ('h', 'i', 1, []), ('h', 'j', 1, []))
__goofyPaths = {'a': (Point3(64.995, 169.665, 10.027), ('b', 'q')), 'b': (Point3(48.893, 208.912, 10.027), ('a', 'c')), 'c': (Point3(5.482, 210.479, 10.03), ('b', 'd')), 'd': (Point3(-34.153, 203.284, 10.029), ('c', 'e')), 'e': (Point3(-66.656, 174.334, 10.026), ('d', 'f')), 'f': (Point3(-55.994, 162.33, 10.026), ('e', 'g')), 'g': (Point3(-84.554, 142.099, 0.027), ('f', 'h')), 'h': (Point3(-92.215, 96.446, 0.027), ('g', 'i')), 'i': (Point3(-63.168, 60.055, 0.027), ('h', 'j')), 'j': (Point3(-37.637, 69.974, 0.027), ('i', 'k')), 'k': (Point3(-3.018, 26.157, 0.027), ('j', 'l', 'm')), 'l': (Point3(-0.711, 46.843, 0.027), 'k'), 'm': (Point3(26.071, 46.401, 0.027), ('k', 'n')), 'n': (Point3(30.87, 67.432, 0.027), ('m', 'o')), 'o': (Point3(93.903, 90.685, 0.027), ('n', 'p')), 'p': (Point3(88.129, 140.575, 0.027), ('o', 'q')), 'q': (Point3(53.988, 158.232, 10.027), ('p', 'a'))}
__goofyWaypoints = (
 (
  'f', 'g', 1, []), ('p', 'q', 1, []))
__donaldPaths = {'a': (Point3(-94.883, -94.024, 0.025), 'b'), 'b': (Point3(-13.962, -92.233, 0.025), ('a', 'h')), 'c': (Point3(68.417, -91.929, 0.025), ('d', 'g')), 'd': (Point3(68.745, 91.227, 0.025), ('c', 'i')), 'e': (Point3(4.047, 94.26, 0.025), ('i', 'j')), 'f': (Point3(-91.271, 90.987, 0.025), 'j'), 'g': (Point3(43.824, -94.129, 0.025), ('c', 'h')), 'h': (Point3(13.905, -91.334, 0.025), ('b', 'g')), 'i': (Point3(43.062, 88.152, 0.025), ('d', 'e')), 'j': (Point3(-48.96, 88.565, 0.025), ('e', 'f'))}
__donaldWaypoints = (
 (
  'd', 'c', 1, []), ('b', 'a', 1, [Point3(-55.883, -89.0, 0.025)]))
__plutoPaths = {'a': (Point3(-110.0, -37.8, 8.6), ('b', 'c')), 'b': (Point3(-11.9, -128.2, 6.2), ('a', 'c')), 'c': (Point3(48.9, -14.4, 6.2), ('b', 'a', 'd')), 'd': (Point3(0.25, 80.5, 6.2), ('c', 'e')), 'e': (Point3(-83.3, 36.1, 6.2), ('d', 'a'))}
__plutoWaypoints = (
 (
  'a', 'b', 1, [Point3(-90.4, -57.2, 3.0), Point3(-63.6, -79.8, 3.0), Point3(-50.1, -89.1, 6.2)]), ('c', 'a', 1, [Point3(-15.6, -25.6, 6.2), Point3(-37.5, -38.5, 3.0), Point3(-55.0, -55.0, 3.0), Point3(-85.0, -46.4, 3.0)]), ('d', 'e', 0, [Point3(-25.8, 60.0, 6.2), Point3(-61.9, 64.5, 6.2)]), ('e', 'a', 1, [Point3(-77.2, 28.5, 6.2), Point3(-76.4, 12.0, 3.0), Point3(-93.2, -21.2, 3.0)]))
startNode = 'a'

def getPaths(charName):
    if charName == 'Mickey':
        return __mickeyPaths
    else:
        if charName == 'Minnie':
            return __minniePaths
        else:
            if charName == 'Goofy':
                return __goofyPaths
            else:
                if charName == 'Donald':
                    return __donaldPaths
                else:
                    if charName == 'Pluto':
                        return __plutoPaths


def __getWaypointList(paths):
    if paths == __mickeyPaths:
        return __mickeyWaypoints
    else:
        if paths == __minniePaths:
            return __minnieWaypoints
        else:
            if paths == __goofyPaths:
                return __goofyWaypoints
            else:
                if paths == __donaldPaths:
                    return __donaldWaypoints
                else:
                    if paths == __plutoPaths:
                        return __plutoWaypoints


def getNodePos(node, paths):
    return paths[node][0]


def getAdjacentNodes(node, paths):
    return paths[node][1]


def getWayPoints(fromNode, toNode, paths, wpts=None):
    list = []
    if fromNode != toNode:
        if wpts == None:
            wpts = __getWaypointList(paths)
        for path in wpts:
            if path[0] == fromNode and path[1] == toNode:
                for point in path[3]:
                    list.append(Point3(point))

                break
            else:
                if path[0] == toNode and path[1] == fromNode:
                    for point in path[3]:
                        list = [
                         Point3(point)] + list

                    break

    return list
    return


def getRaycastFlag(fromNode, toNode, paths):
    result = 0
    if fromNode != toNode:
        wpts = __getWaypointList(paths)
        for path in wpts:
            if path[0] == fromNode and path[1] == toNode:
                if path[2]:
                    result = 1
                    break
            else:
                if path[0] == toNode and path[1] == fromNode:
                    if path[2]:
                        result = 1
                        break

    return result


def getPointsFromTo(fromNode, toNode, paths):
    startPoint = Point3(getNodePos(fromNode, paths))
    endPoint = Point3(getNodePos(toNode, paths))
    return [
     startPoint] + getWayPoints(fromNode, toNode, paths) + [endPoint]


def getWalkDuration(fromNode, toNode, velocity, paths):
    posPoints = getPointsFromTo(fromNode, toNode, paths)
    duration = 0
    for pointIndex in range(len(posPoints) - 1):
        startPoint = posPoints[pointIndex]
        endPoint = posPoints[pointIndex + 1]
        distance = Vec3(endPoint - startPoint).length()
        duration += distance / velocity

    return duration