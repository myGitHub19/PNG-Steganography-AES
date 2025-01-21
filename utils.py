def set_lsb(value, bit):
    """Set the least significant bit of a byte."""
    return (value & ~1) | bit


def text_to_binary(text):
    """Convert a string to a binary string."""
    return ''.join(format(ord(char), '08b') for char in text)


def binary_to_text(binary):
    """Convert a binary string back to text."""
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)


def check_capacity(image, data):
    """Ensure the image has enough capacity to hold the data."""
    width, height = image.size
    max_bytes = width * height * 3 // 8  # 3 color channels, 8 bits per byte
    if len(data) > max_bytes:
        raise ValueError("Message is too large for the image!")
