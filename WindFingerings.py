# WindFingerings 2.0.1 by Valky River

version = "2.0.1"

# VERSION 2.0 — NEW FEATURE: INSTRUMENT EDITOR

from tkinter import *
from tkinter import filedialog as fd
import math
import colorsys
import copy
import platform

class CodeIncompleteError(Exception):
    def __init__(s, message="This functionality has not been coded yet"):
        super().__init__(message)

# PRESETS
colors = {
    "pitch_background": "#008844",
    "pitch_box": "#FFFFFF",
    "pitch_selected": "#FFCC99",
    "description_background":"#770099",
    "dark_description_background":"#440055",
    "options_background":"#006666",
    "dark_options_background":"#004444",
    "custom_background": "#656761",
    "dark_custom_background": "#4B4D48",
    "options_database": "#00BBBB",
    "set_instrument": "#AAEEEE",
    "filters_background": "#887722",
    "searched": "#FFEE88"
}

key_replacements = {
    "period": ".",
    "numbersign": "#",
    "s": "#",
    "S": "#",
    "plus": "+",
    "minus": "-",
    "equal": "+"
}

tempvarparams = {
    "freq": [7, "0123457689."],
    "notename": [4, "abcdefgABCDEFG-0123456789#"],
    "centsdev": [6, "0123457689.-+"],
    "concertname": [4, "abcdefgABCDEFG-0123456789#"],
    "concertdev": [6, "0123457689.-+"],
    "te": [3, "0123456789"],
    "edittranspos": [8, "0123456789.-+"],
    "edittransstep": [7, "0123456789.-+"],
    "editlrspli": [4, "0123456789."],
    "editmidx": [5, "0123456789."],
    "editmid": [5, "0123456789."],
    "labelsize": [5, "0123456789."],
    "xpos": [5, "0123456789."],
    "ypos": [5, "0123456789."],
    "width": [2, "0123456789"],
    "hight": [2, "0123456789"],
    "partialssize": [5, "0123456789."],
    "partialsx": [5, "0123456789."],
    "partialsy": [5, "0123456789."],
}

fingtypes = {
    "note": 1,
    "trill": 2,
    "multi2": 2,
    "multi3": 3,
    "multi4": 4
}

key_colors = {
    "main": ["#FFFFFF", "#000000", "#A3A3A3"],
    "octave": ["#DDDDDD", "#555555", "#898989"],
    "second": ["#99EEBB", "#006633", "#66AA88"],
    "low": ["#FFCCCC", "#770022", "#AA7788"],
    "high": ["#CCE577", "#556600", "#99AA77"],
    "trill": ["#BBDDFF", "#002288", "#7799BB"],
    "model": ["#FFCC99", "#664400", "#AA9977"],
    "special": ["#EEBBFF", "#550077", "#AA88BB"],
    "link": ["#EEBBFF", "#550077"],
    "trilled": "#00EE00"
}

circlednums = "⓪①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯"

instruments = { # key system, transpose
    # some instruments are commented out

    # FLUTES
    "Piccolo": ["piccolo", 12],
    #"Eb Flute": ["?", 3],
    "Flute": ["flute", 0],
    "Alto Flute": ["flute", -5],
    "Bass Flute": ["flute", -12],
    #"Contrabass Flute": ["flute", -24],

    # DOUBLE REEDS
    "Oboe": ["oboe", 0],
    "English Horn": ["corangl", -7],
    #"Bass Oboe": ["?", -12],
    #"Heckelphone": ["?", -12],
    "Bassoon": ["bassoon", 0],
    "Contrabassoon": ["contrafg", -12],
    #"Sarrusophone": ["?", -33],

    # CLARINETS
    #"Piccolo Clarinet in Ab: ["clarinet", 8],
    "Clarinet in Eb": ["clarinet", 3],
    "Clarinet in Bb": ["clarinet", -2],
    "Clarinet in A": ["clarinet", -3],
    "Basset Horn": ["bassclar", -7],
    "Alto Clarinet": ["clarinet", -9],
    "Bass Clarinet": ["bassclar", -14],
    "Contra-alto Clarinet": ["clarinet", -21],
    "Contrabass Clarinet": ["bassclar", -26],

    # SAXOPHONES
    "Sopranino Saxophone": ["saxophone", 3],
    "Soprano Saxophone": ["saxophone", -2],
    "Alto Saxophone": ["saxophone", -9],
    "Tenor Saxophone": ["saxophone", -14],
    "Baritone Saxophone": ["saxophone", -21],
    "Bass Saxophone": ["saxophone", -26],
    "Contrabass Saxophone": ["saxophone", -33],

    # HIGHER BRASS
    "Bb Piccolo Trumpet": ["4valve", 10],
    #"Trumpet in D": ["trumpet", 2],
    "Trumpet in C": ["trumpet", 0],
    "Trumpet in Bb": ["trumpet", -2],
    #"Bass Trumpet": ["trumpet", -14],
    #"Eb Soprano Cornet": ["trumpet", 3],
    "Cornet in Bb": ["trumpet", -2],
    "Flugelhorn": ["4valve", -2],

    # F HORNS
    "Single F Horn": ["4valve", -7],
    "Single Bb Horn": ["4valve", -7],
    "Double F/Bb Horn": ["horn", -7],
    #"Mellophone": ["?", -7],
    #"Wagner Tuba in F": ["?", -7],
    #"Wagner Tuba in Bb": ["?", -7],

    # LOW BRASS
    #"Alto Trombone": ["?", 0],
    "Tenor Trombone": ["trombone", 0],
    "Bass Trombone": ["trombone", 0],
    #"Contrabass Trombone": ["?", 0],
    #"Cimbasso": ["?", 0],
    "Tenor Horn": ["4valve", -9],
    "Baritone Horn": ["4valve", -1],
    "Euphonium": ["4valve", -14],
    "F Tuba": ["tuba", 0],
    "Eb Tuba": ["tuba", 0],
    "CC Tuba": ["tuba", 0],
    "BBb Tuba": ["tuba", 0],

    # OTHERS
    "Sopranino Recorder": ["recorder", 12],
    "Soprano Recorder": ["recorder", 12],
    "Alto Recorder": ["recorder", 0],
    "Tenor Recorder": ["recorder", 0],
    "Bass Recorder": ["recorder", -12],
    "Great Bass Recorder": ["recorder", -12],

    # CUSTOM
    "Custom": ["custom", 0.0]

}

# KEY SYSTEMS
# keys in configuration order
# key info:
#   x1, y1, x2, y2
#   type:
#     main (6 main keys)
#     octave (register keys)
#     second (e.g. G# key, Eb key etc.)
#     low (low extension, e.g. C key, Bb key)
#     high (high extension, e.g. palm keys on sax)
#     trill (typically only used for trills)
#     model (not present on all models)
#     special (not usually pressed directly)
#   halfable
#   label, labelsize
#   descname, descoff

key_systems = {
    "piccolo": {
        "parameters": {"keys":16, "LR_split":7, "separator":" | ", "offsetx":-4, "offsety":-1, "shiftx":3, "shifty":0.5, "Lx":6, "Ly":3, "Mx":39, "My":13, "Bx":36, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": [],
        0: {"x1":8, "y1":22, "x2":10.5, "y2":26, "type":"second", "halfable":False, "label":"Bb", "labelsize":1, "descname":"Bb ", "descoff":""},
        1: {"x1":11, "y1":22, "x2":13.5, "y2":26, "type":"main", "halfable":False, "label":"T", "labelsize":1, "descname":"T ", "descoff":""},
        2: {"x1":8, "y1":12, "x2":15, "y2":19, "type":"main", "halfable":False, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        3: {"x1":15.5, "y1":13.5, "x2":19.5, "y2":17.5, "type":"special", "halfable":False, "label":"Bb*", "labelsize":6/5, "descname":"Bb*", "descoff":""},
        4: {"x1":20, "y1":12, "x2":27, "y2":19, "type":"main", "halfable":False, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        5: {"x1":28, "y1":12, "x2":35, "y2":19, "type":"main", "halfable":False, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        6: {"x1":35, "y1":7.5, "x2":38, "y2":12.5, "type":"second", "halfable":False, "label":"G#", "labelsize":1, "descname":" G#", "descoff":""},
        7: {"x1":37, "y1":13.5, "x2":41, "y2":17.5, "type":"special", "halfable":False, "label":"G*", "labelsize":6/5, "descname":"G*", "descoff":""},
        8: {"x1":41.5, "y1":13.5, "x2":45.5, "y2":17.5, "type":"special", "halfable":False, "label":"F#*", "labelsize":6/5, "descname":"F#*", "descoff":""},
        9: {"x1":45.5, "y1":17, "x2":47.5, "y2":21, "type":"second", "halfable":False, "label":"Bb", "labelsize":5/6, "descname":"Bb ", "descoff":""},
        10: {"x1":47, "y1":12, "x2":54, "y2":19, "type":"main", "halfable":False, "label":"4", "labelsize":2, "descname":"4", "descoff":"−"},
        11: {"x1":53.5, "y1":17, "x2":55.5, "y2":21, "type":"trill", "halfable":False, "label":"d", "labelsize":5/6, "descname":"d", "descoff":""},
        12: {"x1":55, "y1":12, "x2":62, "y2":19, "type":"main", "halfable":False, "label":"5", "labelsize":2, "descname":"5", "descoff":"−"},
        13: {"x1":61.5, "y1":17, "x2":63.5, "y2":21, "type":"trill", "halfable":False, "label":"eb", "labelsize":5/6, "descname":"eb", "descoff":""},
        14: {"x1":63, "y1":12, "x2":70, "y2":19, "type":"main", "halfable":False, "label":"6", "labelsize":2, "descname":"6", "descoff":"−"},
        15: {"x1":70, "y1":16, "x2":73, "y2":22, "type":"second", "halfable":False, "label":"Eb", "labelsize":1, "descname":" Eb", "descoff":""},
    },
    
    "flute": {
        "parameters": {"keys":21, "LR_split":7, "separator":" | ", "offsetx":-4, "offsety":-1, "shiftx":-1, "shifty":0.5, "Lx":6, "Ly":3, "Mx":39, "My":13, "Bx":35.5, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": [],
        0: {"x1":8, "y1":22, "x2":10.5, "y2":26, "type":"second", "halfable":False, "label":"Bb", "labelsize":1, "descname":"Bb ", "descoff":""},
        1: {"x1":11, "y1":22, "x2":13.5, "y2":26, "type":"main", "halfable":False, "label":"T", "labelsize":1, "descname":"T ", "descoff":""},
        2: {"x1":8, "y1":12, "x2":15, "y2":19, "type":"main", "halfable":True, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        3: {"x1":15.5, "y1":13.5, "x2":19.5, "y2":17.5, "type":"special", "halfable":False, "label":"Bb*", "labelsize":6/5, "descname":"Bb*", "descoff":""},
        4: {"x1":20, "y1":12, "x2":27, "y2":19, "type":"main", "halfable":True, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        5: {"x1":28, "y1":12, "x2":35, "y2":19, "type":"main", "halfable":True, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        6: {"x1":35, "y1":7.5, "x2":38, "y2":12.5, "type":"second", "halfable":False, "label":"G#", "labelsize":1, "descname":" G#", "descoff":""},
        7: {"x1":36, "y1":13.5, "x2":40, "y2":17.5, "type":"special", "halfable":False, "label":"G*", "labelsize":6/5, "descname":"G*", "descoff":""},
        8: {"x1":40.5, "y1":13.5, "x2":44.5, "y2":17.5, "type":"special", "halfable":False, "label":"F#*", "labelsize":6/5, "descname":"F#*", "descoff":""},
        9: {"x1":43.5, "y1":17, "x2":45.5, "y2":21, "type":"model", "halfable":False, "label":"C#", "labelsize":5/6, "descname":"C# ", "descoff":""},
        10: {"x1":45.5, "y1":17, "x2":47.5, "y2":21, "type":"second", "halfable":False, "label":"Bb", "labelsize":5/6, "descname":"Bb ", "descoff":""},
        11: {"x1":47, "y1":12, "x2":54, "y2":19, "type":"main", "halfable":True, "label":"4", "labelsize":2, "descname":"4", "descoff":"−"},
        12: {"x1":53.5, "y1":17, "x2":55.5, "y2":21, "type":"trill", "halfable":False, "label":"d", "labelsize":5/6, "descname":"d", "descoff":""},
        13: {"x1":55, "y1":12, "x2":62, "y2":19, "type":"main", "halfable":True, "label":"5", "labelsize":2, "descname":"5", "descoff":"−"},
        14: {"x1":61.5, "y1":17, "x2":63.5, "y2":21, "type":"trill", "halfable":False, "label":"eb", "labelsize":5/6, "descname":"eb", "descoff":""},
        15: {"x1":63, "y1":12, "x2":70, "y2":19, "type":"main", "halfable":True, "label":"6", "labelsize":2, "descname":"6", "descoff":"−"},
        16: {"x1":70, "y1":16, "x2":73, "y2":22, "type":"second", "halfable":False, "label":"Eb", "labelsize":1, "descname":" Eb", "descoff":""},
        17: {"x1":73, "y1":19, "x2":78, "y2":22, "type":"low", "halfable":False, "label":"C#", "labelsize":1, "descname":" C#", "descoff":""},
        18: {"x1":73, "y1":17.5, "x2":78, "y2":19, "type":"low", "halfable":False, "label":"C", "labelsize":3/4, "descname":" C", "descoff":""},
        19: {"x1":73, "y1":16, "x2":78, "y2":17.5, "type":"model", "halfable":False, "label":"B", "labelsize":3/4, "descname":" B", "descoff":""},
        20: {"x1":78, "y1":16, "x2":80, "y2":19, "type":"model", "halfable":False, "label":"g", "labelsize":3/4, "descname":" g", "descoff":""},
    },
    
    "oboe": {
        "parameters": {"keys":28, "LR_split":16, "separator":" | ", "offsetx":-4, "offsety":-1, "shiftx":-1, "shifty":1.75, "Lx":6, "Ly":3, "Mx":45.5, "My":13, "Bx":37, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": [],
        0: {"x1":8, "y1":23, "x2":12.5, "y2":26, "type":"model", "halfable":False, "label":"III", "labelsize":1, "descname":"III ", "descoff":""},
        1: {"x1":12.5, "y1":23, "x2":17, "y2":26, "type":"octave", "halfable":False, "label":"I", "labelsize":1, "descname":"I ", "descoff":""},
        2: {"x1":18, "y1":23, "x2":22.5, "y2":26, "type":"model", "halfable":False, "label":"A", "labelsize":1, "descname":"A ", "descoff":""},
        3: {"x1":8, "y1":9, "x2":14, "y2":12, "type":"octave", "halfable":False, "label":"II", "labelsize":1, "descname":"II ", "descoff":""},
        4: {"x1":12, "y1":12, "x2":19, "y2":19, "type":"main", "halfable":True, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        5: {"x1":18, "y1":18, "x2":21, "y2":20, "type":"trill", "halfable":False, "label":"b", "labelsize":1, "descname":"b", "descoff":""},
        6: {"x1":18.5, "y1":10, "x2":20.5, "y2":13.5, "type":"trill", "halfable":False, "label":"d", "labelsize":1, "descname":"d", "descoff":""},
        7: {"x1":20, "y1":12, "x2":27, "y2":19, "type":"main", "halfable":True, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        8: {"x1":26, "y1":18, "x2":29, "y2":21, "type":"special", "halfable":False, "label":"a*", "labelsize":1, "descname":"a*", "descoff":""},
        9: {"x1":26.5, "y1":10, "x2":28.5, "y2":13.5, "type":"trill", "halfable":False, "label":"c#", "labelsize":1, "descname":"c#", "descoff":""},
        10: {"x1":28, "y1":12, "x2":35, "y2":19, "type":"main", "halfable":True, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        11: {"x1":35, "y1":7.5, "x2":38, "y2":12.5, "type":"second", "halfable":False, "label":"G#", "labelsize":1, "descname":" G#", "descoff":""},
        12: {"x1":38, "y1":10, "x2":44, "y2":12.5, "type":"second", "halfable":False, "label":"Eb", "labelsize":1, "descname":" Eb", "descoff":""},
        13: {"x1":38, "y1":7.5, "x2":41.5, "y2":10, "type":"low", "halfable":False, "label":"B", "labelsize":1, "descname":" B", "descoff":""},
        14: {"x1":38, "y1":5, "x2":44, "y2":7.5, "type":"low", "halfable":False, "label":"Bb", "labelsize":1, "descname":" Bb", "descoff":""},
        15: {"x1":41.5, "y1":7.5, "x2":45, "y2":10, "type":"second", "halfable":False, "label":"F", "labelsize":1, "descname":" F", "descoff":""},
        16: {"x1":39, "y1":20, "x2":44, "y2":23, "type":"model", "halfable":False, "label":"A", "labelsize":1, "descname":"A ", "descoff":""},
        17: {"x1":44, "y1":20, "x2":49, "y2":23, "type":"second", "halfable":False, "label":"G#", "labelsize":1, "descname":"G# ", "descoff":""},
        18: {"x1":45.5, "y1":12, "x2":52.5, "y2":19, "type":"main", "halfable":True, "label":"4", "labelsize":2, "descname":"4", "descoff":"−"},
        19: {"x1":53, "y1":14, "x2":56, "y2":17, "type":"special", "halfable":False, "label":"F+*", "labelsize":5/6, "descname":"F+*", "descoff":""},
        20: {"x1":53.5, "y1":17.5, "x2":55.5, "y2":20.5, "type":"trill", "halfable":False, "label":"d", "labelsize":1, "descname":"d", "descoff":""},
        21: {"x1":56.5, "y1":12, "x2":63.5, "y2":19, "type":"main", "halfable":True, "label":"5", "labelsize":2, "descname":"5", "descoff":"−"},
        22: {"x1":63.5, "y1":16, "x2":66.5, "y2":21, "type":"second", "halfable":False, "label":"F", "labelsize":1, "descname":"F", "descoff":""},
        23: {"x1":66.5, "y1":12, "x2":73.5, "y2":19, "type":"main", "halfable":True, "label":"6", "labelsize":2, "descname":"6", "descoff":"−"},
        24: {"x1":67.5, "y1":8.5, "x2":72.5, "y2":11, "type":"model", "halfable":False, "label":"c", "labelsize":1, "descname":"c", "descoff":""},
        25: {"x1":72.5, "y1":18.5, "x2":76, "y2":22, "type":"low", "halfable":False, "label":"C", "labelsize":1, "descname":" C", "descoff":""},
        26: {"x1":74.5, "y1":15, "x2":78, "y2":18.5, "type":"low", "halfable":False, "label":"C#", "labelsize":1, "descname":" C#", "descoff":""},
        27: {"x1":76.5, "y1":18.5, "x2":80, "y2":22, "type":"second", "halfable":False, "label":"Eb", "labelsize":1, "descname":" Eb", "descoff":""},
    },

    "corangl": {
        "parameters": {"keys":27, "LR_split":16, "separator":" | ", "offsetx":-4, "offsety":-1, "shiftx":-1, "shifty":1.75, "Lx":6, "Ly":3, "Mx":49, "My":13, "Bx":42, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": [],
        0: {"x1":8, "y1":23, "x2":12.5, "y2":26, "type":"model", "halfable":False, "label":"III", "labelsize":1, "descname":"III ", "descoff":""},
        1: {"x1":12.5, "y1":23, "x2":17, "y2":26, "type":"octave", "halfable":False, "label":"I", "labelsize":1, "descname":"I ", "descoff":""},
        2: {"x1":8, "y1":9, "x2":14, "y2":12, "type":"octave", "halfable":False, "label":"II", "labelsize":1, "descname":"II ", "descoff":""},
        3: {"x1":12, "y1":12, "x2":19, "y2":19, "type":"main", "halfable":False, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        4: {"x1":19.5, "y1":13.25, "x2":24, "y2":17.75, "type":"octave", "halfable":False, "label":"½", "labelsize":1.75, "descname":"$⌫", "descoff":""},
        5: {"x1":22.5, "y1":18, "x2":25.5, "y2":20, "type":"trill", "halfable":False, "label":"b", "labelsize":1, "descname":"b", "descoff":""},
        6: {"x1":23, "y1":10, "x2":25, "y2":13.5, "type":"trill", "halfable":False, "label":"d", "labelsize":1, "descname":"d", "descoff":""},
        7: {"x1":24.5, "y1":12, "x2":31.5, "y2":19, "type":"main", "halfable":True, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        8: {"x1":30.5, "y1":18, "x2":33.5, "y2":21, "type":"special", "halfable":False, "label":"a*", "labelsize":1, "descname":"a*", "descoff":""},
        9: {"x1":31, "y1":10, "x2":33, "y2":13.5, "type":"trill", "halfable":False, "label":"c#", "labelsize":1, "descname":"c#", "descoff":""},
        10: {"x1":32.5, "y1":12, "x2":39.5, "y2":19, "type":"main", "halfable":True, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        11: {"x1":38.5, "y1":7.5, "x2":41.5, "y2":12.5, "type":"second", "halfable":False, "label":"G#", "labelsize":1, "descname":" G#", "descoff":""},
        12: {"x1":41.5, "y1":10, "x2":47.5, "y2":12.5, "type":"second", "halfable":False, "label":"Eb", "labelsize":1, "descname":" Eb", "descoff":""},
        13: {"x1":41.5, "y1":7.5, "x2":45, "y2":10, "type":"low", "halfable":False, "label":"B", "labelsize":1, "descname":" B", "descoff":""},
        14: {"x1":41.5, "y1":5, "x2":47.5, "y2":7.5, "type":"model", "halfable":False, "label":"Bb", "labelsize":1, "descname":" Bb", "descoff":""},
        15: {"x1":45, "y1":7.5, "x2":48.5, "y2":10, "type":"second", "halfable":False, "label":"F", "labelsize":1, "descname":" F", "descoff":""},
        16: {"x1":44.5, "y1":20, "x2":52, "y2":23, "type":"second", "halfable":False, "label":"G#", "labelsize":1, "descname":"G# ", "descoff":""},
        17: {"x1":44.5, "y1":14, "x2":47.5, "y2":17, "type":"special", "halfable":False, "label":"Gd*", "labelsize":5/6, "descname":"Gd*", "descoff":""},
        18: {"x1":48.5, "y1":12, "x2":55.5, "y2":19, "type":"main", "halfable":True, "label":"4", "labelsize":2, "descname":"4", "descoff":"−"},
        19: {"x1":55, "y1":17.5, "x2":57, "y2":20.5, "type":"trill", "halfable":False, "label":"d", "labelsize":1, "descname":"d", "descoff":""},
        20: {"x1":56.5, "y1":12, "x2":63.5, "y2":19, "type":"main", "halfable":True, "label":"5", "labelsize":2, "descname":"5", "descoff":"−"},
        21: {"x1":63.5, "y1":16, "x2":66.5, "y2":21, "type":"second", "halfable":False, "label":"F", "labelsize":1, "descname":"F", "descoff":""},
        22: {"x1":66.5, "y1":12, "x2":73.5, "y2":19, "type":"main", "halfable":True, "label":"6", "labelsize":2, "descname":"6", "descoff":"−"},
        23: {"x1":67.5, "y1":8.5, "x2":72.5, "y2":11, "type":"model", "halfable":False, "label":"c", "labelsize":1, "descname":"c", "descoff":""},
        24: {"x1":72.5, "y1":18.5, "x2":76, "y2":22, "type":"low", "halfable":False, "label":"C", "labelsize":1, "descname":" C", "descoff":""},
        25: {"x1":74.5, "y1":15, "x2":78, "y2":18.5, "type":"low", "halfable":False, "label":"C#", "labelsize":1, "descname":" C#", "descoff":""},
        26: {"x1":76.5, "y1":18.5, "x2":80, "y2":22, "type":"second", "halfable":False, "label":"Eb", "labelsize":1, "descname":" Eb", "descoff":""},
    },

    "bassoon": {
        "parameters": {"keys":34, "LR_split":21, "separator":" | ", "offsetx":-4, "offsety":-1, "shiftx":-3.5, "shifty":-2, "Lx":6, "Ly":3, "Mx":48, "My":14.5, "Bx":43, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": [],
        0: {"x1":10, "y1":27.5, "x2":13, "y2":30.5, "type":"special", "halfable":False, "label":"C*", "labelsize":1, "descname":"C* ", "descoff":""},
        1: {"x1":13.5, "y1":27, "x2":18.5, "y2":29, "type":"low", "halfable":False, "label":"Bb", "labelsize":1, "descname":"Bb ", "descoff":""},
        2: {"x1":13.5, "y1":29, "x2":18.5, "y2":31, "type":"low", "halfable":False, "label":"B", "labelsize":1, "descname":"B ", "descoff":""},
        3: {"x1":14.5, "y1":31, "x2":18.5, "y2":33, "type":"low", "halfable":False, "label":"C", "labelsize":1, "descname":"C ", "descoff":""},
        4: {"x1":18.5, "y1":28, "x2":22, "y2":30.5, "type":"model", "halfable":False, "label":"C2", "labelsize":1, "descname":"C2 ", "descoff":""},
        5: {"x1":18.5, "y1":30.5, "x2":25, "y2":33, "type":"low", "halfable":False, "label":"D", "labelsize":1, "descname":"D ", "descoff":""},
        6: {"x1":14, "y1":23.5, "x2":16.5, "y2":27, "type":"octave", "halfable":False, "label":"d", "labelsize":1, "descname":"d ", "descoff":""},
        7: {"x1":16.5, "y1":23.5, "x2":19, "y2":27, "type":"octave", "halfable":False, "label":"c", "labelsize":1, "descname":"c ", "descoff":""},
        8: {"x1":19, "y1":23.5, "x2":21.5, "y2":27, "type":"octave", "halfable":False, "label":"a", "labelsize":1, "descname":"a ", "descoff":""},
        9: {"x1":21.5, "y1":24, "x2":24, "y2":27.5, "type":"second", "halfable":False, "label":"C#", "labelsize":1, "descname":"C# ", "descoff":""},
        10: {"x1":24, "y1":25.5, "x2":26.5, "y2":28, "type":"octave", "halfable":False, "label":"W", "labelsize":1, "descname":"W ", "descoff":""},
        11: {"x1":10, "y1":10.5, "x2":13, "y2":15.5, "type":"high", "halfable":False, "label":"e", "labelsize":1, "descname":"e", "descoff":""},
        12: {"x1":13, "y1":12, "x2":20, "y2":19, "type":"main", "halfable":True, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        13: {"x1":20, "y1":10.5, "x2":23, "y2":15.5, "type":"high", "halfable":False, "label":"eb", "labelsize":1, "descname":"eb", "descoff":""},
        14: {"x1":23, "y1":12, "x2":30, "y2":19, "type":"main", "halfable":True, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        15: {"x1":30, "y1":10.5, "x2":33, "y2":15.5, "type":"model", "halfable":False, "label":"Eb", "labelsize":1, "descname":"Eb", "descoff":""},
        16: {"x1":33, "y1":12, "x2":40, "y2":19, "type":"main", "halfable":True, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        17: {"x1":39, "y1":7.5, "x2":42, "y2":12.5, "type":"second", "halfable":False, "label":"Eb", "labelsize":1, "descname":" Eb", "descoff":""},
        18: {"x1":42, "y1":7.5, "x2":45, "y2":12.5, "type":"low", "halfable":False, "label":"C#", "labelsize":1, "descname":" C#", "descoff":""},
        19: {"x1":45, "y1":10, "x2":47.5, "y2":14, "type":"model", "halfable":False, "label":"W", "labelsize":1, "descname":" W", "descoff":""},
        20: {"x1":45, "y1":6, "x2":47.5, "y2":10, "type":"model", "halfable":False, "label":"A", "labelsize":1, "descname":" A", "descoff":""},
        21: {"x1":45.5, "y1":27.5, "x2":48, "y2":31.5, "type":"second", "halfable":False, "label":"Bb", "labelsize":1, "descname":"Bb ", "descoff":""},
        22: {"x1":48, "y1":27, "x2":53, "y2":32, "type":"low", "halfable":False, "label":"E", "labelsize":1, "descname":"E ", "descoff":""},
        23: {"x1":53, "y1":27.5, "x2":55.5, "y2":31.5, "type":"low", "halfable":False, "label":"F#", "labelsize":1, "descname":"F# ", "descoff":""},
        24: {"x1":55.5, "y1":27.5, "x2":58, "y2":31.5, "type":"second", "halfable":False, "label":"G#", "labelsize":1, "descname":"G# ", "descoff":""},
        25: {"x1":45.5, "y1":17, "x2":48.5, "y2":21, "type":"trill", "halfable":False, "label":"C#", "labelsize":1, "descname":"C# ", "descoff":""},
        26: {"x1":48.5, "y1":12, "x2":55.5, "y2":19, "type":"main", "halfable":True, "label":"4", "labelsize":2, "descname":"4", "descoff":"−"},
        27: {"x1":56, "y1":14, "x2":59, "y2":17, "type":"special", "halfable":False, "label":"Bb*", "labelsize":5/6, "descname":"Bb*", "descoff":""},
        28: {"x1":59.5, "y1":12, "x2":66.5, "y2":19, "type":"main", "halfable":True, "label":"5", "labelsize":2, "descname":"5", "descoff":"−"},
        29: {"x1":66.5, "y1":10.5, "x2":69.5, "y2":15.5, "type":"second", "halfable":False, "label":"Bb", "labelsize":1, "descname":"Bb", "descoff":""},
        30: {"x1":69.5, "y1":12, "x2":76.5, "y2":19, "type":"main", "halfable":False, "label":"6", "labelsize":2, "descname":"6", "descoff":"−"},
        31: {"x1":77, "y1":19, "x2":80, "y2":22, "type":"low", "halfable":False, "label":"F", "labelsize":1, "descname":" F", "descoff":""},
        32: {"x1":77, "y1":14, "x2":80, "y2":19, "type":"low", "halfable":False, "label":"F#", "labelsize":1, "descname":" F#", "descoff":""},
        33: {"x1":80, "y1":17, "x2":83, "y2":22, "type":"second", "halfable":False, "label":"G#", "labelsize":1, "descname":" G#", "descoff":""},
    },

    "contrafg": {
        "parameters": {"keys":29, "LR_split":16, "separator":" | ", "offsetx":-4, "offsety":-1, "shiftx":-5, "shifty":-2.5, "Lx":6, "Ly":3, "Mx":48, "My":13.5, "Bx":43, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": [],
        0: {"x1":13, "y1":26.5, "x2":16, "y2":29.5, "type":"special", "halfable":False, "label":"C*", "labelsize":1, "descname":"C* ", "descoff":""},
        1: {"x1":16.5, "y1":26.5, "x2":20, "y2":29.5, "type":"low", "halfable":False, "label":"Bb", "labelsize":1, "descname":"Bb ", "descoff":""},
        2: {"x1":18, "y1":29.5, "x2":20.5, "y2":32.5, "type":"low", "halfable":False, "label":"B", "labelsize":1, "descname":"B ", "descoff":""},
        3: {"x1":20.5, "y1":29.5, "x2":23, "y2":32.5, "type":"low", "halfable":False, "label":"C", "labelsize":1, "descname":"C ", "descoff":""},
        4: {"x1":23, "y1":29.5, "x2":25.5, "y2":32.5, "type":"low", "halfable":False, "label":"D", "labelsize":1, "descname":"D ", "descoff":""},
        5: {"x1":20, "y1":26, "x2":22.5, "y2":29, "type":"octave", "halfable":False, "label":"d", "labelsize":1, "descname":"d ", "descoff":""},
        6: {"x1":23.5, "y1":24, "x2":26.5, "y2":26, "type":"model", "halfable":False, "label":"d2", "labelsize":5/6, "descname":"d2 ", "descoff":""},
        7: {"x1":22.5, "y1":26, "x2":25, "y2":29, "type":"octave", "halfable":False, "label":"a", "labelsize":1, "descname":"a ", "descoff":""},
        8: {"x1":25, "y1":26, "x2":27.5, "y2":29, "type":"second", "halfable":False, "label":"C#", "labelsize":1, "descname":"C# ", "descoff":""},
        9: {"x1":14.5, "y1":12, "x2":21.5, "y2":19, "type":"main", "halfable":False, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        10: {"x1":22.5, "y1":12, "x2":29.5, "y2":19, "type":"main", "halfable":False, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        11: {"x1":29.5, "y1":10.5, "x2":32.5, "y2":15.5, "type":"second", "halfable":False, "label":"Eb", "labelsize":1, "descname":"Eb", "descoff":""},
        12: {"x1":32.5, "y1":12, "x2":39.5, "y2":19, "type":"main", "halfable":False, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        13: {"x1":38.5, "y1":7.5, "x2":41.5, "y2":12.5, "type":"second", "halfable":False, "label":"Eb", "labelsize":1, "descname":" Eb", "descoff":""},
        14: {"x1":41.5, "y1":7.5, "x2":44.5, "y2":12.5, "type":"low", "halfable":False, "label":"C#", "labelsize":1, "descname":" C#", "descoff":""},
        15: {"x1":44.5, "y1":7.5, "x2":47.5, "y2":12.5, "type":"model", "halfable":False, "label":"A", "labelsize":1, "descname":" A", "descoff":""},
        16: {"x1":45.5, "y1":27.5, "x2":48, "y2":31.5, "type":"model", "halfable":False, "label":"Eb", "labelsize":1, "descname":"G# ", "descoff":""},       
        17: {"x1":48, "y1":27.5, "x2":50.5, "y2":31.5, "type":"second", "halfable":False, "label":"Bb", "labelsize":1, "descname":"Bb ", "descoff":""},
        18: {"x1":50.5, "y1":27, "x2":55.5, "y2":32, "type":"low", "halfable":False, "label":"E", "labelsize":1, "descname":"E ", "descoff":""},
        19: {"x1":55.5, "y1":27.5, "x2":58, "y2":31.5, "type":"low", "halfable":False, "label":"F#", "labelsize":1, "descname":"F# ", "descoff":""},
        20: {"x1":45, "y1":14, "x2":48, "y2":17, "type":"special", "halfable":False, "label":"6*", "labelsize":1, "descname":"6*", "descoff":""},
        21: {"x1":48.5, "y1":10.5, "x2":51.5, "y2":15.5, "type":"model", "halfable":False, "label":"Eb", "labelsize":1, "descname":"Eb ", "descoff":""},
        22: {"x1":51.5, "y1":12, "x2":58.5, "y2":19, "type":"main", "halfable":False, "label":"4", "labelsize":2, "descname":"4", "descoff":"−"},
        23: {"x1":59.5, "y1":12, "x2":66.5, "y2":19, "type":"main", "halfable":False, "label":"5", "labelsize":2, "descname":"5", "descoff":"−"},
        24: {"x1":66.5, "y1":10.5, "x2":69.5, "y2":15.5, "type":"second", "halfable":False, "label":"Bb", "labelsize":1, "descname":"Bb", "descoff":""},
        25: {"x1":69.5, "y1":12, "x2":76.5, "y2":19, "type":"main", "halfable":False, "label":"6", "labelsize":2, "descname":"6", "descoff":"−"},
        26: {"x1":77, "y1":19, "x2":80, "y2":22, "type":"low", "halfable":False, "label":"F", "labelsize":1, "descname":" F", "descoff":""},
        27: {"x1":77, "y1":14, "x2":80, "y2":19, "type":"low", "halfable":False, "label":"F#", "labelsize":1, "descname":" F#", "descoff":""},
        28: {"x1":80, "y1":17, "x2":83, "y2":22, "type":"second", "halfable":False, "label":"G#", "labelsize":1, "descname":" G#", "descoff":""},
    },
    
    "clarinet": {
        "parameters": {"keys":28, "LR_split":14, "separator":" | ", "offsetx":-4, "offsety":-1, "shiftx":0, "shifty":1, "Lx":6, "Ly":3, "Mx":50.5, "My":12, "Bx":42, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": [],
        0: {"x1":7, "y1":23, "x2":13, "y2":26, "type":"octave", "halfable":False, "label":"R", "labelsize":1, "descname":"R ", "descoff":""},
        1: {"x1":13.5, "y1":22.5, "x2":17.5, "y2":26.5, "type":"main", "halfable":True, "label":"T", "labelsize":6/5, "descname":"T ", "descoff":""},
        2: {"x1":9, "y1":10, "x2":14, "y2":13, "type":"high", "halfable":False, "label":"G#", "labelsize":1, "descname":"G# ", "descoff":""},
        3: {"x1":7, "y1":14, "x2":12, "y2":17, "type":"high", "halfable":False, "label":"A", "labelsize":1, "descname":"A ", "descoff":""},
        4: {"x1":13, "y1":12, "x2":20, "y2":19, "type":"main", "halfable":True, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        5: {"x1":20.5, "y1":14, "x2":23.5, "y2":17, "type":"special", "halfable":False, "label":"Eb*\nBb*", "labelsize":2/3, "descname":"Eb*", "descoff":""},
        6: {"x1":24, "y1":12, "x2":31, "y2":19, "type":"main", "halfable":True, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        7: {"x1":30.5, "y1":9, "x2":33.5, "y2":14, "type":"second", "halfable":False, "label":"Eb\nBb", "labelsize":5/6, "descname":"Eb", "descoff":""},
        8: {"x1":33, "y1":12, "x2":40, "y2":19, "type":"main", "halfable":True, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        9: {"x1":39, "y1":9, "x2":41.5, "y2":13, "type":"second", "halfable":False, "label":"C#\nG#", "labelsize":5/6, "descname":" C#", "descoff":""},
        10: {"x1":41.5, "y1":7.5, "x2":43.5, "y2":11.5, "type":"low", "halfable":False, "label":"F\nC", "labelsize":5/6, "descname":" F", "descoff":""},
        11: {"x1":43.5, "y1":7.5, "x2":47, "y2":9.5, "type":"low", "halfable":False, "label":"F# C#", "labelsize":2/3, "descname":" F#", "descoff":""},
        12: {"x1":43.5, "y1":9.5, "x2":47, "y2":11.5, "type":"low", "halfable":False, "label":"E B", "labelsize":2/3, "descname":" E", "descoff":""},
        13: {"x1":46.5, "y1":8.5, "x2":50, "y2":10.5, "type":"model", "halfable":False, "label":"Ab Eb", "labelsize":2/3, "descname":" Ab", "descoff":""},
        14: {"x1":42.5, "y1":20, "x2":44.5, "y2":23, "type":"trill", "halfable":False, "label":"b", "labelsize":2/3, "descname":"b ", "descoff":""},
        15: {"x1":44.5, "y1":20, "x2":46.5, "y2":23, "type":"trill", "halfable":False, "label":"bb", "labelsize":2/3, "descname":"bb ", "descoff":""},
        16: {"x1":46.5, "y1":20, "x2":48.5, "y2":23, "type":"second", "halfable":False, "label":"f#", "labelsize":2/3, "descname":"f# ", "descoff":""},
        17: {"x1":48.5, "y1":20, "x2":50.5, "y2":23, "type":"second", "halfable":False, "label":"eb\nbb", "labelsize":2/3, "descname":"eb ", "descoff":""},
        18: {"x1":45.5, "y1":14, "x2":48.5, "y2":17, "type":"special", "halfable":False, "label":"   B*\nF#*", "labelsize":2/3, "descname":"F#* ", "descoff":""},
        19: {"x1":49, "y1":12, "x2":56, "y2":19, "type":"main", "halfable":True, "label":"4", "labelsize":2, "descname":"4", "descoff":"−"},
        20: {"x1":57, "y1":12, "x2":64, "y2":19, "type":"main", "halfable":True, "label":"5", "labelsize":2, "descname":"5", "descoff":"−"},
        21: {"x1":63, "y1":17.5, "x2":66, "y2":22.5, "type":"second", "halfable":False, "label":"   B\nF#", "labelsize":5/6, "descname":"B", "descoff":""},
        22: {"x1":65, "y1":12, "x2":72, "y2":19, "type":"main", "halfable":True, "label":"6", "labelsize":2, "descname":"6", "descoff":"−"},
        23: {"x1":72, "y1":16, "x2":74.5, "y2":20, "type":"second", "halfable":False, "label":"Ab\nEb", "labelsize":3/4, "descname":" Ab", "descoff":""},
        24: {"x1":74.5, "y1":16, "x2":77, "y2":20, "type":"low", "halfable":False, "label":"F\nC", "labelsize":3/4, "descname":" F", "descoff":""},
        25: {"x1":72, "y1":20, "x2":74.5, "y2":24, "type":"low", "halfable":False, "label":"F#\nC#", "labelsize":3/4, "descname":" F#", "descoff":""},
        26: {"x1":74.5, "y1":20, "x2":77, "y2":24, "type":"low", "halfable":False, "label":"E\nB", "labelsize":3/4, "descname":" E", "descoff":""},
        27: {"x1":77, "y1":20, "x2":79.5, "y2":24, "type":"model", "halfable":False, "label":"Eb", "labelsize":5/6, "descname":" Eb", "descoff":""},
    },

    "bassclar": {
        "parameters": {"keys":33, "LR_split":14, "separator":" | ", "offsetx":-4, "offsety":-1, "shiftx":-1.5, "shifty":-1, "Lx":6, "Ly":3, "Mx":50.5, "My":12, "Bx":42, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": [],
        0: {"x1":10, "y1":28, "x2":16, "y2":31, "type":"octave", "halfable":False, "label":"R", "labelsize":1, "descname":"R ", "descoff":""},
        1: {"x1":16.5, "y1":27.5, "x2":20.5, "y2":31.5, "type":"main", "halfable":False, "label":"T", "labelsize":6/5, "descname":"T ", "descoff":""},
        2: {"x1":12, "y1":10, "x2":17, "y2":13, "type":"high", "halfable":False, "label":"G#", "labelsize":1, "descname":"G# ", "descoff":""},
        3: {"x1":10, "y1":14, "x2":15, "y2":17, "type":"high", "halfable":False, "label":"A", "labelsize":1, "descname":"A ", "descoff":""},
        4: {"x1":16, "y1":12, "x2":23, "y2":19, "type":"main", "halfable":False, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        5: {"x1":24, "y1":12, "x2":31, "y2":19, "type":"main", "halfable":False, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        6: {"x1":30.5, "y1":9, "x2":33.5, "y2":14, "type":"second", "halfable":False, "label":"Eb\nBb", "labelsize":5/6, "descname":"Eb", "descoff":""},
        7: {"x1":33, "y1":12, "x2":40, "y2":19, "type":"main", "halfable":False, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        8: {"x1":39, "y1":9, "x2":41.5, "y2":13, "type":"second", "halfable":False, "label":"C#\nG#", "labelsize":5/6, "descname":" C#", "descoff":""},
        9: {"x1":41.5, "y1":7.5, "x2":43.5, "y2":11.5, "type":"low", "halfable":False, "label":"F\nC", "labelsize":5/6, "descname":" F", "descoff":""},
        10: {"x1":43.5, "y1":7.5, "x2":47, "y2":9.5, "type":"low", "halfable":False, "label":"F# C#", "labelsize":2/3, "descname":" F#", "descoff":""},
        11: {"x1":43.5, "y1":9.5, "x2":47, "y2":11.5, "type":"low", "halfable":False, "label":"E B", "labelsize":2/3, "descname":" E", "descoff":""},
        12: {"x1":43, "y1":5.5, "x2":46.5, "y2":7.5, "type":"model", "halfable":False, "label":"D", "labelsize":3/4, "descname":" D", "descoff":""},
        13: {"x1":46.5, "y1":8.5, "x2":50, "y2":10.5, "type":"model", "halfable":False, "label":"Ab Eb", "labelsize":2/3, "descname":" Ab", "descoff":""},
        14: {"x1":43, "y1":28, "x2":46, "y2":31, "type":"model", "halfable":False, "label":"Eb", "labelsize":1, "descname":"Eb ", "descoff":""},
        15: {"x1":44.5, "y1":25.5, "x2":49, "y2":28.5, "type":"model", "halfable":False, "label":"D", "labelsize":1, "descname":"D ", "descoff":""},
        16: {"x1":46, "y1":28.5, "x2":49, "y2":31.5, "type":"model", "halfable":False, "label":"C#", "labelsize":1, "descname":"C# ", "descoff":""},
        17: {"x1":49, "y1":26, "x2":52, "y2":31, "type":"model", "halfable":False, "label":"C", "labelsize":1, "descname":"C ", "descoff":""},
        18: {"x1":42.5, "y1":19, "x2":44.5, "y2":22, "type":"trill", "halfable":False, "label":"b", "labelsize":2/3, "descname":"b ", "descoff":""},
        19: {"x1":44.5, "y1":19, "x2":46.5, "y2":22, "type":"trill", "halfable":False, "label":"bb", "labelsize":2/3, "descname":"bb ", "descoff":""},
        20: {"x1":46.5, "y1":19, "x2":48.5, "y2":22, "type":"second", "halfable":False, "label":"f#", "labelsize":2/3, "descname":"f# ", "descoff":""},
        21: {"x1":48.5, "y1":19, "x2":50.5, "y2":22, "type":"second", "halfable":False, "label":"eb\nbb", "labelsize":2/3, "descname":"eb ", "descoff":""},
        22: {"x1":45.5, "y1":14, "x2":48.5, "y2":17, "type":"special", "halfable":False, "label":"  B*\nF#*", "labelsize":2/3, "descname":"F#* ", "descoff":""},
        23: {"x1":49, "y1":12, "x2":56, "y2":19, "type":"main", "halfable":False, "label":"4", "labelsize":2, "descname":"4", "descoff":"−"},
        24: {"x1":57, "y1":12, "x2":64, "y2":19, "type":"main", "halfable":False, "label":"5", "labelsize":2, "descname":"5", "descoff":"−"},
        25: {"x1":63, "y1":17.5, "x2":66, "y2":22.5, "type":"second", "halfable":False, "label":"   B\nF#", "labelsize":5/6, "descname":"B", "descoff":""},
        26: {"x1":65, "y1":12, "x2":72, "y2":19, "type":"main", "halfable":False, "label":"6", "labelsize":2, "descname":"6", "descoff":"−"},
        27: {"x1":72, "y1":16, "x2":74.5, "y2":20, "type":"second", "halfable":False, "label":"Ab\nEb", "labelsize":3/4, "descname":" Ab", "descoff":""},
        28: {"x1":74.5, "y1":16, "x2":77, "y2":20, "type":"low", "halfable":False, "label":"F\nC", "labelsize":3/4, "descname":" F", "descoff":""},
        29: {"x1":72, "y1":20, "x2":74.5, "y2":24, "type":"low", "halfable":False, "label":"F#\nC#", "labelsize":3/4, "descname":" F#", "descoff":""},
        30: {"x1":74.5, "y1":20, "x2":77, "y2":24, "type":"low", "halfable":False, "label":"E\nB", "labelsize":3/4, "descname":" E", "descoff":""},
        31: {"x1":77, "y1":20, "x2":79.5, "y2":24, "type":"low", "halfable":False, "label":"Eb", "labelsize":5/6, "descname":" Eb", "descoff":""},
        32: {"x1":77, "y1":16, "x2":79.5, "y2":20, "type":"model", "halfable":False, "label":"D", "labelsize":5/6, "descname":" D", "descoff":""},
    },
    
    "saxophone": {
        "parameters": {"keys":30, "LR_split":15, "separator":" |", "offsetx":-4, "offsety":-1, "shiftx":2, "shifty":3, "Lx":6, "Ly":3, "Mx":46.5, "My":13.5, "Bx":36.5, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": [],
        0: {"x1":13, "y1":22, "x2":15.5, "y2":26, "type":"octave", "halfable":False, "label":"o", "labelsize":1, "descname":"o ", "descoff":""},
        1: {"x1":16, "y1":22, "x2":18.5, "y2":26, "type":"model", "halfable":False, "label":"A", "labelsize":1, "descname":"A ", "descoff":""},
        2: {"x1":14, "y1":7, "x2":19, "y2":10, "type":"high", "halfable":False, "label":"eb", "labelsize":1, "descname":"eb ", "descoff":""},
        3: {"x1":14, "y1":4, "x2":19, "y2":7, "type":"high", "halfable":False, "label":"d", "labelsize":1, "descname":"d ", "descoff":""},
        4: {"x1":7, "y1":14, "x2":10, "y2":17, "type":"special", "halfable":False, "label":"C+*", "labelsize":3/4, "descname":"C+* ", "descoff":""},
        5: {"x1":10.5, "y1":13, "x2":12.5, "y2":18, "type":"second", "halfable":False, "label":"f", "labelsize":1, "descname":"f ", "descoff":""},
        6: {"x1":13, "y1":12, "x2":20, "y2":19, "type":"main", "halfable":False, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        7: {"x1":19, "y1":10, "x2":22, "y2":13, "type":"second", "halfable":False, "label":"bis", "labelsize":3/4, "descname":"Bb", "descoff":""},
        8: {"x1":22, "y1":7, "x2":27, "y2":10, "type":"high", "halfable":False, "label":"f", "labelsize":1, "descname":"f", "descoff":""},
        9: {"x1":21, "y1":12, "x2":28, "y2":19, "type":"main", "halfable":False, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        10: {"x1":29, "y1":12, "x2":36, "y2":19, "type":"main", "halfable":False, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        11: {"x1":35, "y1":7.5, "x2":38, "y2":12.5, "type":"second", "halfable":False, "label":"G#", "labelsize":1, "descname":" G#", "descoff":""},
        12: {"x1":38, "y1":7, "x2":43, "y2":10, "type":"low", "halfable":False, "label":"C#", "labelsize":1, "descname":" C#", "descoff":""},
        13: {"x1":38, "y1":10, "x2":43, "y2":13, "type":"low", "halfable":False, "label":"B", "labelsize":1, "descname":" B", "descoff":""},
        14: {"x1":43, "y1":7.5, "x2":46, "y2":12.5, "type":"low", "halfable":False, "label":"Bb", "labelsize":1, "descname":" Bb", "descoff":""},
        15: {"x1":40, "y1":14, "x2":43, "y2":17, "type":"link", "halfable":False, "label":"      G#\ncancel", "labelsize":1/2, "descname":"| ", "descoff":" "},
        16: {"x1":37, "y1":23, "x2":42, "y2":26, "type":"high", "halfable":False, "label":"e", "labelsize":1, "descname":"e ", "descoff":""},
        17: {"x1":42, "y1":23, "x2":47, "y2":26, "type":"second", "halfable":False, "label":"C", "labelsize":1, "descname":"C ", "descoff":""},
        18: {"x1":47, "y1":23, "x2":52, "y2":26, "type":"second", "halfable":False, "label":"Bb", "labelsize":1, "descname":"Bb ", "descoff":""},
        19: {"x1":43.5, "y1":14, "x2":46.5, "y2":17, "type":"special", "halfable":False, "label":"F#*", "labelsize":3/4, "descname":"F#* ", "descoff":""},
        20: {"x1":47, "y1":12, "x2":54, "y2":19, "type":"main", "halfable":False, "label":"4", "labelsize":2, "descname":"4", "descoff":"−"},
        21: {"x1":47, "y1":19.5, "x2":52, "y2":22.5, "type":"model", "halfable":False, "label":"g", "labelsize":1, "descname":"g", "descoff":""},
        22: {"x1":52, "y1":19.5, "x2":57, "y2":22.5, "type":"high", "halfable":False, "label":"f#", "labelsize":1, "descname":"f#", "descoff":""},
        23: {"x1":48.5, "y1":7, "x2":52.5, "y2":11, "type":"special", "halfable":False, "label":"Bb*", "labelsize":1, "descname":"Bb*", "descoff":""},
        24: {"x1":53.5, "y1":7, "x2":57.5, "y2":11, "type":"special", "halfable":False, "label":"B*", "labelsize":1, "descname":"B*", "descoff":""},
        25: {"x1":55, "y1":12, "x2":62, "y2":19, "type":"main", "halfable":False, "label":"5", "labelsize":2, "descname":"5", "descoff":"−"},
        26: {"x1":61, "y1":17.5, "x2":64, "y2":22.5, "type":"second", "halfable":False, "label":"F#", "labelsize":1, "descname":"F#", "descoff":""},
        27: {"x1":63, "y1":12, "x2":70, "y2":19, "type":"main", "halfable":False, "label":"6", "labelsize":2, "descname":"6", "descoff":"−"},
        28: {"x1":69, "y1":17.5, "x2":72, "y2":22.5, "type":"second", "halfable":False, "label":"Eb", "labelsize":1, "descname":" Eb", "descoff":""},
        29: {"x1":72, "y1":17.5, "x2":75, "y2":22.5, "type":"low", "halfable":False, "label":"C", "labelsize":1, "descname":" C", "descoff":""},
    },

    "trumpet": {
        "parameters": {"keys":7, "LR_split":4, "separator":"", "offsetx":-4, "offsety":-1, "shiftx":3.5, "shifty":2, "Lx":6, "Ly":3, "Mx":39.5, "My":32, "Bx":39.5, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": ["partial", "trumpet"],
        0: {"x1":7, "y1":9, "x2":14, "y2":16, "type":"main", "halfable":True, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        1: {"x1":15, "y1":9, "x2":22, "y2":16, "type":"main", "halfable":True, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        2: {"x1":23, "y1":9, "x2":30, "y2":16, "type":"main", "halfable":True, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        3: {"x1":31, "y1":9, "x2":38, "y2":16, "type":"model", "halfable":True, "label":"4", "labelsize":2, "descname":"4", "descoff":""},
        4: {"x1":21, "y1":20, "x2":32, "y2":22, "type":"sposition1", "preset":"trumpet", "min":0, "max":1, "descname":"", "descoff":""},
        5: {"x1":5, "y1":20, "x2":16, "y2":22, "type":"sposition2", "preset":"trumpet", "min":0, "max":1, "descname":"", "descoff":""},
        6: {"x":58, "y":15, "type":"partial", "size":1, "descname":" ", "descoff":" "},
    },

    "horn": {
        "parameters": {"keys":7, "LR_split":6, "separator":"", "offsetx":-4, "offsety":-1, "shiftx":3, "shifty":2, "Lx":6, "Ly":3, "Mx":40, "My":32, "Bx":40, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": ["partial"],
        0: {"x1":15, "y1":12, "x2":22, "y2":19, "type":"main", "halfable":True, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        1: {"x1":23, "y1":12, "x2":30, "y2":19, "type":"main", "halfable":True, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        2: {"x1":31, "y1":12, "x2":38, "y2":19, "type":"main", "halfable":True, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        3: {"x1":5, "y1":10.5, "x2":10, "y2":15.5, "type":"model", "halfable":True, "label":"F", "labelsize":4/3, "descname":" F", "descoff":""},
        4: {"x1":10, "y1":10.5, "x2":15, "y2":15.5, "type":"model", "halfable":True, "label":"Bb", "labelsize":4/3, "descname":" Bb", "descoff":""},
        5: {"x1":7.5, "y1":15, "x2":12.5, "y2":20, "type":"model", "halfable":True, "label":"alto", "labelsize":1, "descname":" A", "descoff":""},
        6: {"x":58.5, "y":15, "type":"partial", "size":1, "descname":" ", "descoff":" "},
    },

    "trombone": {
        "parameters": {"keys":6, "LR_split":5, "separator":"", "offsetx":-4, "offsety":-1, "shiftx":2, "shifty":2, "Lx":6, "Ly":3, "Mx":41, "My":32, "Bx":41, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": ["partial", "trombone"],
        0: {"x1":6.5, "y1":11, "x2":38.5, "y2":14, "type":"sposition1", "preset":"trombone", "min":1, "max":8, "descname":"", "descoff":""},
        1: {"x1":18, "y1":20, "x2":22, "y2":24, "type":"main", "halfable":False, "label":"F", "labelsize":3/2, "descname":"F", "descoff":""},
        2: {"x1":18, "y1":25, "x2":22, "y2":29, "type":"special", "halfable":False, "label":"E−*", "labelsize":5/4, "descname":"E", "descoff":""},
        3: {"x1":23, "y1":25, "x2":27, "y2":29, "type":"model", "halfable":False, "label":"   G\nEb", "labelsize":1, "descname":"Eb", "descoff":""},
        4: {"x1":23, "y1":20, "x2":27, "y2":24, "type":"model", "halfable":False, "label":"Gb\n    D", "labelsize":1, "descname":"D", "descoff":""},
        5: {"x":59.5, "y":15, "type":"partial", "size":1, "descname":" ", "descoff":" "},
    },

    "4valve": {
        "parameters": {"keys":5, "LR_split":4, "separator":"", "offsetx":-4, "offsety":-1, "shiftx":2, "shifty":2, "Lx":6, "Ly":3, "Mx":41, "My":32, "Bx":41, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": ["partial"],
        0: {"x1":7, "y1":12, "x2":14, "y2":19, "type":"main", "halfable":True, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        1: {"x1":15, "y1":12, "x2":22, "y2":19, "type":"main", "halfable":True, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        2: {"x1":23, "y1":12, "x2":30, "y2":19, "type":"main", "halfable":True, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        3: {"x1":31, "y1":12, "x2":38, "y2":19, "type":"model", "halfable":True, "label":"4", "labelsize":2, "descname":"4", "descoff":""},
        4: {"x":59.5, "y":15, "type":"partial", "size":1, "descname":" ", "descoff":" "},
    },

    "tuba": {
        "parameters": {"keys":7, "LR_split":6, "separator":"", "offsetx":-4, "offsety":-1, "shiftx":2, "shifty":2, "Lx":6, "Ly":3, "Mx":41, "My":32, "Bx":41, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": ["partial"],
        0: {"x1":7, "y1":6, "x2":14, "y2":13, "type":"main", "halfable":True, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        1: {"x1":15, "y1":6, "x2":22, "y2":13, "type":"main", "halfable":True, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        2: {"x1":23, "y1":6, "x2":30, "y2":13, "type":"main", "halfable":True, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        3: {"x1":31, "y1":6, "x2":38, "y2":13, "type":"main", "halfable":True, "label":"4", "labelsize":2, "descname":"4", "descoff":""},
        4: {"x1":15, "y1":18, "x2":22, "y2":25, "type":"model", "halfable":True, "label":"5", "labelsize":2, "descname":"5", "descoff":""},
        5: {"x1":23, "y1":18, "x2":30, "y2":25, "type":"model", "halfable":True, "label":"6", "labelsize":2, "descname":"6", "descoff":""},
        6: {"x":59.5, "y":15, "type":"partial", "size":1, "descname":" ", "descoff":" "},
    },

    "recorder": {
        "parameters": {"keys":11, "LR_split":4, "separator":" | ", "offsetx":-4, "offsety":-1, "shiftx":-2, "shifty":2, "Lx":6, "Ly":3, "Mx":40.5, "My":32, "Bx":40.5, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": [],
        0: {"x1":10, "y1":18.5, "x2":15, "y2":23.5, "type":"main", "halfable":True, "label":"0", "labelsize":3/2, "descname":"0 ", "descoff":""},
        1: {"x1":15, "y1":12, "x2":22, "y2":19, "type":"main", "halfable":True, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        2: {"x1":23, "y1":12, "x2":30, "y2":19, "type":"main", "halfable":True, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        3: {"x1":31, "y1":12, "x2":38, "y2":19, "type":"main", "halfable":True, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        4: {"x1":43, "y1":12, "x2":50, "y2":19, "type":"main", "halfable":True, "label":"4", "labelsize":2, "descname":"4", "descoff":"−"},
        5: {"x1":51, "y1":12, "x2":58, "y2":19, "type":"main", "halfable":True, "label":"5", "labelsize":2, "descname":"5", "descoff":"−"},
        6: {"x1":59, "y1":12, "x2":66, "y2":19, "type":"main", "halfable":True, "label":"6", "labelsize":2, "descname":"6", "descoff":"−"},
        7: {"x1":60.5, "y1":19.5, "x2":64.5, "y2":23.5, "type":"second", "halfable":True, "label":"½", "labelsize":3/2, "descname":"$⌫", "descoff":""},
        8: {"x1":67, "y1":12, "x2":74, "y2":19, "type":"main", "halfable":True, "label":"7", "labelsize":2, "descname":"7", "descoff":"−"},
        9: {"x1":68.5, "y1":19.5, "x2":72.5, "y2":23.5, "type":"second", "halfable":True, "label":"½", "labelsize":3/2, "descname":"$⌫", "descoff":""},
        10: {"x1":75, "y1":13, "x2":80, "y2":18, "type":"special", "halfable":True, "label":"8*", "labelsize":4/3, "descname":" 8*", "descoff":""},
    },

    "custom": {
        "parameters": {"keys":0, "LR_split":0, "separator":" | ", "offsetx":2, "offsety":2, "shiftx":0, "shifty":0, "Lx":0, "Ly":0, "Mx":37, "My":15.5, "Bx":37, "By":29, "Rx":74, "Ry":29, "Descy":33},
        "special": [],
        "name": "New Custom Instrument",
    }
}

# keysystem string
#   Custom — <name> — <keys>-<LR_split>-<separator>-<boundaryX1>-<boundaryX2>-<boundaryY>-<partial>: keys
#   keys:
#     label-type-x1-y1-x2-y2-halfable-labelsize-descname-descoff
#   partial:
#     0-type-x-y-size

def exportkeysystem(key_system):
        
    name = key_system["name"]
    params = str(key_system["parameters"]["keys"]) + "-" + str(key_system["parameters"]["LR_split"]) + "-" + key_system["parameters"]["separator"] + "-" + str(int(round(4*key_system["parameters"]["Bx"], 2))) + "-" + str(int(round(4*key_system["parameters"]["Mx"], 2))) + "-" + str(int(round(4*key_system["parameters"]["My"], 2))) + "-" + ("1" if "partial" in key_system["special"] else "0")
    keys = ""
    for keynum in range(key_system["parameters"]["keys"]):
        key = key_system[keynum]
        if keynum != 0:
            keys += " § "
            
        if key["type"] == "partial":
            keys += "0-partial-" + str(int(round(4*key["x"], 2))) + "-" + str(int(round(4*key["y"], 2))) + "-" + str(round(key["size"], 3))
        else:
            keys += key["label"] + "-" + key["type"] + "-" + str(int(round(4*key["x1"], 2))) + "-" + str(int(round(4*key["y1"], 2))) + "-" + str(int(round(4*key["x2"], 2))) + "-" + str(int(round(4*key["y2"], 2))) + "-" + ("1" if key["halfable"] else "0") + "-" + str(round(key["labelsize"], 3)) + "-" + key["descname"] + "-" + key["descoff"]

    no_comma_key_system = ""
    for char in "Custom — " + name + " — " + params + " — " + keys:
        no_comma_key_system += ("`" if char == "," else ("$" if char == "\"" else ("!" if char == "\n" else char)))

    return no_comma_key_system


def importkeysystem(no_comma_key_system_string):
    key_system_string = ""
    for char in no_comma_key_system_string:
        key_system_string += ("," if char == "`" else ("\"" if char == "$" else ("\n" if char == "!" else char)))
        
    params = key_system_string.split(" — ")[2].split("-")
      
    key_system = {
        "parameters": {"keys":int(params[0]), "LR_split":int(params[1]), "separator":params[2], "offsetx":2, "offsety":2, "shiftx":0, "shifty":0, "Lx":0, "Ly":0, "Mx":int(params[4])/4, "My":int(params[5])/4, "Bx":int(params[3])/4, "By":29, "Rx":74, "Ry":29, "Descy":33},
        "special": ["partial"] if params[6] == "1" else [],
        "name": key_system_string.split(" — ")[1]
    }

    if int(params[0]) != 0:
        keys = key_system_string.split(" — ")[3].split(" § ")
        for k, keystring in enumerate(keys):
            key = keystring.split("-")
            if key[1] == "partial":
                key_system[k] = {"x":int(key[2])/4, "y":int(key[3])/4, "type":"partial", "size":int(key[4]), "descname":" ", "descoff":" "}
            else:
                key_system[k] = {"x1":int(key[2])/4, "y1":int(key[3])/4, "x2":int(key[4])/4, "y2":int(key[5])/4, "type":key[1], "halfable":key[6]=="1", "label":key[0], "labelsize":float(key[7]), "descname":key[8], "descoff":key[9]}

    return key_system
    
    




# SIZE OF APPLICATION WINDOW
horizontalsize = 1536
verticalsize = 792

scale = min(horizontalsize/192, verticalsize/99)
textscale = 1

def onresize(event):
    global horizontalsize
    global verticalsize
    global scale
    
    if not (event.width == horizontalsize and event.height == verticalsize):

        horizontalsize = event.width
        verticalsize = event.height

        if event.widget is root:
            scale = min(horizontalsize/192, verticalsize/99)
            DESCRIPTION.place(x=15*scale, y=36*scale, width=60*scale, height=7*scale)
            create_description()
            create_dbasedesc()
            create_customname()
            render_version_info()
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)
            render_options(INSTRUMENT, DATABASE, SETINSTRUMENT, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
            render_filters(FILTERS, TET, SELECT, TEMPVAR)
            create_editkeys_textboxes()

if platform.system() == "Darwin": # On Mac, text size is shrunk
    textscale = 4/3

root = Tk()
C = Canvas(root)
C.pack(fill=BOTH, expand=1)
root.geometry(str(horizontalsize) + "x" + str(verticalsize))
root.title("WindFingerings "+version)
C.create_rectangle(0,0,horizontalsize*16,verticalsize*16, outline="#FFFFFF", fill="#FFFFFF", width=0)


# GLOBAL VARIABLES
INSTRUMENT = "Flute"
SELECT = ""

# FINGERING: main, half, trill, partial, description
FINGERING = [0, 0, 0, -0.5, complex(0), complex(0), ""]
FINGTYPE = "note"

PITCHES = [440.0]
TEMPVAR = ""

TONIC = 440.0
TET = 12
PAGE = 0
NUM_PAGES = 0
EDITKEYS_ROWSPACING = 7
EDITKEYS_TOPY = 27
EDITKEYS_PER_PAGE = 10
FILTERS = {
    "tolerance": 0.15,
    "fingtype": ["note", "trill", "multi"],
    "tet": "none",
    "search": "none"
}

# DATABASE
DATABASE = [["new-database.csv", INSTRUMENT, TONIC, TET, ""]]

SETINSTRUMENT = "not"

# TEXTBOXES
C.create_rectangle(2*scale, 35*scale, 76*scale, 44*scale, fill=colors["description_background"], width=0, tags="create_description")
C.create_text(8.5*scale, 39.5*scale, text="Description", font=("Arial", int(textscale*1.5*scale), "bold"), fill="#FFFFFF", tags="create_description")
DESCRIPTION = Text(root, fg="#FFFFFF", bg=colors["dark_description_background"], font=("Arial", int(scale * 1.25)))
DESCRIPTION.delete(1.0, END)
DESCRIPTION.insert(END, FINGERING[-1])

DBASEDESC = Text(root, fg="#FFFFFF", bg=colors["dark_options_background"], font=("Arial", int(scale * 1.5)))
DBASEDESC.delete(1.0, END)
DBASEDESC.insert(END, DATABASE[0][-1])

CUSTOMNAME = Text(root, fg="#FFFFFF", bg=colors["dark_options_background"], font=("Arial", int(scale * 1.5)))
CUSTOMNAME.delete(1.0, END)

EDITKEYS_TEXTBOXES = []
for i in range(EDITKEYS_PER_PAGE):
    EDITKEYS_TEXTBOXES.append([
        Text(root, fg="#FFFFFF", bg=colors["dark_custom_background"], font=("Arial", int(scale * 1.5))),
        Text(root, fg="#FFFFFF", bg=colors["dark_custom_background"], font=("Arial", int(scale * 1))),
        Text(root, fg="#FFFFFF", bg=colors["dark_custom_background"], font=("Arial", int(scale * 1)))
    ])

FILTERS_TEMP_FINGERING = list(FINGERING)
FILTERS_TEMP_PITCHES = list(PITCHES)
FILTERS_TEMP_FINGTYPE = FINGTYPE

# DESCRIPTION
def create_description():
    global scale
    global DESCRIPTION
    try:
        DESCRIPTION.place_forget()
    except Exception:
        pass
    C.delete("create_description")
    C.create_rectangle(2*scale, 35*scale, 76*scale, 44*scale, fill=colors["description_background"], width=0, tags="create_description")
    C.create_text(8.5*scale, 39.5*scale, text="Description", font=("Arial", int(textscale*1.5*scale), "bold"), fill="#FFFFFF", tags="create_description")

    DESCRIPTION = Text(root, fg="#FFFFFF", bg=colors["dark_description_background"], font=("Arial", int(scale * 5/4)))
    DESCRIPTION.place(x=15*scale, y=36*scale, width=60*scale, height=7*scale)
    DESCRIPTION.bind("<Button-1>", lambda x: onclick("textbox_description"))
    
# DATABASE DESC
def create_dbasedesc():
    global scale
    global DBASEDESC
    try:
        DBASEDESC.place_forget()
    except Exception:
        pass
    
    DBASEDESC = Text(root, fg="#FFFFFF", bg=colors["dark_options_background"], font=("Arial", int(scale * 3/2)))
    DBASEDESC.place(x=100*scale, y=13*scale, width=68*scale, height=5.5*scale)
    DBASEDESC.bind("<Button-1>", lambda x: onclick("textbox_dbasedesc"))

# CUSTOM INSTRUMENT NAME
def create_customname():
    global scale
    global CUSTOMNAME
    global SETINSTRUMENT
    try:
        CUSTOMNAME.place_forget(); DELIMITER.place_forget()
    except Exception:
        pass

    CUSTOMNAME = Text(root, fg="#FFFFFF", bg=colors["dark_options_background"], font=("Arial", int(scale * 7/6)))
    if SETINSTRUMENT == "edit":
        CUSTOMNAME.insert(END, key_systems["custom"]["name"])
        CUSTOMNAME.place(x=111*scale, y=8*scale, width=22.5*scale, height=4*scale)
        CUSTOMNAME.bind("<Button-1>", lambda x: onclick("textbox_customname"))

        

# EDITKEYS TEXTBOXES
def create_editkeys_textboxes():
    global scale
    global EDITKEYS_TEXTBOXES
    global EDITKEYS_ROWSPACING 
    global EDITKEYS_TOPY
    global EDITKEYS_PER_PAGE
    global PAGE
    for num, textbox in enumerate(EDITKEYS_TEXTBOXES):
        keynum = PAGE*EDITKEYS_PER_PAGE + num

        if SETINSTRUMENT != "edit" or (keynum >= key_systems["custom"]["parameters"]["keys"] - (1 if "partial" in key_systems["custom"]["special"] else 0)):
            textbox[0].place_forget(); textbox[1].place_forget(); textbox[2].place_forget()

        textbox[0].configure(font=("Arial", int(scale * 1.5)))
        textbox[1].configure(font=("Arial", int(scale * 1)))
        textbox[2].configure(font=("Arial", int(scale * 1)))
        
        if SETINSTRUMENT == "edit" and keynum < key_systems["custom"]["parameters"]["keys"] and key_systems["custom"][keynum]["type"] != "partial":
            textbox[0].place(x=84*scale, y=(EDITKEYS_TOPY + EDITKEYS_ROWSPACING*(num%EDITKEYS_PER_PAGE) + 0.5)*scale, width=5*scale, height=(EDITKEYS_ROWSPACING-1.9)*scale)
            textbox[0].delete(1.0, END)
            textbox[0].insert(END, key_systems["custom"][keynum]["label"])
            textbox[0].bind("<Button-1>", lambda x, k=keynum: onclick("textbox_editkeylabel_" + str(k)))

            textbox[1].place(x=97*scale, y=(EDITKEYS_TOPY + EDITKEYS_ROWSPACING*(num%EDITKEYS_PER_PAGE) + 0.5)*scale, width=3*scale, height=(EDITKEYS_ROWSPACING/2 - 1)*scale)
            textbox[1].delete(1.0, END)
            textbox[1].insert(END, key_systems["custom"][keynum]["descname"])
            textbox[1].bind("<Button-1>", lambda x, k=keynum: onclick("textbox_editkeydescname_" + str(k)))

            textbox[2].place(x=97*scale, y=(EDITKEYS_TOPY + EDITKEYS_ROWSPACING*(0.5 + num%EDITKEYS_PER_PAGE) - 0.4)*scale, width=3*scale, height=(EDITKEYS_ROWSPACING/2 - 1)*scale)
            textbox[2].delete(1.0, END)
            textbox[2].insert(END, key_systems["custom"][keynum]["descoff"])
            textbox[2].bind("<Button-1>", lambda x, k=keynum: onclick("textbox_editkeydescoff_" + str(k)))
    

def render_version_info():
    C.delete("render_version_info")

    C.create_rectangle(2*scale, 90*scale, 76*scale, 97*scale, fill="#000000", width=0, tags="render_version_info")
    C.create_text(39*scale, 92.5*scale, text="WindFingerings "+version, font=("Arial", int(textscale*scale*1.75), "bold"), fill="#FFFFFF", tags="render_version_info")
    C.create_text(39*scale, 95*scale, text="by Valky River", font=("Arial", int(textscale*scale*1.25), "bold"), fill="#FFFFFF", tags="render_version_info")

create_description()
create_dbasedesc()
create_customname()
create_editkeys_textboxes()
render_version_info()

try:
    C.clipboard_get()
except Exception:
    pass

# ON CLICK
def onclick(event):
    
    root.focus_set()

    global INSTRUMENT
    global FINGERING
    global SELECT
    global FINGTYPE
    global PITCHES
    global TEMPVAR
    global DATABASE
    global TONIC
    global TET
    global SETINSTRUMENT
    global PAGE
    global FILTERS
    global EDITKEYS_TEXTBOXES
    global EDITKEYS_ROWSPACING 
    global EDITKEYS_TOPY
    global EDITKEYS_PER_PAGE
    global FILTERS_TEMP_FINGERING
    global FILTERS_TEMP_PITCHES
    global FILTERS_TEMP_FINGTYPE

    if isinstance(event, Event):
        item = C.find_closest(event.x, event.y)
        tags = C.itemcget(item, "tags").split(" ")
    else:
        tags = event
        
    #print("tags", tags)
    #print("SELECT", SELECT)

    if "removeentry" in tags and "data" in SELECT and SETINSTRUMENT == "not":
        index = int(SELECT[4:])
        DATABASE.pop(index)
        SELECT = ""
        render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)

    if SELECT != "":
        if "fingeringhelp" in tags or "pitchhelp" in tags or "filtershelp" in tags or "editkeyshelp" in tags:
            pass
        elif "sposition" in SELECT:
            if "number" in SELECT:
                try:
                    temp_sposition = float(TEMPVAR)
                    if temp_sposition >= float(SELECT.split(" ")[1]) and temp_sposition <= float(SELECT.split(" ")[2]):
                        if FINGTYPE == "trill":
                            if temp_sposition <= FINGERING[int(SELECT[9])+3].imag:
                                FINGERING[int(SELECT[9])+3] = complex(temp_sposition, temp_sposition)
                            else:
                                FINGERING[int(SELECT[9])+3] = complex(temp_sposition, FINGERING[int(SELECT[9])+3].imag)
                        else:
                            FINGERING[int(SELECT[9])+3] = complex(temp_sposition, 0)
                except Exception:
                    pass
                TEMPVAR = ""
                SELECT = ""
                render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            elif "trillnum" in SELECT:
                try:
                    temp_sposition = float(TEMPVAR)
                    if temp_sposition >= float(SELECT.split(" ")[1]) and temp_sposition <= float(SELECT.split(" ")[2]):
                        if FINGTYPE == "trill":
                            if temp_sposition >= FINGERING[int(SELECT[9])+3].real:
                                FINGERING[int(SELECT[9])+3] = complex(temp_sposition, temp_sposition)
                            else:
                                FINGERING[int(SELECT[9])+3] = complex(FINGERING[int(SELECT[9])+3].real, temp_sposition)
                        else:
                            FINGERING[int(SELECT[9])+3] = complex(temp_sposition, 0)
                except Exception:
                    pass
                TEMPVAR = ""
                SELECT = ""
                render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
                
        elif "data" in SELECT:
            if "filters" in tags:
                pass
            else:
                SELECT = ""
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
            
        elif "tolerance" in SELECT:
            if SELECT == "tolerance_percent":
                try:
                    tolerance = float(TEMPVAR)/100
                    if tolerance >= 0 and tolerance <= 0.5:
                        FILTERS["tolerance"] = tolerance
                except Exception:
                    pass
            elif SELECT == "tolerance_cents":
                try:
                    tolerance = float(TEMPVAR)/(1200/TET)
                    if tolerance >= 0 and tolerance <= 0.5:
                        FILTERS["tolerance"] = tolerance
                except Exception:
                    pass
            SELECT = ""
            TEMPVAR = ""
            render_filters(FILTERS, TET, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)

        elif "edittrans" in SELECT:
            if SELECT == "edittranspose":
                try:
                    transpose = float(TEMPVAR)/100
                    if abs(transpose) <= 96:
                        instruments["Custom"][1] = transpose
                except Exception:
                    pass
            elif SELECT == "edittranssteps":
                try:
                    transpose = float(TEMPVAR) * 12/TET
                    if abs(transpose) <= 96:
                        instruments["Custom"][1] = transpose
                except Exception:
                    pass
            SELECT = ""
            TEMPVAR = ""
            render_options(INSTRUMENT, DATABASE, SETINSTRUMENT, SELECT, TEMPVAR)

        elif "editlrsplit" in SELECT:
            try:
                LR_split = int(TEMPVAR)
                if LR_split >= 0 and LR_split <= key_systems["custom"]["parameters"]["keys"]:
                    key_systems["custom"]["parameters"]["LR_split"] = LR_split
            except Exception:
                pass
            SELECT = ""
            TEMPVAR = ""
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
            create_editkeys_textboxes()

        elif SELECT in ["editmidx1", "editmidx2", "editmidy"]:
            try:
                if SELECT == "editmidx1" and int(round(2*float(TEMPVAR), 0))/2 >= 0 and int(round(2*float(TEMPVAR), 0))/2 <= 74*4:
                    key_systems["custom"]["parameters"]["Bx"] = int(round(2*float(TEMPVAR), 0))/8
                elif SELECT == "editmidx2" and int(round(2*float(TEMPVAR), 0))/2 >= 0 and int(round(2*float(TEMPVAR), 0))/2 <= 74*4:
                    key_systems["custom"]["parameters"]["Mx"] = int(round(2*float(TEMPVAR), 0))/8
                elif SELECT == "editmidy" and int(round(2*float(TEMPVAR), 0))/2 >= 0 and int(round(2*float(TEMPVAR), 0))/2 <= 29*4:
                    key_systems["custom"]["parameters"]["My"] = int(round(2*float(TEMPVAR), 0))/8

                if key_systems["custom"]["parameters"]["Mx"] >= key_systems["custom"]["parameters"]["Bx"]:
                    key_systems["custom"]["parameters"]["Lx"] = 0
                    key_systems["custom"]["parameters"]["Ly"] = 0
                    key_systems["custom"]["parameters"]["Rx"] = 74
                    key_systems["custom"]["parameters"]["Ry"] = 29
                    key_systems["custom"]["parameters"]["By"] = 29
                else:
                    key_systems["custom"]["parameters"]["Lx"] = 0
                    key_systems["custom"]["parameters"]["Ly"] = 29
                    key_systems["custom"]["parameters"]["Rx"] = 74
                    key_systems["custom"]["parameters"]["Ry"] = 0
                    key_systems["custom"]["parameters"]["By"] = 0
                    
            except Exception:
                pass
            SELECT = ""
            TEMPVAR = ""
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
            

        elif "editkeylabel" in SELECT or "editkeydescname" in SELECT or "editkeydescoff" in SELECT:
            keynum = int(SELECT[13 if "editkeylabel" in SELECT else (16 if "editkeydescname" in SELECT else 15):])
            LR_split = key_systems["custom"]["parameters"]["LR_split"]
            
            label = ""
            
            n = 0 if "editkeylabel" in SELECT else (1 if "editkeydescname" in SELECT else 2)
                
            for character in EDITKEYS_TEXTBOXES[keynum % EDITKEYS_PER_PAGE][n].get("1.0", "end-1c"): # label cannot contain -, §, or —, as these are delimiters
                if n >= 1 and (character == "!" or character == "\n"):
                    label += ""
                elif character == "-" or character == "—":
                    label += "−"
                elif character == "§":
                    label += "S"
                elif character == "!":
                    label += "\n"
                elif character == "`":
                    label += ","
                elif character == "$":
                    label += "\""
                else:
                    label += character

            if "editkeylabel" in SELECT: 
                key_systems["custom"][keynum]["label"] = label
                rerender = True

                # give default values for descname and descoff
                if "½" in label:
                    key_systems["custom"][keynum]["descoff"] = ""
                    key_systems["custom"][keynum]["descname"] = "⌫h"
                else:
                    key_systems["custom"][keynum]["descoff"] = "−" if key_systems["custom"][keynum]["type"] == "main" else ""

                    searchkeys = range(LR_split, key_systems["custom"]["parameters"]["keys"]) if keynum >= LR_split else range(LR_split)
                    mains = []
                    for k in searchkeys:
                        if key_systems["custom"][k]["type"] == "main":
                            mains.append(k)

                    if keynum < mains[0]:
                        key_systems["custom"][keynum]["descname"] = label + " "
                    elif keynum > mains[-1]:
                        key_systems["custom"][keynum]["descname"] = " " + label
                    else:
                        key_systems["custom"][keynum]["descname"] = label
                    
            elif "editkeydescname" in SELECT:
                key_systems["custom"][keynum]["descname"] = label
            elif "editkeydescoff" in SELECT:
                key_systems["custom"][keynum]["descoff"] = label
                
            SELECT = ""
            TEMPVAR = ""
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
            create_editkeys_textboxes()

        elif "labelsize" in SELECT or "xpos" in SELECT or "ypos" in SELECT or "width" in SELECT or "hight" in SELECT or "partialssize" in SELECT or "partialsx" in SELECT or "partialsy" in SELECT:
            
            if "labelsize" in SELECT:
                try:
                    temp_labelsize = round(float(TEMPVAR), 8)
                    if temp_labelsize >= 1/2 and temp_labelsize <= 5/2:
                        key_systems["custom"][int(SELECT[9:])]["labelsize"] = temp_labelsize
                except Exception:
                    pass
            elif "xpos" in SELECT:
                try:
                    key = key_systems["custom"][int(SELECT[4:])]
                    x1 = round(int(round(2*float(TEMPVAR), 0))/8, 8) - (key["x2"]-key["x1"])/2
                    x2 = round(int(round(2*float(TEMPVAR), 0))/8, 8) + (key["x2"]-key["x1"])/2
                    if x1 >= 0 and x2 <= 74:
                        key_systems["custom"][int(SELECT[4:])]["x1"] = x1
                        key_systems["custom"][int(SELECT[4:])]["x2"] = x2
                except Exception:
                    pass
            elif "ypos" in SELECT:
                try:
                    key = key_systems["custom"][int(SELECT[4:])]
                    y1 = round(int(round(2*float(TEMPVAR), 0))/8, 8) - (key["y2"]-key["y1"])/2
                    y2 = round(int(round(2*float(TEMPVAR), 0))/8, 8) + (key["y2"]-key["y1"])/2
                    if y1 >= 0 and y2 <= 29:
                        key_systems["custom"][int(SELECT[4:])]["y1"] = y1
                        key_systems["custom"][int(SELECT[4:])]["y2"] = y2
                except Exception:
                    pass
            elif "width" in SELECT:
                try:
                    key = key_systems["custom"][int(SELECT[5:])]
                    x1 = (key["x2"]+key["x1"])/2 - round(int(TEMPVAR)/8, 8)
                    x2 = (key["x2"]+key["x1"])/2 + round(int(TEMPVAR)/8, 8)
                    if x1 >= 0 and x2 <= 74:
                        key_systems["custom"][int(SELECT[5:])]["x1"] = x1
                        key_systems["custom"][int(SELECT[5:])]["x2"] = x2
                except Exception:
                    pass
            elif "hight" in SELECT:
                try:
                    key = key_systems["custom"][int(SELECT[5:])]
                    y1 = (key["y2"]+key["y1"])/2 - round(int(TEMPVAR)/8, 8)
                    y2 = (key["y2"]+key["y1"])/2 + round(int(TEMPVAR)/8, 8)
                    if y1 >= 0 and y2 <= 29:
                        key_systems["custom"][int(SELECT[5:])]["y1"] = y1
                        key_systems["custom"][int(SELECT[5:])]["y2"] = y2
                except Exception:
                    pass

            elif "partialssize" in SELECT:
                try:
                    temp_partialssize = float(TEMPVAR)
                    x1 = key_systems["custom"][int(SELECT[12:])]["x"] - temp_partialssize*16
                    x2 = key_systems["custom"][int(SELECT[12:])]["x"] + temp_partialssize*16
                    y1 = key_systems["custom"][int(SELECT[12:])]["y"] - temp_partialssize*10
                    y2 = key_systems["custom"][int(SELECT[12:])]["y"] + temp_partialssize*10
                    if temp_partialssize >= 0.5 and temp_partialssize <= 1 and x1 >= 0 and x2 <= 74 and y1 >= 0 and y2 <= 29:
                        key_systems["custom"][int(SELECT[12:])]["size"] = temp_partialssize
                except Exception:
                    pass

            elif "partialsx" in SELECT:
                try:
                    x1 = round(int(round(2*float(TEMPVAR), 0)))/8 - key_systems["custom"][int(SELECT[9:])]["size"]*16
                    x2 = round(int(round(2*float(TEMPVAR), 0)))/8 + key_systems["custom"][int(SELECT[9:])]["size"]*16
                    if x1 >= 0 and x2 <= 74:
                        key_systems["custom"][int(SELECT[9:])]["x"] = round(int(round(2*float(TEMPVAR), 0))/8, 8)
                except Exception:
                    pass

            elif "partialsy" in SELECT:
                try:
                    y1 = round(int(round(2*float(TEMPVAR), 0)))/8 - key_systems["custom"][int(SELECT[9:])]["size"]*10
                    y2 = round(int(round(2*float(TEMPVAR), 0)))/8 + key_systems["custom"][int(SELECT[9:])]["size"]*10
                    if y1 >= 0 and y2 <= 29:
                        key_systems["custom"][int(SELECT[9:])]["y"] = round(int(round(2*float(TEMPVAR), 0))/8, 8)
                except Exception:
                    pass

            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
                
            SELECT = ""
            TEMPVAR = ""
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
            
                  
        else:
            if SELECT == "tet":
                try:
                    temp_tet = int(TEMPVAR)
                    if temp_tet >= 1 and temp_tet <= 342:
                        TET = temp_tet
                        DATABASE[0][3] = TET
                        render_filters(FILTERS, TET, SELECT, TEMPVAR)
                except Exception:
                    pass
            elif SELECT == "description":
                FINGERING[-1] = DESCRIPTION.get("1.0", "end-1c")
            elif SELECT == "dbasedesc":
                DATABASE[0][-1] = DBASEDESC.get("1.0", "end-1c")
            elif SELECT == "customname" and INSTRUMENT == "Custom":
                key_systems["custom"]["name"] = CUSTOMNAME.get("1.0", "end-1c")
            elif SELECT[:-1] == "freq":
                try:
                    temp_pitch = float(TEMPVAR)
                    if temp_pitch >= (55/8) * 2**(5/24) and temp_pitch <= 14080 / 2**(1/8):
                        if SELECT[-1] == "0":
                            TONIC = temp_pitch
                            DATABASE[0][2] = temp_pitch
                        else:
                            PITCHES[int(SELECT[-1])-1] = temp_pitch
                except Exception:
                    pass
            elif SELECT[:-1] == "notename":
                if SELECT[-1] == "0":
                    temp_pitch = notetofreq(TEMPVAR, instruments[INSTRUMENT][1]) * 2**(notename(DATABASE[0][2], instruments[INSTRUMENT][1])[1]/1200)
                else:
                    temp_pitch = notetofreq(TEMPVAR, instruments[INSTRUMENT][1]) * 2**(notename(PITCHES[int(SELECT[-1])-1], instruments[INSTRUMENT][1])[1]/1200)
                if temp_pitch:
                    if temp_pitch >= (55/8) * 2**(5/24) and temp_pitch <= 14080 / 2**(1/8):
                        if SELECT[-1] == "0":
                            TONIC = temp_pitch
                            DATABASE[0][2] = temp_pitch
                        else:
                            PITCHES[int(SELECT[-1])-1] = temp_pitch
            elif SELECT[:-1] == "centsdev":
                try:
                    if SELECT[-1] == "0":
                        temp_pitch = DATABASE[0][2] * 2**((float(TEMPVAR)-notename(DATABASE[0][2], instruments[INSTRUMENT][1])[1])/1200)
                    else:
                        temp_pitch = PITCHES[int(SELECT[-1])-1] * 2**((float(TEMPVAR)-notename(PITCHES[int(SELECT[-1])-1], instruments[INSTRUMENT][1])[1])/1200)
                    if temp_pitch >= (55/8) * 2**(5/24) and temp_pitch <= 14080 / 2**(1/8):
                        if SELECT[-1] == "0":
                            TONIC = temp_pitch
                            DATABASE[0][2] = temp_pitch
                        else:
                            PITCHES[int(SELECT[-1])-1] = temp_pitch
                except Exception:
                    pass
            elif SELECT[:-1] == "concertname":
                if SELECT[-1] == "0":
                    temp_pitch = notetofreq(TEMPVAR, 0) * 2**(notename(DATABASE[0][2], 0)[1]/1200)
                else:
                    temp_pitch = notetofreq(TEMPVAR, 0) * 2**(notename(PITCHES[int(SELECT[-1])-1], 0)[1]/1200)
                if temp_pitch:
                    if temp_pitch >= (55/8) * 2**(5/24) and temp_pitch <= 14080 / 2**(1/8):
                        if SELECT[-1] == "0":
                            TONIC = temp_pitch
                            DATABASE[0][2] = temp_pitch
                        else:
                            PITCHES[int(SELECT[-1])-1] = temp_pitch
            elif SELECT[:-1] == "concertdev":
                try:
                    if SELECT[-1] == "0":
                        temp_pitch = DATABASE[0][2] * 2**((float(TEMPVAR)-notename(DATABASE[0][2], 0)[1])/1200)
                    else:
                        temp_pitch = PITCHES[int(SELECT[-1])-1] * 2**((float(TEMPVAR)-notename(PITCHES[int(SELECT[-1])-1], 0)[1])/1200)
                    if temp_pitch >= (55/8) * 2**(5/24) and temp_pitch <= 14080 / 2**(1/8):
                        if SELECT[-1] == "0":
                            TONIC = temp_pitch
                            DATABASE[0][2] = temp_pitch
                        else:
                            PITCHES[int(SELECT[-1])-1] = temp_pitch
                except Exception:
                    pass
            TEMPVAR = ""
            SELECT = ""
            render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
            if SETINSTRUMENT == "edit":
                render_options(INSTRUMENT, DATABASE, SETINSTRUMENT, SELECT, TEMPVAR)
        
    if "clickable" in tags:

        # HELP
        if "fingeringhelp" in tags:
            fingering_help()
        elif "pitchhelp" in tags:
            pitch_help()
        elif "filtershelp" in tags:
            filters_help()
        elif "editkeyshelp" in tags:
            editkeys_help()

        # EDITKEYS
        elif "editkey" in tags[2]: 
            if "addkey" in tags and tags[2] == "editkeys":
                if "partial" in key_systems["custom"]["special"]:
                    key_systems["custom"][key_systems["custom"]["parameters"]["keys"]] = key_systems["custom"][key_systems["custom"]["parameters"]["keys"] - 1].copy()
                    key_systems["custom"][key_systems["custom"]["parameters"]["keys"] - 1] = {
                        "x1":33.5, "y1":11, "x2":40.5, "y2":18, "type":"main", "halfable":False, "label":"", "labelsize":1, "descname":"", "descoff":""}
                    key_systems["custom"]["parameters"]["keys"] += 1
                else:
                    key_systems["custom"][key_systems["custom"]["parameters"]["keys"]] = {
                        "x1":33.5, "y1":11, "x2":40.5, "y2":18, "type":"main", "halfable":False, "label":"", "labelsize":1, "descname":"", "descoff":""}
                    key_systems["custom"]["parameters"]["keys"] += 1
            elif "addkey" in tags:
                keynum = int(tags[2][7:])
                for k in list(range(keynum, key_systems["custom"]["parameters"]["keys"]))[::-1]:
                    key_systems["custom"][k+1] = key_systems["custom"][k].copy()
                key_systems["custom"][keynum] = {"x1":33.5, "y1":11, "x2":40.5, "y2":18, "type":"main", "halfable":False, "label":"", "labelsize":1, "descname":"", "descoff":""}
                key_systems["custom"]["parameters"]["keys"] += 1
                if keynum < key_systems["custom"]["parameters"]["LR_split"]:
                    key_systems["custom"]["parameters"]["LR_split"] += 1
            elif "removekey" in tags:
                keynum = int(tags[2][7:])
                if keynum % EDITKEYS_PER_PAGE == 0 and PAGE != 0 and key_systems["custom"]["parameters"]["keys"] % EDITKEYS_PER_PAGE == 1:
                    PAGE -= 1
                for k in range(keynum + 1, key_systems["custom"]["parameters"]["keys"]):
                    key_systems["custom"][k-1] = key_systems["custom"][k].copy()
                del key_systems["custom"][key_systems["custom"]["parameters"]["keys"] - 1]
                key_systems["custom"]["parameters"]["keys"] -= 1
                if keynum < key_systems["custom"]["parameters"]["LR_split"]:
                    key_systems["custom"]["parameters"]["LR_split"] -= 1
                
            elif "upkey" in tags:
                keynum = int(tags[2][7:])
                if keynum >= 1:
                    temp_key = key_systems["custom"][keynum].copy()
                    key_systems["custom"][keynum] = key_systems["custom"][keynum-1].copy()
                    key_systems["custom"][keynum-1] = temp_key
            elif "downkey" in tags:
                keynum = int(tags[2][7:])
                if keynum <= key_systems["custom"]["parameters"]["keys"] - 3 or (keynum <= key_systems["custom"]["parameters"]["keys"] - 2 and "partial" not in key_systems["custom"]["special"]):
                    temp_key = key_systems["custom"][keynum].copy()
                    key_systems["custom"][keynum] = key_systems["custom"][keynum+1].copy()
                    key_systems["custom"][keynum+1] = temp_key

            if "partial" in key_systems["custom"]["special"]:
                FINGERING = [0, 0, 0, 1, complex(0), complex(0), ""]
            else:
                FINGERING = [0, 0, 0, -0.5, complex(0), complex(0), ""]

            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
            create_editkeys_textboxes()

        elif tags[2] in ["separatoron", "separatoroff", "partialson", "partialsoff"]:
            if tags[2] == "separatoron":
                key_systems["custom"]["parameters"]["separator"] = " | "
            elif tags[2] == "separatoroff":
                key_systems["custom"]["parameters"]["separator"] = ""
            elif tags[2] == "partialson" and "partial" not in key_systems["custom"]["special"]:
                key_systems["custom"]["special"].append("partial")
                key_systems["custom"][key_systems["custom"]["parameters"]["keys"]] = {"x":55.5, "y":14, "type":"partial", "size":1, "descname":" ", "descoff":" "}
                key_systems["custom"]["parameters"]["keys"] += 1
            elif tags[2] == "partialsoff" and "partial" in key_systems["custom"]["special"]:
                if PAGE*EDITKEYS_PER_PAGE + 1 == key_systems["custom"]["parameters"]["keys"] and PAGE != 0:
                    PAGE -= 1
                key_systems["custom"]["special"].remove("partial")
                del key_systems["custom"][key_systems["custom"]["parameters"]["keys"] - 1]
                key_systems["custom"]["parameters"]["keys"] -= 1

            if "partial" in key_systems["custom"]["special"]:
                FINGERING = [0, 0, 0, 1, complex(0), complex(0), ""]
            else:
                FINGERING = [0, 0, 0, -0.5, complex(0), complex(0), ""]
                
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
            create_editkeys_textboxes()

        elif "setkeytype" in tags[2]:
            key_systems["custom"][int(tags[2][10:])]["type"] = ["main", "octave", "second", "low", "high", "trill", "model", "special"][int(tags[3])]
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)

        elif "halfableon" in tags[2]:
            key_systems["custom"][int(tags[2][10:])]["halfable"] = True
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)

        elif "halfableoff" in tags[2]:
            key_systems["custom"][int(tags[2][11:])]["halfable"] = False
            if "partial" in key_systems["custom"]["special"]:
                FINGERING = [0, 0, 0, 1, complex(0), complex(0), ""]
            else:
                FINGERING = [0, 0, 0, -0.5, complex(0), complex(0), ""]
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
            
        
        elif "key" in tags: # set new fingering
            temp_fingering = ((2**int(tags[2])) ^ FINGERING[0]) | FINGERING[1]
            temp_half = FINGERING[0] & FINGERING[1] & ~(2**int(tags[2]))
            temp_trill = FINGERING[2] & ~(2**int(tags[2]))
            FINGERING[0] = temp_fingering; FINGERING[1] = temp_half; FINGERING[2] = temp_trill
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            
        elif "partial" in tags: # set new partial
            FINGERING[3] = int(tags[2])
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            
        elif "fingtype" in tags: # set new fingtype
            if (tags[2] != "multi" or "multi" not in FINGTYPE) and (tags[2] != FINGTYPE):
                prev_fingtype = FINGTYPE
                FINGTYPE = ("multi2" if tags[2] == "multi" else tags[2])
                if fingtypes[FINGTYPE] > fingtypes[prev_fingtype]:
                    while len(PITCHES) < fingtypes[FINGTYPE]:
                        PITCHES.append(PITCHES[0])
                elif fingtypes[FINGTYPE] < fingtypes[prev_fingtype]:
                    PITCHES = sorted(PITCHES[:fingtypes[FINGTYPE]])
                if prev_fingtype == "trill" and FINGTYPE != "trill":
                    FINGERING[2] = 0
                    if FINGERING[3] <= -1:
                        FINGERING[3] = -FINGERING[3] - 1
                    FINGERING[4] = complex(FINGERING[4].real, 0)
                    FINGERING[5] = complex(FINGERING[5].real, 0)
                elif FINGTYPE == "trill":
                    FINGERING[4] = complex(FINGERING[4].real, FINGERING[4].real)
                    FINGERING[5] = complex(FINGERING[5].real, FINGERING[5].real)
                render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)
                render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
                
        elif "pitch" in tags:
            if tags[2] == "tet":
                SELECT = tags[2]
                TEMPVAR = ""
                render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)
            elif tags[2][:-1] in ["freq", "notename", "centsdev", "concertname", "concertdev"]:
                SELECT = tags[2]
                TEMPVAR = ""
                render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)

        # SPOSITIONS
        elif "sposition" in tags[2] and ("number" in tags[2] or "trillnum" in tags[2]):
            SELECT = tags[2] + " " + tags[3] + " " + tags[4]
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)

        elif "sposition" in tags[2] and ("setto" in tags[2]):
            new_pos = float(tags[3])
            if new_pos <= FINGERING[int(tags[1][-1])+3].imag:     
                FINGERING[int(tags[1][-1])+3] = complex(new_pos, new_pos)
            else:
                FINGERING[int(tags[1][-1])+3] = complex(new_pos, FINGERING[int(tags[1][-1])+3].imag)
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)

        elif "sposition" in tags[1]:
            new_pos = (event.x - float(tags[3])) / ((float(tags[4])-float(tags[3]))/(float(tags[6])-float(tags[5]))) + float(tags[5])
            if "trill" in tags[2]:
                FINGERING[int(tags[1][-1])+3] = complex(new_pos, new_pos)
            else:
                FINGERING[int(tags[1][-1])+3] = complex(new_pos, FINGERING[int(tags[1][-1])+3].imag)
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)


        # OPTIONS
        elif "setinstrument" in tags:
            instrument = ""
            for letter in tags[2]:
                if letter == "_":
                    instrument += " "
                else:
                    instrument += letter

            INSTRUMENT = instrument
            if "partial" in key_systems["custom"]["special"]:
                FINGERING = [0, 0, 0, 1, complex(0), complex(0), ""]
            else:
                FINGERING = [0, 0, 0, -0.5, complex(0), complex(0), ""]
            if "trombone" in key_systems[instruments[instrument][0]]["special"]:
                if FINGTYPE == "trill":
                    FINGERING += [complex(1, 1), complex(0)]
                else:
                    FINGERING += [complex(1), complex(0)]
            else:
                FINGERING += [complex(0), complex(0)]
            FINGERING.append("")
            
            FILTERS["search"] = "none"
            DATABASE = list([["new-database.csv", INSTRUMENT, TONIC, TET, ""]])

            if "Custom" in instrument:
                SETINSTRUMENT = "edit"
                create_customname()
            else:
                SETINSTRUMENT = "not"
                
            FILTERS_TEMP_FINGERING = list(FINGERING)
            FILTERS_TEMP_PITCHES = list(PITCHES)
            FILTERS_TEMP_FINGTYPE = FINGTYPE
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)
            render_filters(FILTERS, TET, SELECT, TEMPVAR)
            render_options(INSTRUMENT, DATABASE, SETINSTRUMENT, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
            create_editkeys_textboxes()

        elif "selectinstrument" in tags:
            SETINSTRUMENT = "set"
            render_options(INSTRUMENT, DATABASE, SETINSTRUMENT, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
   
        elif "cancelsetinstrument" in tags or "confirminstrument" in tags:
            SETINSTRUMENT = "not"
            PAGE = 0
            create_customname()
            render_options(INSTRUMENT, DATABASE, SETINSTRUMENT, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
            create_editkeys_textboxes()

        elif "addentry" in tags and SETINSTRUMENT == "not":
            added = addentry((list(PITCHES), list(FINGERING), FINGTYPE), DATABASE)
            DATABASE = added[1]
            SELECT = "data"+str(added[0])
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)

        elif "savefile" in tags:
            file = fd.asksaveasfilename(
                title="Save file as .csv",
                defaultextension=".csv",
                filetypes=(("Comma-Separated Values File", "*.csv"), ("WindFingerings Collection", "*.wfc"), ("All files", "*.*"))
            )
            if file:
                DATABASE[0][0] = file.split("/")[-1]
                DATABASE[0][-1] = DBASEDESC.get("1.0", "end-1c")
                try:
                    with open(file, "w", encoding="utf-8-sig") as f:
                        f.write(exportfile(DATABASE))
                    render_options(INSTRUMENT, DATABASE, SETINSTRUMENT, SELECT, TEMPVAR)
                except Exception as e:
                    E = Toplevel(C)
                    E.geometry("800x50")
                    E.title("Error saving file")
                    Label(E, text="Error saving file: "+str(e), font=("Arial", 12, "bold")).place(x=10, y=10)
                    

        elif "loadfile" in tags:
            file = fd.askopenfilename(
                title="Select .csv file",
                filetypes=(("Comma-Separated Values File", "*.csv"), ("WindFingerings Collection", "*.wfc"), ("All files", "*.*"))
            )
            if file:
                try:
                    with open(file, "r", encoding="utf-8-sig") as f:
                        filecontent = importfile(f.read().strip().split("\n"))
                        DATABASE = filecontent[0]
                    PAGE = 0

                    if "Custom" in DATABASE[0][1]:
                        INSTRUMENT = "Custom"
                        instruments["Custom"][1] = filecontent[1] / 100
                        key_systems["custom"] = filecontent[2]
                    else:
                        INSTRUMENT = DATABASE[0][1]

                    TONIC = DATABASE[0][2]
                    TET = DATABASE[0][3]
                    FILTERS["search"] = "none"
                    if "partial" in key_systems[instruments[INSTRUMENT][0]]["special"]:
                        FINGERING = [0, 0, 0, 1]
                    else:
                        FINGERING = [0, 0, 0, -0.5]
                    if "trombone" in key_systems[instruments[INSTRUMENT][0]]["special"]:
                        if FINGTYPE == "trill":
                            FINGERING += [complex(1, 1), complex(0)]
                        else:
                            FINGERING += [complex(1), complex(0)]
                    else:
                        FINGERING += [complex(0), complex(0)]
                    FINGERING.append("")
                    FILTERS_TEMP_FINGERING = list(FINGERING)
                    FILTERS_TEMP_PITCHES = list(PITCHES)
                    FILTERS_TEMP_FINGTYPE = FINGTYPE
                    SETINSTRUMENT = "not"
                    create_customname()
                    render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
                    render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)
                    render_filters(FILTERS, TET, SELECT, TEMPVAR)
                    render_options(INSTRUMENT, DATABASE, SETINSTRUMENT, SELECT, TEMPVAR)
                    render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
                    create_editkeys_textboxes()
                except Exception as e:
                    E = Toplevel(C)
                    E.geometry("800x50")
                    E.title("Error loading file")
                    Label(E, text="Error loading file: "+str(e), font=("Arial", 12, "bold")).place(x=10, y=10)

        elif "copytoclipboard" in tags:
            C.clipboard_clear()
            C.clipboard_append(copytoclipboard(sorted(PITCHES), FINGERING, FINGTYPE))

        elif "pastefromclipboard" in tags:
            try:
                imported_fingering = pastefromclipboard(C.clipboard_get())
                PITCHES = list(imported_fingering[0])
                FINGERING = list(imported_fingering[1])
                FINGTYPE = imported_fingering[2]
                render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
                render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)
            except Exception as e:
                E = Toplevel(C)
                E.geometry("800x50")
                E.title("Error loading from clipboard")
                Label(E, text="Error loading from clipboard: "+str(e), font=("Arial", 12, "bold")).place(x=10, y=10)

        # DATABASE — each entry is in the form (pitches, fingering, fingtype)
        elif "prevpage" in tags and NUM_PAGES != 0:
            PAGE = (PAGE - 1) % NUM_PAGES
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
            if SETINSTRUMENT == "edit":
                create_editkeys_textboxes()
        elif "nextpage" in tags and NUM_PAGES != 0:
            PAGE = (PAGE + 1) % NUM_PAGES 
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
            if SETINSTRUMENT == "edit":
                create_editkeys_textboxes()
            
        elif "prevpage2" in tags and NUM_PAGES != 0:
            PAGE = NUM_PAGES - 1 if PAGE == 0 else max(0, PAGE - 10) % NUM_PAGES
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
        elif "nextpage2" in tags and NUM_PAGES != 0:
            PAGE = 0 if PAGE == NUM_PAGES - 1 else min(PAGE + 10, NUM_PAGES - 1) % NUM_PAGES 
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)

        elif "entry" in tags:
            SELECT = tags[2]
            PITCHES = sorted(list(DATABASE[int(tags[2][4:])][0]))
            FINGERING = list(DATABASE[int(tags[2][4:])][1])
            FINGTYPE = DATABASE[int(tags[2][4:])][2]
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)

        # FILTERS
        elif "filters" in tags:
            if tags[2] == "fingtypef":
                if tags[3] in FILTERS["fingtype"]:
                    FILTERS["fingtype"].remove(tags[3])
                else:
                    FILTERS["fingtype"].append(tags[3])
            else:
                FILTERS[tags[2][:-1]] = tags[3]
                
            if "search" in tags[2]:
                FILTERS_TEMP_FINGERING = list(FINGERING)
                FILTERS_TEMP_PITCHES = list(PITCHES)
                FILTERS_TEMP_FINGTYPE = FINGTYPE
                
            render_filters(FILTERS, TET, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)

        elif "clearsearch" in tags:
            FILTERS["search"] = "none"
            FILTERS_TEMP_FINGERING = list(FINGERING)
            FILTERS_TEMP_PITCHES = list(PITCHES)
            FILTERS_TEMP_FINGTYPE = FINGTYPE
            render_filters(FILTERS, TET, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)

        elif "tolerance" in tags:
            SELECT = "tolerance_" + tags[2]
            render_filters(FILTERS, TET, SELECT, TEMPVAR)

        elif tags[2] in ["edittranspose", "edittranssteps", "editlrsplit", "editmidx1", "editmidx2", "editmidy"]:
            SELECT = tags[2]
            render_options(INSTRUMENT, DATABASE, SETINSTRUMENT, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)

        elif "labelsize" in tags[2] or "xpos" in tags[2] or "ypos" in tags[2] or "width" in tags[2] or "hight" in tags[2] or "partialssize" in tags[2] or "partialsx" in tags[2] or "partialsy" in tags[2]:
            SELECT = tags[2]
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
      
    elif "textbox" in tags:
        SELECT = tags[8:]

# MIDDLE CLICK
def middleclick(event):

    global INSTRUMENT
    global FINGERING
    
    item = C.find_closest(event.x, event.y)
    tags = C.itemcget(item, "tags").split(" ")

    if "clickable" in tags:

        if FINGTYPE == "trill":
            if "key" in tags:
                temp_fingering = FINGERING[0] & ~(2**int(tags[2]))
                temp_half = FINGERING[1] & ~(2**int(tags[2]))
                temp_trill = FINGERING[2] ^ (2**int(tags[2]))
                FINGERING[0] = temp_fingering; FINGERING[1] = temp_half; FINGERING[2] = temp_trill
                render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            elif "partial" in tags:
                FINGERING[3] = -int(tags[2])-1
                render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)

            elif "sposition" in tags[2] and ("setto" in tags[2]):
                new_pos = float(tags[3])
                if new_pos >= FINGERING[int(tags[1][-1])+3].real:
                    FINGERING[int(tags[1][-1])+3] = complex(new_pos, new_pos)
                else:
                    FINGERING[int(tags[1][-1])+3] = complex(FINGERING[int(tags[1][-1])+3].real, new_pos)
                render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
                
            elif "sposition" in tags[1]:
                new_pos = (event.x - float(tags[3])) / ((float(tags[4])-float(tags[3]))/(float(tags[6])-float(tags[5]))) + float(tags[5])
                if "left" in tags[2] or "trill" in tags[2]:
                    FINGERING[int(tags[1][-1])+3] = complex(FINGERING[int(tags[1][-1])+3].real, new_pos)
                else:
                    FINGERING[int(tags[1][-1])+3] = complex(new_pos, new_pos)
                render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
                    
# RIGHT CLICK
def rightclick(event):

    global INSTRUMENT
    global FINGERING

    item = C.find_closest(event.x, event.y)
    tags = C.itemcget(item, "tags").split(" ")
    
    if "clickable" in tags:
            
        if "key" in tags and "halfable" in tags:
            temp_fingering = ((2**int(tags[2])) ^ FINGERING[0]) | (FINGERING[0] ^ FINGERING[1])
            temp_half = FINGERING[1] ^ (2**int(tags[2]))
            temp_trill = FINGERING[2] & ~(2**int(tags[2]))
            FINGERING[0] = temp_fingering; FINGERING[1] = temp_half; FINGERING[2] = temp_trill
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)

# WHEN KEY PRESSED
def onkey(event):

    global INSTRUMENT
    global FINGERING
    global SETINSTRUMENT
    global SELECT
    global FINGTYPE
    global PITCHES
    global TEMPVAR
    global DATABASE
    global TONIC
    global TET
    
    if event.keysym != "??":
        pressed = event.keysym.lower()
        if pressed in key_replacements.keys():
            pressed = key_replacements[pressed]
    else:
        pressed = ""

    # PITCH OR TET INPUT
    if SELECT in ["editmidx1", "editmidx2", "editmidy"] and pressed in ["up", "right", "down", "left"]:
        if pressed == "up" and key_systems["custom"]["parameters"]["My"] - 0.125 >= 0:
            key_systems["custom"]["parameters"]["My"] -= 0.125
        elif pressed == "down" and key_systems["custom"]["parameters"]["My"] + 0.125 <= 29:
            key_systems["custom"]["parameters"]["My"] += 0.125
        elif pressed == "left" and min(key_systems["custom"]["parameters"]["Bx"], key_systems["custom"]["parameters"]["Mx"]) - 0.125 >= 0:
            key_systems["custom"]["parameters"]["Bx"] -= 0.125
            key_systems["custom"]["parameters"]["Mx"] -= 0.125
        elif pressed == "right" and max(key_systems["custom"]["parameters"]["Bx"], key_systems["custom"]["parameters"]["Mx"]) + 0.125 <= 74:
            key_systems["custom"]["parameters"]["Bx"] += 0.125
            key_systems["custom"]["parameters"]["Mx"] += 0.125

        render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
        render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)

    elif ("xpos" in SELECT or "ypos" in SELECT) and pressed in ["up", "right", "down", "left"]:
        x1 = key_systems["custom"][int(SELECT[4:])]["x1"]
        y1 = key_systems["custom"][int(SELECT[4:])]["y1"]
        x2 = key_systems["custom"][int(SELECT[4:])]["x2"]
        y2 = key_systems["custom"][int(SELECT[4:])]["y2"]
        if pressed == "up" and y1 - 0.125 >= 0:
            y1 -= 0.125
            y2 -= 0.125
        elif pressed == "down" and y2 + 0.125 <= 29:
            y1 += 0.125
            y2 += 0.125
        elif pressed == "left" and x1 - 0.125 >= 0:
            x1 -= 0.125
            x2 -= 0.125
        elif pressed == "right" and x2 + 0.125 <= 74:
            x1 += 0.125
            x2 += 0.125
        key_systems["custom"][int(SELECT[4:])]["x1"] = x1
        key_systems["custom"][int(SELECT[4:])]["y1"] = y1
        key_systems["custom"][int(SELECT[4:])]["x2"] = x2
        key_systems["custom"][int(SELECT[4:])]["y2"] = y2

        render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
        render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)

    elif ("width" in SELECT or "hight" in SELECT) and pressed in ["up", "right", "down", "left"]:
        x1 = key_systems["custom"][int(SELECT[5:])]["x1"]
        y1 = key_systems["custom"][int(SELECT[5:])]["y1"]
        x2 = key_systems["custom"][int(SELECT[5:])]["x2"]
        y2 = key_systems["custom"][int(SELECT[5:])]["y2"]
        if pressed == "up" and y1 - 0.125 >= 0 and y2 + 0.125 <= 29 and y2-y1 + 0.25 <= 16:
            y1 -= 0.125
            y2 += 0.125
        elif pressed == "down" and y2-y1 - 0.25 >= 1:
            y1 += 0.125
            y2 -= 0.125
        elif pressed == "left" and x2-x1 - 0.25 >= 1:
            x1 += 0.125
            x2 -= 0.125
        elif pressed == "right" and x1 - 0.125 >= 0 and x2 + 0.125 <= 74 and x2-x1 + 0.25 <= 16:
            x1 -= 0.125
            x2 += 0.125
        key_systems["custom"][int(SELECT[5:])]["x1"] = x1
        key_systems["custom"][int(SELECT[5:])]["y1"] = y1
        key_systems["custom"][int(SELECT[5:])]["x2"] = x2
        key_systems["custom"][int(SELECT[5:])]["y2"] = y2

        render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
        render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)

    elif ("partialsx" in SELECT or "partialsy" in SELECT) and pressed in ["up", "right", "down", "left"]:
        x1 = key_systems["custom"][int(SELECT[9:])]["x"] - key_systems["custom"][int(SELECT[9:])]["size"]*16
        x2 = key_systems["custom"][int(SELECT[9:])]["x"] + key_systems["custom"][int(SELECT[9:])]["size"]*16
        y1 = key_systems["custom"][int(SELECT[9:])]["y"] - key_systems["custom"][int(SELECT[9:])]["size"]*10
        y2 = key_systems["custom"][int(SELECT[9:])]["y"] + key_systems["custom"][int(SELECT[9:])]["size"]*10
        if pressed == "up" and y1 - 0.125 >= 0:
            key_systems["custom"][int(SELECT[9:])]["y"] -= 0.125
        elif pressed == "down" and y2 + 0.125 <= 29:
            key_systems["custom"][int(SELECT[9:])]["y"] += 0.125
        elif pressed == "left" and x1 - 0.125 >= 0:
            key_systems["custom"][int(SELECT[9:])]["x"] -= 0.125
        elif pressed == "right" and x2 + 0.125 <= 74:
            key_systems["custom"][int(SELECT[9:])]["x"] += 0.125

        render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
        render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)

    elif "labelsize" in SELECT or "xpos" in SELECT or "ypos" in SELECT or "width" in SELECT or "hight" in SELECT or "partialssize" in SELECT or "partialsx" in SELECT or "partialsy" in SELECT:
        no_num = SELECT
        while no_num[-1] in "0123456789":
            no_num = no_num[:-1]
        if pressed in tempvarparams[no_num][1] and len(TEMPVAR) < tempvarparams[no_num][0]:
            if len(TEMPVAR) != 0 and pressed == "b":
                TEMPVAR += "b"
            else:
                TEMPVAR += pressed.upper()
        elif pressed == "backspace":
            TEMPVAR = TEMPVAR[:-1]
        elif pressed == "up" or pressed == "right":
            if "labelsize" in SELECT:
                temp_labelsize = round(key_systems["custom"][int(SELECT[9:])]["labelsize"] + (1/12), 8)
                if temp_labelsize >= 1/2 and temp_labelsize <= 5/2:
                    key_systems["custom"][int(SELECT[9:])]["labelsize"] = temp_labelsize
            elif "partialssize" in SELECT:
                temp_partialssize = round(key_systems["custom"][int(SELECT[12:])]["size"] + (1/16), 8)
                x1 = key_systems["custom"][int(SELECT[12:])]["x"] - temp_partialssize*16
                x2 = key_systems["custom"][int(SELECT[12:])]["x"] + temp_partialssize*16
                y1 = key_systems["custom"][int(SELECT[12:])]["y"] - temp_partialssize*10
                y2 = key_systems["custom"][int(SELECT[12:])]["y"] + temp_partialssize*10
                if temp_partialssize >= 0.5 and temp_partialssize <= 1 and x1 >= 0 and x2 <= 74 and y1 >= 0 and y2 <= 29:
                    key_systems["custom"][int(SELECT[12:])]["size"] = temp_partialssize
        elif pressed == "down" or pressed == "left":
            if "labelsize" in SELECT:
                temp_labelsize = round(key_systems["custom"][int(SELECT[9:])]["labelsize"] - (1/12), 8)
                if temp_labelsize >= 1/2 and temp_labelsize <= 5/2:
                    key_systems["custom"][int(SELECT[9:])]["labelsize"] = temp_labelsize
            elif "partialssize" in SELECT:
                temp_partialssize = round(key_systems["custom"][int(SELECT[12:])]["size"] - (1/16), 8)
                if temp_partialssize >= 0.5 and temp_partialssize <= 1:
                    key_systems["custom"][int(SELECT[12:])]["size"] = temp_partialssize
                TEMPVAR = ""
        render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)
        render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
        render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
        if SETINSTRUMENT == "edit":
            render_options(INSTRUMENT, DATABASE, SETINSTRUMENT, SELECT, TEMPVAR)
    
    elif SELECT[:-1] in ["freq", "notename", "centsdev", "concertname", "concertdev"] or SELECT in ["tet", "edittranspose", "edittranssteps", "editlrsplit", "editmidx1", "editmidx2", "editmidy"]:
        if pressed in tempvarparams[SELECT[:-1]][1] and len(TEMPVAR) < tempvarparams[SELECT[:-1]][0]:
            if len(TEMPVAR) != 0 and pressed == "b":
                TEMPVAR += "b"
            else:
                TEMPVAR += pressed.upper()
        elif pressed == "backspace":
            TEMPVAR = TEMPVAR[:-1]
        elif pressed == "up" or pressed == "right":
            if SELECT == "tet":
                if TET < 342:
                    TET += 1
                    DATABASE[0][3] = TET
            elif SELECT == "edittranspose" or SELECT == "edittranssteps":
                temp_transpose = instruments["Custom"][1] + (12 / TET)
                if abs(temp_transpose) <= 96:
                    instruments["Custom"][1]  = temp_transpose
            elif SELECT == "editlrsplit":
                temp_LR_split = key_systems["custom"]["parameters"]["LR_split"] + 1
                if temp_LR_split >= 0 and temp_LR_split <= key_systems["custom"]["parameters"]["keys"]:
                    key_systems["custom"]["parameters"]["LR_split"] = temp_LR_split
            else:
                if SELECT[-1] == "0":
                    temp_pitch = TONIC * 2**(1/TET)
                else:
                    temp_pitch = PITCHES[int(SELECT[-1])-1] * 2**(1/TET)
                if temp_pitch >= (55/8) * 2**(5/24) and temp_pitch <= 14080 / 2**(1/8):
                    if SELECT[-1] == "0":
                        TONIC = temp_pitch
                        DATABASE[0][2] = temp_pitch
                    else:
                        PITCHES[int(SELECT[-1])-1] = temp_pitch
                TEMPVAR = ""
        elif pressed == "down" or pressed == "left":
            if SELECT == "tet":
                if TET > 1:
                    TET -= 1
                    DATABASE[0][3] = TET
            elif SELECT == "edittranspose" or SELECT == "edittranssteps":
                temp_transpose = instruments["Custom"][1] - (12 / TET)
                if abs(temp_transpose) <= 96:
                    instruments["Custom"][1]  = temp_transpose
            elif SELECT == "editlrsplit":
                temp_LR_split = key_systems["custom"]["parameters"]["LR_split"] - 1
                if temp_LR_split >= 0 and temp_LR_split <= key_systems["custom"]["parameters"]["keys"]:
                    key_systems["custom"]["parameters"]["LR_split"] = temp_LR_split
            else:
                if SELECT[-1] == "0":
                    temp_pitch = TONIC / 2**(1/TET)
                else:
                    temp_pitch = PITCHES[int(SELECT[-1])-1] / 2**(1/TET)
                if temp_pitch >= (55/8) * 2**(5/24) and temp_pitch <= 14080 / 2**(1/8):
                    if SELECT[-1] == "0":
                        TONIC = temp_pitch
                        DATABASE[0][2] = temp_pitch
                    else:
                        PITCHES[int(SELECT[-1])-1] = temp_pitch
                TEMPVAR = ""
        render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)
        render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
        render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
        if SETINSTRUMENT == "edit":
            render_options(INSTRUMENT, DATABASE, SETINSTRUMENT, SELECT, TEMPVAR)

    # SPOSITION INPUT
    elif "sposition" in SELECT:
        if pressed in "0123456789." and len(TEMPVAR) < 5:
            TEMPVAR += pressed
        elif pressed == "backspace":
            TEMPVAR = TEMPVAR[:-1]

        if "number" in SELECT:
            if pressed == "up" or pressed == "right":
                temp_sposition = FINGERING[int(SELECT[9])+3].real + (3/TET if instruments[INSTRUMENT][0] == "trumpet" else 12/TET)
                if temp_sposition >= float(SELECT.split(" ")[1]) and temp_sposition <= float(SELECT.split(" ")[2]):
                    if FINGTYPE == "trill":
                        if temp_sposition <= FINGERING[int(SELECT[9])+3].imag:
                            FINGERING[int(SELECT[9])+3] = complex(temp_sposition, temp_sposition)
                        else:
                            FINGERING[int(SELECT[9])+3] = complex(temp_sposition, FINGERING[int(SELECT[9])+3].imag)
                    else:
                        FINGERING[int(SELECT[9])+3] = complex(temp_sposition, 0)
                TEMPVAR = ""
            elif pressed == "down" or pressed == "left":
                temp_sposition = FINGERING[int(SELECT[9])+3].real - (3/TET if instruments[INSTRUMENT][0] == "trumpet" else 12/TET)
                if temp_sposition >= float(SELECT.split(" ")[1]) and temp_sposition <= float(SELECT.split(" ")[2]):
                    if FINGTYPE == "trill":
                        if temp_sposition <= FINGERING[int(SELECT[9])+3].imag:
                            FINGERING[int(SELECT[9])+3] = complex(temp_sposition, temp_sposition)
                        else:
                            FINGERING[int(SELECT[9])+3] = complex(temp_sposition, FINGERING[int(SELECT[9])+3].imag)
                    else:
                        FINGERING[int(SELECT[9])+3] = complex(temp_sposition, 0)
                TEMPVAR = ""
        elif "trillnum" in SELECT:
            if pressed == "up" or pressed == "right":
                temp_sposition = FINGERING[int(SELECT[9])+3].imag + 12/TET
                if temp_sposition >= float(SELECT.split(" ")[1]) and temp_sposition <= float(SELECT.split(" ")[2]):
                    if FINGTYPE == "trill":
                        if temp_sposition >= FINGERING[int(SELECT[9])+3].real:
                            FINGERING[int(SELECT[9])+3] = complex(temp_sposition, temp_sposition)
                        else:
                            FINGERING[int(SELECT[9])+3] = complex(FINGERING[int(SELECT[9])+3].real, temp_sposition)
                    else:
                        FINGERING[int(SELECT[9])+3] = complex(temp_sposition, 0)
                TEMPVAR = ""
            elif pressed == "down" or pressed == "left":
                temp_sposition = FINGERING[int(SELECT[9])+3].imag - 12/TET
                if temp_sposition >= float(SELECT.split(" ")[1]) and temp_sposition <= float(SELECT.split(" ")[2]):
                    if FINGTYPE == "trill":
                        if temp_sposition >= FINGERING[int(SELECT[9])+3].real:
                            FINGERING[int(SELECT[9])+3] = complex(temp_sposition, temp_sposition)
                        else:
                            FINGERING[int(SELECT[9])+3] = complex(FINGERING[int(SELECT[9])+3].real, temp_sposition)
                    else:
                        FINGERING[int(SELECT[9])+3] = complex(temp_sposition, 0)
                TEMPVAR = ""
            
        render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)

    # FILTER TOLERANCE INPUT
    elif SELECT == "tolerance_cents" or SELECT == "tolerance_percent":
        if pressed in "0123456789." and len(TEMPVAR) < 6:
            TEMPVAR += pressed
        elif pressed == "backspace":
            TEMPVAR = TEMPVAR[:-1]
        elif pressed == "up" or pressed == "right":
            tolerance = round(FILTERS["tolerance"] + 0.01, 6)
            if tolerance >= 0 and tolerance <= 0.5:
                FILTERS["tolerance"] = tolerance
        elif pressed == "down" or pressed == "left":
            tolerance = round(FILTERS["tolerance"] - 0.01, 6)
            if tolerance >= 0 and tolerance <= 0.5:
                FILTERS["tolerance"] = tolerance
        render_filters(FILTERS, TET, SELECT, TEMPVAR)

    # SCROLLING THROUGH DATABASE
    elif "data" in SELECT:
        if pressed == "down":
            SELECT = "data+" + SELECT.split(" ")[0][4:]
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
            PITCHES = sorted(list(DATABASE[int(SELECT[4:])][0]))
            FINGERING = list(DATABASE[int(SELECT[4:])][1])
            FINGTYPE = DATABASE[int(SELECT[4:])][2]
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)
        elif pressed == "up":
            SELECT = "data-" + SELECT.split(" ")[0][4:]
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
            PITCHES = sorted(list(DATABASE[int(SELECT[4:])][0]))
            FINGERING = list(DATABASE[int(SELECT[4:])][1])
            FINGTYPE = DATABASE[int(SELECT[4:])][2]
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)

# WHEN SPOSITION IS CLICKED
def spositionclick(event):

    global SELECT
    global FINGERING
    global INSTRUMENT
    global TEMPVAR
    
    item = C.find_closest(event.x, event.y)
    tags = C.itemcget(item, "tags").split(" ")
    
    if "clickable" in tags:
        if "sposition" in tags[1] and "number" not in tags[2] and "trillnum" not in tags[2] and "setto" not in tags[2]:
            new_pos = (event.x - float(tags[3])) / ((float(tags[4])-float(tags[3]))/(float(tags[6])-float(tags[5]))) + float(tags[5])
            if "trill" in tags[2]:
                FINGERING[int(tags[1][-1])+3] = complex(new_pos, new_pos)
            else:
                FINGERING[int(tags[1][-1])+3] = complex(new_pos, FINGERING[int(tags[1][-1])+3].imag)
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)

# WHEN SPOSITION IS MIDDLE-CLICKED
def spositiontrillclick(event):

    global SELECT
    global FINGERING
    global INSTRUMENT
    global TEMPVAR
    
    item = C.find_closest(event.x, event.y)
    tags = C.itemcget(item, "tags").split(" ")
    
    if "clickable" in tags:
        if FINGTYPE == "trill":
            if "sposition" in tags[1] and "number" not in tags[2] and "trillnum" not in tags[2] and "setto" not in tags[2]:
                new_pos = (event.x - float(tags[3])) / ((float(tags[4])-float(tags[3]))/(float(tags[6])-float(tags[5]))) + float(tags[5])
                if "left" in tags[2] or "trill" in tags[2]:
                    FINGERING[int(tags[1][-1])+3] = complex(FINGERING[int(tags[1][-1])+3].real, new_pos)
                else:
                    new_pos = (event.x - float(tags[3])) / ((float(tags[4])-float(tags[3]))/(float(tags[6])-float(tags[5]))) + float(tags[5])
                    FINGERING[int(tags[1][-1])+3] = complex(new_pos, new_pos)
                render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            
# KEY AND MOUSE BINDS            
if platform.system() == "Darwin": # On Mac, Button-2 and Button-3 are flipped
    C.bind("<Button-1>", onclick)
    C.bind("<B1-Motion>", spositionclick)
    C.bind("<Button-3>", middleclick)
    C.bind("<B3-Motion>", spositiontrillclick)
    C.bind("<Button-2>", rightclick)
else:
    C.bind("<Button-1>", onclick)
    C.bind("<B1-Motion>", spositionclick)
    C.bind("<Button-2>", middleclick)
    C.bind("<B2-Motion>", spositiontrillclick)
    C.bind("<Button-3>", rightclick)

root.bind("<BackSpace>", onkey)
root.bind("<Return>", onkey)
root.bind("<Up>", onkey)
root.bind("<Down>", onkey)
root.bind("<Left>", onkey)
root.bind("<Right>", onkey)
root.bind("<numbersign>", onkey)
root.bind("<plus>", onkey)
root.bind("<minus>", onkey)
root.bind("<equal>", onkey)

root.bind("<Configure>", onresize)

for key in list("abcdefghijklmnopqrstuvwxy."):
    root.bind("<" + key + ">", onkey)
for key in list("0123457689"):
    root.bind("<Key-" + key + ">", onkey)


# FUNCTIONS

# RENDER + and - SIGNS (e.g. 32 becomes +32)
def styleminus(number):
    if round(number, 6) < 0:
        return "−" + str(abs(number))
    else:
        return str(abs(number))

def csvplus(number):
    if round(number, 6) >= 0:
        return "+" + str(abs(number))
    else:
        return str(number)

def csvplusminus(number):
    if round(number, 6) > 0:
        return "+" + str(abs(number))
    else:
        return str(number)

def dataplus(number):
    if round(number, 6) >= 0:
        return "+" + str(abs(number))
    else:
        return "−" + str(abs(number))

def plusminus(number):
    if round(number, 6) > 0:
        return "+" + str(abs(number))
    else:
        return styleminus(number)

# FREQUENCY TO NOTE NAME AND CENTS DEV
def notename(pitch, transpose=0):
    pitch /= 2**(transpose/12)
    C0 = (55/4) * 2**(1/4)
    notenames = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    notenum = int(round(math.log(pitch/C0, 2**(1/12)), 0))
    centsdev = (((math.log(pitch/C0, 2**(1/12)) + 0.5) % 1) - 0.49999999999) * 100
    name = str(notenames[notenum % 12]) + styleminus(math.floor(notenum / 12))
    return name, centsdev

# NOTE NAME TO FREQUENCY
def notetofreq(notename, transpose=0):
    if notename == "":
        return False
    C0 = (55/4) * 2**(1/4)
    notedict = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
    notename = list(notename)
    note, octave = 0, 0
    if notename[0].upper() in "ABCDEFG" and notename[-1] in "0123456789":
        note = notedict[notename.pop(0)]
        octave = int(notename.pop(-1))
        if len(notename) == 0:
            return C0 * 2**((note + octave*12)/12) * 2**(transpose/12)
        else:
            if notename[-1] == "-":
                octave *= -1
                notename.pop(-1)
            elif notename[-1] == "1":
                octave += 10
                notename.pop(-1)
            elif notename[-1] == "#":
                note += 1
                notename.pop(-1)
            elif notename[-1] == "b":
                note -= 1
                notename.pop(-1)
            if len(notename) == 0:
                return C0 * 2**((note + octave*12)/12) * 2**(transpose/12)
            else:
                if notename[-1] == "#":
                    note += 1
                    return C0 * 2**((note + octave*12)/12) * 2**(transpose/12)
                elif notename[-1] == "b":
                    note -= 1
                    return C0 * 2**((note + octave*12)/12) * 2**(transpose/12)
                else:
                    return False    
    else:
        return False

# ADD ENTRY TO DATABASE
def addentry(entry, database=DATABASE): # entry is a tuple — (pitches, fingering, fingtype)
    entry[0].sort()
    entry = ([round(e, 6) for e in entry[0]], entry[1], entry[2])

    if len(database) == 1:
        return 1, [database[0]] + [entry]
    else:
        notes = []; trills = []; multiphonics = []

        for tup in database[1:]:
            if tup[2] == "note":
                notes.append(tup)
            elif tup[2] == "trill":
                trills.append(tup)
            elif tup[2] in ["multi2", "multi3", "multi4"]:
                multiphonics.append(tup)

        if entry[2] == "note":
            if len(notes) == 0:
                notes.append(entry)
                return 1, [database[0]] + notes + trills + multiphonics
            elif len(notes) == 1:
                if (round(entry[0][0], 4), round(entry[1][4].real, 4), round(entry[1][5].real, 4), entry[1][0], entry[1][1]) < (round(notes[0][0][0], 4), round(notes[0][1][4].real, 4), round(notes[0][1][5].real, 4), notes[0][1][0], notes[0][1][1]):
                    notes.insert(0, entry)
                    return 1, [database[0]] + notes + trills + multiphonics
                else:
                    notes.insert(1, entry)
                    return 2, [database[0]] + notes + trills + multiphonics
            else: # binary search for the location to insert the note
                low = 0; high = len(notes)-1
                while high - low > 1:
                    mid = int((low + high) / 2)
                    if (round(entry[0][0], 4), round(entry[1][4].real, 4), round(entry[1][5].real, 4), entry[1][0], entry[1][1]) == (round(notes[mid][0][0], 4), round(notes[mid][1][4].real, 4), round(notes[mid][1][5].real, 4), notes[mid][1][0], notes[mid][1][1]):
                        notes.insert(mid+1, entry)
                        return mid+2, [database[0]] + notes + trills + multiphonics
                    elif (round(entry[0][0], 4), round(entry[1][4].real, 4), round(entry[1][5].real, 4), entry[1][0], entry[1][1]) < (round(notes[mid][0][0], 4), round(notes[mid][1][4].real, 4), round(notes[mid][1][5].real, 4), notes[mid][1][0], notes[mid][1][1]):
                        high = mid
                    elif (round(entry[0][0], 4), round(entry[1][4].real, 4), round(entry[1][5].real, 4), entry[1][0], entry[1][1]) > (round(notes[mid][0][0], 4), round(notes[mid][1][4].real, 4), round(notes[mid][1][5].real, 4), notes[mid][1][0], notes[mid][1][1]):
                        low = mid
                if (round(entry[0][0], 4), round(entry[1][4].real, 4), round(entry[1][5].real, 4), entry[1][0], entry[1][1]) >= (round(notes[high][0][0], 4), round(notes[high][1][4].real, 4), round(notes[high][1][5].real, 4), notes[high][1][0], notes[high][1][1]):
                    notes.insert(high+1, entry)
                    return high+2, [database[0]] + notes + trills + multiphonics
                elif (round(entry[0][0], 4), round(entry[1][4].real, 4), round(entry[1][5].real, 4), entry[1][0], entry[1][1]) >= (round(notes[low][0][0], 4), round(notes[low][1][4].real, 4), round(notes[low][1][5].real, 4), notes[low][1][0], notes[low][1][1]):
                    notes.insert(high, entry)
                    return high+1, [database[0]] + notes + trills + multiphonics
                else:
                    notes.insert(low, entry)
                    return low+1, [database[0]] + notes + trills + multiphonics

        elif entry[2] == "trill":
            if len(trills) == 0:
                trills.append(entry)
                return 1+len(notes), [database[0]] + notes + trills + multiphonics
            elif len(trills) == 1:
                if (round(entry[0][0], 4), round(entry[0][1], 4), round(entry[1][4].real, 4), round(entry[1][4].imag, 4), round(entry[1][5].real, 4), round(entry[1][5].imag, 4), entry[1][0], entry[1][1]) < (round(trills[0][0][0], 4), round(trills[0][0][1], 4), round(trills[0][1][4].real, 4), round(trills[0][1][4].imag, 4), round(trills[0][1][5].real, 4), round(trills[0][1][5].imag, 4), trills[0][1][0], trills[0][1][1]):
                    trills.insert(0, entry)
                    return 1+len(notes), [database[0]] + notes + trills + multiphonics
                else:
                    trills.insert(1, entry)
                    return 2+len(notes), [database[0]] + notes + trills + multiphonics
            else: # binary search for the location to insert the trill
                low = 0; high = len(trills)-1
                while high - low > 1:
                    mid = int((low + high) / 2)
                    if (round(entry[0][0], 4), round(entry[0][1], 4), round(entry[1][4].real, 4), round(entry[1][4].imag, 4), round(entry[1][5].real, 4), round(entry[1][5].imag, 4), entry[1][0], entry[1][1]) == (round(trills[mid][0][0], 4), round(trills[mid][0][1], 4), round(trills[mid][1][4].real, 4), round(trills[mid][1][4].imag, 4), round(trills[mid][1][5].real, 4), round(trills[mid][1][5].imag, 4), trills[mid][1][0], trills[mid][1][1]):
                        trills.insert(mid+1, entry)
                        return mid+2+len(notes), [database[0]] + notes + trills + multiphonics
                    elif (round(entry[0][0], 4), round(entry[0][1], 4), round(entry[1][4].real, 4), round(entry[1][4].imag, 4), round(entry[1][5].real, 4), round(entry[1][5].imag, 4), entry[1][0], entry[1][1]) < (round(trills[mid][0][0], 4), round(trills[mid][0][1], 4), round(trills[mid][1][4].real, 4), round(trills[mid][1][4].imag, 4), round(trills[mid][1][5].real, 4), round(trills[mid][1][5].imag, 4), trills[mid][1][0], trills[mid][1][1]):
                        high = mid
                    elif (round(entry[0][0], 4), round(entry[0][1], 4), round(entry[1][4].real, 4), round(entry[1][4].imag, 4), round(entry[1][5].real, 4), round(entry[1][5].imag, 4), entry[1][0], entry[1][1]) > (round(trills[mid][0][0], 4), round(trills[mid][0][1], 4), round(trills[mid][1][4].real, 4), round(trills[mid][1][4].imag, 4), round(trills[mid][1][5].real, 4), round(trills[mid][1][5].imag, 4), trills[mid][1][0], trills[mid][1][1]):
                        low = mid
                if (round(entry[0][0], 4), round(entry[0][1], 4), round(entry[1][4].real, 4), round(entry[1][4].imag, 4), round(entry[1][5].real, 4), round(entry[1][5].imag, 4), entry[1][0], entry[1][1]) >= (round(trills[high][0][0], 4), round(trills[high][0][1], 4), round(trills[high][1][4].real, 4), round(trills[high][1][4].imag, 4), round(trills[high][1][5].real, 4), round(trills[high][1][5].imag, 4), trills[high][1][0], trills[high][1][1]):
                    trills.insert(high+1, entry)
                    return high+2+len(notes), [database[0]] + notes + trills + multiphonics
                elif (round(entry[0][0], 4), round(entry[0][1], 4), round(entry[1][4].real, 4), round(entry[1][4].imag, 4), round(entry[1][5].real, 4), round(entry[1][5].imag, 4), entry[1][0], entry[1][1]) >= (round(trills[low][0][0], 4), round(trills[low][0][1], 4), round(trills[low][1][4].real, 4), round(trills[low][1][4].imag, 4), round(trills[low][1][5].real, 4), round(trills[low][1][5].imag, 4), trills[low][1][0], trills[low][1][1]):
                    trills.insert(high, entry)
                    return high+1+len(notes), [database[0]] + notes + trills + multiphonics
                else:
                    trills.insert(low, entry)
                    return low+1+len(notes), [database[0]] + notes + trills + multiphonics

        elif entry[2] in ["multi2", "multi3", "multi4"]:
            if len(multiphonics) == 0:
                multiphonics.append(entry)
                return 1+len(notes)+len(trills), [database[0]] + notes + trills + multiphonics
            elif len(multiphonics) == 1:
                if (round(entry[0][0], 4), round(entry[0][1], 4), (round(entry[0][2], 4) if len(entry[0]) >= 6 else 0), (round(entry[0][3], 4) if len(entry[0]) >= 7 else 0), round(entry[1][4].real, 4), round(entry[1][5].real, 4), entry[1][0], entry[1][1]) < (round(multiphonics[0][0][0], 4), round(multiphonics[0][0][1], 4), (round(multiphonics[0][0][2], 4) if len(multiphonics[0][0]) >= 3 else 0), (round(multiphonics[0][0][3], 4) if len(multiphonics[0][0]) >= 4 else 0), round(multiphonics[0][1][4].real, 4), round(multiphonics[0][1][5].real, 4), multiphonics[0][1][0], multiphonics[0][1][1]):
                    multiphonics.insert(0, entry)
                    return 1+len(notes)+len(trills), [database[0]] + notes + trills + multiphonics
                else:
                    multiphonics.insert(1, entry)
                    return 2+len(notes)+len(trills), [database[0]] + notes + trills + multiphonics
            else: # binary search for the location to insert the multiphonics
                low = 0; high = len(multiphonics)-1
                while high - low > 1:
                    mid = int((low + high) / 2)
                    if (round(entry[0][0], 4), round(entry[0][1], 4), (round(entry[0][2], 4) if len(entry[0]) >= 6 else 0), (round(entry[0][3], 4) if len(entry[0]) >= 7 else 0), round(entry[1][4].real, 4), round(entry[1][5].real, 4), entry[1][0], entry[1][1]) == (round(multiphonics[mid][0][0], 4), round(multiphonics[mid][0][1], 4), (round(multiphonics[mid][0][2], 4) if len(multiphonics[mid][0]) >= 3 else 0), (round(multiphonics[mid][0][3], 4) if len(multiphonics[mid][0]) >= 4 else 0), round(multiphonics[mid][1][4].real, 4), round(multiphonics[mid][1][5].real, 4), multiphonics[mid][1][0], multiphonics[mid][1][1]):
                        multiphonics.insert(mid+1, entry)
                        return mid+2+len(notes)+len(trills), [database[0]] + notes + trills + multiphonics
                    elif (round(entry[0][0], 4), round(entry[0][1], 4), (round(entry[0][2], 4) if len(entry[0]) >= 6 else 0), (round(entry[0][3], 4) if len(entry[0]) >= 7 else 0), round(entry[1][4].real, 4), round(entry[1][5].real, 4), entry[1][0], entry[1][1]) < (round(multiphonics[mid][0][0], 4), round(multiphonics[mid][0][1], 4), (round(multiphonics[mid][0][2], 4) if len(multiphonics[mid][0]) >= 3 else 0), (round(multiphonics[mid][0][3], 4) if len(multiphonics[mid][0]) >= 4 else 0), round(multiphonics[mid][1][4].real, 4), round(multiphonics[mid][1][5].real, 4), multiphonics[mid][1][0], multiphonics[mid][1][1]):
                        high = mid
                    elif (round(entry[0][0], 4), round(entry[0][1], 4), (round(entry[0][2], 4) if len(entry[0]) >= 6 else 0), (round(entry[0][3], 4) if len(entry[0]) >= 7 else 0), round(entry[1][4].real, 4), round(entry[1][5].real, 4), entry[1][0], entry[1][1]) > (round(multiphonics[mid][0][0], 4), round(multiphonics[mid][0][1], 4), (round(multiphonics[mid][0][2], 4) if len(multiphonics[mid][0]) >= 3 else 0), (round(multiphonics[mid][0][3], 4) if len(multiphonics[mid][0]) >= 4 else 0), round(multiphonics[mid][1][4].real, 4), round(multiphonics[mid][1][5].real, 4), multiphonics[mid][1][0], multiphonics[mid][1][1]):
                        low = mid
                if (round(entry[0][0], 4), round(entry[0][1], 4), (round(entry[0][2], 4) if len(entry[0]) >= 6 else 0), (round(entry[0][3], 4) if len(entry[0]) >= 7 else 0), round(entry[1][4].real, 4), round(entry[1][5].real, 4), entry[1][0], entry[1][1]) >= (round(multiphonics[high][0][0], 4), round(multiphonics[high][0][1], 4), (round(multiphonics[high][0][2], 4) if len(multiphonics[high][0]) >= 3 else 0), (round(multiphonics[high][0][3], 4) if len(multiphonics[high][0]) >= 4 else 0), round(multiphonics[high][1][4].real, 4), round(multiphonics[high][1][5].real, 4), multiphonics[high][1][0], multiphonics[high][1][1]):
                    multiphonics.insert(high+1, entry)
                    return high+2+len(notes)+len(trills), [database[0]] + notes + trills + multiphonics
                elif (round(entry[0][0], 4), round(entry[0][1], 4), (round(entry[0][2], 4) if len(entry[0]) >= 6 else 0), (round(entry[0][3], 4) if len(entry[0]) >= 7 else 0), round(entry[1][4].real, 4), round(entry[1][5].real, 4), entry[1][0], entry[1][1]) >= (round(multiphonics[low][0][0], 4), round(multiphonics[low][0][1], 4), (round(multiphonics[low][0][2], 4) if len(multiphonics[low][0]) >= 3 else 0), (round(multiphonics[low][0][3], 4) if len(multiphonics[low][0]) >= 4 else 0), round(multiphonics[low][1][4].real, 4), round(multiphonics[low][1][5].real, 4), multiphonics[low][1][0], multiphonics[low][1][1]):
                    multiphonics.insert(high, entry)
                    return high+1+len(notes)+len(trills), [database[0]] + notes + trills + multiphonics
                else:
                    multiphonics.insert(low, entry)
                    return low+1+len(notes)+len(trills), [database[0]] + notes + trills + multiphonics

# EXPORT FILE
def exportfile(database=DATABASE):

    no_comma_databasedesc = ""
    for char in database[0][4].strip():
        no_comma_databasedesc += ("`" if char == "," else ("$" if char == "\"" else ("!" if char == "\n" else char)))

    if database[0][1] == "Custom":
        instrument_string = exportkeysystem(key_systems[instruments[database[0][1]][0]])
    else:
        instrument_string = database[0][1]

    transposition = transposition = int(round(instruments[database[0][1]][1]*100, 2)) if round(instruments[database[0][1]][1]*100, 2) == int(round(instruments[database[0][1]][1]*100, 2)) else round(instruments[database[0][1]][1]*100, 2)
    csv_string = database[0][0] + "\nInstrument: " + instrument_string + "\nTransposition: " + str(instruments[database[0][1]][1]*100) + " cents\nTonic: " + str(round(database[0][2], 6)) + " Hz\nTemperament: " + str(database[0][3]) + "-TET\nDescription: " + no_comma_databasedesc
    header = "Type,Frequency (Hz),Transposed pitch,Concert pitch,TET step,Fingering,Fingering ID,Description"
    csv = ""
    for fingering in database[1:]: # entry is a tuple — (pitches, fingering, fingtype)

        if "multi" in fingering[2]:
            csv += "multi,"
        else:
            csv += fingering[2]+","
        
        freqs = []
        transposed_pitches = []
        concert_pitches = []
        tet_steps = []
        
        for pitch in fingering[0]:
            freqs.append(str(round(pitch, 8)))
            transposed_note = notename(pitch, instruments[database[0][1]][1])
            concert_note = notename(pitch, 0)
            transposed_pitches.append(transposed_note[0] + csvplus(round(transposed_note[1], 2)))
            concert_pitches.append(concert_note[0] + csvplus(round(concert_note[1], 2)))
            tet_steps.append(str(int(round(database[0][3]*math.log(pitch/database[0][2], 2), 0)) % database[0][3]) + "\\" + str(database[0][3]) + " " + csvplusminus(round(100 * (database[0][3]*math.log(pitch/database[0][2], 2) - round(database[0][3]*math.log(pitch/database[0][2], 2), 0) + 0.0000000001), 2)) + "%")
            
        csv += (" ".join(freqs))+","
        csv += (" ".join(transposed_pitches))+","
        csv += (" ".join(concert_pitches))+","
        csv += (" ".join(tet_steps))+","

        f = list(bin(fingering[1][0]))[2:]
        h = list(bin(fingering[1][1]))[2:]
        t = list(bin(fingering[1][2]))[2:]
        while len(f) < key_systems[instruments[database[0][1]][0]]["parameters"]["keys"]:
            f.insert(0, "0")
        while len(h) < key_systems[instruments[database[0][1]][0]]["parameters"]["keys"]:
            h.insert(0, "0")
        while len(t) < key_systems[instruments[database[0][1]][0]]["parameters"]["keys"]:
            t.insert(0, "0")
        states = []
        for key in range(key_systems[instruments[database[0][1]][0]]["parameters"]["keys"]):
            if key_systems[instruments[database[0][1]][0]][key_systems[instruments[database[0][1]][0]]["parameters"]["keys"] - 1 - key]["type"] == "sposition1":
                states.insert(0, fingering[1][4])
            elif key_systems[instruments[database[0][1]][0]][key_systems[instruments[database[0][1]][0]]["parameters"]["keys"] - 1 - key]["type"] == "sposition2":
                states.insert(0, fingering[1][5])
            elif int(t[key]) == 1:
                states.insert(0, 3)
            else:
                states.insert(0, int(f[key])+int(h[key]))
                
        desc_string = ""
        for key, state in enumerate(states):
            if key == key_systems[instruments[database[0][1]][0]]["parameters"]["LR_split"]:
                desc_string += key_systems[instruments[database[0][1]][0]]["parameters"]["separator"]
            if isinstance(state, complex):
                if fingering[2] != "trill" or round(state.real, 6) == round(state.imag, 6):
                    desc_string += "{"+str(round(state.real, 2))+"} "
                else:
                    desc_string += "[{"+str(round(state.real, 2))+"}{"+str(round(state.imag, 2))+"}] "
            elif state == 3:
                desc_string += "["+key_systems[instruments[database[0][1]][0]][key]["descname"].strip()+"]"
            elif state == 2:
                desc_string += "h"
            elif state == 1:
                desc_string += key_systems[instruments[database[0][1]][0]][key]["descname"]
            elif state == 0:
                if key_systems[instruments[database[0][1]][0]][key]["descoff"] == "−":
                    desc_string += "-"
                else:
                    desc_string += key_systems[instruments[database[0][1]][0]][key]["descoff"]
        if fingering[1][3] == -17:
            desc_string += "[(16)]"
        elif fingering[1][3] == -1:
            desc_string += "[(0)]"
        elif fingering[1][3] >= 0:
            desc_string += "(" + str(fingering[1][3]) + ")"
        elif fingering[1][3] <= -2:
            desc_string += "[(" + str(-fingering[1][3]-1) + ")(" + str(-fingering[1][3]) + ")]"

        csv += " "+desc_string+","

        for fingering_id in fingering[1][:-1]:
            if isinstance(fingering_id, complex):
                csv += str(fingering_id.real) + ":" + str(fingering_id.imag) + "_"
            elif fingering_id == -0.5:
                csv += "|_"
            else:
                csv += str(fingering_id) + "_"

        csv = csv[:-1] + ","

        no_comma_desc = ""
        for char in fingering[1][-1]:
            no_comma_desc += ("`" if char == "," else ("$" if char == "\"" else ("!" if char == "\n" else char)))
        
        csv += no_comma_desc+"\n"
        
    return csv_string + "\n" + header + "\n" + csv

# IMPORT FILE
def importfile(file):

    comma_databasedesc = ""
    for char in file[5].split(",")[0][13:]:
        comma_databasedesc += ("," if char == "`" else ("\"" if char == "$" else ("\n" if char == "!" else char)))

    database = [[
        file[0].split(",")[0], # name
        "Custom" if "Custom" in file[1].split(",")[0][12:] else file[1].split(",")[0][12:], # instrument
        float(file[3].split(",")[0].split(" ")[1]), # tonic
        int(file[4].split(",")[0].split(" ")[1].split("-")[0]), # tet
        comma_databasedesc # databasedesc
    ]]

    for f in file[7:]:
        f = f.split(",")
        pitches = [float(p) for p in f[1].split(" ")]
        fing_elements = f[-2].split("_")
        fingering = []
        for fing_element in fing_elements:
            if fing_element == "|":
                fingering.append(-0.5)
            elif ":" in fing_element:
                fingering.append(complex(float(fing_element.split(":")[0]), float(fing_element.split(":")[1])))
            else:
                fingering.append(int(fing_element))

        comma_desc = ""
        for char in f[-1]:
            comma_desc += ("," if char == "`" else ("\"" if char == "$" else ("\n" if char == "!" else char)))
                
        fingering.append(comma_desc)
        fingtype = "multi" + str(len(pitches)) if f[0] == "multi" else f[0]
        database.append((pitches, fingering, fingtype))

    return database, float(file[2].split(",")[0][15:-6]), (importkeysystem(file[1].split(",")[0][12:]) if "Custom" in file[1].split(",")[0][12:] else "")
                           
# COPY CO CLIPBOARD
def copytoclipboard(pi=PITCHES, fi=FINGERING, ft=FINGTYPE):

    global TET
    global TONIC
    global INSTRUMENT

    fingering = (sorted(pi), fi, ft) # entry is a tuple — (pitches, fingering, fingtype)
    csv = ""

    if "multi" in fingering[2]:
        csv += "multi,"
    else:
        csv += fingering[2]+","
    
    freqs = []
    transposed_pitches = []
    concert_pitches = []
    tet_steps = []
    
    for pitch in fingering[0]:
        freqs.append(str(round(pitch, 8)))
        transposed_note = notename(pitch, instruments[INSTRUMENT][1])
        concert_note = notename(pitch, 0)
        transposed_pitches.append(transposed_note[0] + csvplus(round(transposed_note[1], 2)))
        concert_pitches.append(concert_note[0] + csvplus(round(concert_note[1], 2)))
        tet_steps.append(str(int(round(TET*math.log(pitch/TONIC, 2), 0)) % TET) + "\\" + str(TET) + " " + csvplusminus(round(100 * (TET*math.log(pitch/TONIC, 2) - round(TET*math.log(pitch/TONIC, 2), 0) + 0.0000000001), 2)) + "%")
        
    csv += (" ".join(freqs))+","
    csv += (" ".join(transposed_pitches))+","
    csv += (" ".join(concert_pitches))+","
    csv += (" ".join(tet_steps))+","

    f = list(bin(fingering[1][0]))[2:]
    h = list(bin(fingering[1][1]))[2:]
    t = list(bin(fingering[1][2]))[2:]
    while len(f) < key_systems[instruments[INSTRUMENT][0]]["parameters"]["keys"]:
        f.insert(0, "0")
    while len(h) < key_systems[instruments[INSTRUMENT][0]]["parameters"]["keys"]:
        h.insert(0, "0")
    while len(t) < key_systems[instruments[INSTRUMENT][0]]["parameters"]["keys"]:
        t.insert(0, "0")
    states = []
    for key in range(key_systems[instruments[INSTRUMENT][0]]["parameters"]["keys"]):
        if key_systems[instruments[INSTRUMENT][0]][key_systems[instruments[INSTRUMENT][0]]["parameters"]["keys"] - 1 - key]["type"] == "sposition1":
            states.insert(0, fingering[1][4])
        elif key_systems[instruments[INSTRUMENT][0]][key_systems[instruments[INSTRUMENT][0]]["parameters"]["keys"] - 1 - key]["type"] == "sposition2":
            states.insert(0, fingering[1][5])
        elif int(t[key]) == 1:
            states.insert(0, 3)
        else:
            states.insert(0, int(f[key])+int(h[key]))
            
    desc_string = ""
    for key, state in enumerate(states):
        descname = key_systems[instruments[INSTRUMENT][0]][key]["descname"]
        if key == key_systems[instruments[INSTRUMENT][0]]["parameters"]["LR_split"]:
            desc_string += key_systems[instruments[INSTRUMENT][0]]["parameters"]["separator"]
        if isinstance(state, complex):
            if fingering[2] != "trill" or round(state.real, 6) == round(state.imag, 6):
                desc_string += "{"+str(round(state.real, 2))+"} "
            else:
                desc_string += "[{"+str(round(state.real, 2))+"}{"+str(round(state.imag, 2))+"}] "
        elif state == 3:
            if len(descname) >= 1 and descname[0] == "⌫":
                desc_string = desc_string[:-1] if len(desc_string) >= 1 and desc_string[-1] == "−" else desc_string
                descname = descname[1:]
            desc_string += "["+descname.strip()+"]"
        elif state == 2:
            desc_string += "h " if descname[-1] == " " else (" h" if descname[0] == " " else "h")
        elif state == 1:
            if len(descname) >= 1 and descname[0] == "⌫":
                desc_string = desc_string[:-1] if len(desc_string) >= 1 and desc_string[-1] == "−" else desc_string
                descname = descname[1:]
            desc_string += descname
        elif state == 0:
            if key_systems[instruments[INSTRUMENT][0]][key]["descoff"] == "−":
                desc_string += "-"
            else:
                desc_string += key_systems[instruments[INSTRUMENT][0]][key]["descoff"]
    if fingering[1][3] == -17:
        desc_string += "[(16)]"
    elif fingering[1][3] == -1:
        desc_string += "[(0)]"
    elif fingering[1][3] >= 0:
        desc_string += "(" + str(fingering[1][3]) + ")"
    elif fingering[1][3] <= -2:
        desc_string += "[(" + str(-fingering[1][3]-1) + ")(" + str(-fingering[1][3]) + ")]"

    csv += " "+desc_string+","

    for fingering_id in fingering[1][:-1]:
        if isinstance(fingering_id, complex):
            csv += str(fingering_id.real) + ":" + str(fingering_id.imag) + "_"
        elif fingering_id == -0.5:
            csv += "|_"
        else:
            csv += str(fingering_id) + "_"

    csv = csv[:-1] + ","

    no_comma_desc = ""
    for char in fingering[1][-1]:
        no_comma_desc += ("`" if char == "," else ("$" if char == "\"" else ("!" if char == "\n" else char)))
        
    csv += no_comma_desc
        
    return csv

# PASTE FROM CLIPBOARD
def pastefromclipboard(f):

    f = f.split(",")
    pitches = [float(p) for p in f[1].split(" ")]
    fing_elements = f[-2].split("_")
    fingering = []
    for fing_element in fing_elements:
        if fing_element == "|":
            fingering.append(-0.5)
        elif ":" in fing_element:
            fingering.append(complex(float(fing_element.split(":")[0]), float(fing_element.split(":")[1])))
        else:
            fingering.append(int(fing_element))

    comma_desc = ""
    for char in f[-1]:
        comma_desc += ("," if char == "`" else ("\"" if char == "$" else ("\n" if char == "!" else char)))

    fingering.append(comma_desc)
    fingtype = "multi" + str(len(pitches)) if f[0] == "multi" else f[0]
    return (pitches, fingering, fingtype)
    
    
# RENDERING

# RENDER KEY
def render_key(key, keynum, offsetx=0, offsety=0, shiftx=0, shifty=0, state=0, partial=0, select=SELECT, tempvar=TEMPVAR):

    global FINGTYPE
    global FINGERING

    # IF DIAGRAM HAS PARTIALS
    if key["type"] == "partial":
        for p in range(17):
            partialscale = 4*key["size"]
            if p == 0:
                x = 7
                y = 0
                text_string = "other"
                text_size = 1*key["size"]
            elif p == 16:
                x = 6
                y = 0
                text_string = "16+"
                text_size = 5/4*key["size"]
            else:
                x = (p / (2**int(math.log(p, 2))) % 1)*8
                y = int(math.log(p, 2))
                text_string = str(p) + "+"*int(p/16)
                text_size = 5/4*key["size"]
                
            x1 = (key["x"] - 16*key["size"] + offsetx + shiftx + partialscale*x)*scale
            x2 = (key["x"] - 16*key["size"] + offsetx + shiftx + partialscale*(x+1))*scale
            y1 = (key["y"] - 7.25*key["size"] + offsety + shifty + partialscale*y)*scale
            y2 = (key["y"] - 7.25*key["size"] + offsety + shifty + partialscale*(y+1))*scale
            if p == partial:
                keycolor = key_colors["main"][1]
                textcolor = "#FFFFFF"
            elif ((p == -partial or p == -partial-1) and partial != -1) or (p == 0 and partial == -1):
                keycolor = key_colors["trilled"]
                textcolor = "#AA22FF"
            else:
                keycolor = key_colors["main"][0]
                textcolor = "#000000"
            C.create_oval(x1, y1, x2, y2, fill=keycolor, width=0, tags=("clickable", "partial", str(p)))
            C.create_text((x1+x2)/2, (y1+y2)/2, text=text_string, font=("Arial", int(textscale*text_size*scale), "bold"), fill=textcolor, tags=("clickable", "partial", str(p)))
            if p >= 8 and p <= 15:
                C.create_text((x1+x2)/2, (key["y"] - 7.25*key["size"] + offsety + shifty + partialscale*4.2)*scale, text=str(int(round(1200*math.log(p/8, 2), 0)))+"c", font=("Arial", int(textscale*text_size*scale*(5/6)), "bold"), fill="#FFFFFF", tags=("partial"))
            elif p == 0:
                C.create_text((key["x"]-16*key["size"]+offsetx+shiftx+partialscale*4)*scale, (key["y"]-7.25*key["size"]+offsety+shifty+partialscale*-0.5)*scale, text="partials", font=("Arial", int(textscale*text_size*scale*2), "bold"), fill="#FFFFFF", tags=("partial"))

    # IF DIAGRAM HAS SPOSITIONS
    elif "sposition" in key["type"]:
        minimum = key["min"]
        maximum = key["max"]
        x1 = (key["x1"] + offsetx + shiftx)*scale
        y1 = (key["y1"] + offsety + shifty)*scale
        x2 = (key["x2"] + offsetx + shiftx)*scale
        y2 = (key["y2"] + offsety + shifty)*scale
        C.create_rectangle(x1, y1, x2, y2, fill=key_colors["main"][0], width=0, tags=("clickable", key["type"], key["type"]+"right", str(x1), str(x2), minimum, maximum))
        if FINGTYPE == "trill":
            x_position = x1 + ((x2-x1)/(maximum-minimum))*(state.real - minimum)
            C.create_rectangle(x1, y1, x_position, y2, fill=key_colors["main"][1], width=0, tags=("clickable", key["type"], key["type"]+"left", str(x1), str(x2), minimum, maximum))
            if round(state.real, 6) != round(state.imag, 6):
                tr_position = x1 + ((x2-x1)/(maximum-minimum))*(state.imag - minimum)
                C.create_rectangle(x1, y1, tr_position, y2, fill=key_colors["trilled"], width=0, tags=("clickable", key["type"], key["type"]+"trill", str(x1), str(x2), minimum, maximum))

            C.create_rectangle((x1+x2)/2 + 0.25*scale, y2 + 0.5*scale, (x1+x2)/2 + 5.5*scale, y2 + 3.5*scale, fill=(key_colors["model"][0] if key["type"]+"number" in select else key_colors["main"][0]), width=0, tags=("clickable", key["type"], key["type"]+"number", minimum, maximum))
            C.create_text((x1+x2)/2 + 2.875*scale, y2 + 2*scale, text=tempvar if key["type"]+"number" in select and tempvar != "" in select else round(state.real, 2), font=("Arial", int(textscale*scale*1.25), "bold"), fill="#000000", tags=("clickable", key["type"], key["type"]+"number", minimum, maximum))
            C.create_rectangle((x1+x2)/2 - 5.5*scale, y2 + 0.5*scale, (x1+x2)/2 - 0.25*scale, y2 + 3.5*scale, fill=(key_colors["model"][0] if key["type"]+"trillnum" in select else key_colors["main"][0]), width=0, tags=("clickable", key["type"], key["type"]+"trillnum", minimum, maximum))
            C.create_text((x1+x2)/2 - 2.875*scale, y2 + 2*scale, text=tempvar if key["type"]+"trillnum" in select and tempvar != "" in select else round(state.imag, 2), font=("Arial", int(textscale*scale*1.25), "bold"), fill="#000000", tags=("clickable", key["type"], key["type"]+"trillnum", minimum, maximum))

        else:
            x_position = x1 + ((x2-x1)/(maximum-minimum))*(state.real - minimum)
            C.create_rectangle(x1, y1, x_position, y2, fill=key_colors["main"][1], width=0, tags=("clickable", key["type"], key["type"]+"left", str(x1), str(x2), minimum, maximum))

            C.create_rectangle((x1+x2)/2 - 3*scale, y2 + 0.5*scale, (x1+x2)/2 + 3*scale, y2 + 3.5*scale, fill=(key_colors["model"][0] if key["type"]+"number" in select else key_colors["main"][0]), width=0, tags=("clickable", key["type"], key["type"]+"number", minimum, maximum))
            C.create_text((x1+x2)/2, y2 + 2*scale, text=tempvar if key["type"]+"number" in select and tempvar != "" in select else round(state.real, 2), font=("Arial", int(textscale*scale*1.25), "bold"), fill="#000000", tags=("clickable", key["type"], key["type"]+"number", minimum, maximum))

        if key["preset"] == "trombone":
            t = 1
            if FINGERING[0] == 8: # Eb trigger alone (G)
                multiplier = 2**(3/12)
                pos = minimum - (3 - 3)
            elif FINGERING[0] == 16: # D trigger alone (Gb)
                multiplier = 2**(4/12)
                pos = minimum - (4 - 4)
            elif FINGERING[0] == 2: # F trigger
                multiplier = 2**(5/12)
                pos = minimum - (5 - 5)
            elif FINGERING[0] == 4: # F trigger set to E-*
                multiplier = 2**(5.715/12)
                pos = minimum - (6 - 5.715)
            elif FINGERING[0] == 10: # Eb trigger
                multiplier = 2**(7/12)
                pos = minimum - (7 - 7)
            elif FINGERING[0] == 18: # D trigger
                multiplier = 2**(8/12)
                pos = minimum - (8 - 8)
            else: # no triggers, or invalid trigger combination
                multiplier = 1
                pos = minimum
                
            while pos <= (maximum-0.25):
                if pos < minimum:
                    pos += multiplier
                    continue

                if FINGERING[0] == 8: # Eb trigger alone (G)
                    position_text = "G"+str(t)
                elif FINGERING[0] == 16: # D trigger alone (Gb)
                    position_text = "Gb"+str(t)
                elif FINGERING[0] == 2: # F trigger
                    position_text = "F"+str(t)
                elif FINGERING[0] == 4: # F trigger set to E-*
                    position_text = "E"+str(t)+"*"
                elif FINGERING[0] == 10: # Eb trigger
                    position_text = "Eb"+str(t)
                elif FINGERING[0] == 18: # D trigger
                    position_text = "D"+str(t)
                else: # no triggers, or invalid trigger combination
                    multiplier = 1
                    position_text = str(t)
                
                xpos = x1 + ((x2-x1)/(maximum-minimum))*(pos - minimum)
                
                C.create_oval(xpos - 1.5*scale, y1 - 0.5*scale, xpos + 1.5*scale, y1 - 3.5*scale, fill=key_colors["main"][0], width=0, tags=("clickable", key["type"], key["type"]+"setto", pos))
                C.create_text(xpos, y1 - 2*scale, text=position_text, font=("Arial", int(textscale*scale*1.15), "bold"), fill="#000000", tags=("clickable", key["type"], key["type"]+"setto", pos))
                
                t += 1
                pos += multiplier
                
        elif key["preset"] == "trumpet":
            for pos in range(3):
                position_text = "0¼½"[pos]
                pos /= 4
                xpos = x1 + ((x2-x1)/(maximum-minimum))*(pos - minimum) 
                C.create_oval(xpos - 1*scale, y1 - 0.5*scale, xpos + 1*scale, y1 - 2.5*scale, fill=key_colors["main"][0], width=0, tags=("clickable", key["type"], key["type"]+"setto", pos))
                C.create_text(xpos, y1 - 1.5*scale, text=position_text, font=("Arial", int(textscale*scale*1.15), "bold"), fill="#000000", tags=("clickable", key["type"], key["type"]+"setto", pos))
    
    else:
        if state == 3:
            keycolor = key_colors["trilled"]
            textcolor = "#AA22FF"
        elif state == 0:
            keycolor = key_colors[key["type"]][state]
            textcolor = "#000000"
        else:
            keycolor = key_colors[key["type"]][state]
            textcolor = "#FFFFFF"
        x1 = (key["x1"] + offsetx + shiftx)*scale
        y1 = (key["y1"] + offsety + shifty)*scale
        x2 = (key["x2"] + offsetx + shiftx)*scale
        y2 = (key["y2"] + offsety + shifty)*scale
        if key["halfable"]:
            C.create_oval(x1, y1, x2, y2, fill=keycolor, width=0, tags=("clickable", "key", str(keynum), "halfable"))
            C.create_text((x1+x2)/2, (y1+y2)/2, text=key["label"], font=("Arial", int(textscale*key["labelsize"]*scale*1.25), "bold"), fill=textcolor, tags=("clickable", "key", str(keynum), "halfable"))
        else:
            C.create_oval(x1, y1, x2, y2, fill=keycolor, width=0, tags=("clickable", "key", str(keynum)))
            C.create_text((x1+x2)/2, (y1+y2)/2, text=key["label"], font=("Arial", int(textscale*key["labelsize"]*scale*1.25), "bold"), fill=textcolor, tags=("clickable", "key", str(keynum)))
    
# RENDER FINGERING
def render_fingering(key_system, fingering=FINGERING, select=SELECT, tempvar=TEMPVAR):
    global FINGTYPE
    C.delete("key")
    C.delete("partial")
    C.delete("fingeringhelp")
    C.delete("sposition1")
    C.delete("sposition2")

    DESCRIPTION.delete(1.0, END)
    DESCRIPTION.insert(END, FINGERING[-1])

    parameters = key_systems[key_system]["parameters"]

    Lx = (parameters["Lx"]+parameters["offsetx"])*scale; Ly = (parameters["Ly"]+parameters["offsety"])*scale
    Mx = (parameters["Mx"]+parameters["offsetx"]+parameters["shiftx"])*scale; My = (parameters["My"]+parameters["offsety"]+parameters["shifty"])*scale
    Bx = (parameters["Bx"]+parameters["offsetx"]+parameters["shiftx"])*scale; By = (parameters["By"]+parameters["offsety"])*scale
    Rx = (parameters["Rx"]+parameters["offsetx"])*scale; Ry = (parameters["Ry"]+parameters["offsety"])*scale
    Descy = (parameters["Descy"]+parameters["offsety"])*scale

    C.create_rectangle(Lx, Ly, Rx, Ry, fill="#EE2266", width=0, tags=("key")) 
    C.create_rectangle(Lx, Ly, max(Mx, Bx), My, fill="#5588BB", width=0, tags=("key"))
    C.create_rectangle(Lx, Ly, min(Mx, Bx), By, fill="#5588BB", width=0, tags=("key"))

    f = list(bin(fingering[0]))[2:]
    h = list(bin(fingering[1]))[2:]
    t = list(bin(fingering[2]))[2:]
    while len(f) < parameters["keys"]:
        f.insert(0, "0")
    while len(h) < parameters["keys"]:
        h.insert(0, "0")
    while len(t) < parameters["keys"]:
        t.insert(0, "0")
    states = []
    for key in range(parameters["keys"]):
        if key_systems[key_system][parameters["keys"] - 1 - key]["type"] == "sposition1":
            states.insert(0, fingering[4])
        elif key_systems[key_system][parameters["keys"] - 1 - key]["type"] == "sposition2":
            states.insert(0, fingering[5])
        elif int(t[key]) == 1:
            states.insert(0, 3)
        else:
            states.insert(0, int(f[key])+int(h[key]))
    for key in range(parameters["keys"]):
        render_key(key_systems[key_system][key], key, parameters["offsetx"], parameters["offsety"], parameters["shiftx"], parameters["shifty"], states[key], fingering[3], select, tempvar)

    C.create_rectangle(Lx, max(Ly, Ry), Rx, Descy, fill="#000000", width=0, tags=("key"))
    desc_string = ""
    for key, state in enumerate(states):
        descname = key_systems[key_system][key]["descname"]
        if key == parameters["LR_split"]:
            desc_string += parameters["separator"]
        if isinstance(state, complex):
            if FINGTYPE != "trill" or round(state.real, 6) == round(state.imag, 6):
                desc_string += "{"+str(round(state.real, 2))+"} "
            else:
                desc_string += "[{"+str(round(state.real, 2))+"}{"+str(round(state.imag, 2))+"}] "
        elif state == 3:
            if len(descname) >= 1 and descname[0] == "⌫":
                desc_string = desc_string[:-1] if len(desc_string) >= 1 and desc_string[-1] == "−" else desc_string
                descname = descname[1:]
            desc_string += "["+descname.strip()+"]"
        elif state == 2:
            desc_string += "½ " if descname[-1] == " " else (" ½" if descname[0] == " " else "½")
        elif state == 1:
            if len(descname) >= 1 and descname[0] == "⌫":
                desc_string = desc_string[:-1] if len(desc_string) >= 1 and desc_string[-1] == "−" else desc_string
                descname = descname[1:]
            desc_string += descname
        elif state == 0:
            desc_string += key_systems[key_system][key]["descoff"]
    if fingering[3] == -17:
        desc_string += "[" + circlednums[16] + "]"
    elif fingering[3] == -1:
        desc_string += "[" + circlednums[0] + "]"
    elif fingering[3] >= 0:
        desc_string += circlednums[fingering[3]]
    elif fingering[3] <= -2:
        desc_string += "[" + circlednums[-fingering[3]-1] + circlednums[-fingering[3]] + "]"
    C.create_text((Lx+Rx)/2, (max(Ly, Ry)+Descy)/2, text=desc_string, font=("Arial", int(textscale*scale*1.5*min(1, 75/max(1, len(desc_string)))), "bold"), fill="#FFFFFF", tags=("key"))

    C.create_text((parameters["Lx"]+parameters["offsetx"]+8.4)*scale, (min(parameters["Ly"], parameters["Ry"])+parameters["offsety"]+1.9)*scale, text="Right-click to half-press\nMiddle-click to trill", font=("Arial", int(textscale*scale*1), "bold"), fill="#FFFFFF", tags=("key"))
    C.create_oval(72*scale, 3*scale, 75*scale, 6*scale, fill=colors["dark_description_background"], width=0, tags=("clickable", "fingeringhelp"))
    C.create_text(73.5*scale, 4.5*scale, text="?", font=("Arial", int(textscale*scale*1.5), "bold"), fill="#FFFFFF", tags=("clickable", "fingeringhelp"))
    
# RENDER PITCHES
def render_pitches(pitches=[440.0], fingtype="note", select="", tempvar="", transpose=0, tonic=440.0, tet=12):
    C.delete("pitch")
    C.delete("fingtype")
    C.delete("pitchhelp")
    C.create_rectangle(2*scale, 46*scale, 76*scale, 65*scale, fill=colors["pitch_background"], width=0, tags=("pitch"))
    C.create_rectangle(2*scale, 65*scale, 76*scale, 70*scale, fill="#000000", width=0, tags=("pitch"))

    # FINGERING TYPE
    C.create_text(10*scale, 48.5*scale, text="Fingering type:", font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF", tags=("fingtype"))
    C.create_rectangle(18*scale, 47*scale, 30*scale, 50*scale, fill=("#000000" if fingtype == "note" else "#FFFFFF"), width=0, tags=("clickable", "fingtype", "note"))
    C.create_text(24*scale, 48.5*scale, text="Note/Microtone", font=("Arial", int(textscale*scale*6/5), "bold"), fill=("#FFFFFF" if fingtype == "note" else "#000000"), tags=("clickable", "fingtype", "note"))
    C.create_rectangle(30.5*scale, 47*scale, 42.5*scale, 50*scale, fill=("#000000" if fingtype == "trill" else "#FFFFFF"), width=0, tags=("clickable", "fingtype", "trill"))
    C.create_text(36.5*scale, 48.5*scale, text="Trill/Tremolo", font=("Arial", int(textscale*scale*6/5), "bold"), fill=("#FFFFFF" if fingtype == "trill" else "#000000"), tags=("clickable", "fingtype", "trill"))
    C.create_rectangle(43*scale, 47*scale, 55*scale, 50*scale, fill=("#000000" if "multi" in fingtype else "#FFFFFF"), width=0, tags=("clickable", "fingtype", "multi"))
    C.create_text(49*scale, 48.5*scale, text="Multiphonic", font=("Arial", int(textscale*scale*6/5), "bold"), fill=("#FFFFFF" if "multi" in fingtype else "#000000"), tags=("clickable", "fingtype", "multi"))
    if "multi" in fingtype:
        C.create_text(60.5*scale, 48.5*scale, text="Pitches:", font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF", tags=("fingtype"))
        C.create_rectangle(65*scale, 47*scale, 68*scale, 50*scale, fill=("#000000" if fingtype == "multi2" else "#FFFFFF"), width=0, tags=("clickable", "fingtype", "multi2"))
        C.create_text(66.5*scale, 48.5*scale, text="2", font=("Arial", int(textscale*scale*4/3), "bold"), fill=("#FFFFFF" if fingtype == "multi2" else "#000000"), tags=("clickable", "fingtype", "multi2"))
        C.create_rectangle(68.5*scale, 47*scale, 71.5*scale, 50*scale, fill=("#000000" if fingtype == "multi3" else "#FFFFFF"), width=0, tags=("clickable", "fingtype", "multi3"))
        C.create_text(70*scale, 48.5*scale, text="3", font=("Arial", int(textscale*scale*4/3), "bold"), fill=("#FFFFFF" if fingtype == "multi3" else "#000000"), tags=("clickable", "fingtype", "multi3"))
        C.create_rectangle(72*scale, 47*scale, 75*scale, 50*scale, fill=("#000000" if fingtype == "multi4" else "#FFFFFF"), width=0, tags=("clickable", "fingtype", "multi4"))
        C.create_text(73.5*scale, 48.5*scale, text="4", font=("Arial", int(textscale*scale*4/3), "bold"), fill=("#FFFFFF" if fingtype == "multi4" else "#000000"), tags=("clickable", "fingtype", "multi4"))
    else:
         C.create_text(66*scale, 48.5*scale, text=" Select a box to change pitch by\ntyping it in or using arrow keys", font=("Arial", int(textscale*scale*0.95), "bold"), fill="#FFFFFF", tags=("fingtype"))
        
    # PITCHES
    for p, pitch in enumerate(pitches):
        C.create_text((7.1*scale if fingtype == "note" else 6.4*scale), (52 + 3.5*p)*scale, text=("Pitch:" if fingtype == "note" else "Pitch "+str(p+1)+":"), font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF", tags=("pitch"))

        C.create_rectangle(10.5*scale, (50.5 + 3.5*p)*scale, 17.5*scale, (53.5 + 3.5*p)*scale, fill=(colors["pitch_selected"] if select == "freq"+str(p+1) else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "freq"+str(p+1)))
        C.create_text(14*scale, (52 + 3.5*p)*scale, text=(tempvar if select == "freq"+str(p+1) and tempvar != "" else round(pitch, 2)), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "freq"+str(p+1)))
        C.create_text(19.3*scale, (52 + 3.5*p)*scale, text="Hz", font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF", tags=("pitch"))

        C.create_rectangle(22*scale, (50.5 + 3.5*p)*scale, 26*scale, (53.5 + 3.5*p)*scale, fill=(colors["pitch_selected"] if select == "notename"+str(p+1) else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "notename"+str(p+1)))
        C.create_text(24*scale, (52 + 3.5*p)*scale, text=(tempvar if select == "notename"+str(p+1) and tempvar != "" else notename(pitch, transpose)[0]), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "notename"+str(p+1)))
        C.create_rectangle(26.5*scale, (50.5 + 3.5*p)*scale, 32.5*scale, (53.5 + 3.5*p)*scale, fill=(colors["pitch_selected"] if select == "centsdev"+str(p+1) else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "centsdev"+str(p+1)))
        C.create_text(29.5*scale, (52 + 3.5*p)*scale, text=(tempvar if select == "centsdev"+str(p+1) and tempvar != "" else plusminus(round(notename(pitch, transpose)[1], 2))), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "centsdev"+str(p+1)))

        C.create_text(37.5*scale, (52 + 3.5*p)*scale, text="(concert", font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF", tags=("pitch"))
        C.create_rectangle(42.5*scale, (50.5 + 3.5*p)*scale, 46.5*scale, (53.5 + 3.5*p)*scale, fill=(colors["pitch_selected"] if select == "concertname"+str(p+1) else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "concertname"+str(p+1)))
        C.create_text(44.5*scale, (52 + 3.5*p)*scale, text=(tempvar if select == "concertname"+str(p+1) and tempvar != "" else notename(pitch, 0)[0]), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "concertname"+str(p+1)))
        C.create_rectangle(47*scale, (50.5 + 3.5*p)*scale, 53*scale, (53.5 + 3.5*p)*scale, fill=(colors["pitch_selected"] if select == "concertdev"+str(p+1) else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "concertdev"+str(p+1)))
        C.create_text(50*scale, (52 + 3.5*p)*scale, text=(tempvar if select == "concertdev"+str(p+1) and tempvar != "" else plusminus(round(notename(pitch, 0)[1], 2))), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "concertdev"+str(p+1)))
        C.create_text(53.5*scale, (52 + 3.5*p)*scale, text=")", font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF", tags=("pitch"))

        tup = colorsys.hsv_to_rgb(math.log(pitch/tonic, 2) % 1, 0.5, (math.sin(2*math.pi*(math.log(pitch/tonic, 2) % 1 - 3/5))/12) + (5/12))
        hx = []
        for elem in tup:
            if int(elem*255) <= 15:
                hx.append("0"+((str(hex(int(elem*255))).upper()+"d")[2:-1]))
            else:
                hx.append((str(hex(int(elem*255))).upper()+"d")[2:-1])
        pitchcolor = "#"+"".join(hx)

        C.create_rectangle(55*scale, (50.5 + 3.5*p)*scale, 75*scale, (53.5 + 3.5*p)*scale, fill=pitchcolor, width=0, tags=("pitch"))
        C.create_text(65*scale, (52 + 3.5*p)*scale, text=str(int(round(tet*math.log(pitch/tonic, 2), 0)) % tet) + "\\" + str(TET) + " " + plusminus(round(100 * (tet*math.log(pitch/tonic, 2) - round(tet*math.log(pitch/tonic, 2), 0) + 0.0000000001), 2)) + "%", font=("Arial", int(textscale*scale*7/4), "bold"), fill="#FFFFFF", tags=("pitch"))

    # TONIC
    C.create_text(6.9*scale, 67.5*scale, text=("Tonic:"), font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF", tags=("pitch"))

    C.create_rectangle(10.5*scale, 66*scale, 17.5*scale, 69*scale, fill=(colors["pitch_selected"] if select == "freq0" else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "freq0"))
    C.create_text(14*scale, 67.5*scale, text=(tempvar if select == "freq0" and tempvar != "" else round(tonic, 2)), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "freq0"))
    C.create_text(19.3*scale, 67.5*scale, text="Hz", font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF", tags=("pitch"))

    C.create_rectangle(22*scale, 66*scale, 26*scale, 69*scale, fill=(colors["pitch_selected"] if select == "notename0" else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "notename0"))
    C.create_text(24*scale, 67.5*scale, text=(tempvar if select == "notename0" and tempvar != "" else notename(tonic, transpose)[0]), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "notename0"))
    C.create_rectangle(26.5*scale, 66*scale, 32.5*scale, 69*scale, fill=(colors["pitch_selected"] if select == "centsdev0" else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "centsdev0"))
    C.create_text(29.5*scale, 67.5*scale, text=(tempvar if select == "centsdev0" and tempvar != "" else plusminus(round(notename(tonic, transpose)[1], 2))), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "centsdev0"))

    C.create_text(37.5*scale, 67.5*scale, text="(concert", font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF", tags=("pitch"))
    C.create_rectangle(42.5*scale, 66*scale, 46.5*scale, 69*scale, fill=(colors["pitch_selected"] if select == "concertname0" else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "concertname0"))
    C.create_text(44.5*scale, 67.5*scale, text=(tempvar if select == "concertname0" and tempvar != "" else notename(tonic, 0)[0]), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "concertname0"))
    C.create_rectangle(47*scale, 66*scale, 53*scale, 69*scale, fill=(colors["pitch_selected"] if select == "concertdev0" else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "concertdev0"))
    C.create_text(50*scale, 67.5*scale, text=(tempvar if select == "concertdev0" and tempvar != "" else plusminus(round(notename(tonic, 0)[1], 2))), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "concertdev0"))
    C.create_text(53.5*scale, 67.5*scale, text=")", font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF", tags=("pitch"))

    C.create_rectangle(63*scale, 65.75*scale, 69*scale, 69.25*scale, fill=(colors["pitch_selected"] if select == "tet" else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "tet"))
    C.create_text(66*scale, 67.5*scale, text=(tempvar if select == "tet" and tempvar != "" else tet), font=("Arial", int(textscale*scale*7/4), "bold"), fill="#000000", tags=("clickable", "pitch", "tet"))
    C.create_text(72*scale, 67.5*scale, text="TET", font=("Arial", int(textscale*scale*7/4), "bold"), fill="#FFFFFF", tags=("pitch"))

    C.create_oval(56.75*scale, 66*scale, 59.75*scale, 69*scale, fill=key_colors["second"][0], width=0, tags=("clickable", "pitchhelp"))
    C.create_text(58.25*scale, 67.5*scale, text="?", font=("Arial", int(textscale*scale*1.5), "bold"), fill="#000000", tags=("clickable", "pitchhelp"))

# RENDER OPTIONS
def render_options(instrument=INSTRUMENT, database=DATABASE, setinstrument=False, select=SELECT, tempvar=TEMPVAR):
    global TET
    
    DBASEDESC.delete(1.0, END)
    DBASEDESC.insert(END, DATABASE[0][4])

    C.delete("options")
    C.create_rectangle(78*scale, 2*scale, 190*scale, 19.5*scale, fill=colors["options_background"], width=0, tags=("options"))

    C.create_rectangle(79*scale, 3*scale, 99*scale, 7*scale, fill=colors["options_database"], width=0, tags=("clickable", "options", "addentry"))
    C.create_text(89*scale, 5*scale, text="ADD ENTRY", font=("Arial", int(textscale*scale*1.75), "bold"), fill="#FFFFFF", tags=("clickable", "options", "addentry"))

    C.create_rectangle(79*scale, 8*scale, 99*scale, 12*scale, fill=colors["options_database"], width=0, tags=("clickable", "options", "removeentry"))
    C.create_text(89*scale, 10*scale, text="REMOVE ENTRY", font=("Arial", int(textscale*scale*1.75), "bold"), fill="#FFFFFF", tags=("clickable", "options", "removeentry"))

    C.create_rectangle(79*scale, 13*scale, 99*scale, 18.5*scale, fill="#AA55CC", width=0, tags=("clickable", "options", "copytoclipboard"))
    C.create_text(89*scale, 15.75*scale, text="      Copy to\nclipboard", font=("Arial", int(textscale*scale*1.5), "bold"), fill="#FFFFFF", tags=("clickable", "options", "copytoclipboard"))

    C.create_rectangle(169*scale, 13*scale, 189*scale, 18.5*scale, fill="#AA55CC", width=0, tags=("clickable", "options", "pastefromclipboard"))
    C.create_text(179*scale, 15.75*scale, text="Paste from\n     clipboard", font=("Arial", int(textscale*scale*1.5), "bold"), fill="#FFFFFF", tags=("clickable", "options", "pastefromclipboard"))

    C.create_rectangle(169*scale, 3*scale, 189*scale, 7*scale, fill=colors["options_database"], width=0, tags=("clickable", "options", "loadfile"))
    C.create_text(179*scale, 5*scale, text="LOAD FILE", font=("Arial", int(textscale*scale*1.75), "bold"), fill="#FFFFFF", tags=("clickable", "options", "loadfile"))

    C.create_rectangle(169*scale, 8*scale, 189*scale, 12*scale, fill=colors["options_database"], width=0, tags=("clickable", "options", "savefile"))
    C.create_text(179*scale, 10*scale, text="SAVE FILE", font=("Arial", int(textscale*scale*1.75), "bold"), fill="#FFFFFF", tags=("clickable", "options", "savefile"))

    C.create_text(134*scale, 5*scale, text=database[0][0], font=("Arial", int(textscale*scale*2), "bold"), fill="#FFFFFF", tags=("options"))

    if setinstrument == "set":
        C.create_rectangle(100*scale, 8*scale, 133.5*scale, 12*scale, fill=colors["set_instrument"], width=0, tags=("clickable", "options", "cancelsetinstrument"))
        C.create_text(116.75*scale, 10*scale, text="CANCEL", font=("Arial", int(textscale*scale*1.75), "bold"), fill="#000000", tags=("clickable", "options", "cancelsetinstrument"))

        C.create_text(150.75*scale, 10*scale, text="Warning: changing instruments\nwill erase the current database", font=("Arial", int(textscale*scale*1.375), "bold"), fill="#FFFFFF", tags=("clickable", "options"))

    elif setinstrument == "edit":
        C.create_rectangle(100*scale, 8*scale, 110*scale, 12*scale, fill=colors["set_instrument"], width=0, tags=("clickable", "options", "confirminstrument"))
        C.create_text(105*scale, 10*scale, text="DONE", font=("Arial", int(textscale*scale*1.75), "bold"), fill="#000000", tags=("clickable", "options", "confirminstrument"))

        C.create_text(137.75*scale, 10*scale, text="Transp:", font=("Arial", int(textscale*scale*1.5), "bold"), fill="#FFFFFF", tags=("options"))

        C.create_rectangle(142*scale, 8.5*scale, 149.5*scale, 11.5*scale, fill=key_colors["model"][0] if select == "edittranspose" else "#FFFFFF", width=0, tags=("clickable", "options", "edittranspose"))
        C.create_text(145.75*scale, 10*scale, text=tempvar if select == "edittranspose" and tempvar != "" else plusminus(round(100*instruments[instrument][1], 2)), font=("Arial", int(textscale*scale*4/3), "bold"), fill="#000000", tags=("clickable", "options", "edittranspose"))

        C.create_text(153.5*scale, 10*scale, text="cents (", font=("Arial", int(textscale*scale*1.5), "bold"), fill="#FFFFFF", tags=("options"))

        C.create_rectangle(157*scale, 8.5*scale, 163.5*scale, 11.5*scale, fill=key_colors["model"][0] if select == "edittranssteps" else "#FFFFFF", width=0, tags=("clickable", "options", "edittranssteps"))
        C.create_text(160.25*scale, 10*scale, text=tempvar if select == "edittranssteps" and tempvar != "" else plusminus(round(12/TET * instruments[instrument][1], 2)), font=("Arial", int(textscale*scale*4/3), "bold"), fill="#000000", tags=("clickable", "options", "edittranssteps"))

        C.create_text(166*scale, 10*scale, text="\\" + str(TET) + ")", font=("Arial", int(textscale*scale*1.5), "bold"), fill="#FFFFFF", tags=("options"))
        
    else:
        C.create_rectangle(100*scale, 8*scale, 133.5*scale, 12*scale, fill=colors["set_instrument"], width=0, tags=("clickable", "options", "selectinstrument"))
        if "Custom" in instrument:
            C.create_text(116.75*scale, 10*scale, text="Custom: " + key_systems["custom"]["name"], font=("Arial", int(textscale*scale*1.5) if len(key_systems["custom"]["name"]) <= 15 else int(scale*1.375), "bold"), fill="#000000", tags=("clickable", "options", "selectinstrument"))
        else:
            C.create_text(116.75*scale, 10*scale, text="Instrument: " + instrument, font=("Arial", int(textscale*scale*1.5) if len(instrument) <= 15 else int(scale*1.375), "bold"), fill="#000000", tags=("clickable", "options", "selectinstrument"))

        transposition = int(round(instruments[instrument][1]*100, 2)) if round(instruments[instrument][1]*100, 2) == int(round(instruments[instrument][1]*100, 2)) else round(instruments[instrument][1]*100, 2)
        C.create_text(150.75*scale, 10*scale, text="Transposition: "+plusminus(transposition) + " cents", font=("Arial", int(textscale*scale*1.5), "bold"), fill="#FFFFFF", tags=("clickable", "options"))\


# FILTERS

# Fingtype filter:
#   note
#   trill
#   multi
# TET filter:
#   filter off
#   at least one note in TET
#   all notes in TET

# Fingering search:
#   main fingering match (excl. half, partial; including both in trill)
#   all aspects match (fingering, half, trill, partial)
# Pitch search:
#   at least one pitch matches
#   all pitches match

def render_filters(filters=FILTERS, tet=TET, select=SELECT, tempvar=TEMPVAR):
    C.delete("filters")
    C.delete("filterbackground")
    C.delete("filtershelp")
    C.delete("tolerance")
    C.create_rectangle(2*scale, 72*scale, 76*scale, 88*scale, fill=colors["filters_background"], width=0, tags=("filterbackground"))

    # FINGTYPE FILTER
    C.create_text(14.5*scale, 74.5*scale, text="Filter for fingering type:", font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF", tags=("filterbackground"))
    C.create_rectangle(26.5*scale, 73*scale, 38.5*scale, 76*scale, fill=("#000000" if "note" in filters["fingtype"] else "#FFFFFF"), width=0, tags=("clickable", "filters", "fingtypef", "note"))
    C.create_text(32.5*scale, 74.5*scale, text="Note/Microtone", font=("Arial", int(textscale*scale*6/5), "bold"), fill=("#FFFFFF" if "note" in filters["fingtype"] else "#000000"), tags=("clickable", "filters", "fingtypef", "note"))
    C.create_rectangle(39*scale, 73*scale, 51*scale, 76*scale, fill=("#000000" if "trill" in filters["fingtype"] else "#FFFFFF"), width=0, tags=("clickable", "filters", "fingtypef", "trill"))
    C.create_text(45*scale, 74.5*scale, text="Trill/Tremolo", font=("Arial", int(textscale*scale*6/5), "bold"), fill=("#FFFFFF" if "trill" in filters["fingtype"] else "#000000"), tags=("clickable", "filters", "fingtypef", "trill"))
    C.create_rectangle(51.5*scale, 73*scale, 63.5*scale, 76*scale, fill=("#000000" if "multi" in filters["fingtype"] else "#FFFFFF"), width=0, tags=("clickable", "filters", "fingtypef", "multi"))
    C.create_text(57.5*scale, 74.5*scale, text="Multiphonic", font=("Arial", int(textscale*scale*6/5), "bold"), fill=("#FFFFFF" if "multi" in filters["fingtype"] else "#000000"), tags=("clickable", "filters", "fingtypef", "multi"))

    # TET FILTER
    C.create_text(14.25*scale, 78*scale, text="Filter for pitches in TET:", font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF", tags=("filterbackground"))
    C.create_rectangle(26.5*scale, 76.5*scale, 38.5*scale, 79.5*scale, fill=("#000000" if filters["tet"] == "none" else "#FFFFFF"), width=0, tags=("clickable", "filters", "tetf", "none"))
    C.create_text(32.5*scale, 78*scale, text="No filter", font=("Arial", int(textscale*scale*6/5), "bold"), fill=("#FFFFFF" if filters["tet"] == "none" else "#000000"), tags=("clickable", "filters", "tetf", "none"))
    C.create_rectangle(39*scale, 76.5*scale, 51*scale, 79.5*scale, fill=("#000000" if filters["tet"] == "part" else "#FFFFFF"), width=0, tags=("clickable", "filters", "tetf", "part"))
    C.create_text(45*scale, 78*scale, text="At least 1 in TET", font=("Arial", int(textscale*scale*6/5), "bold"), fill=("#FFFFFF" if filters["tet"] == "part" else "#000000"), tags=("clickable", "filters", "tetf", "part"))
    C.create_rectangle(51.5*scale, 76.5*scale, 63.5*scale, 79.5*scale, fill=("#000000" if filters["tet"] == "all" else "#FFFFFF"), width=0, tags=("clickable", "filters", "tetf", "all"))
    C.create_text(57.5*scale, 78*scale, text="All in TET", font=("Arial", int(textscale*scale*6/5), "bold"), fill=("#FFFFFF" if filters["tet"] == "all" else "#000000"), tags=("clickable", "filters", "tetf", "all"))

    # FINGERING SEARCH
    C.create_text(15.75*scale, 82*scale, text="Search for fingering:", font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF", tags=("filterbackground"))
    C.create_rectangle(26.5*scale, 80.5*scale, 44.75*scale, 83.5*scale, fill=colors["searched"] if filters["search"] == "fingering_primary" else "#FFFFFF", width=0, tags=("clickable", "filters", "searchf", "fingering_primary"))
    C.create_text(35.625*scale, 82*scale, text="Match primary fingering", font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "filters", "searchf", "fingering_primary"))
    C.create_rectangle(45.25*scale, 80.5*scale, 63.5*scale, 83.5*scale, fill=colors["searched"] if filters["search"] == "fingering_exact" else "#FFFFFF", width=0, tags=("clickable", "filters", "searchf", "fingering_exact"))
    C.create_text(54.375*scale, 82*scale, text="Match exact fingering", font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "filters", "searchf", "fingering_exact"))

    # PITCH SEARCH
    C.create_text(16.5*scale, 85.5*scale, text="Search for pitches:", font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF", tags=("filterbackground"))
    C.create_rectangle(26.5*scale, 84*scale, 44.75*scale, 87*scale, fill=colors["searched"] if filters["search"] == "pitch_single" else "#FFFFFF", width=0, tags=("clickable", "filters", "searchf", "pitch_single"))
    C.create_text(35.625*scale, 85.5*scale, text="At least 1 pitch match", font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "filters", "searchf", "pitch_single"))
    C.create_rectangle(45.25*scale, 84*scale, 63.5*scale, 87*scale, fill=colors["searched"] if filters["search"] == "pitch_full" else "#FFFFFF", width=0, tags=("clickable", "filters", "searchf", "pitch_full"))
    C.create_text(54.375*scale, 85.5*scale, text="All pitches match", font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "filters", "searchf", "pitch_full"))

    # TOLERANCE
    C.create_text(70*scale, 79*scale, text="Tolerance", font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF", tags=("tolerance"))
    
    C.create_rectangle(65.5*scale, 80.5*scale, 72.5*scale, 83.5*scale, fill=key_colors["model"][0] if select == "tolerance_cents" else "#FFFFFF", width=0, tags=("clickable", "tolerance", "cents"))
    C.create_text(69*scale, 82*scale, text=tempvar if select == "tolerance_cents" and tempvar != "" else round((1200/tet)*filters["tolerance"], 2), font=("Arial", int(textscale*scale*11/8), "bold"), fill="#000000", tags=("clickable", "tolerance", "cents"))
    C.create_text(74*scale, 82*scale, text="c", font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF", tags=("tolerance"))

    C.create_rectangle(65.5*scale, 84*scale, 72.5*scale, 87*scale, fill=key_colors["model"][0] if select == "tolerance_percent" else "#FFFFFF", width=0, tags=("clickable", "tolerance", "percent"))
    C.create_text(69*scale, 85.5*scale, text=tempvar if select == "tolerance_percent" and tempvar != "" else round(100*filters["tolerance"], 2), font=("Arial", int(textscale*scale*11/8), "bold"), fill="#000000", tags=("clickable", "tolerance", "percent"))
    C.create_text(74*scale, 85.5*scale, text="%", font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF", tags=("tolerance"))

    C.create_oval(72*scale, 73*scale, 75*scale, 76*scale, fill=colors["searched"], width=0, tags=("clickable", "filtershelp"))
    C.create_text(73.5*scale, 74.5*scale, text="?", font=("Arial", int(textscale*scale*1.5), "bold"), fill="#000000", tags=("clickable", "filtershelp"))
    
                   
def render_database(instrument=INSTRUMENT, database=DATABASE, setinstrument=False, page=0, filters=FILTERS, select=SELECT, tempvar=TEMPVAR):
    global PAGE
    global NUM_PAGES
    global TET
    global FINGERING
    global FINGTYPE
    global PITCHES
    global SELECT
    global FILTERS_TEMP_FINGERING
    global FILTERS_TEMP_PITCHES
    global FILTERS_TEMP_FINGTYPE
    global EDITKEYS_ROWSPACING
    global EDITKEYS_TOPY
    global EDITKEYS_PER_PAGE
    
    C.delete("database")
    C.delete("setinstrument")
    C.delete("custom")
    C.delete("entry")
    
    if setinstrument == "set":
        percolumn = 23
        rowexpand = 2.875
        totalcolumns = 2
        for i, instrument2 in enumerate(instruments):
            transcents = round(instruments[instrument2][1]*100, 1)
            underscored_instrument = ""
            for letter in instrument2:
                if letter == " ":
                    underscored_instrument += "_"
                else:
                    underscored_instrument += letter
            transposition = " (Transpose: " + ("+" + str(transcents) if transcents > 0 else ("−" + str(-transcents) if transcents < 0 else "0")) + " cents)"
            
            if "Custom" not in instrument2:
                C.create_rectangle((78 + (112/totalcolumns)*int(i/percolumn))*scale, (21.75 + (i%percolumn)*rowexpand)*scale, (78 + (112/totalcolumns)*int(i/percolumn + 1))*scale, (21.75 + ((i%percolumn)+1)*rowexpand)*scale, fill=(colors["set_instrument"] if instrument2 == instrument else "#FFFFFF"), width=1, tags=("clickable", "setinstrument", underscored_instrument))
                C.create_text((78 + (112/totalcolumns)*(int(i/percolumn)+0.5))*scale, (21.75 + ((i%percolumn)+0.5)*rowexpand)*scale, text=instrument2 + transposition, font=("Arial", int(textscale*scale*11/8), "bold"), fill=("#000000"), tags=("clickable", "setinstrument", underscored_instrument))
            else:
                C.create_rectangle(78*scale, 90*scale, 190*scale, 97*scale, fill=(colors["set_instrument"] if len(instrument) >= 6 and instrument[0:6] == "custom" else "#FFFFFF"), width=1, tags=("clickable", "setinstrument", "Custom"))
                if key_systems["custom"]["parameters"]["keys"] == 0:
                    C.create_text(134*scale, 93.5*scale, text="SET CUSTOM INSTRUMENT", font=("Arial", int(textscale*scale*2), "bold"), fill=("#000000"), tags=("clickable", "setinstrument", underscored_instrument))
                else:
                    C.create_text(134*scale, 93.5*scale, text="Custom: " + key_systems["custom"]["name"] + transposition, font=("Arial", int(textscale*scale*2), "bold"), fill=("#000000"), tags=("clickable", "setinstrument", underscored_instrument))
        
    elif setinstrument == "edit":
        

        C.create_rectangle(78*scale, 21.5*scale, 190*scale, 97*scale, fill=colors["custom_background"], width=0, tags=("custom"))

        if platform.system() == "Darwin": # On Mac, the arrows are rendered too large
            extra_scale = 0.75
        else:
            extra_scale = 1

        C.create_rectangle(79*scale, 22.5*scale, 89*scale, 26*scale, fill="#949494", width=0, tags=("clickable", "custom", "editkeys", "addkey"))
        C.create_text(84*scale, 24.25*scale, text="ADD KEY", font=("Arial", int(textscale*scale*1.5), "bold"), fill=("#FFFFFF"), tags=("clickable", "custom", "editkeys", "addkey"))

        # SECTION SPLIT
        C.create_text(96.5*scale, 24.25*scale, text="Section split", font=("Arial", int(textscale*scale*1.5), "bold"), fill=("#FFFFFF"), tags=("custom"))
        C.create_rectangle(103.5*scale, 22.5*scale, 108*scale, 26*scale, fill=key_colors["model"][0] if select == "editlrsplit" else "#FFFFFF", width=0, tags=("clickable", "custom", "editlrsplit"))
        C.create_text(105.75*scale, 24.25*scale, text=tempvar if select == "editlrsplit" and tempvar != "" else key_systems["custom"]["parameters"]["LR_split"], font=("Arial", int(textscale*scale*3/2), "bold"), fill="#000000", tags=("clickable", "custom", "editlrsplit"))

        C.create_text(113.5*scale, 22.75*scale, text="separator", font=("Arial", int(textscale*scale*0.875), "bold"), fill=("#FFFFFF"), tags=("custom"))
        C.create_rectangle(110*scale, 23.75*scale, 113.5*scale, 26.25*scale, fill="#000000" if key_systems["custom"]["parameters"]["separator"] == " | " else "#FFFFFF", width=0, tags=("clickable", "custom", "separatoron"))
        C.create_text(111.75*scale, 25*scale, text="ON", font=("Arial", int(textscale*scale*1), "bold"), fill="#FFFFFF" if key_systems["custom"]["parameters"]["separator"] == " | " else "#000000", tags=("clickable", "custom", "separatoron"))
        C.create_rectangle(113.5*scale, 23.75*scale, 117*scale, 26.25*scale, fill="#000000" if key_systems["custom"]["parameters"]["separator"] == "" else "#FFFFFF", width=0, tags=("clickable", "custom", "separatoroff"))
        C.create_text(115.25*scale, 25*scale, text="OFF", font=("Arial", int(textscale*scale*1), "bold"), fill="#FFFFFF" if key_systems["custom"]["parameters"]["separator"] == "" else "#000000", tags=("clickable", "custom", "separatoroff"))

        C.create_text(120.5*scale, 22.75*scale, text="mid X1", font=("Arial", int(textscale*scale*0.875), "bold"), fill=("#FFFFFF"), tags=("custom"))
        C.create_rectangle(118*scale, 23.75*scale, 123*scale, 26.25*scale, fill=key_colors["model"][0] if select == "editmidx1" else "#FFFFFF", width=0, tags=("clickable", "custom", "editmidx1"))
        C.create_text(120.5*scale, 25*scale, text=tempvar if select == "editmidx1" and tempvar != "" else (int(round(4*key_systems["custom"]["parameters"]["Bx"], 2)) if int(round(4*key_systems["custom"]["parameters"]["Bx"], 2)) == round(4*key_systems["custom"]["parameters"]["Bx"], 2) else round(4*key_systems["custom"]["parameters"]["Bx"], 2)), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "custom", "editmidx1"))

        C.create_text(126.5*scale, 22.75*scale, text="mid X2", font=("Arial", int(textscale*scale*0.875), "bold"), fill=("#FFFFFF"), tags=("custom"))
        C.create_rectangle(124*scale, 23.75*scale, 129*scale, 26.25*scale, fill=key_colors["model"][0] if select == "editmidx2" else "#FFFFFF", width=0, tags=("clickable", "custom", "editmidx2"))
        C.create_text(126.5*scale, 25*scale, text=tempvar if select == "editmidx2" and tempvar != "" else (int(round(4*key_systems["custom"]["parameters"]["Mx"], 2)) if int(round(4*key_systems["custom"]["parameters"]["Mx"], 2)) == round(4*key_systems["custom"]["parameters"]["Mx"], 2) else round(4*key_systems["custom"]["parameters"]["Mx"], 2)), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "custom", "editmidx2"))

        C.create_text(132.5*scale, 22.75*scale, text="mid Y", font=("Arial", int(textscale*scale*0.875), "bold"), fill=("#FFFFFF"), tags=("custom"))
        C.create_rectangle(130*scale, 23.75*scale, 135*scale, 26.25*scale, fill=key_colors["model"][0] if select == "editmidy" else "#FFFFFF", width=0, tags=("clickable", "custom", "editmidy"))
        C.create_text(132.5*scale, 25*scale, text=tempvar if select == "editmidy" and tempvar != "" else (int(round(4*key_systems["custom"]["parameters"]["My"], 2)) if int(round(4*key_systems["custom"]["parameters"]["My"], 2)) == round(4*key_systems["custom"]["parameters"]["My"], 2) else round(4*key_systems["custom"]["parameters"]["My"], 2)), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "custom", "editmidy"))

        # PARTIALS
        C.create_text(140.5*scale, 24.25*scale, text="Partials", font=("Arial", int(textscale*scale*1.5), "bold"), fill=("#FFFFFF"), tags=("custom"))
        C.create_rectangle(145*scale, 22.5*scale, 150*scale, 26*scale, fill="#000000" if "partial" in key_systems["custom"]["special"] else "#FFFFFF", width=0, tags=("clickable", "custom", "partialson"))
        C.create_text(147.5*scale, 24.25*scale, text="ON", font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF" if "partial" in key_systems["custom"]["special"] else "#000000", tags=("clickable", "custom", "partialson"))
        C.create_rectangle(150*scale, 22.5*scale, 155*scale, 26*scale, fill="#000000" if "partial" not in key_systems["custom"]["special"] else "#FFFFFF", width=0, tags=("clickable", "custom", "partialsoff"))
        C.create_text(152.5*scale, 24.25*scale, text="OFF", font=("Arial", int(textscale*scale*3/2), "bold"), fill="#FFFFFF" if "partial" not in key_systems["custom"]["special"] else "#000000", tags=("clickable", "custom", "partialsoff"))
        
        C.create_oval(159.5*scale, 22.75*scale, 162.5*scale, 25.75*scale, fill="#DDDDDD", width=0, tags=("clickable", "custom", "editkeyshelp"))
        C.create_text(161*scale, 24.25*scale, text="?", font=("Arial", int(textscale*scale*1.5), "bold"), fill="#000000", tags=("clickable", "custom", "editkeyshelp"))
        
        # PAGE
        C.create_rectangle(167*scale, 22.5*scale, 170.5*scale, 26*scale, fill="#FFFFFF", width=1, tags=("clickable", "custom", "prevpage"))
        C.create_text(168.75*scale, 24.25*scale, text="◀", font=("Arial", int(textscale*scale*extra_scale*2.25), "bold"), fill=("#000000"), tags=("clickable", "custom", "prevpage"))

        C.create_rectangle(185.5*scale, 22.5*scale, 189*scale, 26*scale, fill="#FFFFFF", width=1, tags=("clickable", "custom", "nextpage"))
        C.create_text(187.25*scale, 24.25*scale, text="▶", font=("Arial", int(textscale*scale*extra_scale*2.25), "bold"), fill=("#000000"), tags=("clickable", "custom", "nextpage"))

        # key system params
        #   LR split
        #   separator
        #   MX1, MX2, BX
        #   partial

        #     label-type-x1-y1-x2-y2-halfable-labelsize-descname-descoff



        rowspacing = EDITKEYS_ROWSPACING # 7
        topy = EDITKEYS_TOPY # 27
        per_page = EDITKEYS_PER_PAGE # 10
        total_keys = key_systems["custom"]["parameters"]["keys"]

        NUM_PAGES = math.ceil(total_keys / per_page)

        if NUM_PAGES == 0:
            C.create_text(178*scale, 24.25*scale, text="0−0 of 0", font=("Arial", int(textscale*scale*1.5), "bold"), fill=("#FFFFFF"), tags=("custom"))
        else:
            C.create_text(178*scale, 24.25*scale, text=str((page*per_page) + 1) + "−" + str(min(total_keys, (page+1)*per_page)) + " of " + str(total_keys), font=("Arial", int(textscale*scale*1.5), "bold"), fill=("#FFFFFF"), tags=("custom"))
        
        for k in range(total_keys):
            key = key_systems["custom"][k]
            if int(k / per_page) == page:
                C.create_rectangle(79*scale, (topy + rowspacing*(k%per_page))*scale, 189*scale, (topy + rowspacing*(1 + k%per_page) - 1)*scale, fill="#EE2266" if k >= key_systems["custom"]["parameters"]["LR_split"] else "#5588BB", width=0, tags=("custom"))
                C.create_text(81.5*scale, (topy + rowspacing*(0.5 + k%per_page) - 0.5)*scale, text=str(k+1), font=("Arial", int(textscale*scale*2), "bold"), fill=("#FFFFFF"), tags=("custom"))

                if key["type"] == "partial":
                    offsetx1 = 21
                    
                    C.create_text(105*scale, (topy + rowspacing*(k%per_page) + 1.375)*scale, text="size", font=("Arial", int(textscale*scale*1), "bold"), fill=("#FFFFFF"), tags=("custom"))
                    C.create_rectangle(102.5*scale, (topy + rowspacing*(0.5 + k%per_page) - 1)*scale, 107.5*scale, (topy + rowspacing*(1 + k%per_page) - 1.75)*scale, fill=key_colors["model"][0] if select == "partialssize"+str(k) else "#FFFFFF", width=0, tags=("clickable", "custom", "partialssize"+str(k)))
                    C.create_text(105*scale, (topy + rowspacing*(0.75 + k%per_page) - 1.375)*scale, text=tempvar if select == "partialssize"+str(k) and tempvar != "" else str(round(float(4*key["size"]), 2)), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "custom", "partialssize"+str(k)))

                    C.create_text(112.25*scale, (topy + rowspacing*(0.5 + k%per_page) - 0.5)*scale, text="Type:", font=("Arial", int(textscale*scale*3/2), "bold"), fill=("#FFFFFF"), tags=("custom"))
                    C.create_text(122*scale, (topy + rowspacing*(0.5 + k%per_page) - 0.5)*scale, text="PARTIALS", font=("Arial", int(textscale*scale*2), "bold"), fill=("#FFFFFF"), tags=("custom"))

                    C.create_text((130.5+offsetx1)*scale, (topy + rowspacing*(k%per_page) + 1.375)*scale, text="xpos", font=("Arial", int(textscale*scale*1), "bold"), fill=("#FFFFFF"), tags=("custom"))
                    C.create_rectangle((128+offsetx1)*scale, (topy + rowspacing*(0.5 + k%per_page) - 1)*scale, (133+offsetx1)*scale, (topy + rowspacing*(1 + k%per_page) - 1.75)*scale, fill=key_colors["model"][0] if select == "partialsx"+str(k) else "#FFFFFF", width=0, tags=("clickable", "custom", "partialsx"+str(k)))
                    C.create_text((130.5+offsetx1)*scale, (topy + rowspacing*(0.75 + k%per_page) - 1.375)*scale, text=tempvar if select == "partialsx"+str(k) and tempvar != "" else (int(round(key["x"]*4, 2)) if round(key["x"]*4, 2) == int(round(key["x"]*4, 2)) else round(key["x"]*4, 2)), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "custom", "partialsx"+str(k)))

                    C.create_text((136.5+offsetx1)*scale, (topy + rowspacing*(k%per_page) + 1.375)*scale, text="ypos", font=("Arial", int(textscale*scale*1), "bold"), fill=("#FFFFFF"), tags=("custom"))
                    C.create_rectangle((134+offsetx1)*scale, (topy + rowspacing*(0.5 + k%per_page) - 1)*scale, (139+offsetx1)*scale, (topy + rowspacing*(1 + k%per_page) - 1.75)*scale, fill=key_colors["model"][0] if select == "partialsy"+str(k) else "#FFFFFF", width=0, tags=("clickable", "custom", "partialsy"+str(k)))
                    C.create_text((136.5+offsetx1)*scale, (topy + rowspacing*(0.75 + k%per_page) - 1.375)*scale, text=tempvar if select == "partialsy"+str(k) and tempvar != "" else (int(round(key["y"]*4, 2)) if round(key["y"]*4, 2) == int(round(key["y"]*4, 2)) else round(key["y"]*4, 2)), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "custom", "partialsy"+str(k)))
                    
                else:
                    # DESC TEXT
                    C.create_text(93*scale, (topy + rowspacing*(0.5 + k%per_page) - 1.75)*scale, text="SLFN on:", font=("Arial", int(textscale*scale*1.25), "bold"), fill=("#FFFFFF"), tags=("custom"))
                    C.create_text(93*scale, (topy + rowspacing*(0.5 + k%per_page) + 0.75)*scale, text="SLFN off:", font=("Arial", int(textscale*scale*1.25), "bold"), fill=("#FFFFFF"), tags=("custom"))

                    # LABEL SIZE
                    C.create_text(105*scale, (topy + rowspacing*(k%per_page) + 1.375)*scale, text="label size", font=("Arial", int(textscale*scale*1), "bold"), fill=("#FFFFFF"), tags=("custom"))
                    C.create_rectangle(102.5*scale, (topy + rowspacing*(0.5 + k%per_page) - 1)*scale, 107.5*scale, (topy + rowspacing*(1 + k%per_page) - 1.75)*scale, fill=key_colors["model"][0] if select == "labelsize"+str(k) else "#FFFFFF", width=0, tags=("clickable", "custom", "labelsize"+str(k)))
                    C.create_text(105*scale, (topy + rowspacing*(0.75 + k%per_page) - 1.375)*scale, text=tempvar if select == "labelsize"+str(k) and tempvar != "" else str(round(float(key["labelsize"]), 2)), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "custom", "labelsize"+str(k)))

                    # TYPES
                    C.create_text(112.25*scale, (topy + rowspacing*(0.5 + k%per_page) - 0.5)*scale, text="Type:", font=("Arial", int(textscale*scale*3/2), "bold"), fill=("#FFFFFF"), tags=("custom"))

                    types = ["main", "octave", "second", "low", "high", "trill", "model", "special"]
                    for i in range(8):
                        x = i; y = 0
                        color = key_colors[types[i]][1] if key["type"] == types[i] else key_colors[types[i]][0]
                        C.create_oval((115.5 + (4*i))*scale, (topy + rowspacing*(0.5 + k%per_page) - 0.5 + 1.75)*scale, (115.5 + 3.5 + (4*i))*scale, (topy + rowspacing*(0.5 + k%per_page) - 0.5 - 1.75)*scale, fill=color, width=0, tags=("clickable", "custom", "setkeytype"+str(k), str(i)))

                    # XPOS, YPOS, WIDTH, HEIGHT
                    offsetx1 = 21
                    
                    C.create_text((130.5+offsetx1)*scale, (topy + rowspacing*(k%per_page) + 1.375)*scale, text="xpos", font=("Arial", int(textscale*scale*1), "bold"), fill=("#FFFFFF"), tags=("custom"))
                    C.create_rectangle((128+offsetx1)*scale, (topy + rowspacing*(0.5 + k%per_page) - 1)*scale, (133+offsetx1)*scale, (topy + rowspacing*(1 + k%per_page) - 1.75)*scale, fill=key_colors["model"][0] if select == "xpos"+str(k) else "#FFFFFF", width=0, tags=("clickable", "custom", "xpos"+str(k)))
                    C.create_text((130.5+offsetx1)*scale, (topy + rowspacing*(0.75 + k%per_page) - 1.375)*scale, text=tempvar if select == "xpos"+str(k) and tempvar != "" else (int(round((key["x1"]+key["x2"]) * 2, 2)) if round((key["x1"]+key["x2"]) * 2, 2) == int(round((key["x1"]+key["x2"]) * 2, 2)) else round((key["x1"]+key["x2"]) * 2, 2)), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "custom", "xpos"+str(k)))

                    C.create_text((136.5+offsetx1)*scale, (topy + rowspacing*(k%per_page) + 1.375)*scale, text="ypos", font=("Arial", int(textscale*scale*1), "bold"), fill=("#FFFFFF"), tags=("custom"))
                    C.create_rectangle((134+offsetx1)*scale, (topy + rowspacing*(0.5 + k%per_page) - 1)*scale, (139+offsetx1)*scale, (topy + rowspacing*(1 + k%per_page) - 1.75)*scale, fill=key_colors["model"][0] if select == "ypos"+str(k) else "#FFFFFF", width=0, tags=("clickable", "custom", "ypos"+str(k)))
                    C.create_text((136.5+offsetx1)*scale, (topy + rowspacing*(0.75 + k%per_page) - 1.375)*scale, text=tempvar if select == "ypos"+str(k) and tempvar != "" else (int(round((key["y1"]+key["y2"]) * 2, 2)) if round((key["y1"]+key["y2"]) * 2, 2) == int(round((key["y1"]+key["y2"]) * 2, 2)) else round((key["y1"]+key["y2"]) * 2, 2)), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "custom", "ypos"+str(k)))

                    C.create_text((142.5+offsetx1)*scale, (topy + rowspacing*(k%per_page) + 1.375)*scale, text="width", font=("Arial", int(textscale*scale*1), "bold"), fill=("#FFFFFF"), tags=("custom"))
                    C.create_rectangle((140+offsetx1)*scale, (topy + rowspacing*(0.5 + k%per_page) - 1)*scale, (145+offsetx1)*scale, (topy + rowspacing*(1 + k%per_page) - 1.75)*scale, fill=key_colors["model"][0] if select == "width"+str(k) else "#FFFFFF", width=0, tags=("clickable", "custom", "width"+str(k)))
                    C.create_text((142.5+offsetx1)*scale, (topy + rowspacing*(0.75 + k%per_page) - 1.375)*scale, text=tempvar if select == "width"+str(k) and tempvar != "" else int(round((key["x2"]-key["x1"]) * 4, 2)), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "custom", "width"+str(k)))

                    C.create_text((148.5+offsetx1)*scale, (topy + rowspacing*(k%per_page) + 1.375)*scale, text="height", font=("Arial", int(textscale*scale*1), "bold"), fill=("#FFFFFF"), tags=("custom"))
                    C.create_rectangle((146+offsetx1)*scale, (topy + rowspacing*(0.5 + k%per_page) - 1)*scale, (151+offsetx1)*scale, (topy + rowspacing*(1 + k%per_page) - 1.75)*scale, fill=key_colors["model"][0] if select == "hight"+str(k) else "#FFFFFF", width=0, tags=("clickable", "custom", "hight"+str(k)))
                    C.create_text((148.5+offsetx1)*scale, (topy + rowspacing*(0.75 + k%per_page) - 1.375)*scale, text=tempvar if select == "hight"+str(k) and tempvar != "" else int(round((key["y2"]-key["y1"]) * 4, 2)), font=("Arial", int(textscale*scale*6/5), "bold"), fill="#000000", tags=("clickable", "custom", "hight"+str(k)))

                    C.create_text((155.5+offsetx1)*scale, (topy + rowspacing*(k%per_page) + 1.375)*scale, text="halfable", font=("Arial", int(textscale*scale*1), "bold"), fill=("#FFFFFF"), tags=("custom"))
                    C.create_rectangle((152+offsetx1)*scale, (topy + rowspacing*(0.5 + k%per_page) - 1)*scale, (155.5+offsetx1)*scale, (topy + rowspacing*(1 + k%per_page) - 1.75)*scale, fill="#000000" if key["halfable"] else "#FFFFFF", width=0, tags=("clickable", "custom", "halfableon"+str(k)))
                    C.create_text((153.75+offsetx1)*scale, (topy + rowspacing*(0.75 + k%per_page) - 1.375)*scale, text="ON", font=("Arial", int(textscale*scale*6/5), "bold"), fill="#FFFFFF" if key["halfable"] else "#000000", tags=("clickable", "custom", "halfableon"+str(k)))
                    C.create_rectangle((155.5+offsetx1)*scale, (topy + rowspacing*(0.5 + k%per_page) - 1)*scale, (159+offsetx1)*scale, (topy + rowspacing*(1 + k%per_page) - 1.75)*scale, fill="#000000" if not key["halfable"] else "#FFFFFF", width=0, tags=("clickable", "custom", "halfableoff"+str(k)))
                    C.create_text((157.25+offsetx1)*scale, (topy + rowspacing*(0.75 + k%per_page) - 1.375)*scale, text="OFF", font=("Arial", int(textscale*scale*6/5), "bold"), fill="#FFFFFF" if not key["halfable"] else "#000000", tags=("clickable", "custom", "halfableoff"+str(k)))
                    
                    
                    # ADD/DELETE/MOVE KEY

                    C.create_rectangle(185*scale, (topy + rowspacing*(k%per_page) + 1)*scale, 188*scale, (topy + rowspacing*(0.5 + k%per_page) - 0.5)*scale, fill="#DDDDDD", width=1, tags=("clickable", "custom", "editkey"+str(k), "addkey"))
                    C.create_text(186.5*scale, (topy + rowspacing*(0.25 + k%per_page) + 0.375)*scale, text="+", font=("Arial", int(textscale*scale*7/4), "bold"), fill=("#000000"), tags=("clickable", "custom", "editkey"+str(k), "addkey"))
                    
                    C.create_rectangle(185*scale, (topy + rowspacing*(0.5 + k%per_page) - 0.5)*scale, 188*scale, (topy + rowspacing*(1 + k%per_page) - 2)*scale, fill="#DDDDDD", width=1, tags=("clickable", "custom", "editkey"+str(k), "removekey"))
                    C.create_text(186.5*scale, (topy + rowspacing*(0.75 + k%per_page) - 1.125)*scale, text="×", font=("Arial", int(textscale*scale*2), "bold"), fill=("#000000"), tags=("clickable", "custom", "editkey"+str(k), "removekey"))
    
                    C.create_rectangle(182*scale, (topy + rowspacing*(k%per_page) + 1)*scale, 185*scale, (topy + rowspacing*(0.5 + k%per_page) - 0.5)*scale, fill="#DDDDDD", width=1, tags=("clickable", "custom", "editkey"+str(k), "upkey"))
                    C.create_text(183.5*scale, (topy + rowspacing*(0.25 + k%per_page) + 0.25)*scale, text="▲", font=("Arial", int(textscale*scale*extra_scale*1.25), "bold"), fill=("#000000"), tags=("clickable", "custom", "editkey"+str(k), "upkey"))

                    C.create_rectangle(182*scale, (topy + rowspacing*(0.5 + k%per_page) - 0.5)*scale, 185*scale, (topy + rowspacing*(1 + k%per_page) - 2)*scale, fill="#DDDDDD", width=1, tags=("clickable", "custom", "editkey"+str(k), "downkey"))
                    C.create_text(183.5*scale, (topy + rowspacing*(0.75 + k%per_page) - 1.25)*scale, text="▼", font=("Arial", int(textscale*scale*extra_scale*1.25), "bold"), fill=("#000000"), tags=("clickable", "custom", "editkey"+str(k), "downkey"))  
    
    elif setinstrument == "not":
        rowspacing = 2.75
        topy = 28
        per_page = 25

        if platform.system() == "Darwin": # On Mac, the arrows are rendered too large
            extra_scale = 0.75
        else:
            extra_scale = 1

        C.create_rectangle(122*scale, 21*scale, 125*scale, 24*scale, fill="#FFFFFF", width=1, tags=("clickable", "database", "prevpage"))
        C.create_text(123.5*scale, 22.5*scale, text="◀", font=("Arial", int(textscale*scale*extra_scale*2.25), "bold"), fill=("#000000"), tags=("clickable", "database", "prevpage"))

        C.create_rectangle(143*scale, 21*scale, 146*scale, 24*scale, fill="#FFFFFF", width=1, tags=("clickable", "database", "nextpage"))
        C.create_text(144.5*scale, 22.5*scale, text="▶", font=("Arial", int(textscale*scale*extra_scale*2.25), "bold"), fill=("#000000"), tags=("clickable", "database", "nextpage"))

        C.create_rectangle(118.5*scale, 21*scale, 121.5*scale, 24*scale, fill="#FFFFFF", width=1, tags=("clickable", "database", "prevpage2"))
        C.create_text(120*scale, 22.5*scale, text="◀◀", font=("Arial", int(textscale*scale*extra_scale*1.5), "bold"), fill=("#000000"), tags=("clickable", "database", "prevpage2"))

        C.create_rectangle(146.5*scale, 21*scale, 149.5*scale, 24*scale, fill="#FFFFFF", width=1, tags=("clickable", "database", "nextpage2"))
        C.create_text(148*scale, 22.5*scale, text="▶▶", font=("Arial", int(textscale*scale*extra_scale*1.5), "bold"), fill=("#000000"), tags=("clickable", "database", "nextpage2"))

        if filters["search"] != "none":
            C.create_text(89.75*scale, 22.5*scale, text="SEARCH RESULTS", font=("Arial", int(textscale*scale*2), "bold"), fill=("#000000"), tags=("database"))
            C.create_rectangle(175*scale, 21*scale, 190*scale, 24*scale, fill="#FFFFFF", width=1, tags=("clickable", "database", "clearsearch"))
            C.create_text(182.5*scale, 22.5*scale, text="Clear search", font=("Arial", int(textscale*scale*1.5), "bold"), fill=("#000000"), tags=("clickable", "database", "clearsearch"))

        filtered_values = []
        filtered_database = []
        
        for f, fingering in enumerate(database[1:]): # tuple: (pitches, fingering, fingtype)
            include = True
            
            # FILTER FINGTYPE
            if ("multi" if "multi" in fingering[2] else fingering[2]) not in filters["fingtype"]:
                include = False

            # FILTER TET
            if filters["tet"] == "all":
                for pitch in fingering[0]:
                    if abs(database[0][3]*math.log(pitch/database[0][2], 2) - round(database[0][3]*math.log(pitch/database[0][2], 2), 0) + 0.0000000001) > filters["tolerance"]:
                        include = False
                        break
            elif filters["tet"] == "part":
                include = False
                for pitch in fingering[0]:
                    if abs(database[0][3]*math.log(pitch/database[0][2], 2) - round(database[0][3]*math.log(pitch/database[0][2], 2), 0) + 0.0000000001) <= filters["tolerance"]:
                        include = True
                        break

            # FILTER SEARCH
            if filters["search"] == "fingering_primary":
                if fingering[1][0] != FILTERS_TEMP_FINGERING[0] and fingering[1][0] != (FILTERS_TEMP_FINGERING[0] | FILTERS_TEMP_FINGERING[2]) and (fingering[1][0] | fingering[1][2]) != FILTERS_TEMP_FINGERING[0] and (fingering[1][0] | fingering[1][2]) != (FILTERS_TEMP_FINGERING[0] | FILTERS_TEMP_FINGERING[2]):
                    include = False

                # special case: trombone
                if instruments[database[0][1]][0] == "trombone":
                    sposmatch = False
                    if (round(abs((fingering[1][4].real - FILTERS_TEMP_FINGERING[4].real) * 12/database[0][3]), 3) <= FILTERS["tolerance"] or
                        (round(abs((fingering[1][4].real - FILTERS_TEMP_FINGERING[4].imag) * 12/database[0][3]), 3) <= FILTERS["tolerance"] and FILTERS_TEMP_FINGTYPE == "trill") or
                        (round(abs((fingering[1][4].imag - FILTERS_TEMP_FINGERING[4].real) * 12/database[0][3]), 3) <= FILTERS["tolerance"] and fingering[2] == "trill") or
                        (round(abs((fingering[1][4].imag - FILTERS_TEMP_FINGERING[4].imag) * 12/database[0][3]), 3) <= FILTERS["tolerance"] and FILTERS_TEMP_FINGTYPE == "trill" and fingering[2] == "trill")):
                        sposmatch = True
                    if not sposmatch:
                        include = False
                
            elif filters["search"] == "fingering_exact":
                if fingering[1][0:4] != FINGERING[0:4]:
                    include = False

                # special case: trombone
                if instruments[database[0][1]][0] == "trombone":
                    sposmatch = False
                    if ((round(abs((fingering[1][4].real - FILTERS_TEMP_FINGERING[4].real) * 12/database[0][3]), 3) <= FILTERS["tolerance"] and fingering[2] != "trill") or
                        (round(abs((fingering[1][4].real - FILTERS_TEMP_FINGERING[4].real) * 12/database[0][3]), 3) <= FILTERS["tolerance"] and
                        round(abs((fingering[1][4].imag - FILTERS_TEMP_FINGERING[4].imag) * 12/database[0][3]), 3) <= FILTERS["tolerance"] and fingering[2] == "trill")):
                        sposmatch = True
                    if not sposmatch:
                        include = False
                    
            elif filters["search"] == "pitch_single":
                include = False
                for pitch in fingering[0]:
                    match = False
                    for searchpitch in FILTERS_TEMP_PITCHES:
                        if abs(database[0][3]*math.log(pitch/database[0][2], 2) - database[0][3]*math.log(searchpitch/database[0][2], 2)) <= filters["tolerance"]:
                            match = True
                            break
                    if match:
                        include = True
                        break
            elif filters["search"] == "pitch_full":
                include = True
                for searchpitch in FILTERS_TEMP_PITCHES:
                    match = False
                    for pitch in fingering[0]:
                        if abs(database[0][3]*math.log(pitch/database[0][2], 2) - database[0][3]*math.log(searchpitch/database[0][2], 2)) <= filters["tolerance"]:
                            match = True
                            break
                    if not match:
                        include = False
                        break

            if include:
                filtered_database.append(fingering)
                filtered_values.append(f+1)

        NUM_PAGES = math.ceil(len(filtered_database) / per_page)
        if page >= NUM_PAGES:
            page = max(0, NUM_PAGES-1)
            PAGE = page
        
        if "data+" in select: # data+
            if len(filtered_database) == 0:
                select = ""
            elif len(filtered_database) == 1:
                select = "data" + str(filtered_values[0])
            else:
                next_entry = ((int(select[5:])+1) - 1) % (len(database)) +1
                while next_entry % (len(database)) not in filtered_values:
                    next_entry = ((next_entry+1) - 1) % (len(database)) +1
                select = "data" + str(next_entry)
            SELECT = select
        elif "data-" in select: # data-
            if len(filtered_database) == 0:
                select = ""
            elif len(filtered_database) == 1:
                select = "data" + str(filtered_values[0])
            else:
                prev_entry = ((int(select[5:])-1) - 1) % (len(database)) +1
                while prev_entry % (len(database)) not in filtered_values:
                    prev_entry = ((prev_entry-1) - 1) % (len(database)) +1
                select = "data" + str(prev_entry)
            SELECT = select

        if "data" in select and len(filtered_database) > 0: # if entry is selected, binary search for entry
            select = select.split(" ")[0]
            
            low = 0; high = len(filtered_database)-1
            while high - low > 1:
                mid = int((low + high) / 2)
                if int(select[4:]) == filtered_values[mid]:
                    page = int(mid / per_page)
                    PAGE = page
                    break
                elif int(select[4:]) < filtered_values[mid]:
                    high = mid
                elif int(select[4:]) > filtered_values[mid]:
                    low = mid
            if int(select[4:]) == filtered_values[high]:
                    page = int(high / per_page)
                    PAGE = page
            elif int(select[4:]) == filtered_values[low]:
                    page = int(low / per_page)
                    PAGE = page

        C.create_text(134*scale, 22.5*scale, text=("0" if NUM_PAGES == 0 else str(page*per_page + 1)) + "−" + str(min((page+1)*per_page, len(filtered_database))) + " of " + str(len(filtered_database)), font=("Arial", int(textscale*scale*1.25), "bold"), fill=("#000000"), tags=("database"))

        C.create_text(80*scale, (topy-1)*scale, text="Type", font=("Arial", int(textscale*scale*1), "bold"), fill=("#000000"), tags=("database"))
        C.create_text(86*scale, (topy-1)*scale, text="Freq (Hz)", font=("Arial", int(textscale*scale*1), "bold"), fill=("#000000"), tags=("database"))
        C.create_text(95*scale, (topy-1)*scale, text="Trans Pitch", font=("Arial", int(textscale*scale*1), "bold"), fill=("#000000"), tags=("database"))
        C.create_text(105*scale, (topy-1)*scale, text="Concert Pitch", font=("Arial", int(textscale*scale*1), "bold"), fill=("#000000"), tags=("database"))
        C.create_text(117.5*scale, (topy-1)*scale, text="Steps of "+str(TET)+"−TET", font=("Arial", int(textscale*scale*1), "bold"), fill=("#000000"), tags=("database"))
        C.create_text(140*scale, (topy-1)*scale, text="Fingering", font=("Arial", int(textscale*scale*1), "bold"), fill=("#000000"), tags=("database"))
        C.create_text(172.5*scale, (topy-1)*scale, text="Description", font=("Arial", int(textscale*scale*1), "bold"), fill=("#000000"), tags=("database"))
        
        for f, entry in enumerate(filtered_database[page*per_page : (page+1)*per_page] if len(filtered_database) >= (page+1)*per_page else filtered_database[page*per_page :]):
            
            entry_num = filtered_values[f + page*per_page]

            if "multi" in entry[2]:
                fingtype = "multi"
            else:
                fingtype = entry[2]

            # fingtype
            C.create_rectangle(78*scale, (topy + rowspacing*f)*scale, 82*scale, (topy + rowspacing*(f+1))*scale, fill=key_colors["model"][0] if select == "data"+str(entry_num) else "#FFFFFF", width=1, tags=("clickable", "entry", "data"+str(entry_num)))
            C.create_text(80*scale, (topy + rowspacing*(f+0.5))*scale, text=fingtype, font=("Arial", int(textscale*scale*1), "bold"), fill=("#000000"), tags=("clickable", "entry", "data"+str(entry_num)))
        
            freqs = []
            transposed_pitches = []
            concert_pitches = []
            tet_steps = []
            
            for pitch in entry[0]:
                freqs.append(str(round(pitch, 2)))
                transposed_note = notename(pitch, instruments[database[0][1]][1])
                concert_note = notename(pitch, 0)
                transposed_pitches.append(transposed_note[0] + dataplus(round(transposed_note[1], 1)))
                concert_pitches.append(concert_note[0] + dataplus(round(concert_note[1], 1)))
                tet_steps.append(str(int(round(database[0][3]*math.log(pitch/database[0][2], 2), 0)) % database[0][3]) + "\\" + str(database[0][3]) + " " + plusminus(round(100 * (database[0][3]*math.log(pitch/database[0][2], 2) - round(database[0][3]*math.log(pitch/database[0][2], 2), 0) + 0.0000000001), 1)) + "%")

            # freqs
            if entry[2] in ["multi3", "multi4"]:
                freqtext = ", ".join(freqs[0:2]) + ",\n" + ", ".join(freqs[2:]); freqsize = min(23/max(len(", ".join(freqs[0:2])), len(", ".join(freqs[2:]))), 0.75)
                notetext = ", ".join(transposed_pitches[0:2]) + ",\n" + ", ".join(transposed_pitches[2:]); notesize = min(14/max(len(", ".join(transposed_pitches[0:2])), len(", ".join(transposed_pitches[2:]))), 0.75)
                conctext = ", ".join(concert_pitches[0:2]) + ",\n" + ", ".join(concert_pitches[2:]); concsize = min(14/max(len(", ".join(concert_pitches[0:2])), len(", ".join(concert_pitches[2:]))), 0.75)
                steptext = ", ".join(tet_steps[0:2]) + ",\n" + ", ".join(tet_steps[2:]); stepsize = min(20/max(len(", ".join(tet_steps[0:2])), len(", ".join(tet_steps[2:]))), 0.75)
            elif entry[2] in ["multi2", "trill"]:
                freqtext = ", ".join(freqs); freqsize = min(11/len(freqtext), 1)
                notetext = ", ".join(transposed_pitches); notesize = min(14/len(notetext), 1)
                conctext = ", ".join(concert_pitches); concsize = min(14/len(conctext), 1)
                steptext = ", ".join(tet_steps); stepsize = min(20/len(steptext), 1)
            else:
                freqtext = ", ".join(freqs); freqsize = min(11/len(freqtext), 1)
                notetext = ", ".join(transposed_pitches); notesize = min(14/len(notetext), 1)
                conctext = ", ".join(concert_pitches); concsize = min(14/len(conctext), 1)
                steptext = ", ".join(tet_steps); stepsize = min(20/len(steptext), 1)
                
            C.create_rectangle(82*scale, (topy + rowspacing*f)*scale, 90*scale, (topy + rowspacing*(f+1))*scale, fill=key_colors["model"][0] if select == "data"+str(entry_num) else "#FFFFFF", width=1, tags=("clickable", "entry", "data"+str(entry_num)))
            C.create_text(86*scale, (topy + rowspacing*(f+0.5))*scale, text=freqtext, font=("Arial", int(textscale*scale*freqsize), "bold"), fill=("#000000"), tags=("clickable", "entry", "data"+str(entry_num)))

            C.create_rectangle(90*scale, (topy + rowspacing*f)*scale, 100*scale, (topy + rowspacing*(f+1))*scale, fill=key_colors["model"][0] if select == "data"+str(entry_num) else "#FFFFFF", width=1, tags=("clickable", "entry", "data"+str(entry_num)))
            C.create_text(95*scale, (topy + rowspacing*(f+0.5))*scale, text=notetext, font=("Arial", int(textscale*scale*notesize), "bold"), fill=("#000000"), tags=("clickable", "entry", "data"+str(entry_num)))

            C.create_rectangle(100*scale, (topy + rowspacing*f)*scale, 110*scale, (topy + rowspacing*(f+1))*scale, fill=key_colors["model"][0] if select == "data"+str(entry_num) else "#FFFFFF", width=1, tags=("clickable", "entry", "data"+str(entry_num)))
            C.create_text(105*scale, (topy + rowspacing*(f+0.5))*scale, text=conctext, font=("Arial", int(textscale*scale*concsize), "bold"), fill=("#000000"), tags=("clickable", "entry", "data"+str(entry_num)))

            C.create_rectangle(110*scale, (topy + rowspacing*f)*scale, 125*scale, (topy + rowspacing*(f+1))*scale, fill=key_colors["model"][0] if select == "data"+str(entry_num) else "#FFFFFF", width=1, tags=("clickable", "entry", "data"+str(entry_num)))
            C.create_text(117.5*scale, (topy + rowspacing*(f+0.5))*scale, text=steptext, font=("Arial", int(textscale*scale*stepsize), "bold"), fill=("#000000"), tags=("clickable", "entry", "data"+str(entry_num)))

            F = list(bin(entry[1][0]))[2:]
            H = list(bin(entry[1][1]))[2:]
            T = list(bin(entry[1][2]))[2:]
            while len(F) < key_systems[instruments[database[0][1]][0]]["parameters"]["keys"]:
                F.insert(0, "0")
            while len(H) < key_systems[instruments[database[0][1]][0]]["parameters"]["keys"]:
                H.insert(0, "0")
            while len(T) < key_systems[instruments[database[0][1]][0]]["parameters"]["keys"]:
                T.insert(0, "0")
            states = []

            for key in range(key_systems[instruments[database[0][1]][0]]["parameters"]["keys"]):                
                if key_systems[instruments[database[0][1]][0]][key_systems[instruments[database[0][1]][0]]["parameters"]["keys"] - 1 - key]["type"] == "sposition1":
                    states.insert(0, entry[1][4])
                elif key_systems[instruments[database[0][1]][0]][key_systems[instruments[database[0][1]][0]]["parameters"]["keys"] - 1 - key]["type"] == "sposition2":
                    states.insert(0, entry[1][5])
                elif int(T[key]) == 1:
                    states.insert(0, 3)
                else:
                    states.insert(0, int(F[key])+int(H[key]))
                    
            desc_string = ""
            for key, state in enumerate(states):
                descname = key_systems[instruments[database[0][1]][0]][key]["descname"]
                if key == key_systems[instruments[database[0][1]][0]]["parameters"]["LR_split"]:
                    desc_string += key_systems[instruments[database[0][1]][0]]["parameters"]["separator"]
                if isinstance(state, complex):
                    if fingering[1][2] != "trill" or round(state.real, 6) == round(state.imag, 6):
                        desc_string += "{"+str(round(state.real, 2))+"} "
                    else:
                        desc_string += "[{"+str(round(state.real, 2))+"}{"+str(round(state.imag, 2))+"}] "
                elif state == 3:
                    if len(descname) >= 1 and descname[0] == "⌫":
                        desc_string = desc_string[:-1] if len(desc_string) >= 1 and desc_string[-1] == "−" else desc_string
                        descname = descname[1:]
                    desc_string += "["+descname.strip()+"]"
                elif state == 2:
                    desc_string += "½ " if descname[-1] == " " else (" ½" if descname[0] == " " else "½")
                elif state == 1:
                    if len(descname) >= 1 and descname[0] == "⌫":
                        desc_string = desc_string[:-1] if len(desc_string) >= 1 and desc_string[-1] == "−" else desc_string
                        descname = descname[1:]
                    desc_string += descname
                elif state == 0:
                    desc_string += key_systems[instruments[database[0][1]][0]][key]["descoff"]
            if entry[1][3] == -17:
                desc_string += "[(16)]"
            elif entry[1][3] == -1:
                desc_string += "[(0)]"
            elif entry[1][3] >= 0:
                desc_string += "(" + str(entry[1][3]) + ")"
            elif entry[1][3] <= -2:
                desc_string += "[(" + str(-entry[1][3]-1) + ")(" + str(-entry[1][3]) + ")]"

            descsize = min(40/max(1, len(desc_string)), 1)
            if descsize <= 2/3:
                desc_left = desc_string.split("|[|")[0] if "|[|" in desc_string else (desc_string.split("||")[0] if "||" in desc_string else desc_string.split("|")[0])
                desc_right = desc_string.split("|[|")[1] if "|[|" in desc_string else (desc_string.split("||")[1] if "||" in desc_string else desc_string.split("|")[1])
                descsize = min(50/max(len(desc_left), len(desc_right)), 0.75)
                desc_string = desc_left + "|\n[|" + desc_right if "|[|" in desc_string else (desc_left + "||\n" + desc_right if "||" in desc_string else desc_left + "|\n" + desc_right)
            C.create_rectangle(125*scale, (topy + rowspacing*f)*scale, 155*scale, (topy + rowspacing*(f+1))*scale, fill=key_colors["model"][0] if select == "data"+str(entry_num) else "#FFFFFF", width=1, tags=("clickable", "entry", "data"+str(entry_num)))
            C.create_text(140*scale, (topy + rowspacing*(f+0.5))*scale, text=desc_string, font=("Arial", int(textscale*scale*descsize), "bold"), fill=("#000000"), tags=("clickable", "entry", "data"+str(entry_num)))

            descriptionsize = max(min(40/(len(entry[1][-1])+0.000000001), 1), 0.75)
            description = entry[1][-1]
            if len(description) > 110:
                descriptionsize = max(min(47/(len(entry[1][-1])+0.000000001), 1), 2/3)
            if len(description) > 207:
                description = description[:205] + "..."
            C.create_rectangle(155*scale, (topy + rowspacing*f)*scale, 190*scale, (topy + rowspacing*(f+1))*scale, fill=key_colors["model"][0] if select == "data"+str(entry_num) else "#FFFFFF", width=1, tags=("clickable", "entry", "data"+str(entry_num)))
            C.create_text(172.5*scale, (topy + rowspacing*(f+0.5))*scale, text=description, width=34.5*scale, font=("Arial", int(textscale*scale*descriptionsize), "bold"), fill=("#000000"), tags=("clickable", "entry", "data"+str(entry_num)))
    


# HELP SCREENS
def fingering_help():
    H = Toplevel(C)
    fhx = int(scale*71.5)
    fhy = int(scale*66)
    textcolor = "#FFFFFF"
    bgcolor = "#AA55CC"
    H.geometry(str(fhx) + "x" + str(fhy))
    H.title("Fingering Diagram Help")
    FH = Canvas(H)
    FH.pack(fill=BOTH, expand=1)
    FH.create_rectangle(0,0,fhx+360,fhy+480, fill=bgcolor, width=0)

    Label(FH, text="Fingering Diagram Help", font=("Arial", int(textscale*scale*2), "bold"), fg=textcolor, bg=bgcolor).place(x = 1*scale, y = 1*scale)

    FH.create_oval(1.5*scale, 5*scale, 5.5*scale, 9*scale, fill=key_colors["main"][0], width=0)
    FH.create_oval(6*scale, 5*scale, 10*scale, 9*scale, fill=key_colors["main"][1], width=0)
    Label(FH, text="Main key directly controlling a tone hole / Main valve", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 5.5*scale)

    FH.create_oval(1.5*scale, 10*scale, 5.5*scale, 14*scale, fill=key_colors["octave"][0], width=0)
    FH.create_oval(6*scale, 10*scale, 10*scale, 14*scale, fill=key_colors["octave"][1], width=0)
    Label(FH, text="Key for controlling the register of the instrument", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 10.5*scale)

    FH.create_oval(1.5*scale, 15*scale, 5.5*scale, 19*scale, fill=key_colors["second"][0], width=0)
    FH.create_oval(6*scale, 15*scale, 10*scale, 19*scale, fill=key_colors["second"][1], width=0)
    Label(FH, text="Key used for some pitch a chromatic from the main keys", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 15.5*scale)

    FH.create_oval(1.5*scale, 20*scale, 5.5*scale, 24*scale, fill=key_colors["low"][0], width=0)
    FH.create_oval(6*scale, 20*scale, 10*scale, 24*scale, fill=key_colors["low"][1], width=0)
    Label(FH, text="Key for notes lower than with all main keys depressed", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 20.5*scale)

    FH.create_oval(1.5*scale, 25*scale, 5.5*scale, 29*scale, fill=key_colors["high"][0], width=0)
    FH.create_oval(6*scale, 25*scale, 10*scale, 29*scale, fill=key_colors["high"][1], width=0)
    Label(FH, text="Key for notes higher than with all main keys released", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 25.5*scale)

    FH.create_oval(1.5*scale, 30*scale, 5.5*scale, 34*scale, fill=key_colors["trill"][0], width=0)
    FH.create_oval(6*scale, 30*scale, 10*scale, 34*scale, fill=key_colors["trill"][1], width=0)
    Label(FH, text="Key primarily used for trills and fast passages", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 30.5*scale)

    FH.create_oval(1.5*scale, 35*scale, 5.5*scale, 39*scale, fill=key_colors["model"][0], width=0)
    FH.create_oval(6*scale, 35*scale, 10*scale, 39*scale, fill=key_colors["model"][1], width=0)
    Label(FH, text="Key/valve not present on all models of the instrument", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 35.5*scale)

    FH.create_oval(1.5*scale, 40*scale, 5.5*scale, 44*scale, fill=key_colors["special"][0], width=0)
    FH.create_oval(6*scale, 40*scale, 10*scale, 44*scale, fill=key_colors["special"][1], width=0)
    Label(FH, text="Key part of a mechanism not normally touched", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 40.5*scale)

    FH.create_oval(6*scale, 45*scale, 10*scale, 49*scale, fill=key_colors["main"][2], width=0)
    Label(FH, text="Half−hole (e.g. key is pressed but hole is not fully covered)", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 45.5*scale)

    FH.create_oval(6*scale, 50*scale, 10*scale, 54*scale, fill=key_colors["trilled"], width=0)
    Label(FH, text="Key is being trilled as part of a trill fingering", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 50.5*scale)

    FH.create_rectangle(2.25*scale, 57.5*scale, 9.25*scale, 58.5*scale, fill=key_colors["main"][0], width=0)
    FH.create_rectangle(2.25*scale, 57.5*scale, 5.75*scale, 58.5*scale, fill=key_colors["main"][1], width=0)
    FH.create_oval(1.5*scale, 55.5*scale, 3*scale, 57*scale, fill=key_colors["main"][0], width=0)
    FH.create_oval(5*scale, 55.5*scale, 6.5*scale, 57*scale, fill=key_colors["main"][0], width=0)
    FH.create_oval(8.5*scale, 55.5*scale, 10*scale, 57*scale, fill=key_colors["main"][0], width=0)
    Label(FH, text="Continuous pitch parameter (e.g. on trombone)", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 55.5*scale)

    for p in range(17):
        if p == 0:
            x = 7
            y = 0
        elif p == 16:
            x = 6
            y = 0
        else:
            x = (p / (2**int(math.log(p, 2))) % 1)*8
            y = int(math.log(p, 2))
        FH.create_oval((1.75 + x)*scale, (60 + y)*scale, (2.75 + x)*scale, (61 + y)*scale, fill=key_colors["main"][0], width=0)
        
    Label(FH, text="Partials (notes of the harmonic series); \"other\" for false tones", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 60.5*scale)

def pitch_help():
    H = Toplevel(C)
    fhx = int(scale*82)
    fhy = int(scale*36)
    textcolor = "#FFFFFF"
    bgcolor = colors["pitch_background"]
    H.geometry(str(fhx) + "x" + str(fhy))
    H.title("Pitch Help")
    FH = Canvas(H)
    FH.pack(fill=BOTH, expand=1)
    FH.create_rectangle(0,0,fhx+360,fhy+480, fill=bgcolor, width=0)

    Label(FH, text="Pitch Help", font=("Arial", int(textscale*scale*2), "bold"), fg=textcolor, bg=bgcolor).place(x = 1*scale, y = 1*scale)

    FH.create_rectangle(5*scale, 5*scale, 12*scale, 8*scale, fill="#FFFFFF", width=0)
    FH.create_text(8.5*scale, 6.5*scale, text="327.68", fill="#000000", font=("Arial", int(textscale*scale*1.2), "bold"))
    Label(FH, text="Frequency of pitch in Hz", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 13*scale, y = 5*scale)

    FH.create_rectangle(1.5*scale, 9*scale, 5.5*scale, 12*scale, fill="#FFFFFF", width=0)
    FH.create_text(3.5*scale, 10.5*scale, text="C#5", fill="#000000", font=("Arial", int(textscale*scale*1.2), "bold"))
    FH.create_rectangle(6*scale, 9*scale, 12*scale, 12*scale, fill="#FFFFFF", width=0)
    FH.create_text(9*scale, 10.5*scale, text="−10.26", fill="#000000", font=("Arial", int(textscale*scale*1.2), "bold"))
    Label(FH, text="Transposed pitch, given as note and cent deviation", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 13*scale, y = 9*scale)

    FH.create_rectangle(1.5*scale, 13*scale, 5.5*scale, 16*scale, fill="#FFFFFF", width=0)
    FH.create_text(3.5*scale, 14.5*scale, text="E4", fill="#000000", font=("Arial", int(textscale*scale*1.2), "bold"))
    FH.create_rectangle(6*scale, 13*scale, 12*scale, 16*scale, fill="#FFFFFF", width=0)
    FH.create_text(9*scale, 14.5*scale, text="−10.26", fill="#000000", font=("Arial", int(textscale*scale*1.2), "bold"))
    Label(FH, text="Concert pitch, given as note and cent deviation", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 13*scale, y = 13*scale)

    Label(FH, text="To change the pitch, select one of these boxes and type in the desired pitch,\nor use arrow keys to shift the pitch by 1 TET−step", justify="left", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 1*scale, y = 17*scale)

    FH.create_text(4*scale, 25*scale, text="Tonic:", fill="#FFFFFF", font=("Arial", int(textscale*scale*1.375), "bold"))
    FH.create_rectangle(7.5*scale, 23.5*scale, 12*scale, 26.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(9.75*scale, 25*scale, text="440.0", fill="#000000", font=("Arial", int(textscale*scale*1.2), "bold"))
    Label(FH, text="Tonic pitch to tune other notes relative to", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 13*scale, y = 23.5*scale)

    FH.create_text(9.75*scale, 29*scale, text="TET", fill="#FFFFFF", font=("Arial", int(textscale*scale*1.5), "bold"))
    FH.create_rectangle(1.5*scale, 27.25*scale, 7*scale, 30.75*scale, fill="#FFFFFF", width=0)
    FH.create_text(4.25*scale, 29*scale, text="19", fill="#000000", font=("Arial", int(textscale*scale*1.75), "bold"))
    Label(FH, text="Number of evenly-distributed pitches per octave", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 13*scale, y = 27.5*scale)

    FH.create_rectangle(1.5*scale, 31.5*scale, 12*scale, 34.5*scale, fill="#334F66", width=0)
    FH.create_text(6.75*scale, 33*scale, text="11\\19 −7.91%", fill="#FFFFFF", font=("Arial", int(textscale*scale*1.25), "bold"))
    Label(FH, text="Pitch class within TET (built on tonic) and deviation in % of 1 TET−step", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 13*scale, y = 31.5*scale)


def filters_help():
    H = Toplevel(C)
    fhx = int(scale*96)
    fhy = int(scale*50)
    textcolor = "#FFFFFF"
    bgcolor = colors["filters_background"]
    H.geometry(str(fhx) + "x" + str(fhy))
    H.title("Filters and Search Help")
    FH = Canvas(H)
    FH.pack(fill=BOTH, expand=1)
    FH.create_rectangle(0,0,fhx+360,fhy+480, fill=bgcolor, width=0)

    Label(FH, text="Filters and Search Help", font=("Arial", int(textscale*scale*2), "bold"), fg=textcolor, bg=bgcolor).place(x = 1*scale, y = 1*scale)

    Label(FH, text="When filtering for TET or searching for pitches, \"Tolerance\" indicates the maximum pitch deviation\nfrom the TET/pitch (specified in the \"pitch\" section) that can show up in the search/filtered results", justify="left", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 1*scale, y = 5*scale)

    FH.create_rectangle(1.5*scale, 11.5*scale, 8.5*scale, 14.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(5*scale, 13*scale, text="7.89", fill="#000000", font=("Arial", int(textscale*scale*1.375), "bold"))
    FH.create_text(10*scale, 13*scale, text="c", fill="#FFFFFF", font=("Arial", int(textscale*scale*1.5), "bold"))
    Label(FH, text="(Absolute) tolerance in cents", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11.5*scale, y = 11.5*scale)

    FH.create_rectangle(1.5*scale, 15.5*scale, 8.5*scale, 18.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(5*scale, 17*scale, text="12.5", fill="#000000", font=("Arial", int(textscale*scale*1.375), "bold"))
    FH.create_text(10*scale, 17*scale, text="%", fill="#FFFFFF", font=("Arial", int(textscale*scale*1.5), "bold"))
    Label(FH, text="(Relative) tolerance in percentage of 1 TET−step", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11.5*scale, y = 15.5*scale)

    FH.create_rectangle(1.5*scale, 19.5*scale, 16.5*scale, 22*scale, fill="#FFFFFF", width=0)
    FH.create_text(9*scale, 20.75*scale, text="At least 1 in TET", fill="#000000", font=("Arial", int(textscale*scale*1), "bold"))
    FH.create_rectangle(1.5*scale, 22.5*scale, 16.5*scale, 25*scale, fill="#FFFFFF", width=0)
    FH.create_text(9*scale, 23.75*scale, text="At least 1 pitch match", fill="#000000", font=("Arial", int(textscale*scale*1), "bold"))
    Label(FH, text="A fingering will show up if at least ONE of its pitches is in the TET within tolerance\nor if at least ONE of its pitches matches any of the specified pitches", justify="left", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 17*scale, y = 19.5*scale)

    FH.create_rectangle(1.5*scale, 26*scale, 16.5*scale, 28.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(9*scale, 27.25*scale, text="All in TET", fill="#000000", font=("Arial", int(textscale*scale*1), "bold"))
    FH.create_rectangle(1.5*scale, 29*scale, 16.5*scale, 31.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(9*scale, 30.25*scale, text="All pitches match", fill="#000000", font=("Arial", int(textscale*scale*1), "bold"))
    Label(FH, text="A fingering will only show up if ALL of its pitches are in the TET within tolerance\nor if ALL of its pitches can be matched with one of the specified pitches", justify="left", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 17*scale, y = 26*scale)

    Label(FH, text="In a fingering search, input the fingering to be searched in the diagram on the top left\nNote: \"Tolerance\" also indicates the maximum deviation when searching trombone positions", justify="left", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 1*scale, y = 32.5*scale)

    FH.create_rectangle(1.5*scale, 39*scale, 13.5*scale, 43*scale, fill="#FFFFFF", width=0)
    FH.create_text(7.5*scale, 41*scale, text="Match primary\n        fingering", fill="#000000", font=("Arial", int(textscale*scale*1), "bold"))
    Label(FH, text="A fingering will show up if its keys match (half−holes and partials are ignored)\nor for trills, if either of the 2 result fingerings matches either specified fingering", justify="left", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 14*scale, y = 38.25*scale)

    FH.create_rectangle(1.5*scale, 44.5*scale, 13.5*scale, 48.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(7.5*scale, 46.5*scale, text="Match exact\n     fingering", fill="#000000", font=("Arial", int(textscale*scale*1), "bold"))
    Label(FH, text="A fingering will only show up if all aspects match (keys, half−holes, partials etc.)\nor for trills, if both of the result fingerings match the two specified fingerings", justify="left", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 14*scale, y = 43.75*scale)

def editkeys_help():
    H = Toplevel(C)
    fhx = int(scale*138)
    fhy = int(scale*74)
    textcolor = "#FFFFFF"
    bgcolor = colors["custom_background"]
    H.geometry(str(fhx) + "x" + str(fhy))
    H.title("Instrument Editor Help")
    FH = Canvas(H)
    FH.pack(fill=BOTH, expand=1)
    FH.create_rectangle(0,0,fhx+360,fhy+480, fill=bgcolor, width=0)

    Label(FH, text="Instrument Editor Help", font=("Arial", int(textscale*scale*2.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 1*scale, y = 0.75*scale)

    Label(FH, text="General Properties", font=("Arial", int(textscale*scale*2), "bold"), fg=textcolor, bg=bgcolor).place(x = 1*scale, y = 5*scale)

    Label(FH, text="Section split", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 3*scale, y = 11.5*scale)
    FH.create_rectangle(16*scale, 11.5*scale, 20*scale, 14.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(18*scale, 13*scale, text="15", fill="#000000", font=("Arial", int(textscale*scale*1.25), "bold"))
    Label(FH, text="In the single-line notation for a fingering, \"Section split\" indicates which keys are placed before or after the separator |\n(which usually separates LH and RH keys). All keys whose number is less than or equal to \"Section split\" will be in the\nfirst group (blue), and all keys whose number is greater than \"Section split\" will be in the second group (red)", justify="left", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 21*scale, y = 9*scale)

    Label(FH, text="separator", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 2*scale, y = 18*scale)
    FH.create_rectangle(12*scale, 18*scale, 16*scale, 21*scale, fill="#000000", width=0)
    FH.create_text(14*scale, 19.5*scale, text="ON", fill="#FFFFFF", font=("Arial", int(textscale*scale*1.25), "bold"))
    FH.create_rectangle(16*scale, 18*scale, 20*scale, 21*scale, fill="#FFFFFF", width=0)
    FH.create_text(18*scale, 19.5*scale, text="OFF", fill="#000000", font=("Arial", int(textscale*scale*1.25), "bold"))
    Label(FH, text="Toggle whether the separator | is displayed in the single-line fingering notation", justify="left", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 21*scale, y = 18*scale)

    Label(FH, text="mid X1\nmid X2\nmid Y", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 8.5*scale, y = 22*scale)
    FH.create_rectangle(16*scale, 22.5*scale, 20*scale, 24.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(18*scale, 23.5*scale, text="148", fill="#000000", font=("Arial", int(textscale*scale*1.25), "bold"))
    FH.create_rectangle(16*scale, 25*scale, 20*scale, 27*scale, fill="#FFFFFF", width=0)
    FH.create_text(18*scale, 26*scale, text="148", fill="#000000", font=("Arial", int(textscale*scale*1.25), "bold"))
    FH.create_rectangle(16*scale, 27.5*scale, 20*scale, 29.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(18*scale, 28.5*scale, text="62", fill="#000000", font=("Arial", int(textscale*scale*1.25), "bold"))
    Label(FH, text="The boundary between the blue and red regions in the diagram forms a ┌┘ shape\nThese are the coordinates of the center points (note that they have the same Y coordinate)\nThe boundary can also be shifted using arrow keys", justify="left", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 21*scale, y = 22*scale)

    Label(FH, text="Partials", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 4*scale, y = 31*scale)
    FH.create_rectangle(12*scale, 31*scale, 16*scale, 34*scale, fill="#FFFFFF", width=0)
    FH.create_text(14*scale, 32.5*scale, text="ON", fill="#000000", font=("Arial", int(textscale*scale*1.25), "bold"))
    FH.create_rectangle(16*scale, 31*scale, 20*scale, 34*scale, fill="#000000", width=0)
    FH.create_text(18*scale, 32.5*scale, text="OFF", fill="#FFFFFF", font=("Arial", int(textscale*scale*1.25), "bold"))
    Label(FH, text="Toggle whether this instrument uses partials", justify="left", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 21*scale, y = 31*scale)

    Label(FH, text="Key Properties", font=("Arial", int(textscale*scale*2), "bold"), fg=textcolor, bg=bgcolor).place(x = 1*scale, y = 36*scale)

    Label(FH, text="SLFN on:\nSLFN off:", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 7.5*scale, y = 40*scale)
    FH.create_rectangle(16*scale, 40.5*scale, 20*scale, 42.5*scale, fill=colors["dark_custom_background"], width=0)
    FH.create_text(18*scale, 41.5*scale, text="6", fill="#FFFFFF", font=("Arial", int(textscale*scale*1.25), "bold"))
    FH.create_rectangle(16*scale, 43*scale, 20*scale, 45*scale, fill=colors["dark_custom_background"], width=0)
    FH.create_text(18*scale, 44*scale, text="−", fill="#FFFFFF", font=("Arial", int(textscale*scale*1.25), "bold"))
    Label(FH, text="Representation of the key in the single-line fingering notation, on and off (e.g. in 123 | 456, 6 is on, but in 123 | 45−, 6 is off)\nNote that when changing the label of the key, these values will update to the default value corresponding to the label", justify="left", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 21*scale, y = 40*scale)

    Label(FH, text="label size", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 6*scale, y = 46.5*scale)
    FH.create_rectangle(16*scale, 46.5*scale, 20*scale, 49.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(18*scale, 48*scale, text="1.0", fill="#000000", font=("Arial", int(textscale*scale*1.25), "bold"))
    Label(FH, text="Text size of key label (can be adjusted with arrow keys)", justify="left", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 21*scale, y = 46.5*scale)

    Label(FH, text="Type:", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 1.5*scale, y = 52*scale)
    for i, keytype in enumerate(["main", "octave", "second", "low", "high", "trill", "model", "special"]):
        x = i%4; y = i//4
        FH.create_oval((8 + x*3)*scale, (50.5 + y*3)*scale, (11 + x*3)*scale, (53.5 + y*3)*scale, fill=key_colors[keytype][0], width=0)
    Label(FH, text="Set type of key (see Fingering Diagram Help for more information)", justify="left", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 21*scale, y = 52*scale)

    Label(FH, text="xpos\nypos\nwidth\nheight", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 8.75*scale, y = 57.25*scale)
    FH.create_rectangle(16*scale, 57.5*scale, 20*scale, 59.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(18*scale, 58.5*scale, text="148", fill="#000000", font=("Arial", int(textscale*scale*1.25), "bold"))
    FH.create_rectangle(16*scale, 60*scale, 20*scale, 62*scale, fill="#FFFFFF", width=0)
    FH.create_text(18*scale, 61*scale, text="58", fill="#000000", font=("Arial", int(textscale*scale*1.25), "bold"))
    FH.create_rectangle(16*scale, 62.5*scale, 20*scale, 64.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(18*scale, 63.5*scale, text="28", fill="#000000", font=("Arial", int(textscale*scale*1.25), "bold"))
    FH.create_rectangle(16*scale, 65*scale, 20*scale, 67*scale, fill="#FFFFFF", width=0)
    FH.create_text(18*scale, 66*scale, text="28", fill="#000000", font=("Arial", int(textscale*scale*1.25), "bold"))
    Label(FH, text="Position and size of key on diagram\nChange position with arrow keys after selecting xpos or ypos\nChange size with arrow keys after selecting height or width", justify="left", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 21*scale, y = 58.15*scale)

    Label(FH, text="halfable", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 3.5*scale, y = 68.5*scale)
    FH.create_rectangle(12*scale, 68.5*scale, 16*scale, 71.5*scale, fill="#000000", width=0)
    FH.create_text(14*scale, 70*scale, text="ON", fill="#FFFFFF", font=("Arial", int(textscale*scale*1.25), "bold"))
    FH.create_rectangle(16*scale, 68.5*scale, 20*scale, 71.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(18*scale, 70*scale, text="OFF", fill="#000000", font=("Arial", int(textscale*scale*1.25), "bold"))
    Label(FH, text="Toggle whether this key can be half-pressed", justify="left", font=("Arial", int(textscale*scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 21*scale, y = 68.5*scale)

# WHEN APPLICATION OPENED
try:
    with open("temp.wfc", "r", encoding="utf-8-sig") as f:
        filecontent = importfile(f.read().strip().split("\n"))
        DATABASE = filecontent[0]
    PAGE = 0

    if "Custom" in DATABASE[0][1]:
        INSTRUMENT = "Custom"
        instruments["Custom"][1] = filecontent[1] / 100
        key_systems["custom"] = filecontent[2]
    else:
        INSTRUMENT = DATABASE[0][1]

    
    TONIC = DATABASE[0][2]
    TET = DATABASE[0][3]
    FILTERS["search"] = "none"
    if "partial" in key_systems[instruments[INSTRUMENT][0]]["special"]:
        FINGERING = [0, 0, 0, 1]
    else:
        FINGERING = [0, 0, 0, -0.5]
    if "trombone" in key_systems[instruments[INSTRUMENT][0]]["special"]:
        if FINGTYPE == "trill":
            FINGERING += [complex(1, 1), complex(0)]
        else:
            FINGERING += [complex(1), complex(0)]
    else:
        FINGERING += [complex(0), complex(0)]
    FINGERING.append("")
    FILTERS_TEMP_FINGERING = list(FINGERING)
    FILTERS_TEMP_PITCHES = list(PITCHES)
    FILTERS_TEMP_FINGTYPE = FINGTYPE
    render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
    render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)
    render_filters(FILTERS, TET, SELECT, TEMPVAR)
    render_options(INSTRUMENT, DATABASE, SETINSTRUMENT, SELECT, TEMPVAR)
    render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
except Exception:
    pass

# WHEN APPLICATION CLOSED
def onclose():
    with open("temp.wfc", "w", encoding="utf-8-sig") as f:
        f.write(exportfile(DATABASE))
    root.destroy()
root.protocol("WM_DELETE_WINDOW", onclose)

# APPLICATION START
render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)
render_options(INSTRUMENT, DATABASE, SETINSTRUMENT, SELECT, TEMPVAR)
render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, FILTERS, SELECT, TEMPVAR)
render_filters(FILTERS, TET, SELECT, TEMPVAR)

root.mainloop()
