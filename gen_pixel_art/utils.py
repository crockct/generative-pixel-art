"""Utility functions for generative pixel art."""
from PIL import Image, ImageDraw
import numpy as np

def crop_border(image : Image.Image, num_pixels: int=1) -> Image.Image:
    """Crop the boder of an image by a few pixels."""
    width, height = image.size
    box = (num_pixels, num_pixels, width - num_pixels, height - num_pixels)
    cropped = image.crop(box)
    return cropped

def rgba_to_masked_grayscale(image: Image.Image, opacity_threshold: int = 128) -> Image.Image:
    """
    Convert an RGBA image to 8-bit grayscale,
    forcing any semi- or fully-transparent pixel to zero.
    """
    rgba = image.convert("RGBA")
    arr = np.array(rgba)

    # get channels and compute luma (Rec. 601)
    r, g, b, a = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]
    luma = (0.299*r + 0.587*g + 0.114*b).astype(np.uint8)

    # zero out anything below the opacity threshold
    luma[a < opacity_threshold] = 0

    greyscale = Image.fromarray(luma, mode="L")
    return greyscale

def overlay_grid_lines(
        image: Image.Image,
        lines_x: list[int],
        lines_y: list[int],
        line_color: tuple[int, int, int] = (255, 0, 0),
        line_width: int = 1
        ) -> Image.Image:
    """
    Overlay vertical and horizontal grid lines over image for visualization.

    inputs:
        image: The source PIL image (RGBA or RGB).
        lines_x: Sorted x-coordinates of vertical grid lines.
        lines_y: Sorted y-coordinates of horizontal grid lines.
        line_color: RGB tuple for the line color (default red).
        line_width: Width of the drawn lines in pixels.
    """
    # Ensure we draw on an RGBA canvas
    canvas = image.convert("RGBA")
    draw = ImageDraw.Draw(canvas)

    w, h = canvas.size
    # Draw each vertical line
    for x in lines_x:
        draw.line([(x, 0), (x, h)], fill=(*line_color, 255), width=line_width)

    # Draw each horizontal line
    for y in lines_y:
        draw.line([(0, y), (w, y)], fill=(*line_color, 255), width=line_width)

    return canvas

def scale_img(img: Image.Image, scale: int) -> Image.Image:
    w, h = img.size
    w_new, h_new = int(w * scale), int(h * scale)
    new_size = w_new, h_new
    scaled_img = img.resize(new_size, resample=Image.NEAREST)
    return scaled_img

def naive_downsample_upsample(img: Image.Image, scale: int) -> Image.Image:
    downsampled = scale_img(img, 1/scale)
    naive = scale_img(downsampled, scale)
    return naive
