# WindFingerings 1.1.4
WindFingerings is an interface for viewing and storing fingerings on wind instruments. It was designed to be microtone-compatible, and offers searching for fingerings and for microtones in other temperaments (rather than as a mere deviation from 12−TET). The current version of WindFingerings contains interfaces for 30+ instruments, including flute, oboe, bassoon, clarinet, saxophone, trumpet, horn, trombone, euphonium, and tuba.

## Note: "G# cancel" on saxophone
The "G# cancel" refers to the screw on top of the tone-hole key for G#. It serves two purposes:
- When the RH presses F#*, 4, 5, or 6, the G# key is prevented from activating
- When the RH presses F#*, 4, 5, or 6, the bis key is automatically pressed

While this mechanism allows smoother transitions to the note G#, it also eliminates a lot of microtonal fingerings between G and G# that would have worked if the G# key was not canceled out by the right hand keys. Because WindFingerings is designed to be microtone-compatible, it assumes that this screw is unscrewed from the instrument. If you are inputting a fingering that relies on one of the above (e.g. low Bb, low B, low C#, F#/G# trill), you need to also select "G# cancel" on the fingering diagram. This will change the fingering description to contain a double vertical bar (||) — e.g. low B is 123 B || 456 C, not 123 B | 456 C.

### README TO BE COMPLETED

## Version overview
- 1.0 — first version of WindFingerings
- 1.1 — added "standard" collection
- 1.1.1 — bug fixes
- 1.1.2 — partially fixed trills and multiphonics sorting bug
- 1.1.3 — fixed trills and multiphonics sorting bug
- 1.1.4 — more bug fixes

## Issues
