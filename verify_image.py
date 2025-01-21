from PIL import Image, ImageChops

def compare_images(image1_path, image2_path):
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)

    # Check if images are the same
    diff = ImageChops.difference(img1, img2)
    if not diff.getbbox():
        print("Images are identical.")
    else:
        print("Images differ.")
compare_images('test_images/originals/input.png', 'test_images/stego/output.png')
