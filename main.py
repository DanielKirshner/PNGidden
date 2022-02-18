import numpy as np
import PIL.Image
import os


STOP_INDICATOR = "$STOP$"


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


def hide_message_in_image(image_path, message_to_hide):
    if is_file_exists(image_path) == False:
        return "Image path is invalid."
    if is_file_png(image_path) == False:
        return "The image is not a PNG file."
    if len(message_to_hide) == 0:
        return "Message can not be empty"

    image = PIL.Image.open(image_path, 'r')
    width, height = image.size
    img_arr = np.array(list(image.getdata()))

    if image.mode == 'P':
        return "Image not supported."
    
    channels = 4 if image.mode == 'RGBA' else 3
    pixels = img_arr.size // channels
    message_to_hide += STOP_INDICATOR
    byte_message = ''.join(f"{ord(c):08b}" for c in message_to_hide)
    print(f"Message to hide (in bits) :\n{byte_message}")
    bits = len(byte_message)

    if bits > pixels:
        return "Not enough space to encode the message"
    else:
        index = 0
        for i in range(pixels):
            for j in range(0, 3):
                if index < bits:
                    img_arr[i][j] = int(bin(img_arr[i][j])[2:-1] + byte_message[index], 2)
                    index += 1
    img_arr = img_arr.reshape((height, width, channels))
    result = PIL.Image.fromarray(img_arr.astype('uint8'), image.mode)
    encoded_image_path = 'encoded.png'
    result.save(encoded_image_path)
    return f"Successfully hidden the message inside the image!\nNew png file is -> {encoded_image_path}"


def extract_message_from_image(image_path):
    if is_file_exists(image_path) == False:
        return "Image path is invalid."
    if is_file_png(image_path) == False:
        return "The image is not a PNG file."
    
    image = PIL.Image.open(image_path, 'r')
    img_arr = np.array(list(image.getdata()))
    channels = 4 if image.mode == 'RGBA' else 3
    pixels = img_arr.size // channels

    secret_bits = [bin(img_arr[i][j])[-1] for i in range(pixels) for j in range(0, 3)]
    secret_bits = ''.join(secret_bits)
    secret_bits = [secret_bits[i:i+8] for i in range(0, len(secret_bits), 8)]

    secret_message = [chr(int(secret_bits[i], 2)) for i in range(len(secret_bits))]
    secret_message = ''.join(secret_message)

    if STOP_INDICATOR in secret_message:
        print(secret_message[:secret_message.index(STOP_INDICATOR)])
    else:
        print("Could not find secret message")


def main():
    # hiding_result = hide_message_in_image('a.png', 'This is my secret!')
    # print(hiding_result)
    extract_message_from_image('encoded.png')


if __name__ == '__main__':
    main()
