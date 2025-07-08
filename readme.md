# Chat History Converter 
This script is a edited of Skystapper's original that allows it to be used on a local system and not on Google Colab.

# Why?
Google Colab cringe af

# Things to know
This script doesn't convert any special formating like quotations being marked in orange, it'll do a straight text convert, so keep that in mind. It also has no batch functionality, because I have no idea how to jerry rig it to do that.

# Usage
Have a folder called content in the root directory (haven't bothered auto detecting and creating it if it doesnt exist), as the script uses it for tempory storage durring the conversion. It also adds the correct extension to the exported file name, you don't need to add it yourself.
```
python ooba-to-sillytavern.py [-h] [--input INPUT] [--output OUTPUT]
                              [--yourname YOURNAME] [--charname CHARNAME]

options:
  -h, --help           show this help message and exit
  --input INPUT        The Oggabooga Chat to convert
  --output OUTPUT      The Chat output for Sillytavern
  --yourname YOURNAME  Your name
  --charname CHARNAME  Your Character's name
```

# Example
```
python ooba-to-sillytavern.py --input oobachat.json --output sillytavernchat --yourname Dell --charname Casey
```
