def compare_messages(original_file_path, decoded_file_path):
    # Read the original message file
    with open(original_file_path, "r") as file1:
        original_message = file1.read()

    # Read the decoded message file
    with open(decoded_file_path, "r") as file2:
        decoded_message = file2.read()

    # Compare the two files
    if original_message == decoded_message:
        print("There is no difference between the original and decoded messages. They are identical.")
    else:
        print("Differences detected between the original and decoded messages.")
        print("\n--- Original Message ---")
        print(original_message)
        print("\n--- Decoded Message ---")
        print(decoded_message)


if __name__ == "__main__":
    original_file = "message.txt"  # Path to the original message file
    decoded_file = "decoded_message.txt"  # Path to the decoded message file

    compare_messages(original_file, decoded_file)
