# python obfuscation

IMPORTANT NOTE!
- this works with like anything not only stuff like python but i call it python obfuscation cuz technically its an obfuscator in python

a small tkinter gui for obfuscating and deobfuscating stuff like code

this repo is for learning and simple workflow use not for security

how it works
- source is compressed with zlib
- compressed bytes are stored with a key
- result is encoded with base64
- deobfuscation reverses the same steps with the same key

usage
- run python app py
- paste or open a py or lua file in the obfuscate tab
- choose language and key then click obfuscate
- save the obfuscated blob or copy it
- in the deobfuscate tab paste or open the blob choose the same language and key then deobfuscate

notes
- this is not a secure protection layer
- use licensing signing or server execution for sensitive content

