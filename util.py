# Sara Carrasquillo
# 03-08-2025
# Here we have our backend(utility) of our QR Code generator util.py

# Imports
from typing import cast, Literal  # Static type checker treats a value as a given type/specifics that an annotation must be a provided literal value(s)
import qrcode # Lets you convert any text (like a URL) into a QR code
from PIL import Image # Tool for working with images used to create and edit images
from qrcode.main import QRCode # This is the class we use to create the QR code object

# Casts the constant once so it's literal:
EC_M = cast(Literal[0, 1, 2, 3], qrcode.constants.ERROR_CORRECT_M)

# Generates a new QR code image
def new_qr(data: str,  # data: The string data to encode into the QR code
           box_size: int = 10,  # box_size: Pixel size of each singular QR box that makes up the QR code
           border: int = 4,  # fill_color: Color of the QR modules
           fill_color: str = "black",  # fill_color: Default color of the QR boxes
           # back_color: Background color
           back_color: str = "white") -> Image.Image:  # -> Pillow Image object of the QR code.
    # Makes a QR code image from some text data
    qr = QRCode(
        version=None,  # Library will choose the best version based on the data
        error_correction=EC_M,  # Medium error correction (15%)
        box_size=box_size,  #  Size of each singular small square (module) in the QR code
        border=border  # Number of small squares to use as a border around the QR code
    )
    # Adds the text or URL you want encoded
    qr.add_data(data)
    # Automatically adjust the QR code size to fit the data
    qr.make(fit=True)
    # Returns a QR code image with the given colors
    return qr.make_image(fill_color=fill_color, back_color=back_color)

# Generates a QR code image that is exactly specified pixels
def qr_size(data: str, # data: The string data to encode
            size_px: int, # size_px: Desired final image size in pixels (width and height)
            fill_color: str = "black", # fill_color: Default color of the QR boxes
            # back_color: Background color
            back_color: str = "white") -> Image.Image: # Image object of the QR code at the exact size

    # A temporary QR code for measurements to count how many modules (squares) make up one side of the QR code
    qr_temp = QRCode(
        version=None,  # Let the library decide what fits best
        error_correction=EC_M,  # Medium error correction
        box_size=1,   # Use a box size of 1 to measure the number of modules
        border=0  # Do not include any border while measuring
    )
    qr_temp.add_data(data)  # Add data to the temporary QR object
    qr_temp.make(fit=True)  # Layout calculation
    num_boxes = qr_temp.modules_count  # Total modules per side in the QR grid final count is stored

    # Calculates the size of each module so the QR fits in the total desired pixel size
    box_size = size_px // num_boxes
    # Calculates the number of modules as a border to center the QR
    border = (size_px - (num_boxes * box_size)) // (2 * box_size)

    # Builds the final QR code
    qr = QRCode(
        version=qr_temp.version,  # Auto-select version
        error_correction=EC_M, # Medium error correction
        box_size=box_size,  # Each module is 1 pixel for measurement
        border=border # No border for measurement
    )
    qr.add_data(data)  # Data gets added to final QR object
    qr.make(fit=True)  # Layout calculation
    img = qr.make_image(fill_color=fill_color, back_color=back_color)   # Render the final QR code image

    # Resizes to exactly size_px × size_px
    return img.resize((size_px, size_px), Image.Resampling.NEAREST)



