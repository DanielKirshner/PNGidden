# Steganography - PNGidden

## PNG file structure

First 8 bytes:
```
89 50 4E 47 0D 0A 1A 0A               |   PNG File Signature
```
Last 12 bytes:
```
00 00 00 00 49 45 4e 44 ae 42 60 82   |   ....IEND.B`.|
```

*File Chunks*

IHDR = Header

PLTE = Palette Table

IDAT = Image Data (Pixels)

IEND = End of file