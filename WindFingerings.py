# WindFingerings 1.1.9 by Valky River

version = "1.1.9"

from tkinter import *
from tkinter import filedialog as fd
import math
import colorsys
import copy

class CodeIncompleteError(Exception):
    def __init__(s, message="This functionality has not been coded yet"):
        super().__init__(message)

colors = {
    "pitch_background": "#008844",
    "pitch_box": "#FFFFFF",
    "pitch_selected": "#FFCC99",
    "description_background":"#770099",
    "dark_description_background":"#440055",
    "options_background":"#006666",
    "dark_options_background":"#004444",
    "options_database": "#00BBBB",
    "set_instrument": "#AAEEEE",
    "filters_background": "#887722",
    "searched": "#FFEE88"
}

scale = 8

horizontalscale = 1536
verticalscale = 792

h = horizontalscale # total horizontal
v = verticalscale # total vertical

root = Tk()
C = Canvas(root)
C.pack(fill=BOTH, expand=1)
root.geometry(str(h) + "x" + str(v))
root.title("WindFingerings "+version)
C.create_rectangle(0,0,horizontalscale+480,verticalscale+360, outline="#FFFFFF", fill="#FFFFFF", width=0)

# GLOBAL VARIABLES

INSTRUMENT = "Alto Saxophone"
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
FILTERS = {
    "tolerance": 0.15,
    "fingtype": ["note", "trill", "multi"],
    "tet": "none",
    "search": "none"
}

DATABASE = [["new-database.csv", INSTRUMENT, TONIC, TET, ""]]

SETINSTRUMENT = False

# DESCRIPTION
C.create_rectangle(2*scale, 35*scale, 76*scale, 44*scale, fill=colors["description_background"], width=0)
C.create_text(8.5*scale, 39.5*scale, text="Description", font=("Arial", int(1.5*scale), "bold"), fill="#FFFFFF")
DESCRIPTION = Text(root, fg="#FFFFFF", bg=colors["dark_description_background"], font=("Arial", 10))
DESCRIPTION.delete(1.0, END)
DESCRIPTION.insert(END, FINGERING[-1])
DESCRIPTION.place(x=15*scale, y=36*scale, width=60*scale, height=7*scale)

# DATABASE DESC
DATABASEDESC = Text(root, fg="#FFFFFF", bg=colors["dark_options_background"], font=("Arial", 12))
DATABASEDESC.place(x=100*scale, y=13*scale, width=68*scale, height=5.5*scale)

C.create_rectangle(2*scale, 90*scale, 76*scale, 97*scale, fill="#000000", width=0)
C.create_text(39*scale, 92.5*scale, text="WindFingerings "+version, font=("Arial", int(scale*1.75), "bold"), fill="#FFFFFF")
C.create_text(39*scale, 95*scale, text="by Valky River", font=("Arial", int(scale*1.25), "bold"), fill="#FFFFFF")

try:
    C.clipboard_get()
except:
    pass




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

    if isinstance(event, Event):
        item = C.find_closest(event.x, event.y)
        tags = C.itemcget(item, "tags").split(" ")
    else:
        tags = event
        
    #print(tags)
    #print(SELECT)

    if "removeentry" in tags and "data" in SELECT:
        SETINSTRUMENT = False
        index = int(SELECT[4:])
        DATABASE.pop(index)
        SELECT = ""
        render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)

    if SELECT != "":
        if "sposition" in SELECT:
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
            SELECT = ""
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)
            
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
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)
            
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
            elif SELECT == "databasedesc":
                DATABASE[0][-1] = DATABASEDESC.get("1.0", "end-1c")
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
                        temp_pitch = PITCHES[int(SELECT[-1])-1] * 2**(float(TEMPVAR)-notename(PITCHES[int(SELECT[-1])-1], 0)/1200)
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
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)
        
    if "clickable" in tags:
        if "key" in tags: # set new fingering
            temp_fingering = ((2**int(tags[2])) ^ FINGERING[0]) | FINGERING[1]
            temp_half = FINGERING[0] & FINGERING[1] & ~(2**int(tags[2]))
            temp_trill = FINGERING[2] & ~(2**int(tags[2]))
            FINGERING[0] = temp_fingering; FINGERING[1] = temp_half; FINGERING[2] = temp_trill
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            if "fingering" in FILTERS["search"]:
                render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)
            
        elif "partial" in tags: # set new partial
            FINGERING[3] = int(tags[2])
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            if "fingering" in FILTERS["search"]:
                render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)
            
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

        # HELP
        elif "fingeringhelp" in tags:
            fingering_help()
        elif "pitchhelp" in tags:
            pitch_help()
        elif "filtershelp" in tags:
            filters_help()


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
            if "fingering" in FILTERS["search"]:
                render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS) 

        elif "sposition" in tags[1]:
            new_pos = (event.x - float(tags[3])) / ((float(tags[4])-float(tags[3]))/(float(tags[6])-float(tags[5]))) + float(tags[5])
            if "trill" in tags[2]:
                FINGERING[int(tags[1][-1])+3] = complex(new_pos, new_pos)
            else:
                FINGERING[int(tags[1][-1])+3] = complex(new_pos, FINGERING[int(tags[1][-1])+3].imag)
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            if "fingering" in FILTERS["search"]:
                render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)


        # OPTIONS
        elif "setinstrument" in tags:
            instrument = ""
            for letter in tags[2]:
                if letter == "_":
                    instrument += " "
                else:
                    instrument += letter
            if "partial" in key_systems[instruments[instrument][0]]["special"]:
                FINGERING = [0, 0, 0, 1]
            else:
                FINGERING = [0, 0, 0, -0.5]
            if "trombone" in key_systems[instruments[instrument][0]]["special"]:
                if FINGTYPE == "trill":
                    FINGERING += [complex(1, 1), complex(0)]
                else:
                    FINGERING += [complex(1), complex(0)]
            else:
                FINGERING += [complex(0), complex(0)]
            FINGERING.append("")
            INSTRUMENT = instrument
            FILTERS["search"] = "none"
            DATABASE = list([["new-database.csv", INSTRUMENT, TONIC, TET, ""]])
            SETINSTRUMENT = False
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)
            render_filters(FILTERS, TET, SELECT, TEMPVAR)
            render_options(INSTRUMENT, DATABASE, SETINSTRUMENT)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)

        elif "selectinstrument" in tags:
            SETINSTRUMENT = True
            render_options(INSTRUMENT, DATABASE, SETINSTRUMENT)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)
   
        elif "cancelsetinstrument" in tags:
            SETINSTRUMENT = False
            render_options(INSTRUMENT, DATABASE, SETINSTRUMENT)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)

        elif "addentry" in tags:
            SETINSTRUMENT = False
            added = addentry((list(PITCHES), list(FINGERING), FINGTYPE), DATABASE)
            DATABASE = added[1]
            SELECT = "data"+str(added[0])
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)

        elif "savefile" in tags:
            file = fd.asksaveasfilename(
                title="Save file as .csv",
                defaultextension=".csv",
                filetypes=(("Comma-Separated Values File", "*.csv"), ("All files", "*.*"))
            )
            if file:
                DATABASE[0][0] = file.split("/")[-1]
                DATABASE[0][-1] = DATABASEDESC.get("1.0", "end-1c")
                try:
                    with open(file, "w", encoding="utf-8") as f:
                        f.write(exportfile(DATABASE))
                    render_options(INSTRUMENT, DATABASE, SETINSTRUMENT)
                except Exception as e:
                    E = Toplevel(C)
                    E.geometry("800x50")
                    E.title("Error saving file")
                    Label(E, text="Error saving file: "+str(e), font=("Arial", 12, "bold")).place(x=10, y=10)
                    

        elif "loadfile" in tags:
            file = fd.askopenfilename(
                title="Select .csv file",
                filetypes=(("Comma-Separated Values File", "*.csv"), ("All files", "*.*"))
            )
            if file:
                try:
                    with open(file, "r", encoding="utf-8") as f:
                        DATABASE = importfile(f.read().strip().split("\n"))
                    PAGE = 0
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
                    render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
                    render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)
                    render_filters(FILTERS, TET, SELECT, TEMPVAR)
                    render_options(INSTRUMENT, DATABASE, SETINSTRUMENT)
                    render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)
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
                if "fingering" in FILTERS["search"]:
                    render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)
            except Exception as e:
                E = Toplevel(C)
                E.geometry("800x50")
                E.title("Error loading from clipboard")
                Label(E, text="Error loading from clipboard: "+str(e), font=("Arial", 12, "bold")).place(x=10, y=10)

        # DATABASE — each entry is in the form (pitches, fingering, fingtype)
        elif "prevpage" in tags and NUM_PAGES != 0:
            PAGE = (PAGE - 1) % NUM_PAGES
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)
        elif "nextpage" in tags and NUM_PAGES != 0:
            PAGE = (PAGE + 1) % NUM_PAGES 
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)
            
        elif "prevpage2" in tags and NUM_PAGES != 0:
            PAGE = NUM_PAGES - 1 if PAGE == 0 else max(0, PAGE - 20) % NUM_PAGES
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)
        elif "nextpage2" in tags and NUM_PAGES != 0:
            PAGE = 0 if PAGE == NUM_PAGES - 1 else min(PAGE + 20, NUM_PAGES - 1) % NUM_PAGES 
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)

        elif "entry" in tags:
            SELECT = tags[2]
            PITCHES = sorted(list(DATABASE[int(tags[2][4:])][0]))
            FINGERING = list(DATABASE[int(tags[2][4:])][1])
            FINGTYPE = DATABASE[int(tags[2][4:])][2]
            render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
            render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)

        elif "filters" in tags:
            if tags[2] == "fingtypef":
                if tags[3] in FILTERS["fingtype"]:
                    FILTERS["fingtype"].remove(tags[3])
                else:
                    FILTERS["fingtype"].append(tags[3])
            else:
                FILTERS[tags[2][:-1]] = tags[3]
            render_filters(FILTERS, TET, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)

        elif "clearsearch" in tags:
            FILTERS["search"] = "none"
            render_filters(FILTERS, TET, SELECT, TEMPVAR)
            render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)

        elif "tolerance" in tags:
            SELECT = "tolerance_" + tags[2]
            render_filters(FILTERS, TET, SELECT, TEMPVAR)
      
    elif "description" in tags or "databasedesc" in tags:
        SELECT = tags[0]
            
def descriptionclick(event):
    onclick(["description"])

def databasedescclick(event):
    onclick(["databasedesc"])

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
                if "fingering" in FILTERS["search"]:
                    render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)
            elif "partial" in tags:
                FINGERING[3] = -int(tags[2])-1
                render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
                if "fingering" in FILTERS["search"]:
                    render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)

            elif "sposition" in tags[2] and ("setto" in tags[2]):
                new_pos = float(tags[3])
                if new_pos >= FINGERING[int(tags[1][-1])+3].real:
                    FINGERING[int(tags[1][-1])+3] = complex(new_pos, new_pos)
                else:
                    FINGERING[int(tags[1][-1])+3] = complex(FINGERING[int(tags[1][-1])+3].real, new_pos)
                render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
                if "fingering" in FILTERS["search"]:
                    render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)
                
            elif "sposition" in tags[1]:
                new_pos = (event.x - float(tags[3])) / ((float(tags[4])-float(tags[3]))/(float(tags[6])-float(tags[5]))) + float(tags[5])
                if "left" in tags[2] or "trill" in tags[2]:
                    FINGERING[int(tags[1][-1])+3] = complex(FINGERING[int(tags[1][-1])+3].real, new_pos)
                else:
                    FINGERING[int(tags[1][-1])+3] = complex(new_pos, new_pos)
                render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
                if "fingering" in FILTERS["search"]:
                    render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)
                    

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
            if "fingering" in FILTERS["search"]:
                render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)


def onkey(event):

    global INSTRUMENT
    global FINGERING
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

    if SELECT[:-1] in ["freq", "notename", "centsdev", "concertname", "concertdev"] or SELECT == "tet":
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
        render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)
        
    elif "sposition" in SELECT:
        if pressed in "0123456789." and len(TEMPVAR) < 5:
            TEMPVAR += pressed
        elif pressed == "backspace":
            TEMPVAR = TEMPVAR[:-1]

        if "number" in SELECT:
            if pressed == "up" or pressed == "right":
                temp_sposition = FINGERING[int(SELECT[9])+3].real + 12/TET
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
                temp_sposition = FINGERING[int(SELECT[9])+3].real - 12/TET
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
            if "fingering" in FILTERS["search"]:
                    render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)


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
                if "fingering" in FILTERS["search"]:
                    render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)
            
            


C.bind("<Button-1>", onclick)
C.bind("<B1-Motion>", spositionclick)
C.bind("<Button-2>", middleclick)
C.bind("<B2-Motion>", spositiontrillclick)
C.bind("<Button-3>", rightclick)

DESCRIPTION.bind("<Button-1>", descriptionclick)
DATABASEDESC.bind("<Button-1>", databasedescclick)


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

for key in list("abcdefghijklmnopqrstuvwxyz."):
    root.bind("<" + key + ">", onkey)
for key in list("0123457689"):
    root.bind("<Key-" + key + ">", onkey)

key_replacements = {
    "period": ".",
    "numbersign": "#",
    "s": "#",
    "S": "#",
    "plus": "+",
    "minus": "-",
    "equal": "+"
}
    






# PRESETS

tempvarparams = {
    "freq": [7, "0123457689."],
    "notename": [4, "abcdefgABCDEFG-0123456789#"],
    "centsdev": [6, "0123457689.-+"],
    "concertname": [4, "abcdefgABCDEFG-0123456789#"],
    "concertdev": [6, "0123457689.-+"],
    "te": [3, "0123457689"],
}

fingtypes = {
    "note": 1,
    "trill": 2,
    "multi2": 2,
    "multi3": 3,
    "multi4": 4
}

key_colors = {
    "main": ["#FFFFFF", "#000000", "#999999"],
    "octave": ["#DDDDDD", "#555555"],
    "second": ["#99EEBB", "#006633"],
    "low": ["#FFCCCC", "#770022"],
    "high": ["#CCEE77", "#556600"],
    "trill": ["#BBDDFF", "#002288"],
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
    "Flute": ["flute", 0],
    #"Alto Flute": ["?", -5],
    #"Bass Flute": ["?", -12],

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
    #"Contra-alto Cl": ["?", -21],
    "Contrabass Clarinet": ["bassclar", -26],

    # SAXOPHONES
    "Sopranino Saxophone": ["saxophone", 3],
    "Soprano Saxophone": ["saxophone", -2],
    "Alto Saxophone": ["saxophone", -9],
    "Tenor Saxophone": ["saxophone", -14],
    "Baritone Saxophone": ["saxophone", -21],
    "Bass Saxophone": ["saxophone", -26],
    #"Contrabass Saxophone": ["?", -33],

    # HIGHER BRASS
    "Bb Piccolo Trumpet": ["4valve", 10],
    "Trumpet in C": ["trumpet", 0],
    "Trumpet in Bb": ["trumpet", -2],
    #"Bass Trumpet": ["?", -14],
    #"Eb Soprano Cornet": ["?", 3],
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
    "Baritone Horn": ["4valve", -14],
    "Euphonium": ["4valve", -14],
    "F Tuba": ["tuba", 0],
    "Eb Tuba": ["tuba", 0],
    "CC Tuba": ["tuba", 0],
    "BBb Tuba": ["tuba", 0],

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
    "piccolo": { # needs confirmation
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
        2: {"x1":8, "y1":12, "x2":15, "y2":19, "type":"main", "halfable":False, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
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
        24: {"x1":67.5, "y1":8.5, "x2":72.5, "y2":11, "type":"model", "halfable":True, "label":"c", "labelsize":1, "descname":"c", "descoff":""},
        25: {"x1":72.5, "y1":18.5, "x2":76, "y2":22, "type":"low", "halfable":True, "label":"C", "labelsize":1, "descname":" C", "descoff":""},
        26: {"x1":74.5, "y1":15, "x2":78, "y2":18.5, "type":"low", "halfable":True, "label":"C#", "labelsize":1, "descname":" C#", "descoff":""},
        27: {"x1":76.5, "y1":18.5, "x2":80, "y2":22, "type":"second", "halfable":True, "label":"Eb", "labelsize":1, "descname":" Eb", "descoff":""},
    },

    "corangl": {
        "parameters": {"keys":27, "LR_split":16, "separator":" | ", "offsetx":-4, "offsety":-1, "shiftx":-1, "shifty":1.75, "Lx":6, "Ly":3, "Mx":49, "My":13, "Bx":42, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": [],
        0: {"x1":8, "y1":23, "x2":12.5, "y2":26, "type":"model", "halfable":False, "label":"III", "labelsize":1, "descname":"III ", "descoff":""},
        1: {"x1":12.5, "y1":23, "x2":17, "y2":26, "type":"octave", "halfable":False, "label":"I", "labelsize":1, "descname":"I ", "descoff":""},
        2: {"x1":8, "y1":9, "x2":14, "y2":12, "type":"octave", "halfable":False, "label":"II", "labelsize":1, "descname":"II ", "descoff":""},
        3: {"x1":12, "y1":12, "x2":19, "y2":19, "type":"main", "halfable":False, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        4: {"x1":19.5, "y1":13.25, "x2":24, "y2":17.75, "type":"octave", "halfable":False, "label":"½", "labelsize":1.75, "descname":"h", "descoff":""},
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
        23: {"x1":67.5, "y1":8.5, "x2":72.5, "y2":11, "type":"model", "halfable":True, "label":"c", "labelsize":1, "descname":"c", "descoff":""},
        24: {"x1":72.5, "y1":18.5, "x2":76, "y2":22, "type":"low", "halfable":True, "label":"C", "labelsize":1, "descname":" C", "descoff":""},
        25: {"x1":74.5, "y1":15, "x2":78, "y2":18.5, "type":"low", "halfable":True, "label":"C#", "labelsize":1, "descname":" C#", "descoff":""},
        26: {"x1":76.5, "y1":18.5, "x2":80, "y2":22, "type":"second", "halfable":True, "label":"Eb", "labelsize":1, "descname":" Eb", "descoff":""},
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
        1: {"x1":13.5, "y1":22.5, "x2":17.5, "y2":26.5, "type":"main", "halfable":False, "label":"T", "labelsize":6/5, "descname":"T ", "descoff":" "},
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
        16: {"x1":46.5, "y1":20, "x2":48.5, "y2":23, "type":"trill", "halfable":False, "label":"f#", "labelsize":2/3, "descname":"f# ", "descoff":""},
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
        1: {"x1":16.5, "y1":27.5, "x2":20.5, "y2":31.5, "type":"main", "halfable":False, "label":"T", "labelsize":6/5, "descname":"T ", "descoff":" "},
        2: {"x1":12, "y1":10, "x2":17, "y2":13, "type":"high", "halfable":False, "label":"G#", "labelsize":1, "descname":"G# ", "descoff":""},
        3: {"x1":10, "y1":14, "x2":15, "y2":17, "type":"high", "halfable":False, "label":"A", "labelsize":1, "descname":"A ", "descoff":""},
        4: {"x1":16, "y1":12, "x2":23, "y2":19, "type":"main", "halfable":True, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
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
        20: {"x1":46.5, "y1":19, "x2":48.5, "y2":22, "type":"trill", "halfable":False, "label":"f#", "labelsize":2/3, "descname":"f# ", "descoff":""},
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
        "parameters": {"keys":7, "LR_split":4, "separator":" ", "offsetx":-4, "offsety":-1, "shiftx":3.5, "shifty":2, "Lx":6, "Ly":3, "Mx":39.5, "My":32, "Bx":39.5, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": ["partial", "trumpet"],
        0: {"x1":7, "y1":9, "x2":14, "y2":16, "type":"main", "halfable":True, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        1: {"x1":15, "y1":9, "x2":22, "y2":16, "type":"main", "halfable":True, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        2: {"x1":23, "y1":9, "x2":30, "y2":16, "type":"main", "halfable":True, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        3: {"x1":31, "y1":9, "x2":38, "y2":16, "type":"model", "halfable":True, "label":"4", "labelsize":2, "descname":"4", "descoff":""},
        4: {"x1":21, "y1":20, "x2":32, "y2":22, "type":"sposition1", "preset":"trumpet", "min":0, "max":1, "descname":"", "descoff":""},
        5: {"x1":5, "y1":20, "x2":16, "y2":22, "type":"sposition2", "preset":"trumpet", "min":0, "max":1, "descname":"", "descoff":""},
        6: {"x":42, "y":8, "type":"partial", "descname":"", "descoff":""},
    },

    "horn": {
        "parameters": {"keys":7, "LR_split":6, "separator":" ", "offsetx":-4, "offsety":-1, "shiftx":3, "shifty":2, "Lx":6, "Ly":3, "Mx":40, "My":32, "Bx":40, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": ["partial"],
        0: {"x1":15, "y1":12, "x2":22, "y2":19, "type":"main", "halfable":True, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        1: {"x1":23, "y1":12, "x2":30, "y2":19, "type":"main", "halfable":True, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        2: {"x1":31, "y1":12, "x2":38, "y2":19, "type":"main", "halfable":True, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        3: {"x1":5, "y1":10.5, "x2":10, "y2":15.5, "type":"model", "halfable":True, "label":"F", "labelsize":4/3, "descname":" F", "descoff":""},
        4: {"x1":10, "y1":10.5, "x2":15, "y2":15.5, "type":"model", "halfable":True, "label":"Bb", "labelsize":4/3, "descname":" Bb", "descoff":""},
        5: {"x1":7.5, "y1":15, "x2":12.5, "y2":20, "type":"model", "halfable":True, "label":"alto", "labelsize":1, "descname":" A", "descoff":""},
        6: {"x":42.5, "y":8, "type":"partial", "descname":"", "descoff":""},
    },

    "trombone": {
        "parameters": {"keys":6, "LR_split":5, "separator":" ", "offsetx":-4, "offsety":-1, "shiftx":2, "shifty":2, "Lx":6, "Ly":3, "Mx":41, "My":32, "Bx":41, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": ["partial", "trombone"],
        0: {"x1":6.5, "y1":11, "x2":38.5, "y2":14, "type":"sposition1", "preset":"trombone", "min":1, "max":8, "descname":"", "descoff":""},
        1: {"x1":18, "y1":20, "x2":22, "y2":24, "type":"main", "halfable":False, "label":"F", "labelsize":3/2, "descname":"F", "descoff":""},
        2: {"x1":18, "y1":25, "x2":22, "y2":29, "type":"special", "halfable":False, "label":"E−*", "labelsize":5/4, "descname":"E", "descoff":""},
        3: {"x1":23, "y1":25, "x2":27, "y2":29, "type":"model", "halfable":False, "label":"   G\nEb", "labelsize":1, "descname":"Eb", "descoff":""},
        4: {"x1":23, "y1":20, "x2":27, "y2":24, "type":"model", "halfable":False, "label":"Gb\n    D", "labelsize":1, "descname":"D", "descoff":""},
        5: {"x":43.5, "y":8, "type":"partial", "descname":"", "descoff":""},
    },

    "4valve": {
        "parameters": {"keys":5, "LR_split":4, "separator":" ", "offsetx":-4, "offsety":-1, "shiftx":2, "shifty":2, "Lx":6, "Ly":3, "Mx":41, "My":32, "Bx":41, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": ["partial"],
        0: {"x1":7, "y1":12, "x2":14, "y2":19, "type":"main", "halfable":True, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        1: {"x1":15, "y1":12, "x2":22, "y2":19, "type":"main", "halfable":True, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        2: {"x1":23, "y1":12, "x2":30, "y2":19, "type":"main", "halfable":True, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        3: {"x1":31, "y1":12, "x2":38, "y2":19, "type":"model", "halfable":True, "label":"4", "labelsize":2, "descname":"4", "descoff":""},
        4: {"x":43.5, "y":8, "type":"partial", "descname":"", "descoff":""},
    },

    "tuba": {
        "parameters": {"keys":7, "LR_split":6, "separator":" ", "offsetx":-4, "offsety":-1, "shiftx":2, "shifty":2, "Lx":6, "Ly":3, "Mx":41, "My":32, "Bx":41, "By":32, "Rx":80, "Ry":32, "Descy":36},
        "special": ["partial"],
        0: {"x1":7, "y1":6, "x2":14, "y2":13, "type":"main", "halfable":True, "label":"1", "labelsize":2, "descname":"1", "descoff":"−"},
        1: {"x1":15, "y1":6, "x2":22, "y2":13, "type":"main", "halfable":True, "label":"2", "labelsize":2, "descname":"2", "descoff":"−"},
        2: {"x1":23, "y1":6, "x2":30, "y2":13, "type":"main", "halfable":True, "label":"3", "labelsize":2, "descname":"3", "descoff":"−"},
        3: {"x1":31, "y1":6, "x2":38, "y2":13, "type":"main", "halfable":True, "label":"4", "labelsize":2, "descname":"4", "descoff":""},
        4: {"x1":15, "y1":18, "x2":22, "y2":25, "type":"model", "halfable":True, "label":"5", "labelsize":2, "descname":"5", "descoff":""},
        5: {"x1":23, "y1":18, "x2":30, "y2":25, "type":"model", "halfable":True, "label":"6", "labelsize":2, "descname":"6", "descoff":""},
        6: {"x":43.5, "y":8, "type":"partial", "descname":"", "descoff":""},
    }
}




# FUNCTIONS

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

def notename(pitch, transpose=0):
    pitch /= 2**(transpose/12)
    C0 = (55/4) * 2**(1/4)
    notenames = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    notenum = int(round(math.log(pitch/C0, 2**(1/12)), 0))
    centsdev = (((math.log(pitch/C0, 2**(1/12)) + 0.5) % 1) - 0.49999999999) * 100
    name = str(notenames[notenum % 12]) + styleminus(math.floor(notenum / 12))
    return name, centsdev


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


def exportfile(database=DATABASE):

    no_comma_databasedesc = ""
    for char in database[0][4].strip():
        no_comma_databasedesc += ("`" if char == "," else ("$" if char == "\"" else ("!" if char == "\n" else char)))

    csv_string = database[0][0] + "\nInstrument: " + database[0][1] + "\nTransposition: " + str(instruments[database[0][1]][1]*100) + " cents\nTonic: " + str(round(database[0][2], 6)) + " Hz\nTemperament: " + str(database[0][3]) + "-TET\nDescription: " + no_comma_databasedesc
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


def importfile(file):

    comma_databasedesc = ""
    for char in file[5].split(",")[0][13:]:
        comma_databasedesc += ("," if char == "`" else ("\"" if char == "$" else ("\n" if char == "!" else char)))

    database = [[
        file[0].split(",")[0], # name
        file[1].split(",")[0][12:], # instrument
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

    return database


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
        if key == key_systems[instruments[INSTRUMENT][0]]["parameters"]["LR_split"]:
            desc_string += key_systems[instruments[INSTRUMENT][0]]["parameters"]["separator"]
        if isinstance(state, complex):
            if fingering[2] != "trill" or round(state.real, 6) == round(state.imag, 6):
                desc_string += "{"+str(round(state.real, 2))+"} "
            else:
                desc_string += "[{"+str(round(state.real, 2))+"}{"+str(round(state.imag, 2))+"}] "
        elif state == 3:
            desc_string += "["+key_systems[instruments[INSTRUMENT][0]][key]["descname"].strip()+"]"
        elif state == 2:
            desc_string += "h"
        elif state == 1:
            desc_string += key_systems[instruments[INSTRUMENT][0]][key]["descname"]
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

def render_key(key, keynum, offsetx=0, offsety=0, shiftx=0, shifty=0, state=0, partial=0, select=SELECT, tempvar=TEMPVAR):

    global FINGTYPE
    global FINGERING
    
    if key["type"] == "partial":
        for p in range(17):
            partialscale = 4
            if p == 0:
                x = 7
                y = 0
                text_string = "other"
                text_size = 1
            elif p == 16:
                x = 6
                y = 0
                text_string = "16+"
                text_size = 5/4
            else:
                x = (p / (2**int(math.log(p, 2))) % 1)*8
                y = int(math.log(p, 2))
                text_string = str(p) + "+"*int(p/16)
                text_size = 5/4
                
            x1 = (key["x"] + offsetx + shiftx + partialscale*x)*scale
            x2 = (key["x"] + offsetx + shiftx + partialscale*(x+1))*scale
            y1 = (key["y"] + offsety + shifty + partialscale*y)*scale
            y2 = (key["y"] + offsety + shifty + partialscale*(y+1))*scale
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
            C.create_text((x1+x2)/2, (y1+y2)/2, text=text_string, font=("Arial", int(text_size*scale), "bold"), fill=textcolor, tags=("clickable", "partial", str(p)))
            if p >= 8 and p <= 15:
                C.create_text((x1+x2)/2, (key["y"] + offsety + shifty + partialscale*4.2)*scale, text=str(int(round(1200*math.log(p/8, 2), 0)))+"c", font=("Arial", int(text_size*scale*(5/6)), "bold"), fill="#FFFFFF", tags=("partial"))
            elif p == 0:
                C.create_text((key["x"]+offsetx+shiftx+partialscale*4)*scale, (key["y"]+offsety+shifty+partialscale*-0.5)*scale, text="partials", font=("Arial", int(text_size*scale*2), "bold"), fill="#FFFFFF", tags=("partial"))

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
            C.create_text((x1+x2)/2 + 2.875*scale, y2 + 2*scale, text=tempvar if key["type"]+"number" in select and tempvar != "" in select else round(state.real, 2), font=("Arial", int(scale*1.25), "bold"), fill="#000000", tags=("clickable", key["type"], key["type"]+"number", minimum, maximum))
            C.create_rectangle((x1+x2)/2 - 5.5*scale, y2 + 0.5*scale, (x1+x2)/2 - 0.25*scale, y2 + 3.5*scale, fill=(key_colors["model"][0] if key["type"]+"trillnum" in select else key_colors["main"][0]), width=0, tags=("clickable", key["type"], key["type"]+"trillnum", minimum, maximum))
            C.create_text((x1+x2)/2 - 2.875*scale, y2 + 2*scale, text=tempvar if key["type"]+"trillnum" in select and tempvar != "" in select else round(state.imag, 2), font=("Arial", int(scale*1.25), "bold"), fill="#000000", tags=("clickable", key["type"], key["type"]+"trillnum", minimum, maximum))

        else:
            x_position = x1 + ((x2-x1)/(maximum-minimum))*(state.real - minimum)
            C.create_rectangle(x1, y1, x_position, y2, fill=key_colors["main"][1], width=0, tags=("clickable", key["type"], key["type"]+"left", str(x1), str(x2), minimum, maximum))

            C.create_rectangle((x1+x2)/2 - 3*scale, y2 + 0.5*scale, (x1+x2)/2 + 3*scale, y2 + 3.5*scale, fill=(key_colors["model"][0] if key["type"]+"number" in select else key_colors["main"][0]), width=0, tags=("clickable", key["type"], key["type"]+"number", minimum, maximum))
            C.create_text((x1+x2)/2, y2 + 2*scale, text=tempvar if key["type"]+"number" in select and tempvar != "" in select else round(state.real, 2), font=("Arial", int(scale*1.25), "bold"), fill="#000000", tags=("clickable", key["type"], key["type"]+"number", minimum, maximum))

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
                C.create_text(xpos, y1 - 2*scale, text=position_text, font=("Arial", int(scale*1.15), "bold"), fill="#000000", tags=("clickable", key["type"], key["type"]+"setto", pos))
                
                t += 1
                pos += multiplier
                
        elif key["preset"] == "trumpet":
            for pos in range(3):
                position_text = "0¼½"[pos]
                pos /= 4
                xpos = x1 + ((x2-x1)/(maximum-minimum))*(pos - minimum) 
                C.create_oval(xpos - 1*scale, y1 - 0.5*scale, xpos + 1*scale, y1 - 2.5*scale, fill=key_colors["main"][0], width=0, tags=("clickable", key["type"], key["type"]+"setto", pos))
                C.create_text(xpos, y1 - 1.5*scale, text=position_text, font=("Arial", int(scale*1.15), "bold"), fill="#000000", tags=("clickable", key["type"], key["type"]+"setto", pos))
    
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
            C.create_text((x1+x2)/2, (y1+y2)/2, text=key["label"], font=("Arial", int(key["labelsize"]*scale*1.25), "bold"), fill=textcolor, tags=("clickable", "key", str(keynum), "halfable"))
        else:
            C.create_oval(x1, y1, x2, y2, fill=keycolor, width=0, tags=("clickable", "key", str(keynum)))
            C.create_text((x1+x2)/2, (y1+y2)/2, text=key["label"], font=("Arial", int(key["labelsize"]*scale*1.25), "bold"), fill=textcolor, tags=("clickable", "key", str(keynum)))
    
    
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
    C.create_rectangle(Lx, Ly, Mx, My, fill="#5588BB", width=0, tags=("key"))
    C.create_rectangle(Lx, Ly, Bx, By, fill="#5588BB", width=0, tags=("key"))

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

    C.create_rectangle(Lx, Ry, Rx, Descy, fill="#000000", width=0, tags=("key"))
    desc_string = ""
    for key, state in enumerate(states):
        if key == parameters["LR_split"]:
            desc_string += parameters["separator"]
        if isinstance(state, complex):
            if FINGTYPE != "trill" or round(state.real, 6) == round(state.imag, 6):
                desc_string += "{"+str(round(state.real, 2))+"} "
            else:
                desc_string += "[{"+str(round(state.real, 2))+"}{"+str(round(state.imag, 2))+"}] "
        elif state == 3:
            desc_string += "["+key_systems[key_system][key]["descname"].strip()+"]"
        elif state == 2:
            desc_string += "½"
        elif state == 1:
            desc_string += key_systems[key_system][key]["descname"]
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
    C.create_text((Lx+Rx)/2, (Ry+Descy)/2, text=desc_string, font=("Arial", int(scale*1.5*min(1, 75/len(desc_string))), "bold"), fill="#FFFFFF", tags=("key"))

    C.create_text((parameters["Lx"]+parameters["offsetx"]+8.4)*scale, (parameters["Ly"]+parameters["offsety"]+1.9)*scale, text="Right-click to half-press\nMiddle-click to trill", font=("Arial", int(scale*1), "bold"), fill="#FFFFFF", tags=("key"))
    C.create_oval(72*scale, 3*scale, 75*scale, 6*scale, fill=colors["dark_description_background"], width=0, tags=("clickable", "fingeringhelp"))
    C.create_text(73.5*scale, 4.5*scale, text="?", font=("Arial", int(scale*1.5), "bold"), fill="#FFFFFF", tags=("clickable", "fingeringhelp"))
    

def render_pitches(pitches=[440.0], fingtype="note", select="", tempvar="", transpose=0, tonic=440.0, tet=12):
    C.delete("pitch")
    C.delete("fingtype")
    C.create_rectangle(2*scale, 46*scale, 76*scale, 65*scale, fill=colors["pitch_background"], width=0, tags=("pitch"))
    C.create_rectangle(2*scale, 65*scale, 76*scale, 70*scale, fill="#000000", width=0, tags=("pitch"))

    # FINGERING TYPE
    C.create_text(10*scale, 48.5*scale, text="Fingering type:", font=("Arial", int(scale*3/2), "bold"), fill="#FFFFFF", tags=("fingtype"))
    C.create_rectangle(18*scale, 47*scale, 30*scale, 50*scale, fill=("#000000" if fingtype == "note" else "#FFFFFF"), width=0, tags=("clickable", "fingtype", "note"))
    C.create_text(24*scale, 48.5*scale, text="Note/Microtone", font=("Arial", int(scale*6/5), "bold"), fill=("#FFFFFF" if fingtype == "note" else "#000000"), tags=("clickable", "fingtype", "note"))
    C.create_rectangle(30.5*scale, 47*scale, 42.5*scale, 50*scale, fill=("#000000" if fingtype == "trill" else "#FFFFFF"), width=0, tags=("clickable", "fingtype", "trill"))
    C.create_text(36.5*scale, 48.5*scale, text="Trill/Tremolo", font=("Arial", int(scale*6/5), "bold"), fill=("#FFFFFF" if fingtype == "trill" else "#000000"), tags=("clickable", "fingtype", "trill"))
    C.create_rectangle(43*scale, 47*scale, 55*scale, 50*scale, fill=("#000000" if "multi" in fingtype else "#FFFFFF"), width=0, tags=("clickable", "fingtype", "multi"))
    C.create_text(49*scale, 48.5*scale, text="Multiphonic", font=("Arial", int(scale*6/5), "bold"), fill=("#FFFFFF" if "multi" in fingtype else "#000000"), tags=("clickable", "fingtype", "multi"))
    if "multi" in fingtype:
        C.create_text(60.5*scale, 48.5*scale, text="Pitches:", font=("Arial", int(scale*3/2), "bold"), fill="#FFFFFF", tags=("fingtype"))
        C.create_rectangle(65*scale, 47*scale, 68*scale, 50*scale, fill=("#000000" if fingtype == "multi2" else "#FFFFFF"), width=0, tags=("clickable", "fingtype", "multi2"))
        C.create_text(66.5*scale, 48.5*scale, text="2", font=("Arial", int(scale*4/3), "bold"), fill=("#FFFFFF" if fingtype == "multi2" else "#000000"), tags=("clickable", "fingtype", "multi2"))
        C.create_rectangle(68.5*scale, 47*scale, 71.5*scale, 50*scale, fill=("#000000" if fingtype == "multi3" else "#FFFFFF"), width=0, tags=("clickable", "fingtype", "multi3"))
        C.create_text(70*scale, 48.5*scale, text="3", font=("Arial", int(scale*4/3), "bold"), fill=("#FFFFFF" if fingtype == "multi3" else "#000000"), tags=("clickable", "fingtype", "multi3"))
        C.create_rectangle(72*scale, 47*scale, 75*scale, 50*scale, fill=("#000000" if fingtype == "multi4" else "#FFFFFF"), width=0, tags=("clickable", "fingtype", "multi4"))
        C.create_text(73.5*scale, 48.5*scale, text="4", font=("Arial", int(scale*4/3), "bold"), fill=("#FFFFFF" if fingtype == "multi4" else "#000000"), tags=("clickable", "fingtype", "multi4"))
    else:
         C.create_text(66*scale, 48.5*scale, text=" Select a box to change pitch by\ntyping it in or using arrow keys", font=("Arial", int(scale*0.95), "bold"), fill="#FFFFFF", tags=("fingtype"))
        
    # PITCHES
    for p, pitch in enumerate(pitches):
        C.create_text((7.1*scale if fingtype == "note" else 6.4*scale), (52 + 3.5*p)*scale, text=("Pitch:" if fingtype == "note" else "Pitch "+str(p+1)+":"), font=("Arial", int(scale*3/2), "bold"), fill="#FFFFFF", tags=("pitch"))

        C.create_rectangle(10.5*scale, (50.5 + 3.5*p)*scale, 17.5*scale, (53.5 + 3.5*p)*scale, fill=(colors["pitch_selected"] if select == "freq"+str(p+1) else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "freq"+str(p+1)))
        C.create_text(14*scale, (52 + 3.5*p)*scale, text=(tempvar if select == "freq"+str(p+1) and tempvar != "" else round(pitch, 2)), font=("Arial", int(scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "freq"+str(p+1)))
        C.create_text(19.3*scale, (52 + 3.5*p)*scale, text="Hz", font=("Arial", int(scale*3/2), "bold"), fill="#FFFFFF", tags=("pitch"))

        C.create_rectangle(22*scale, (50.5 + 3.5*p)*scale, 26*scale, (53.5 + 3.5*p)*scale, fill=(colors["pitch_selected"] if select == "notename"+str(p+1) else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "notename"+str(p+1)))
        C.create_text(24*scale, (52 + 3.5*p)*scale, text=(tempvar if select == "notename"+str(p+1) and tempvar != "" else notename(pitch, transpose)[0]), font=("Arial", int(scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "notename"+str(p+1)))
        C.create_rectangle(26.5*scale, (50.5 + 3.5*p)*scale, 32.5*scale, (53.5 + 3.5*p)*scale, fill=(colors["pitch_selected"] if select == "centsdev"+str(p+1) else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "centsdev"+str(p+1)))
        C.create_text(29.5*scale, (52 + 3.5*p)*scale, text=(tempvar if select == "centsdev"+str(p+1) and tempvar != "" else plusminus(round(notename(pitch, transpose)[1], 2))), font=("Arial", int(scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "centsdev"+str(p+1)))

        C.create_text(37.5*scale, (52 + 3.5*p)*scale, text="(concert", font=("Arial", int(scale*3/2), "bold"), fill="#FFFFFF", tags=("pitch"))
        C.create_rectangle(42.5*scale, (50.5 + 3.5*p)*scale, 46.5*scale, (53.5 + 3.5*p)*scale, fill=(colors["pitch_selected"] if select == "concertname"+str(p+1) else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "concertname"+str(p+1)))
        C.create_text(44.5*scale, (52 + 3.5*p)*scale, text=(tempvar if select == "concertname"+str(p+1) and tempvar != "" else notename(pitch, 0)[0]), font=("Arial", int(scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "concertname"+str(p+1)))
        C.create_rectangle(47*scale, (50.5 + 3.5*p)*scale, 53*scale, (53.5 + 3.5*p)*scale, fill=(colors["pitch_selected"] if select == "concertdev"+str(p+1) else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "concertdev"+str(p+1)))
        C.create_text(50*scale, (52 + 3.5*p)*scale, text=(tempvar if select == "concertdev"+str(p+1) and tempvar != "" else plusminus(round(notename(pitch, 0)[1], 2))), font=("Arial", int(scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "concertdev"+str(p+1)))
        C.create_text(53.5*scale, (52 + 3.5*p)*scale, text=")", font=("Arial", int(scale*3/2), "bold"), fill="#FFFFFF", tags=("pitch"))

        tup = colorsys.hsv_to_rgb(math.log(pitch/tonic, 2) % 1, 0.5, (math.sin(2*math.pi*(math.log(pitch/tonic, 2) % 1 - 3/5))/12) + (5/12))
        hx = []
        for elem in tup:
            if int(elem*255) <= 15:
                hx.append("0"+((str(hex(int(elem*255))).upper()+"d")[2:-1]))
            else:
                hx.append((str(hex(int(elem*255))).upper()+"d")[2:-1])
        pitchcolor = "#"+"".join(hx)

        C.create_rectangle(55*scale, (50.5 + 3.5*p)*scale, 75*scale, (53.5 + 3.5*p)*scale, fill=pitchcolor, width=0, tags=("pitch"))
        C.create_text(65*scale, (52 + 3.5*p)*scale, text=str(int(round(tet*math.log(pitch/tonic, 2), 0)) % tet) + "\\" + str(TET) + " " + plusminus(round(100 * (tet*math.log(pitch/tonic, 2) - round(tet*math.log(pitch/tonic, 2), 0) + 0.0000000001), 2)) + "%", font=("Arial", int(scale*7/4), "bold"), fill="#FFFFFF", tags=("pitch"))

    # TONIC
    C.create_text(6.9*scale, 67.5*scale, text=("Tonic:"), font=("Arial", int(scale*3/2), "bold"), fill="#FFFFFF", tags=("pitch"))

    C.create_rectangle(10.5*scale, 66*scale, 17.5*scale, 69*scale, fill=(colors["pitch_selected"] if select == "freq0" else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "freq0"))
    C.create_text(14*scale, 67.5*scale, text=(tempvar if select == "freq0" and tempvar != "" else round(tonic, 2)), font=("Arial", int(scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "freq0"))
    C.create_text(19.3*scale, 67.5*scale, text="Hz", font=("Arial", int(scale*3/2), "bold"), fill="#FFFFFF", tags=("pitch"))

    C.create_rectangle(22*scale, 66*scale, 26*scale, 69*scale, fill=(colors["pitch_selected"] if select == "notename0" else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "notename0"))
    C.create_text(24*scale, 67.5*scale, text=(tempvar if select == "notename0" and tempvar != "" else notename(tonic, transpose)[0]), font=("Arial", int(scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "notename0"))
    C.create_rectangle(26.5*scale, 66*scale, 32.5*scale, 69*scale, fill=(colors["pitch_selected"] if select == "centsdev0" else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "centsdev0"))
    C.create_text(29.5*scale, 67.5*scale, text=(tempvar if select == "centsdev0" and tempvar != "" else plusminus(round(notename(tonic, transpose)[1], 2))), font=("Arial", int(scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "centsdev0"))

    C.create_text(37.5*scale, 67.5*scale, text="(concert", font=("Arial", int(scale*3/2), "bold"), fill="#FFFFFF", tags=("pitch"))
    C.create_rectangle(42.5*scale, 66*scale, 46.5*scale, 69*scale, fill=(colors["pitch_selected"] if select == "concertname0" else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "concertname0"))
    C.create_text(44.5*scale, 67.5*scale, text=(tempvar if select == "concertname0" and tempvar != "" else notename(tonic, 0)[0]), font=("Arial", int(scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "concertname0"))
    C.create_rectangle(47*scale, 66*scale, 53*scale, 69*scale, fill=(colors["pitch_selected"] if select == "concertdev0" else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "concertdev0"))
    C.create_text(50*scale, 67.5*scale, text=(tempvar if select == "concertdev0" and tempvar != "" else plusminus(round(notename(tonic, 0)[1], 2))), font=("Arial", int(scale*6/5), "bold"), fill="#000000", tags=("clickable", "pitch", "concertdev0"))
    C.create_text(53.5*scale, 67.5*scale, text=")", font=("Arial", int(scale*3/2), "bold"), fill="#FFFFFF", tags=("pitch"))

    C.create_rectangle(63*scale, 65.75*scale, 69*scale, 69.25*scale, fill=(colors["pitch_selected"] if select == "tet" else colors["pitch_box"]), width=0, tags=("clickable", "pitch", "tet"))
    C.create_text(66*scale, 67.5*scale, text=(tempvar if select == "tet" and tempvar != "" else tet), font=("Arial", int(scale*7/4), "bold"), fill="#000000", tags=("clickable", "pitch", "tet"))
    C.create_text(72*scale, 67.5*scale, text="TET", font=("Arial", int(scale*7/4), "bold"), fill="#FFFFFF", tags=("pitch"))

    C.create_oval(56.75*scale, 66*scale, 59.75*scale, 69*scale, fill=key_colors["second"][0], width=0, tags=("clickable", "pitchhelp"))
    C.create_text(58.25*scale, 67.5*scale, text="?", font=("Arial", int(scale*1.5), "bold"), fill="#000000", tags=("clickable", "pitchhelp"))


def render_options(instrument=INSTRUMENT, database=DATABASE, setinstrument=False):
    DATABASEDESC.delete(1.0, END)
    DATABASEDESC.insert(END, DATABASE[0][4])

    C.delete("options")
    C.create_rectangle(78*scale, 2*scale, 190*scale, 19.5*scale, fill=colors["options_background"], width=0, tags=("options"))
    
    C.create_rectangle(79*scale, 3*scale, 99*scale, 7*scale, fill=colors["options_database"], width=0, tags=("clickable", "options", "addentry"))
    C.create_text(89*scale, 5*scale, text="ADD ENTRY", font=("Arial", int(scale*1.75), "bold"), fill="#FFFFFF", tags=("clickable", "options", "addentry"))

    C.create_rectangle(79*scale, 8*scale, 99*scale, 12*scale, fill=colors["options_database"], width=0, tags=("clickable", "options", "removeentry"))
    C.create_text(89*scale, 10*scale, text="REMOVE ENTRY", font=("Arial", int(scale*1.75), "bold"), fill="#FFFFFF", tags=("clickable", "options", "removeentry"))

    C.create_rectangle(79*scale, 13*scale, 99*scale, 18.5*scale, fill="#AA55CC", width=0, tags=("clickable", "options", "copytoclipboard"))
    C.create_text(89*scale, 15.75*scale, text="      Copy to\nclipboard", font=("Arial", int(scale*1.5), "bold"), fill="#FFFFFF", tags=("clickable", "options", "copytoclipboard"))

    C.create_rectangle(169*scale, 13*scale, 189*scale, 18.5*scale, fill="#AA55CC", width=0, tags=("clickable", "options", "pastefromclipboard"))
    C.create_text(179*scale, 15.75*scale, text="Paste from\n     clipboard", font=("Arial", int(scale*1.5), "bold"), fill="#FFFFFF", tags=("clickable", "options", "pastefromclipboard"))

    C.create_rectangle(169*scale, 3*scale, 189*scale, 7*scale, fill=colors["options_database"], width=0, tags=("clickable", "options", "loadfile"))
    C.create_text(179*scale, 5*scale, text="LOAD FILE", font=("Arial", int(scale*1.75), "bold"), fill="#FFFFFF", tags=("clickable", "options", "loadfile"))

    C.create_rectangle(169*scale, 8*scale, 189*scale, 12*scale, fill=colors["options_database"], width=0, tags=("clickable", "options", "savefile"))
    C.create_text(179*scale, 10*scale, text="SAVE FILE", font=("Arial", int(scale*1.75), "bold"), fill="#FFFFFF", tags=("clickable", "options", "savefile"))

    C.create_text(134*scale, 5*scale, text=database[0][0], font=("Arial", int(scale*2), "bold"), fill="#FFFFFF", tags=("options"))

    if setinstrument:
        C.create_rectangle(100*scale, 8*scale, 133.5*scale, 12*scale, fill=colors["set_instrument"], width=0, tags=("clickable", "options", "cancelsetinstrument"))
        C.create_text(116.75*scale, 10*scale, text="CANCEL", font=("Arial", int(scale*1.75), "bold"), fill="#000000", tags=("clickable", "options", "cancelsetinstrument"))
    else:
        C.create_rectangle(100*scale, 8*scale, 133.5*scale, 12*scale, fill=colors["set_instrument"], width=0, tags=("clickable", "options", "selectinstrument"))
        C.create_text(116.75*scale, 10*scale, text="Instrument: " + instrument, font=("Arial", int(scale*1.5) if len(instrument) <= 15 else int(scale*1.375), "bold"), fill="#000000", tags=("clickable", "options", "selectinstrument"))

    if setinstrument:
        C.create_text(150.75*scale, 10*scale, text="Warning: changing instruments\nwill erase the current database", font=("Arial", int(scale*1.375), "bold"), fill="#FFFFFF", tags=("clickable", "options", "cancelsetinstrument"))
    else:
        C.create_text(150.75*scale, 10*scale, text="Transposition: "+plusminus(instruments[instrument][1]*100) + " cents", font=("Arial", int(scale*1.5), "bold"), fill="#FFFFFF", tags=("clickable", "options", "selectinstrument"))


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

#FILTERS = {
    #"tolerance": 0.15,
    #"fingtype": ["note", "trill", "multi"],
    #"tet": "none",
    #"search": "none"  
#}

def render_filters(filters=FILTERS, tet=TET, select=SELECT, tempvar=TEMPVAR):
    C.delete("filters")
    C.delete("tolerance")
    C.create_rectangle(2*scale, 72*scale, 76*scale, 88*scale, fill=colors["filters_background"], width=0, tags=("filters"))

    # FINGTYPE FILTER
    C.create_text(14.5*scale, 74.5*scale, text="Filter for fingering type:", font=("Arial", int(scale*3/2), "bold"), fill="#FFFFFF", tags=("filters"))
    C.create_rectangle(26.5*scale, 73*scale, 38.5*scale, 76*scale, fill=("#000000" if "note" in filters["fingtype"] else "#FFFFFF"), width=0, tags=("clickable", "filters", "fingtypef", "note"))
    C.create_text(32.5*scale, 74.5*scale, text="Note/Microtone", font=("Arial", int(scale*6/5), "bold"), fill=("#FFFFFF" if "note" in filters["fingtype"] else "#000000"), tags=("clickable", "filters", "fingtypef", "note"))
    C.create_rectangle(39*scale, 73*scale, 51*scale, 76*scale, fill=("#000000" if "trill" in filters["fingtype"] else "#FFFFFF"), width=0, tags=("clickable", "filters", "fingtypef", "trill"))
    C.create_text(45*scale, 74.5*scale, text="Trill/Tremolo", font=("Arial", int(scale*6/5), "bold"), fill=("#FFFFFF" if "trill" in filters["fingtype"] else "#000000"), tags=("clickable", "filters", "fingtypef", "trill"))
    C.create_rectangle(51.5*scale, 73*scale, 63.5*scale, 76*scale, fill=("#000000" if "multi" in filters["fingtype"] else "#FFFFFF"), width=0, tags=("clickable", "filters", "fingtypef", "multi"))
    C.create_text(57.5*scale, 74.5*scale, text="Multiphonic", font=("Arial", int(scale*6/5), "bold"), fill=("#FFFFFF" if "multi" in filters["fingtype"] else "#000000"), tags=("clickable", "filters", "fingtypef", "multi"))

    # TET FILTER
    C.create_text(14.25*scale, 78*scale, text="Filter for pitches in TET:", font=("Arial", int(scale*3/2), "bold"), fill="#FFFFFF", tags=("filters"))
    C.create_rectangle(26.5*scale, 76.5*scale, 38.5*scale, 79.5*scale, fill=("#000000" if filters["tet"] == "none" else "#FFFFFF"), width=0, tags=("clickable", "filters", "tetf", "none"))
    C.create_text(32.5*scale, 78*scale, text="No filter", font=("Arial", int(scale*6/5), "bold"), fill=("#FFFFFF" if filters["tet"] == "none" else "#000000"), tags=("clickable", "filters", "tetf", "none"))
    C.create_rectangle(39*scale, 76.5*scale, 51*scale, 79.5*scale, fill=("#000000" if filters["tet"] == "part" else "#FFFFFF"), width=0, tags=("clickable", "filters", "tetf", "part"))
    C.create_text(45*scale, 78*scale, text="At least 1 in TET", font=("Arial", int(scale*6/5), "bold"), fill=("#FFFFFF" if filters["tet"] == "part" else "#000000"), tags=("clickable", "filters", "tetf", "part"))
    C.create_rectangle(51.5*scale, 76.5*scale, 63.5*scale, 79.5*scale, fill=("#000000" if filters["tet"] == "all" else "#FFFFFF"), width=0, tags=("clickable", "filters", "tetf", "all"))
    C.create_text(57.5*scale, 78*scale, text="All in TET", font=("Arial", int(scale*6/5), "bold"), fill=("#FFFFFF" if filters["tet"] == "all" else "#000000"), tags=("clickable", "filters", "tetf", "all"))

    # FINGERING SEARCH
    C.create_text(15.75*scale, 82*scale, text="Search for fingering:", font=("Arial", int(scale*3/2), "bold"), fill="#FFFFFF", tags=("filters"))
    C.create_rectangle(26.5*scale, 80.5*scale, 44.75*scale, 83.5*scale, fill=colors["searched"] if filters["search"] == "fingering_primary" else "#FFFFFF", width=0, tags=("clickable", "filters", "searchf", "fingering_primary"))
    C.create_text(35.625*scale, 82*scale, text="Match primary fingering", font=("Arial", int(scale*6/5), "bold"), fill="#000000", tags=("clickable", "filters", "searchf", "fingering_primary"))
    C.create_rectangle(45.25*scale, 80.5*scale, 63.5*scale, 83.5*scale, fill=colors["searched"] if filters["search"] == "fingering_exact" else "#FFFFFF", width=0, tags=("clickable", "filters", "searchf", "fingering_exact"))
    C.create_text(54.375*scale, 82*scale, text="Match exact fingering", font=("Arial", int(scale*6/5), "bold"), fill="#000000", tags=("clickable", "filters", "searchf", "fingering_exact"))

    # PITCH SEARCH
    C.create_text(16.5*scale, 85.5*scale, text="Search for pitches:", font=("Arial", int(scale*3/2), "bold"), fill="#FFFFFF", tags=("filters"))
    C.create_rectangle(26.5*scale, 84*scale, 44.75*scale, 87*scale, fill=colors["searched"] if filters["search"] == "pitch_single" else "#FFFFFF", width=0, tags=("clickable", "filters", "searchf", "pitch_single"))
    C.create_text(35.625*scale, 85.5*scale, text="At least 1 pitch match", font=("Arial", int(scale*6/5), "bold"), fill="#000000", tags=("clickable", "filters", "searchf", "pitch_single"))
    C.create_rectangle(45.25*scale, 84*scale, 63.5*scale, 87*scale, fill=colors["searched"] if filters["search"] == "pitch_full" else "#FFFFFF", width=0, tags=("clickable", "filters", "searchf", "pitch_full"))
    C.create_text(54.375*scale, 85.5*scale, text="All pitches match", font=("Arial", int(scale*6/5), "bold"), fill="#000000", tags=("clickable", "filters", "searchf", "pitch_full"))

    # TOLERANCE
    C.create_text(70*scale, 79*scale, text="Tolerance", font=("Arial", int(scale*3/2), "bold"), fill="#FFFFFF", tags=("tolerance"))
    
    C.create_rectangle(65.5*scale, 80.5*scale, 72.5*scale, 83.5*scale, fill=key_colors["model"][0] if select == "tolerance_cents" else "#FFFFFF", width=0, tags=("clickable", "tolerance", "cents"))
    C.create_text(69*scale, 82*scale, text=tempvar if select == "tolerance_cents" and tempvar != "" else round((1200/tet)*filters["tolerance"], 2), font=("Arial", int(scale*11/8), "bold"), fill="#000000", tags=("clickable", "tolerance", "cents"))
    C.create_text(74*scale, 82*scale, text="c", font=("Arial", int(scale*3/2), "bold"), fill="#FFFFFF", tags=("tolerance"))

    C.create_rectangle(65.5*scale, 84*scale, 72.5*scale, 87*scale, fill=key_colors["model"][0] if select == "tolerance_percent" else "#FFFFFF", width=0, tags=("clickable", "tolerance", "percent"))
    C.create_text(69*scale, 85.5*scale, text=tempvar if select == "tolerance_percent" and tempvar != "" else round(100*filters["tolerance"], 2), font=("Arial", int(scale*11/8), "bold"), fill="#000000", tags=("clickable", "tolerance", "percent"))
    C.create_text(74*scale, 85.5*scale, text="%", font=("Arial", int(scale*3/2), "bold"), fill="#FFFFFF", tags=("tolerance"))

    C.create_oval(72*scale, 73*scale, 75*scale, 76*scale, fill=colors["searched"], width=0, tags=("clickable", "filtershelp"))
    C.create_text(73.5*scale, 74.5*scale, text="?", font=("Arial", int(scale*1.5), "bold"), fill="#000000", tags=("clickable", "filtershelp"))
    
                   
def render_database(instrument=INSTRUMENT, database=DATABASE, setinstrument=False, page=0, select=SELECT, filters=FILTERS):
    global PAGE
    global NUM_PAGES
    global TET
    global FINGERING
    global FINGTYPE
    global PITCHES
    
    C.delete("database")
    C.delete("setinstrument")
    C.delete("entry")
    if setinstrument:
        percolumn = 25
        rowexpand = 3
        totalcolumns = 2
        for i, instrument in enumerate(instruments):
            transcents = round(instruments[instrument][1]*100, 1)
            underscored_instrument = ""
            for letter in instrument:
                if letter == " ":
                    underscored_instrument += "_"
                else:
                    underscored_instrument += letter
            transposition = " (Transpose: " + ("+" + str(transcents) if transcents > 0 else ("−" + str(-transcents) if transcents < 0 else "0")) + " cents)"
            C.create_rectangle((78 + (112/totalcolumns)*int(i/percolumn))*scale, (21.75 + (i%percolumn)*rowexpand)*scale, (78 + (112/totalcolumns)*int(i/percolumn + 1))*scale, (21.75 + ((i%percolumn)+1)*rowexpand)*scale, fill=(colors["set_instrument"] if instrument == INSTRUMENT else "#FFFFFF"), width=1, tags=("clickable", "setinstrument", underscored_instrument))
            C.create_text((78 + (112/totalcolumns)*(int(i/percolumn)+0.5))*scale, (21.75 + ((i%percolumn)+0.5)*rowexpand)*scale, text=instrument + transposition, font=("Arial", int(scale*11/8), "bold"), fill=("#000000"), tags=("clickable", "setinstrument", underscored_instrument))
    else:
        rowspacing = 2.75
        topy = 28
        per_page = 25

        C.create_rectangle(122*scale, 21*scale, 125*scale, 24*scale, fill="#FFFFFF", width=1, tags=("clickable", "database", "prevpage"))
        C.create_text(123.5*scale, 22.5*scale, text="◀", font=("Arial", int(scale*2.25), "bold"), fill=("#000000"), tags=("clickable", "database", "prevpage"))

        C.create_rectangle(143*scale, 21*scale, 146*scale, 24*scale, fill="#FFFFFF", width=1, tags=("clickable", "database", "nextpage"))
        C.create_text(144.5*scale, 22.5*scale, text="▶", font=("Arial", int(scale*2.25), "bold"), fill=("#000000"), tags=("clickable", "database", "nextpage"))

        C.create_rectangle(118.5*scale, 21*scale, 121.5*scale, 24*scale, fill="#FFFFFF", width=1, tags=("clickable", "database", "prevpage2"))
        C.create_text(120*scale, 22.5*scale, text="◀◀", font=("Arial", int(scale*1.5), "bold"), fill=("#000000"), tags=("clickable", "database", "prevpage2"))

        C.create_rectangle(146.5*scale, 21*scale, 149.5*scale, 24*scale, fill="#FFFFFF", width=1, tags=("clickable", "database", "nextpage2"))
        C.create_text(148*scale, 22.5*scale, text="▶▶", font=("Arial", int(scale*1.5), "bold"), fill=("#000000"), tags=("clickable", "database", "nextpage2"))

        if filters["search"] != "none":
            C.create_text(89.75*scale, 22.5*scale, text="SEARCH RESULTS", font=("Arial", int(scale*2), "bold"), fill=("#000000"), tags=("database"))
            C.create_rectangle(175*scale, 21*scale, 190*scale, 24*scale, fill="#FFFFFF", width=1, tags=("clickable", "database", "clearsearch"))
            C.create_text(182.5*scale, 22.5*scale, text="Clear search", font=("Arial", int(scale*1.5), "bold"), fill=("#000000"), tags=("clickable", "database", "clearsearch"))

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
                if fingering[1][0] != FINGERING[0] and fingering[1][0] != (FINGERING[0] | FINGERING[2]) and (fingering[1][0] | fingering[1][2]) != FINGERING[0] and (fingering[1][0] | fingering[1][2]) != (FINGERING[0] | FINGERING[2]):
                    include = False

                # special case: trombone
                if instruments[database[0][1]][0] == "trombone":
                    sposmatch = False
                    if (abs((fingering[1][4].real - FINGERING[4].real) * 12/database[0][3]) <= FILTERS["tolerance"] or
                        (abs((fingering[1][4].real - FINGERING[4].imag) * 12/database[0][3]) <= FILTERS["tolerance"] and FINGTYPE == "trill") or
                        (abs((fingering[1][4].imag - FINGERING[4].real) * 12/database[0][3]) <= FILTERS["tolerance"] and fingering[2] == "trill") or
                        (abs((fingering[1][4].imag - FINGERING[4].imag) * 12/database[0][3]) <= FILTERS["tolerance"] and FINGTYPE == "trill" and fingering[2] == "trill")):
                        sposmatch = True
                    if not sposmatch:
                        include = False
                
            elif filters["search"] == "fingering_exact":
                if fingering[1][0:4] != FINGERING[0:4]:
                    include = False

                # special case: trombone
                if instruments[database[0][1]][0] == "trombone":
                    sposmatch = False
                    if ((abs((fingering[1][4].real - FINGERING[4].real) * 12/database[0][3]) <= FILTERS["tolerance"] and fingering[2] != "trill") or
                        (abs((fingering[1][4].real - FINGERING[4].real) * 12/database[0][3]) <= FILTERS["tolerance"] and
                        abs((fingering[1][4].imag - FINGERING[4].imag) * 12/database[0][3]) <= FILTERS["tolerance"] and fingering[2] == "trill")):
                        sposmatch = True
                    if not sposmatch:
                        include = False
                    
            elif filters["search"] == "pitch_single":
                include = False
                for pitch in fingering[0]:
                    match = False
                    for searchpitch in PITCHES:
                        if abs(database[0][3]*math.log(pitch/database[0][2], 2) - database[0][3]*math.log(searchpitch/database[0][2], 2)) <= filters["tolerance"]:
                            match = True
                            break
                    if match:
                        include = True
                        break
            elif filters["search"] == "pitch_full":
                include = True
                for searchpitch in PITCHES:
                    match = False
                    for pitch in fingering[0]:
                        if abs(database[0][3]*math.log(pitch/database[0][2], 2) - database[0][3]*math.log(searchpitch/database[0][2], 2)) <= filters["tolerance"]:
                            match = True
                            break
                    if not match:
                        include = False
                        break

            if include:
                filtered_database.append((f+1, fingering))

        NUM_PAGES = math.ceil(len(filtered_database) / per_page)
        if page >= NUM_PAGES:
            page = max(0, NUM_PAGES-1)
            PAGE = page

        if "data" in SELECT: # if entry is selected, binary search for entry
            low = 0; high = len(filtered_database)-1
            while high - low > 1:
                mid = int((low + high) / 2)
                if int(SELECT[4:]) == filtered_database[mid][0]:
                    page = int(mid / per_page)
                    PAGE = page
                    break
                elif int(SELECT[4:]) < filtered_database[mid][0]:
                    high = mid
                elif int(SELECT[4:]) > filtered_database[mid][0]:
                    low = mid
            if int(SELECT[4:]) == filtered_database[high][0]:
                    page = int(high / per_page)
                    PAGE = page
            elif int(SELECT[4:]) == filtered_database[low][0]:
                    page = int(low / per_page)
                    PAGE = page

        C.create_text(134*scale, 22.5*scale, text=("0" if NUM_PAGES == 0 else str(page*per_page + 1)) + "−" + str(min((page+1)*per_page, len(filtered_database))) + " of " + str(len(filtered_database)), font=("Arial", int(scale*1.25), "bold"), fill=("#000000"), tags=("database"))

        C.create_text(80*scale, (topy-1)*scale, text="Type", font=("Arial", int(scale*1), "bold"), fill=("#000000"), tags=("database"))
        C.create_text(86*scale, (topy-1)*scale, text="Freq (Hz)", font=("Arial", int(scale*1), "bold"), fill=("#000000"), tags=("database"))
        C.create_text(95*scale, (topy-1)*scale, text="Trans Pitch", font=("Arial", int(scale*1), "bold"), fill=("#000000"), tags=("database"))
        C.create_text(105*scale, (topy-1)*scale, text="Concert Pitch", font=("Arial", int(scale*1), "bold"), fill=("#000000"), tags=("database"))
        C.create_text(117.5*scale, (topy-1)*scale, text="Steps of "+str(TET)+"−TET", font=("Arial", int(scale*1), "bold"), fill=("#000000"), tags=("database"))
        C.create_text(140*scale, (topy-1)*scale, text="Fingering", font=("Arial", int(scale*1), "bold"), fill=("#000000"), tags=("database"))
        C.create_text(172.5*scale, (topy-1)*scale, text="Description", font=("Arial", int(scale*1), "bold"), fill=("#000000"), tags=("database"))
        
        for f, fingering in enumerate(filtered_database[page*per_page : (page+1)*per_page] if len(filtered_database) >= (page+1)*per_page else filtered_database[page*per_page :]):
            entry_num = fingering[0]
            entry = fingering[1]

            if "multi" in entry[2]:
                fingtype = "multi"
            else:
                fingtype = entry[2]

            # left side: 78
            # right side: 188

            # fingtype
            C.create_rectangle(78*scale, (topy + rowspacing*f)*scale, 82*scale, (topy + rowspacing*(f+1))*scale, fill=key_colors["model"][0] if SELECT == "data"+str(entry_num) else "#FFFFFF", width=1, tags=("clickable", "entry", "data"+str(entry_num)))
            C.create_text(80*scale, (topy + rowspacing*(f+0.5))*scale, text=fingtype, font=("Arial", int(scale*1), "bold"), fill=("#000000"), tags=("clickable", "entry", "data"+str(entry_num)))
        
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
                
            C.create_rectangle(82*scale, (topy + rowspacing*f)*scale, 90*scale, (topy + rowspacing*(f+1))*scale, fill=key_colors["model"][0] if SELECT == "data"+str(entry_num) else "#FFFFFF", width=1, tags=("clickable", "entry", "data"+str(entry_num)))
            C.create_text(86*scale, (topy + rowspacing*(f+0.5))*scale, text=freqtext, font=("Arial", int(scale*freqsize), "bold"), fill=("#000000"), tags=("clickable", "entry", "data"+str(entry_num)))

            C.create_rectangle(90*scale, (topy + rowspacing*f)*scale, 100*scale, (topy + rowspacing*(f+1))*scale, fill=key_colors["model"][0] if SELECT == "data"+str(entry_num) else "#FFFFFF", width=1, tags=("clickable", "entry", "data"+str(entry_num)))
            C.create_text(95*scale, (topy + rowspacing*(f+0.5))*scale, text=notetext, font=("Arial", int(scale*notesize), "bold"), fill=("#000000"), tags=("clickable", "entry", "data"+str(entry_num)))

            C.create_rectangle(100*scale, (topy + rowspacing*f)*scale, 110*scale, (topy + rowspacing*(f+1))*scale, fill=key_colors["model"][0] if SELECT == "data"+str(entry_num) else "#FFFFFF", width=1, tags=("clickable", "entry", "data"+str(entry_num)))
            C.create_text(105*scale, (topy + rowspacing*(f+0.5))*scale, text=conctext, font=("Arial", int(scale*concsize), "bold"), fill=("#000000"), tags=("clickable", "entry", "data"+str(entry_num)))

            C.create_rectangle(110*scale, (topy + rowspacing*f)*scale, 125*scale, (topy + rowspacing*(f+1))*scale, fill=key_colors["model"][0] if SELECT == "data"+str(entry_num) else "#FFFFFF", width=1, tags=("clickable", "entry", "data"+str(entry_num)))
            C.create_text(117.5*scale, (topy + rowspacing*(f+0.5))*scale, text=steptext, font=("Arial", int(scale*stepsize), "bold"), fill=("#000000"), tags=("clickable", "entry", "data"+str(entry_num)))

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
                if key == key_systems[instruments[database[0][1]][0]]["parameters"]["LR_split"]:
                    desc_string += key_systems[instruments[database[0][1]][0]]["parameters"]["separator"]
                if isinstance(state, complex):
                    if fingering[1][2] != "trill" or round(state.real, 6) == round(state.imag, 6):
                        desc_string += "{"+str(round(state.real, 2))+"} "
                    else:
                        desc_string += "[{"+str(round(state.real, 2))+"}{"+str(round(state.imag, 2))+"}] "
                elif state == 3:
                    desc_string += "["+key_systems[instruments[database[0][1]][0]][key]["descname"].strip()+"]"
                elif state == 2:
                    desc_string += "½"
                elif state == 1:
                    desc_string += key_systems[instruments[database[0][1]][0]][key]["descname"]
                elif state == 0:
                    desc_string += key_systems[instruments[database[0][1]][0]][key]["descoff"]
            if entry[1][3] == -17:
                desc_string += "[(16)]"
            elif entry[1][3] == -1:
                desc_string += "[(0)]"
            elif entry[1][3] >= 0:
                desc_string += "(" + str(entry[1][3]) + ")"
            elif entry[1][3] <= -2:
                desc_string += "[(" + str(-entry[1][3]-1) + ")(" + str(-fingering[1][1][3]) + ")]"

            descsize = min(40/len(desc_string), 1)
            if descsize <= 2/3:
                desc_left = desc_string.split("|[|")[0] if "|[|" in desc_string else (desc_string.split("||")[0] if "||" in desc_string else desc_string.split("|")[0])
                desc_right = desc_string.split("|[|")[1] if "|[|" in desc_string else (desc_string.split("||")[1] if "||" in desc_string else desc_string.split("|")[1])
                descsize = min(50/max(len(desc_left), len(desc_right)), 0.75)
                desc_string = desc_left + "|\n[|" + desc_right if "|[|" in desc_string else (desc_left + "||\n" + desc_right if "||" in desc_string else desc_left + "|\n" + desc_right)
            C.create_rectangle(125*scale, (topy + rowspacing*f)*scale, 155*scale, (topy + rowspacing*(f+1))*scale, fill=key_colors["model"][0] if SELECT == "data"+str(entry_num) else "#FFFFFF", width=1, tags=("clickable", "entry", "data"+str(entry_num)))
            C.create_text(140*scale, (topy + rowspacing*(f+0.5))*scale, text=desc_string, font=("Arial", int(scale*descsize), "bold"), fill=("#000000"), tags=("clickable", "entry", "data"+str(entry_num)))

            descriptionsize = max(min(40/(len(entry[1][-1])+0.000000001), 1), 0.75)
            description = entry[1][-1]
            if len(description) > 110:
                descriptionsize = max(min(47/(len(entry[1][-1])+0.000000001), 1), 2/3)
            if len(description) > 207:
                description = description[:205] + "..."
            C.create_rectangle(155*scale, (topy + rowspacing*f)*scale, 190*scale, (topy + rowspacing*(f+1))*scale, fill=key_colors["model"][0] if SELECT == "data"+str(entry_num) else "#FFFFFF", width=1, tags=("clickable", "entry", "data"+str(entry_num)))
            C.create_text(172.5*scale, (topy + rowspacing*(f+0.5))*scale, text=description, width=34.5*scale, font=("Arial", int(scale*descriptionsize), "bold"), fill=("#000000"), tags=("clickable", "entry", "data"+str(entry_num)))
    


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

    Label(FH, text="Fingering Diagram Help", font=("Arial", int(scale*2), "bold"), fg=textcolor, bg=bgcolor).place(x = 1*scale, y = 1*scale)

    FH.create_oval(1.5*scale, 5*scale, 5.5*scale, 9*scale, fill=key_colors["main"][0], width=0)
    FH.create_oval(6*scale, 5*scale, 10*scale, 9*scale, fill=key_colors["main"][1], width=0)
    Label(FH, text="Main key directly controlling a tone hole / Main valve", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 5.5*scale)

    FH.create_oval(1.5*scale, 10*scale, 5.5*scale, 14*scale, fill=key_colors["octave"][0], width=0)
    FH.create_oval(6*scale, 10*scale, 10*scale, 14*scale, fill=key_colors["octave"][1], width=0)
    Label(FH, text="Key for controlling the register of the instrument", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 10.5*scale)

    FH.create_oval(1.5*scale, 15*scale, 5.5*scale, 19*scale, fill=key_colors["second"][0], width=0)
    FH.create_oval(6*scale, 15*scale, 10*scale, 19*scale, fill=key_colors["second"][1], width=0)
    Label(FH, text="Key used for some pitch a chromatic from the main keys", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 15.5*scale)

    FH.create_oval(1.5*scale, 20*scale, 5.5*scale, 24*scale, fill=key_colors["low"][0], width=0)
    FH.create_oval(6*scale, 20*scale, 10*scale, 24*scale, fill=key_colors["low"][1], width=0)
    Label(FH, text="Key for notes lower than with all main keys depressed", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 20.5*scale)

    FH.create_oval(1.5*scale, 25*scale, 5.5*scale, 29*scale, fill=key_colors["high"][0], width=0)
    FH.create_oval(6*scale, 25*scale, 10*scale, 29*scale, fill=key_colors["high"][1], width=0)
    Label(FH, text="Key for notes higher than with all main keys released", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 25.5*scale)

    FH.create_oval(1.5*scale, 30*scale, 5.5*scale, 34*scale, fill=key_colors["trill"][0], width=0)
    FH.create_oval(6*scale, 30*scale, 10*scale, 34*scale, fill=key_colors["trill"][1], width=0)
    Label(FH, text="Key primarily used for trills and fast passages", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 30.5*scale)

    FH.create_oval(1.5*scale, 35*scale, 5.5*scale, 39*scale, fill=key_colors["model"][0], width=0)
    FH.create_oval(6*scale, 35*scale, 10*scale, 39*scale, fill=key_colors["model"][1], width=0)
    Label(FH, text="Key/valve not present on all models of the instrument", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 35.5*scale)

    FH.create_oval(1.5*scale, 40*scale, 5.5*scale, 44*scale, fill=key_colors["special"][0], width=0)
    FH.create_oval(6*scale, 40*scale, 10*scale, 44*scale, fill=key_colors["special"][1], width=0)
    Label(FH, text="Key part of a mechanism not normally touched", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 40.5*scale)

    FH.create_oval(6*scale, 45*scale, 10*scale, 49*scale, fill=key_colors["main"][2], width=0)
    Label(FH, text="Half−hole (e.g. key is pressed but hole is not fully covered)", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 45.5*scale)

    FH.create_oval(6*scale, 50*scale, 10*scale, 54*scale, fill=key_colors["trilled"], width=0)
    Label(FH, text="Key is being trilled as part of a trill fingering", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 50.5*scale)

    FH.create_rectangle(2.25*scale, 57.5*scale, 9.25*scale, 58.5*scale, fill=key_colors["main"][0], width=0)
    FH.create_rectangle(2.25*scale, 57.5*scale, 5.75*scale, 58.5*scale, fill=key_colors["main"][1], width=0)
    FH.create_oval(1.5*scale, 55.5*scale, 3*scale, 57*scale, fill=key_colors["main"][0], width=0)
    FH.create_oval(5*scale, 55.5*scale, 6.5*scale, 57*scale, fill=key_colors["main"][0], width=0)
    FH.create_oval(8.5*scale, 55.5*scale, 10*scale, 57*scale, fill=key_colors["main"][0], width=0)
    Label(FH, text="Continuous pitch parameter (e.g. on trombone)", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 55.5*scale)

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
        
    Label(FH, text="Partials (notes of the harmonic series); \"other\" for false tones", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11*scale, y = 60.5*scale)

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

    Label(FH, text="Pitch Help", font=("Arial", int(scale*2), "bold"), fg=textcolor, bg=bgcolor).place(x = 1*scale, y = 1*scale)

    FH.create_rectangle(5*scale, 5*scale, 12*scale, 8*scale, fill="#FFFFFF", width=0)
    FH.create_text(8.5*scale, 6.5*scale, text="327.68", fill="#000000", font=("Arial", int(scale*1.2), "bold"))
    Label(FH, text="Frequency of pitch in Hz", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 13*scale, y = 5*scale)

    FH.create_rectangle(1.5*scale, 9*scale, 5.5*scale, 12*scale, fill="#FFFFFF", width=0)
    FH.create_text(3.5*scale, 10.5*scale, text="C#5", fill="#000000", font=("Arial", int(scale*1.2), "bold"))
    FH.create_rectangle(6*scale, 9*scale, 12*scale, 12*scale, fill="#FFFFFF", width=0)
    FH.create_text(9*scale, 10.5*scale, text="−10.26", fill="#000000", font=("Arial", int(scale*1.2), "bold"))
    Label(FH, text="Transposed pitch, given as note and cent deviation", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 13*scale, y = 9*scale)

    FH.create_rectangle(1.5*scale, 13*scale, 5.5*scale, 16*scale, fill="#FFFFFF", width=0)
    FH.create_text(3.5*scale, 14.5*scale, text="E4", fill="#000000", font=("Arial", int(scale*1.2), "bold"))
    FH.create_rectangle(6*scale, 13*scale, 12*scale, 16*scale, fill="#FFFFFF", width=0)
    FH.create_text(9*scale, 14.5*scale, text="−10.26", fill="#000000", font=("Arial", int(scale*1.2), "bold"))
    Label(FH, text="Concert pitch, given as note and cent deviation", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 13*scale, y = 13*scale)

    Label(FH, text="To change the pitch, select one of these boxes and type in the desired pitch,\nor use arrow keys to shift the pitch by 1 TET−step", justify="left", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 1*scale, y = 17*scale)

    FH.create_text(4*scale, 25*scale, text="Tonic:", fill="#FFFFFF", font=("Arial", int(scale*1.375), "bold"))
    FH.create_rectangle(7.5*scale, 23.5*scale, 12*scale, 26.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(9.75*scale, 25*scale, text="440.0", fill="#000000", font=("Arial", int(scale*1.2), "bold"))
    Label(FH, text="Tonic pitch to tune other notes relative to", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 13*scale, y = 23.5*scale)

    FH.create_text(9.75*scale, 29*scale, text="TET", fill="#FFFFFF", font=("Arial", int(scale*1.5), "bold"))
    FH.create_rectangle(1.5*scale, 27.25*scale, 7*scale, 30.75*scale, fill="#FFFFFF", width=0)
    FH.create_text(4.25*scale, 29*scale, text="19", fill="#000000", font=("Arial", int(scale*1.75), "bold"))
    Label(FH, text="Number of evenly-distributed pitches per octave", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 13*scale, y = 27.5*scale)

    FH.create_rectangle(1.5*scale, 31.5*scale, 12*scale, 34.5*scale, fill="#334F66", width=0)
    FH.create_text(6.75*scale, 33*scale, text="11\\19 −7.91%", fill="#FFFFFF", font=("Arial", int(scale*1.25), "bold"))
    Label(FH, text="Pitch class within TET (built on tonic) and deviation in % of 1 TET−step", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 13*scale, y = 31.5*scale)


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

    Label(FH, text="Filters and Search Help", font=("Arial", int(scale*2), "bold"), fg=textcolor, bg=bgcolor).place(x = 1*scale, y = 1*scale)

    Label(FH, text="When filtering for TET or searching for pitches, \"Tolerance\" indicates the maximum pitch deviation\nfrom the TET/pitch (specified in the \"pitch\" section) that can show up in the search/filtered results", justify="left", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 1*scale, y = 5*scale)

    FH.create_rectangle(1.5*scale, 11.5*scale, 8.5*scale, 14.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(5*scale, 13*scale, text="7.89", fill="#000000", font=("Arial", int(scale*1.375), "bold"))
    FH.create_text(10*scale, 13*scale, text="c", fill="#FFFFFF", font=("Arial", int(scale*1.5), "bold"))
    Label(FH, text="(Absolute) tolerance in cents", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11.5*scale, y = 11.5*scale)

    FH.create_rectangle(1.5*scale, 15.5*scale, 8.5*scale, 18.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(5*scale, 17*scale, text="12.5", fill="#000000", font=("Arial", int(scale*1.375), "bold"))
    FH.create_text(10*scale, 17*scale, text="%", fill="#FFFFFF", font=("Arial", int(scale*1.5), "bold"))
    Label(FH, text="(Relative) tolerance in percentage of 1 TET−step", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 11.5*scale, y = 15.5*scale)

    FH.create_rectangle(1.5*scale, 19.5*scale, 16.5*scale, 22*scale, fill="#FFFFFF", width=0)
    FH.create_text(9*scale, 20.75*scale, text="At least 1 in TET", fill="#000000", font=("Arial", int(scale*1), "bold"))
    FH.create_rectangle(1.5*scale, 22.5*scale, 16.5*scale, 25*scale, fill="#FFFFFF", width=0)
    FH.create_text(9*scale, 23.75*scale, text="At least 1 pitch match", fill="#000000", font=("Arial", int(scale*1), "bold"))
    Label(FH, text="A fingering will show up if at least ONE of its pitches is in the TET within tolerance\nor if at least ONE of its pitches matches any of the specified pitches", justify="left", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 17*scale, y = 19.5*scale)

    FH.create_rectangle(1.5*scale, 26*scale, 16.5*scale, 28.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(9*scale, 27.25*scale, text="All in TET", fill="#000000", font=("Arial", int(scale*1), "bold"))
    FH.create_rectangle(1.5*scale, 29*scale, 16.5*scale, 31.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(9*scale, 30.25*scale, text="All pitches match", fill="#000000", font=("Arial", int(scale*1), "bold"))
    Label(FH, text="A fingering will only show up if ALL of its pitches are in the TET within tolerance\nor if ALL of its pitches can be matched with one of the specified pitches", justify="left", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 17*scale, y = 26*scale)

    Label(FH, text="In a fingering search, input the fingering to be searched in the diagram on the top left\nNote: \"Tolerance\" also indicates the maximum deviation when searching trombone positions", justify="left", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 1*scale, y = 32.5*scale)

    FH.create_rectangle(1.5*scale, 39*scale, 13.5*scale, 43*scale, fill="#FFFFFF", width=0)
    FH.create_text(7.5*scale, 41*scale, text="Match primary\n        fingering", fill="#000000", font=("Arial", int(scale*1), "bold"))
    Label(FH, text="A fingering will show up if its keys match (half−holes and partials are ignored)\nor for trills, if either of the 2 result fingerings matches either specified fingering", justify="left", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 14*scale, y = 38.25*scale)

    FH.create_rectangle(1.5*scale, 44.5*scale, 13.5*scale, 48.5*scale, fill="#FFFFFF", width=0)
    FH.create_text(7.5*scale, 46.5*scale, text="Match exact\n     fingering", fill="#000000", font=("Arial", int(scale*1), "bold"))
    Label(FH, text="A fingering will only show up if all aspects match (keys, half−holes, partials etc.)\nor for trills, if both of the result fingerings match the two specified fingerings", justify="left", font=("Arial", int(scale*1.5), "bold"), fg=textcolor, bg=bgcolor).place(x = 14*scale, y = 43.75*scale)
    
render_fingering(instruments[INSTRUMENT][0], FINGERING, SELECT, TEMPVAR)
render_pitches(PITCHES, FINGTYPE, SELECT, TEMPVAR, instruments[INSTRUMENT][1], TONIC, TET)
render_options(INSTRUMENT, DATABASE, SETINSTRUMENT)
render_database(INSTRUMENT, DATABASE, SETINSTRUMENT, PAGE, SELECT, FILTERS)
render_filters(FILTERS, TET, SELECT, TEMPVAR)

root.mainloop()



