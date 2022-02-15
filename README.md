# Steganography - PNGidden

Hide text messages in PNG files using the LSB – least significant bit.

In this way, we change the lowest bits in the image to be our message – and we’ll have an almost imperceptible change on the actual way the image looks.


## PNG file structure

First 8 bytes:
```
89 50 4E 47 0D 0A 1A 0A               |   PNG File Signature
```
Last 12 bytes:
```
00 00 00 00 49 45 4e 44 ae 42 60 82   |   ....IEND.B`.|
```

### File Chunks

IHDR = Header

PLTE = Palette Table

IDAT = Image Data (Pixels)

IEND = End of file

## Setup
Install pip prerequisites
```
pip install -r requirements.txt
```

## Run
```
python main.py
```