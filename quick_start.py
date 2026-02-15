"""
Quick Start Template - Segmentation GIF Generator

Copy this template and modify the paths to your images and masks.
"""

from segmentation_gif import create_segmentation_gif
import glob

# ============================================================================
# STEP 1: Define your image and mask paths
# ============================================================================

# Option A: List specific files
images = [
    "path/to/image1.png",
    "path/to/image2.png",
    "path/to/image3.png",
]

masks = [
    "path/to/mask1.png",
    "path/to/mask2.png",
    "path/to/mask3.png",
]

# Option B: Use glob to find all images in a folder
# images = sorted(glob.glob("path/to/images/*.png"))
# masks = sorted(glob.glob("path/to/masks/*.png"))

# ============================================================================
# STEP 2: Generate the GIF (that's it!)
# ============================================================================

create_segmentation_gif(
    images=images,
    masks=masks,
    output_path="my_segmentation_results.gif"
)

# ============================================================================
# Optional: Customize the appearance
# ============================================================================

# Uncomment and modify these parameters as needed:
"""
create_segmentation_gif(
    images=images,
    masks=masks,
    output_path="my_segmentation_results.gif",
    image_duration=300,        # How long to show image alone (milliseconds)
    mask_duration=700,          # How long to show mask overlay (milliseconds)
    mask_alpha=0.6,             # Mask transparency (0.0 = transparent, 1.0 = opaque)
    mask_color=(0, 255, 0),     # Mask color (R, G, B) - default is red (255, 0, 0)
    resize=(512, 512),          # Optional: resize frames to save space
    loop=0                      # 0 = infinite loop, or specify number of loops
)
"""

print("Done! Check 'my_segmentation_results.gif' in the current directory")
