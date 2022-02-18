from rich import print
import numpy as np
import PIL.Image
import sys
import os


VERSION = "v1.0.1"
STOP_INDICATOR = "$STOP$"
MAJOR_VERSION_REQUIRED = 3
MINIMUM_MINOR_VERSION_REQUIRED = 10
REQUIRED_PIP_PACKAGES = ["numpy", "pillow", "rich"]


def is_file_exists(file_path: str):
    return os.path.isfile(file_path)


def is_file_png(file_path: str):
    return file_path.endswith('.png')


def is_file_exe(file_path: str):
    return file_path.endswith('.exe')


def get_png_path_from_user():
    is_file = False
    is_png = False
    while is_file == False or is_png == False:
        image_path = input("Enter image path -> ")
        is_file = is_file_exists(image_path)
        if is_file == False:
            print("[bold red]Image path is invalid.")
        is_png = is_file_png(image_path)
        if is_png == False:
            print("[bold red]The image is not a PNG file.")
    return image_path


def get_secret_message_from_user():
    secret_message = input("Enter your secret message -> ")
    while(len(secret_message) == 0):
        secret_message = input("Message can not be empty... Try again -> ")
    return secret_message


def get_exe_path_from_user():
    is_file = False
    is_exe = False
    while is_file == False or is_exe == False:
        exe_path = input("Enter EXE path -> ")
        is_file = is_file_exists(exe_path)
        if is_file == False:
            print("[bold red]EXE path is invalid.")
        is_exe = is_file_exe(exe_path)
        if is_exe == False:
            print("[bold red]The file is not an EXE file.")
    return exe_path


def hide_exe_in_image(image_path: str, exe_path: str):
    """
    Hiding the exe file inside the png image file. Returns a message to print.
    """
    with open(image_path, 'ab') as f, open(exe_path, 'rb') as e:
        f.write(e.read())
    print("[bold green]Successfully hidden exe file in the image!")


def extract_exe_from_image(image_path: str):
    """
    Extracting the exe file from the png image file. Returns a message to print.
    """
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
    print(f"[bold green]Successfully extracted exe file from the image!\nNew exe is -> {exe_path}")


def hide_message_in_image(image_path: str, message_to_hide: str):
    image = PIL.Image.open(image_path, 'r')
    width, height = image.size
    img_arr = np.array(list(image.getdata()))

    if image.mode == 'P':
        print("[bold red]Image not supported.")
        return
    
    channels = 4 if image.mode == 'RGBA' else 3
    pixels = img_arr.size // channels
    message_to_hide += STOP_INDICATOR
    byte_message = ''.join(f"{ord(c):08b}" for c in message_to_hide)
    print(f"Message to hide (in bits) :\n{byte_message}")
    bits = len(byte_message)

    if bits > pixels:
        print("[bold red]Not enough space to encode the message")
        return
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
    print(f"[bold green]Successfully hidden the message inside the image!\nNew png file is -> {encoded_image_path}")


def extract_message_from_image(image_path: str):    
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
        print(f"\n[bold green]Secret Message ->\n{secret_message[:secret_message.index(STOP_INDICATOR)]}\n")
    else:
        print("[bold yellow]Could not find secret message")


def print_title():
    print(
        "[bold green]"
        " ____  _   _  ____ _     _     _\n"
        "|  _ \| \ | |/ ___(_) __| | __| | ___ _ __  ©\n"
        "| |_) |  \| | |  _| |/ _` |/ _` |/ _ \ '_ \ \n"
        "|  __/| |\  | |_| | | (_| | (_| |  __/ | | |\n"
        "|_|   |_| \_|\____|_|\__,_|\__,_|\___|_| |_|\n"
        f"\n\t\t  [italic green]{VERSION}\n"
    )


def run_TUI():
    options = ["Exit (or Ctrl+C anytime)", "Hide message in image", "Extract message from image",
    "Hide exe in image", "Extract exe from image."]
    print_options = ''
    for index in range(len(options)):
        print_options += f"[bold green][{index}] [cyan]{options[index]}\n"
    print((f"[bold magenta]Enter your choice:\n\n{print_options}"))
    user_choice = str(input().strip())
    match user_choice:
        case '0':
            print("[bold cyan]Abort.")
            exit()
        case '1':
            hide_message_in_image(get_png_path_from_user(), get_secret_message_from_user())
        case '2':
            extract_message_from_image(get_png_path_from_user())
        case '3':
            hide_exe_in_image(get_png_path_from_user(), get_exe_path_from_user())
        case '4':
            extract_exe_from_image(get_png_path_from_user())
        case _:
            print("[bold red]Invalid option. Abort.")
            exit()


def check_python_version():
    major = sys.version_info.major
    minor = sys.version_info.minor
    micro = sys.version_info.micro
    
    if (major < MAJOR_VERSION_REQUIRED or (major == MAJOR_VERSION_REQUIRED and minor < MINIMUM_MINOR_VERSION_REQUIRED)):
        print(
            "[bold red]You are using an old python version "
            f"[{major}.{minor}.{micro}]\n"
            f"Please update your python to {MAJOR_VERSION_REQUIRED}.{MINIMUM_MINOR_VERSION_REQUIRED}+"
        )
        exit()


def main():
    try:
        check_python_version()
        print_title()
        run_TUI()
    except KeyboardInterrupt:
        print("[bold red]\nStopped.")
    except ModuleNotFoundError:
        print("[bold red]Missing one of the pip packages.\nPlease run: pip install -r requirements.txt")
    except Exception:
        print("[bold red]\nError occured.")
    


if __name__ == '__main__':
    main()
