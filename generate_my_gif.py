"""
Example script for generating GIF from axon/myelin segmentation data.

This script demonstrates how to use the multi-class segmentation GIF generator
with your own data. It matches images with their corresponding masks and creates
an animated GIF showing the segmentation results.

Expected structure:
- sample_data/images/    : Contains input images
- sample_data/masks/     : Contains corresponding segmentation masks

Mask format:
- Black (0)      : Background (transparent in GIF)
- Gray (126-127) : Myelin (displayed in red)
- White (255)    : Axon (displayed in blue)
"""

import os
import glob
from multiclass_segmentation_gif import create_multiclass_segmentation_gif


def match_images_and_masks(image_dir, mask_dir):
    """
    Match images with their corresponding masks based on filename.
    
    Returns:
        Tuple of (image_paths, mask_paths) with matching pairs
    """
    # Get all image files
    image_files = sorted(glob.glob(os.path.join(image_dir, "*.png")))
    
    # Find matching masks
    matched_images = []
    matched_masks = []
    
    for img_path in image_files:
        # Extract filename without directory
        img_filename = os.path.basename(img_path)
        
        # Look for corresponding mask
        mask_path = os.path.join(mask_dir, img_filename)
        
        if os.path.exists(mask_path):
            matched_images.append(img_path)
            matched_masks.append(mask_path)
            print(f"Matched: {img_filename}")
        else:
            print(f"No mask found for: {img_filename}")
    
    return matched_images, matched_masks


def main():
    print("="*70)
    print("Axon/Myelin Segmentation GIF Generator")
    print("="*70)
    print()
    
    # Directories
    image_dir = "sample_data/images"
    mask_dir = "sample_data/masks"
    output_file = "axon_myelin_segmentation.gif"
    
    # Check if directories exist
    if not os.path.exists(image_dir):
        print(f"Error: '{image_dir}' directory not found!")
        return
    
    if not os.path.exists(mask_dir):
        print(f"Error: '{mask_dir}' directory not found!")
        return
    
    # Match images with masks
    print("Matching images with masks...")
    print()
    images, masks = match_images_and_masks(image_dir, mask_dir)
    
    if len(images) == 0:
        print("No matching image-mask pairs found!")
        return
    
    print()
    print(f"Found {len(images)} matching image-mask pairs")
    print()
    
    # Define colors for each class
    # Mask values: 0 (black/background), 126-127 (gray/myelin), 255 (white/axon)
    class_colors = {
        255: (0, 0, 255),      # Axon (white in mask) -> Blue
        126: (255, 0, 0),      # Myelin (gray in mask) -> Red
        127: (255, 0, 0),      # Myelin variant
    }
    
    print("Color mapping:")
    print("  - Axons (white) → Blue")
    print("  - Myelin (gray) → Red")
    print("  - Background (black) → Transparent")
    print()
    
    # Generate the GIF
    create_multiclass_segmentation_gif(
        images=images,
        masks=masks,
        output_path=output_file,
        image_duration=700,        # Show image for 400ms
        mask_duration=1200,        # Show overlay for 1200ms
        class_colors=class_colors,
        mask_alpha=0.4,            # Low opacity (40%) for better visibility
        resize=None,               # Keep original size (or set to (512, 512) to reduce file size)
        loop=0                     # Infinite loop
    )
    
    print()
    print("="*70)
    print(f"Done! Open '{output_file}' to view your results")
    print("="*70)


if __name__ == "__main__":
    main()
