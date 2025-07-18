# Generative Pixel Art 
## Summary
- Converts text-to-art generated pixel-art-style images from LLMs to true pixel resolution assets.

- Extracts pixel art from screenshots.

## Installation

### Clone the Repository:
```bash
git clone git@github.com:KennethJAllen/generative-pixel-art.git
cd generative-pixel-art
```
### Create Virtual Environment

- Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if not already installed.
- Sync environments
    - `uv sync`

## Using the Tool

1) Get a pixel art image from an LLM, e.g. GPT-4o, or pixel art from low-quality video, streams, photographs, or screenshots.
    - If using GPT-4o it can be helpful to request a transparent background for the image.

2) Use CLI

```bash
python gen_pixel_art/cli.py -i <path/to/img> -o <output/directory> -c <num colors> -p <pixel size>
```
## Challenges
The result of pixel-art style images from LLMs are noisy, high resolution images with a non-uniform grid and random artifacts. Due to these issues, standard downsampling techniques do not work. How can we recover the pixel art with "true" resolution and colors?

The current approach to turning pixel art into useable assets for games are either
1) Use naive downsampling which does not give a result that is faithful to the original image.
2) Manually re-create the image in the approperiate resolution pixel by pixel.

## Algorithm
- The main algorithm solves these challenges. Here is a high level overview. We will apply it step by step on this example image of blob pixel art that was generated from GPT-4o.

<img src="./data/creatures/blob.png" width="800" alt="blob"/>

- Note that this image is high resolution and noisy.

<img src="./assets/blob/blob_resolution.png" width="800" alt="The blob is noisy."/>

1) Trim the edges of the image and zero out pixels with more than 50% alpha.
    - This is to work around some issues with models such as GPT-4o not giving a perfectly transparent background.

2) Find edges of the pixel art using [Canny edge detection](https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html).

<img src="./assets/blob/edges.png" width="800" alt="edges"/>

3) Close small gaps in edges with a [morphological closing](https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html).

<img src="./assets/blob/closed_edges.png" width="800" alt="closed edges"/>

4) Use [Hough transform](https://docs.opencv.org/3.4/d3/de6/tutorial_js_houghlines.html) to get the coordinates of lines in the detected edges. Only keep lines that are close to vertical or horizontal giving some grid coordinates.

<img src="./assets/blob/lines.png" width="800" alt="lines"/>

5) Find the grid spacing by filtering outliers and taking the median of the spacings, then complete the mesh.

<img src="./assets/blob/mesh.png" width="800" alt="mesh"/>

6) Quantize the original image to a small number of colors.

7) In each cell specified by the mesh, choose the most common color in the cell as the color for the pixel. Recreate the original image with one pixel per cell.

    - Result upsampled by a factor of $20 \times$

<img src="./assets/blob/upsampled.png" width="800" alt="upsampled"/>

## Examples

The algorithm is robust. It performs well for images that are already approximately alligned to a grid. Here are a few examples

### Bat
- Original image generated by GPT-4o. Note the noisy edges.
<p align="center">
  <img src="./data/creatures/bat.png" width="400" />
  <img src="./assets/bat/mesh.png" width="400" />
  <img src="./assets/bat/upsampled.png" width="400" />
</p>

### Ash
- Screenshot from Google images of Pokemon asset.
<p align="center">
  <img src="./data/game/ash.png" width="400" />
  <img src="./assets/ash/mesh.png" width="400" />
  <img src="./assets/ash/upsampled.png" width="400" />
</p>

### Demon
- Original image generated by GPT-4o.
<p align="center">
  <img src="./data/large/demon.png" width="400" />
  <img src="./assets/demon/mesh.png" width="400" />
  <img src="./assets/demon/upsampled.png" width="400" />
</p>

### Pumpkin
- Screenshot from Google Images of Stardew Valley asset.
<p align="center">
  <img src="./data/game/pumpkin.png" width="400" />
  <img src="./assets/pumpkin/mesh.png" width="400" />
  <img src="./assets/pumpkin/upsampled.png" width="400" />
</p>

## Real Images To Pixel Art

- This tool can also be used to convert real images to pixel art by first requesting a pixelated image of the original image from GPT-4o, then using the tool to get the true resolution of the iomage.

- Consider this image of a mountain

<img src="./assets/mountain/original.jpg" width="800" alt="Original mountain"/>

- Here are the results of first requesting a pixalated version of the mountain, then using the tool to get a true resolution pixel art version.

<p align="center">
  <img src="./data/real/mountain.png" width="400" />
  <img src="./assets/mountain/mesh.png" width="400" />
  <img src="./assets/mountain/upsampled.png" width="400" />
</p>
