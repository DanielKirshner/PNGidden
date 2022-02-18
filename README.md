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

## Setup & Requirements

* Install `python 3.10.0` or upper from -> https://www.python.org/

* Make sure your version is 3.10.0 or upper
```
python --version
```

* Install pip prerequisites
```
pip install -r requirements.txt
```
## Usage
* Windows 10/11:
```
python main.py
```

* Linux or Mac OS:
```
python3 main.py
```

![](2022-02-18-18-06-52.png)

### © 2022 Daniel Kirshner. All rights reserved.