import numpy as np
import PIL.Image
import os    


def is_file_exists(file_path):
    return os.path.isfile(file_path)


def is_file_png(file_path):
    return file_path.endswith('.png')


def hide_exe_in_image(image_path, exe_path):
    """
    Hiding the exe file inside the png image file. Returns a message to print.
    """
    if is_file_exists(image_path) == False:
        return "Image path is invalid."
    if is_file_png(image_path) == False:
        return "The image is not a PNG file."
    if is_file_exists(exe_path) == False:
        return "EXE path is invalid."
    
    with open(image_path, 'ab') as f, open(exe_path, 'rb') as e:
        f.write(e.read())
    return "Successfully hidden exe file in the image!"


def extract_exe_from_image(image_path):
    """
    Extracting the exe file from the png image file. Returns a message to print.
    """
    if is_file_exists(image_path) == False:
        return "Image path is invalid."
    if is_file_png(image_path) == False:
        return "The image is not a PNG file."
    
    end_hex = b"\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"
    # Seeking the exe file in the image:
    with open(image_path, 'rb') as f:
        content = f.read()
        offset = content.index(end_hex)
        f.seek(offset + len(end_hex))
        
        # Extracting the exe file out to a file:
        exe_path = 'extracted_exe.exe'
        with open(exe_path, 'wb') as e:
            e.write(f.read())
    return f"Successfully extracted exe file from the image!\nNew exe is -> {exe_path}"


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