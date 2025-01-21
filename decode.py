from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import argparse
import os
import sys


def decode_image(input_image, key, iv):
    print(f"Decoding from: {input_image}")

    # Validate the input image file
    if not os.path.isfile(input_image) or not input_image.lower().endswith('.png'):
        print(f"Error: {input_image} is not a valid PNG file.")
        sys.exit(1)

    img = Image.open(input_image)
    print(f"Image opened successfully: {img.format}, {img.mode}, {img.size}")

    pixels = img.load()

    # Extract binary data from LSBs
    binary_length = ''
    binary_message = ''
    length_extracted = False
    message_length = 0

    # Iterate over pixels to extract binary data
    for y in range(img.height):
        for x in range(img.width):
            pixel = list(pixels[x, y])
            for channel in range(len(pixel) - 1):  # Skip alpha channel
                if not length_extracted:
                    binary_length += str(pixel[channel] & 1)
                    if len(binary_length) == 32:
                        message_length = int(binary_length, 2)
                        print(f"Binary representation of message length: {binary_length}")
                        print(f"Message length extracted: {message_length} bits")
                        length_extracted = True
                else:
                    binary_message += str(pixel[channel] & 1)
                    if len(binary_message) == message_length:
                        break
            if length_extracted and len(binary_message) == message_length:
                break
        if length_extracted and len(binary_message) == message_length:
            break

    print(f"Total binary data extracted: {len(binary_message)} bits")
    print(f"Binary message (first 64 bits): {binary_message[:64]}...")

    # Convert binary message to bytes
    encrypted_bytes = bytes(int(binary_message[i:i + 8], 2) for i in range(0, len(binary_message), 8))
    print(f"Encrypted data (hex): {encrypted_bytes.hex()}")
    print(f"Encrypted data length: {len(encrypted_bytes)} bytes")

    # Decrypt the message
    try:
        cipher = AES.new(key.encode(), AES.MODE_CBC, bytes.fromhex(iv))
        decrypted_message = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        decoded_message = decrypted_message.decode()
        print(f"Decoded message: {decoded_message}")

        # Save the decoded message to a text file
        output_file = "decoded_message.txt"
        with open(output_file, "w") as file:
            file.write(decoded_message)
        print(f"Decoded message saved to: {output_file}")

    except Exception as e:
        print(f"Decryption failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decode hidden message from an image.")
    parser.add_argument("--input", required=True, help="Path to the input image.")
    parser.add_argument("--key", required=True, help="Encryption key.")
    parser.add_argument("--iv", required=True, help="Initialization vector (IV) in hex format.")
    args = parser.parse_args()

    decode_image(args.input, args.key, args.iv)
