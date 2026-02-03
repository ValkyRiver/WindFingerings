### README TO BE COMPLETED
# WindFingerings 1.1.5
WindFingerings is an interface for viewing and storing fingerings on wind instruments. It was designed to be microtone-compatible, and offers searching for fingerings and for microtones in other temperaments (rather than as a mere deviation from 12−TET). The current version of WindFingerings contains interfaces for 30+ instruments, including flute, oboe, bassoon, clarinet, saxophone, trumpet, horn, trombone, euphonium, and tuba.

## Current supported instruments
- Piccolo, Flute
- Oboe, English Horn, Bassoon, Contrabassoon
- Clarinet in Eb, Clarinet in Bb, Clarinet in A, Basset Horn, Alto Clarinet, Bass Clarinet, Contrabass Clarinet
- Sopranino Saxophone, Soprano Saxophone, Alto Saxophone, Tenor Saxophone, Baritone Saxophone, Bass Saxophone
- Piccolo Trumpet in Bb, Trumpet in C, Trumpet in Bb, Cornet in Bb, Flugelhorn
- Single F Horn, Single Bb Horn, Double F/Bb Horn
- Tenor Trombone, Bass Trombone
- Tenor Horn, Baritone Horn, Euphonium, F Tuba, Eb Tuba, CC Tuba, BBb Tuba

## Fingering
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

### Special purple "keys"
#### G# cancel on saxophone
The "G# cancel" refers to the screw on top of the tone-hole key for G#. It serves two purposes:
- When the RH presses F#*, 4, 5, or 6, the G# key is prevented from activating
- When the RH presses F#*, 4, 5, or 6, the bis key is automatically pressed

While this mechanism allows smoother transitions to the note G#, it also eliminates a lot of microtonal fingerings between G and G# that would have worked if the G# key was not canceled out by the right hand keys. Because WindFingerings is designed to be microtone-compatible, it assumes that this screw is unscrewed from the instrument. If you are inputting a fingering that relies on one of the above (e.g. low Bb, low B, low C#, F#/G# trill), you need to also select "G# cancel" on the fingering diagram. This will change the fingering description to contain a double vertical bar (||) — e.g. low B is 123 B || 456 C, not 123 B | 456 C.

#### E−* on trombone
On a trombone, the lowest "normal" note is E2 (played in 7th position). Then, there is a gap until Bb1, the first pedal tone (in 1st position). The notes within this gap are partially filled by a trombone with a F attachment, namely Eb2, D2, C#2, and C2, however this still leaves a 1-note gap at B1. In order to play this note on a single-(F)-trigger trombone without resorting to lipping or using false tones, the tuning of the F attachment has to be pulled out to just below E. This turns the F-trigger into a "E−trigger", and this what the E−* refers to.

## Pitch
to be completed

## Filters
to be completed

## Version overview
- 1.0 — first version of WindFingerings
- 1.1 — added "standard" collection
- 1.1.1 — bug fixes
- 1.1.2 — partially fixed trills and multiphonics sorting bug
- 1.1.3 — fixed trills and multiphonics sorting bug
- 1.1.4 — more bug fixes
- 1.1.5 — added some trills to "standard" collection, fixed more bugs
- 1.1.6 — bug fixed with copying to clipboard, added Contrabass Clarinet

## Issues
