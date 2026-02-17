# WindFingerings 1.1.11
WindFingerings is an interface for viewing and storing fingerings on wind instruments. It was designed to be microtone-compatible, and offers searching for fingerings and for microtones in other temperaments (rather than as a mere deviation from 12−TET). The current version of WindFingerings contains interfaces for 30+ instruments, including flute, oboe, bassoon, clarinet, saxophone, trumpet, horn, trombone, euphonium, and tuba.

## Current supported instruments
- Piccolo, Flute†
- Oboe†, English Horn, Bassoon†, Contrabassoon
- Clarinet in Eb, Clarinet in Bb†, Clarinet in A, Basset Horn*, Alto Clarinet, Bass Clarinet, Contrabass Clarinet*
- Sopranino Saxophone*, Soprano Saxophone, Alto Saxophone†, Tenor Saxophone†, Baritone Saxophone, Bass Saxophone*
- Piccolo Trumpet in Bb*, Trumpet in C, Trumpet in Bb†, Cornet in Bb, Flugelhorn
- Single F Horn, Single Bb Horn, Double F/Bb Horn†
- Tenor Trombone, Bass Trombone
- Tenor Horn, Baritone Horn, Euphonium†, F Tuba, Eb Tuba, CC Tuba, BBb Tuba†

### Standard collections
The "standard" collections consist of a template of fingerings for all of the above instruments except for the ones marked with an asterisk (*). The instruments marked with a dagger (†) also contain a template of trill fingerings. In these standard collections, all pitches are shown as if they were perfectly in tune to 12−TET, even though this might not be the case on your instrument. Also, there may be a few errors.

## Fingering section
To select a fingering, click on the keys in the fingering diagram on the top left corner. Right-click on a key to "half-press" it (such as pressing the key but not covering the tone hole) and change the key's color to gray, and if "trill" is selected in the pitch section, middle-click on a key to trill it (which will change the color of the key to bright green).

The keys in the diagram are colored based on their function on the instrument:
- White: main key directly controlling a tone hole / main valve
- Gray: key controlling the register of the instrument
- Green: key used for some pitch a chromatic from the main keys
- Red: key for notes lower than with all main keys depressed
- Yellow: key for notes higher than with all main keys released
- Blue: key primarily used for trills and fast passages
- Orange: key/valve not present on all models of the instrument
- Purple: key part of a mechanism not normally touched

Brass instruments will also come with a "partials" section, where the partial used for playing a pitch can be selected. "Other" refers to any pitch that is not produced with a partial in the harmonic series (e.g. false tones).

The trombone and trumpet contain continuous pitch parameters:
- for trombone, the number is the position. Note that the fractional values for positions involving triggers might not be exact and might differ between instruments.
- for trumpet, "¼" corresponds to the position for D4 (1−3 {0.25} {0.0} ③), and "½" corresponds to the position for C#4 (123 {0.5} {0.0} ③). 123 {0.5} {0.5} ② is a low F3.

Note: the fingering diagram doesn't "know" whether pressing down one key automatically presses down another (e.g. pressing down the low C key on a flute will automatically depress the low C# as well). The convention in the "standard" collections is to only include the key being pressed, and not any keys that are automatically depressed as a result of some other key being pressed. So low C on flute is stored as T 123 | 456 C, instead of T 123 | 456 C# C (or T 1Bb\*23 | G*F#*456 C).

### Special: G# cancel on saxophone
The "G# cancel" refers to the screw on top of the tone-hole key for G#. It serves two purposes:
- When the RH presses F#*, 4, 5, or 6, the G# key is prevented from activating
- When the RH presses F#*, 4, 5, or 6, the bis key is automatically pressed

While this mechanism allows smoother transitions to the note G#, it also eliminates a lot of microtonal fingerings between G and G# (as well as between Bb and B) that would have worked if the G# key was not canceled out by the right hand keys. Because WindFingerings is designed to be microtone-compatible, it assumes that this screw is unscrewed from the instrument. If you are inputting a fingering that relies on one of the above (e.g. low Bb, low B, low C#, F#/G# trill, 1−− || 4−− Bb), you need to also select "G# cancel" on the fingering diagram. This will change the fingering description to contain a double vertical bar (||) — e.g. B3 (low B) is 123 B || 456 C, not 123 B | 456 C.

### Special: E−* on trombone
On a trombone, the lowest "normal" note is E2 (played in 7th position). Then, there is a gap until Bb1, the first pedal tone (in 1st position). The notes within this gap are partially filled by a trombone with a F attachment, namely Eb2, D2, C#2, and C2, however this still leaves a 1-note gap at B1. In order to play this note on a single-(F)-trigger trombone without resorting to lipping or using false tones, the tuning of the F attachment has to be pulled out to just below E. This turns the F-trigger into a "E−-trigger", and this what the E−* refers to.

## Pitch section
### Fingering type
After selecting a fingering, you can also specify what type of fingering this is, and which pitch this fingering plays in the "pitch" section. There are three options for fingering type:
- Note/Microtone (1 pitch) — for static fingerings that produces one pitch. If the same fingering is capable of producing different pitches depending on other factors, include as two separate entries (e.g. flute T 123 | 1−− Eb can produce both F4 and F5 — these would be stored as two separate entries) 
- Trill/Tremolo (2 pitches) — for a non-static fingering that involves alternation between two pitches. In the description, trilled keys will appear in square brackets (e.g. on saxophone, T 123 B || 4\[Bb*]56 C is a trill between Bb3 and B3).
- Multiphonic (2−4 pitches) — for static fingerings that produce more than one pitch. When selecting this option, it will also popup whether the multiphonic has 2, 3, or 4 pitches.

### Pitches
After selecting the type of fingering, there are five boxes for each pitch. Select on one of the boxes to type in a pitch, or use the arrow keys to shift the pitch in increments of 1 TET−step. The first box shows the frequency of this pitch in Hz. The second and third boxes display the pitch by a note name and cent deviation from A=440 12−TET, in transposed pitch. The fourth and fifth boxes are the same but in concert pitch instead of transposed pitch.

For example, if the selected instrument is Bass Clarinet, the pitch 300 Hz will also display as E5 +36.95 (i.e. 36.95 cents higher than transposed E5) and concert D4 +36.95 (i.e. 36.95 cents higher than concert D4).

### Tonic and TET
On the bottom, "tonic" refers to the pitch to be labeled as pitch class 0. "TET" refers to the number of equally-spaced notes in an octave (i.e. which equal temperament is used). After this is set, every pitch class is given a "pitch class name" which is shown to the right of the pitch (e.g. with the tonic at 256 Hz and 19−TET, the frequency 440 Hz would be in pitch class "15\\19 −15.42%".

## Filters and Search section
The bottom left corner offers options for narrowing down results of the database based on several criteria. "Filter for fingering type" allows only certain types of fingerings to show up (notes, trills, multiphonics). The other types are bit more nuanced.

All of the examples given in this section will assume that the selected TET is 12−TET with a tonic of 440 Hz, but the same applies regardless of what the chosen tonic and TET are.

### Tolerance
When searching for pitch (or TET), this shows the maximum deviation from the pitch (or TET) being searched. Tolerance can be specified in cents (absolute), or as a percentage of 1 TET−step (relative). All of the examples given here will assume a tolerance of 15%, but the same applies regardless of the tolerance.

### Filter for pitches in TET
When this filter is active, only pitches that are within tolerance of the TET (specified in the "pitch" section) will remain (i.e. "in tune" with the TET). For example, 392 Hz and 440 Hz will remain, but 475 Hz is filtered out as it is not with 15% of the selected TET (it is 1\\12 +32.51%).

- At least 1 in TET: A trill or multiphonic fingering will remain if at least one of the pitches is in the TET. For instance, a trill between 440 Hz and 475 Hz will not be filtered out, as although 475 Hz is not within 15% of the TET, 440 Hz is in the TET, and this setting only requires at least 1 pitch to be in the TET.
- All in TET: A trill or multiphonic fingering will only remain if all of its pitches are in the TET. The same 440 Hz to 475 Hz trill would now be filtered out, as even though 440 Hz is in the TET, 475 Hz is not, and this setting requires all pitches to be in the TET.
These two settings are identical for fingerings of type "note", as notes only have one pitch to begin with.

### Search for fingering
To search a fingering, select a fingering on the diagram in the top left, and then press either "Match primary fingering" or "Match exact fingering"

Match primary fingering: only the main elements of the fingering need to match for a fingering to remain. Aspects like half-holes, trills, and partials will be ignored.
- Example 1: in oboe-standard.csv, searching 123 | 456 C# (the fingering for C#4) will also cause ½23 | 456 C# (the fingering for C#5) to remain, as the half-hole is ignored by "Match primary fingering".
- Example 2: in trumpet-bb-standard.csv, searching 1−3 {0.0} {0.0} ③ (a slightly sharp D4) will not only cause 1−3 {0.25} {0.0} ③ (in-tune D4) to remain (as the 3rd valve tuning is ignored by "Match primary fingering"), but also leave 1−3 {0.0} {0.0} ② (G3), 1−3 {0.25} {0.0} ④ (G4), etc. untouched — partials are ignored by "Match primary fingering", and only the 1−3 matters here.
- Example 3: in clarinet-bb-trill.csv, searching T 123 | 4\[5]− (A3 to Bb3 trill) will not only cause the matched T 123 | 4\[5]− to remain, but also any trill that contains T 123 | 4−− or T 123 | 45−. Doing the same search in clarinet-bb-standard.csv will return two results: T 123 | 4−− (A3) and T 123 | 45− (Bb3), as the fingering only needs to match either of the two trilled positions.

Match exact fingering: all aspects of the fingering need to match for a fingering to remain, including half-holes, trills, and partials.
- Example 1: in oboe-standard.csv, searching 123 | 456 C# (the fingering for C#4) will only return 123 | 456 C#, not ½23 | 456 C#.
- Example 2: in trumpet-bb-standard.csv, searching 1−− {0.0} {0.0} ④ (Bb4) will only return 1−− {0.0} {0.0} ④ (Bb4), and not 1−− {0.0} {0.0} ② (Bb3), 1−− {0.0} {0.0} ③ (F4), or anything else.
- Example 3: in clarinet-bb-trill.csv, searching T 123 | 4\[5]− (A3 to Bb3 trill) will only return T 123 | 4\[5]−. Doing the same in clarinet-bb-standard.csv will return no results, as that collection does not contain any trills.

Exceptions: continuous pitch parameters
- Trumpet: the tuning of the 1st and 3rd valves are ignored
- Trombone: positions follow the same "tolerance" as pitch searches. So it the tolerance is 15 cents, a search will return if the position is at most 15% of a position off.

### Search for pitches
This search works similarly to "Filter for pitches in TET", except instead of searching for all pitches in a temperament, it only searches for fingerings that contain pitches within tolerance of searched pitches.
- At least 1 pitch match: a fingering will remain if one of its pitches matches one of the searched pitches. For example, if searching for 392 Hz and 440 Hz, a trill between 440 Hz and 475 Hz will remain, because one of its pitches (440 Hz) matches with one of the searched pitches (440 Hz).
- All pitches match: a fingering will only remain if all of its pitches can individually match up with a searched pitch. For example, if searching for 392 Hz and 440 Hz, a multiphonic consisting of 392 Hz, 440 Hz, and 475 Hz will remain (as both 392 Hz and 440 Hz are present), but a trill between 440 Hz and 475 Hz will not, because the 475 Hz doesn't match either the searched 392 Hz or 440 Hz. 

## Version overview
- 1.0 — first version of WindFingerings
- 1.1 — added "standard" collection
- 1.1.1 — bug fixes
- 1.1.2 — partially fixed trills and multiphonics sorting bug
- 1.1.3 — fixed trills and multiphonics sorting bug
- 1.1.4 — more bug fixes
- 1.1.5 — added some trills to "standard" collection, fixed more bugs
- 1.1.6 — bug fixed with copying to clipboard, added Contrabass Clarinet
- 1.1.7 — bug fixes
- 1.1.8 — bug fixes
- 1.1.9 — added super-steps to page select for large collections
- 1.1.10 — bug fixes
- 1.1.11 — bug fixes

## Issues
