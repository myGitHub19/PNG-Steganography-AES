from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from utils import set_lsb, check_capacity
import os
import sys


def encode_image(input_image, output_image, message_file, key):
    print("Function encode_image called.")

    # Validate the input image file
    if not os.path.isfile(input_image) or not input_image.lower().endswith('.png'):
        print(f"Error: {input_image} is not a valid PNG file.")
        sys.exit(1)

    # Read the message from a file and validate
    if not os.path.isfile(message_file) or os.path.getsize(message_file) == 0:
        print(f"Error: {message_file} is not a valid or non-empty text file.")
        sys.exit(1)

    with open(message_file, 'r') as file:
        message = file.read()

    # Open the image
    print(f"Opening image: {input_image}")
    img = Image.open(input_image)
    print(f"Image opened successfully: {img.format}, {img.mode}, {img.size}")

    pixels = img.load()

    # Check image mode
    print("Checking image mode...")
    mode = img.mode
    if mode not in ["RGB", "RGBA"]:
        print(f"Unsupported image mode: {mode}")
        sys.exit(1)

    # Convert message to binary and encrypt
    print("Encrypting message...")
    cipher = AES.new(key.encode(), AES.MODE_CBC)
    encrypted_message = cipher.encrypt(pad(message.encode(), AES.block_size))
    binary_message = ''.join(format(byte, '08b') for byte in encrypted_message)
    print(f"Encrypted message length: {len(binary_message)} bits")

    # Prepend the message length
    message_length = len(binary_message)
    length_binary = f"{message_length:032b}"  # Convert length to a 32-bit binary string
    binary_message = length_binary + binary_message  # Prepend length to the message

    print(f"Message length in bits: {message_length}")
    print(f"Binary representation of message length: {length_binary}")

    # Check capacity
    print("Checking image capacity...")
    check_capacity(img, binary_message)
    print("Capacity check passed.")

    # Embed binary data into LSBs of the image
    idx = 0
    for y in range(img.height):
        for x in range(img.width):
            pixel = list(pixels[x, y])  # Convert pixel to a list for mutability
            for channel in range(len(pixel) - 1):  # Skip alpha channel if present
                if idx < len(binary_message):
                    pixel[channel] = set_lsb(pixel[channel], int(binary_message[idx]))
                    idx += 1
            pixels[x, y] = tuple(pixel)  # Update the pixel
            if idx >= len(binary_message):
                break
        if idx >= len(binary_message):
            break
    print(f"Message embedded. Total bits written: {idx}")

    # Ensure output directory exists
    print(f"Ensuring output directory exists: {os.path.dirname(output_image)}")
    os.makedirs(os.path.dirname(output_image), exist_ok=True)

    # Save the encoded image
    print(f"Saving encoded image to: {output_image}")
    img.save(output_image)
    print(f"Encoded image saved successfully to: {output_image}")

    # Print the IV for decoding
    print(f"Message hidden in {output_image}. IV: {cipher.iv.hex()}")

    print(f"Original encrypted message (hex): {encrypted_message.hex()}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Encode hidden message into an image.")
    parser.add_argument("--input", required=True, help="Path to the input image.")
    parser.add_argument("--output", required=True, help="Path to the output image.")
    parser.add_argument("--message", required=True, help="Path to the text file containing the message.")
    parser.add_argument("--key", required=True, help="Encryption key.")
    args = parser.parse_args()

    encode_image(args.input, args.output, args.message, args.key)
