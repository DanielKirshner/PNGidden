import numpy as np
import PIL.Image
import os


def is_file_exists(file_path):
    return os.path.isfile(file_path)


def main():
    message_to_hide = "This is my secret!"
    image = PIL.Image.open('image.png', 'r')
    width, height = image.size
    img_arr = np.array(list(image.getdata()))

    if image.mode == 'P':
        print("Not Supported.")
        exit()
    
    channels = 4 if image.mode == 'RGBA' else 3
    pixels = img_arr.size // channels
    stop_indicator = "$STOP$"
    stop_indicator_length = len(stop_indicator)

    message_to_hide += stop_indicator

    byte_message = ''.join(f"{ord(c):08b}" for c in message_to_hide)
    print(byte_message)



if __name__ == '__main__':
    main()