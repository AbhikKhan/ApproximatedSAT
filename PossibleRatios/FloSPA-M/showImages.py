from PIL import Image

def save_images_side_by_side(image1_path, image2_path, output_path):
    # Open the two input images
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    # Determine the width and height of the output image
    width = image1.width + image2.width
    height = max(image1.height, image2.height)

    # Create a new image with the calculated dimensions
    output_image = Image.new('RGB', (width, height))

    # Paste the first image onto the left side of the output image
    output_image.paste(image1, (0, 0))

    # Paste the second image onto the right side of the output image
    output_image.paste(image2, (image1.width, 0))

    # Save the resulting image
    output_image.save(output_path)