from time import strftime
from rich import print
import numpy as np
import imageio
import PIL.Image
import sys
import os


PROGRAM_VERSION = "v1.0.3"
STOP_INDICATOR = "$STOP$"


def is_file_exists(file_path: str) -> bool:
    return os.path.isfile(file_path)


def is_file_png(file_path: str) -> bool:
    return file_path.endswith('.png')


def is_file_exe(file_path: str) -> bool:
    return file_path.endswith('.exe')


def timestamp() -> str:
    return strftime("%H-%M-%S")


def get_png_path_from_user() -> str:
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


def get_secret_message_from_user() -> str:
    secret_message = input("Enter your secret message -> ")
    while(len(secret_message) == 0):
        secret_message = input("Message can not be empty... Try again -> ")
    return secret_message


def get_exe_path_from_user() -> str:
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


def hide_exe_in_image(image_path: str, exe_path: str) -> None:
    """
    Hiding the exe file inside the png image file.
    """
    with open(image_path, 'ab') as f, open(exe_path, 'rb') as e:
        f.write(e.read())
    print("[bold green]Successfully hidden exe file in the image!")


def extract_exe_from_image(image_path: str) -> None:
    """
    Extracting the exe file from the png image file and display the new exe path.
    """
    end_hex = b"\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"
    # Seeking the exe file in the image:
    with open(image_path, 'rb') as f:
        content = f.read()
        offset = content.index(end_hex)
        f.seek(offset + len(end_hex))
        
        # Extracting the exe file out to a file:
        exe_path = f"extracted-exe-{timestamp()}.exe"
        with open(exe_path, 'wb') as e:
            e.write(f.read())
    print(
        f"[bold green]Successfully extracted exe file from the image!\n"
        f"New exe is -> {exe_path}"
    )


def hide_message_in_image(image_path: str, message_to_hide: str) -> None:
    image = imageio.imread(image_path, as_gray=False, pilmode="RGB")
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
    encoded_image_path = f"encoded-{timestamp()}.png"
    result.save(encoded_image_path)
    print(
        f"[bold green]Successfully hidden the message inside the image!\n"
        f"New png file is -> {encoded_image_path}"
    )


def extract_message_from_image(image_path: str) -> None:    
    image = imageio.imread(image_path, as_gray=False, pilmode="RGB")
    img_arr = np.array(list(image.getdata()))
    channels = 4 if image.mode == 'RGBA' else 3
    pixels = img_arr.size // channels

    secret_bits = [bin(img_arr[i][j])[-1] for i in range(pixels) for j in range(0, 3)]
    secret_bits = ''.join(secret_bits)
    secret_bits = [secret_bits[i:i+8] for i in range(0, len(secret_bits), 8)]

    secret_message = [chr(int(secret_bits[i], 2)) for i in range(len(secret_bits))]
    secret_message = ''.join(secret_message)

    if STOP_INDICATOR in secret_message:
        print(
            f"\n[bold green]Secret Message ->\n"
            f"{secret_message[:secret_message.index(STOP_INDICATOR)]}\n"
        )
    else:
        print("[bold yellow]Could not find secret message")


def print_title() -> None:
    print(
        "[bold green]"
        " ____  _   _  ____ _     _     _\n"
        "|  _ \| \ | |/ ___(_) __| | __| | ___ _ __  ©\n"
        "| |_) |  \| | |  _| |/ _` |/ _` |/ _ \ '_ \ \n"
        "|  __/| |\  | |_| | | (_| | (_| |  __/ | | |\n"
        "|_|   |_| \_|\____|_|\__,_|\__,_|\___|_| |_|\n"
        f"\n\t\t  [italic green]{PROGRAM_VERSION}\n"
    )


def run_TUI() -> None:
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
            sys.exit()
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
            sys.exit()


def run_pngidden():
    try:
        print_title()
        run_TUI()
    except KeyboardInterrupt:
        print("[bold red]\nStopped.")
    except ModuleNotFoundError:
        print("[bold red]\nMissing one of the pip packages.\nPlease run setup.py")
    except Exception:
        print("[bold red]\nError occured.")
    

if __name__ == '__main__':
    run_pngidden()
