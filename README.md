# PNG Steganography Tool with AES Encryption

## Overview
The **PNG Steganography Tool with AES Encryption** is a Python-based project designed to hide secret messages within PNG images using the **Least Significant Bit (LSB)** technique. It also provides optional **AES encryption** for message security, making it suitable for secure communication and data hiding purposes.

This project was developed as part of an academic assignment on **data hiding techniques and cryptography**.

---

## Features
- **Message Encoding**: Embed a secret message into a PNG image using LSB steganography.
- **AES Encryption**: Encrypt the message with AES before embedding it in the image.
- **Message Decoding**: Extract hidden messages from PNG images, with optional decryption.
- **Verification**: Compare the original and decoded messages to ensure accuracy.
- **Support for Various Image Types**: Compatible with grayscale, binary, and color images.

---

## How It Works
1. **Encoding**:
   - Converts the message into binary format.
   - (Optional) Encrypts the binary message using AES.
   - Embeds the binary data into the least significant bits of the image pixels.

2. **Decoding**:
   - Reads the LSBs of the image pixels to reconstruct the binary message.
   - (Optional) Decrypts the binary data if encryption was applied.

3. **Verification**:
   - Compares the decoded message with the original to verify integrity.

---

## Prerequisites
- Python 3.8 or higher

---

## Project Structure
```plaintext
PNG-Steganography-AES/
├── encode.py                # Script to encode messages into images
├── decode.py                # Script to decode messages from images
├── verify_image.py          # Script to verify the integrity of decoded messages
├── utils.py                 # Helper functions for encryption, decryption, and LSB operations
├── message.txt              # Example message file
├── largemessage.txt         # Example large message file
├── test_images/             # Directory for test images
│   ├── originals/           # Original unmodified images
│   ├── stego/               # Images with embedded messages
├── decoded_message.txt      # File to store the decoded message
├── requirements.txt         # Python dependencies
├── .gitignore               # File to exclude unnecessary files
└── README.md                # Project documentation

