"""
Example usage of the Segmentation GIF Generator

This script demonstrates how to use the tool with sample data.
"""

import numpy as np
from PIL import Image, ImageDraw
import os
from segmentation_gif import create_segmentation_gif, SegmentationGifGenerator


def create_sample_data(output_dir="sample_data"):
    """
    Create sample images and masks for demonstration.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    image_dir = os.path.join(output_dir, "images")
    mask_dir = os.path.join(output_dir, "masks")
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(mask_dir, exist_ok=True)
    
    print("Creating sample images and masks...")
    
    # Create 5 sample images with different colored backgrounds
    colors = [(100, 150, 200), (150, 200, 100), (200, 100, 150), 
              (180, 180, 100), (100, 180, 180)]
    
    for i, color in enumerate(colors):
        # Create image with colored background and some shapes
        img = Image.new('RGB', (400, 300), color)
        draw = ImageDraw.Draw(img)
        
        # Draw some shapes
        draw.ellipse([50 + i*20, 50, 150 + i*20, 150], fill=(255, 255, 255))
        draw.rectangle([200, 100 + i*10, 350, 200 + i*10], fill=(200, 200, 200))
        
        img.save(os.path.join(image_dir, f"image_{i:03d}.png"))
        
        # Create corresponding mask
        mask = np.zeros((300, 400), dtype=np.uint8)
        mask_img = Image.new('L', (400, 300), 0)
        mask_draw = ImageDraw.Draw(mask_img)
        
        # Draw mask regions (white = segmented region)
        mask_draw.ellipse([50 + i*20, 50, 150 + i*20, 150], fill=255)
        mask_draw.rectangle([200, 100 + i*10, 350, 200 + i*10], fill=255)
        
        mask_img.save(os.path.join(mask_dir, f"mask_{i:03d}.png"))
    
    print(f"Sample data created in '{output_dir}' directory")
    return image_dir, mask_dir


def example_1_simple():
    """
    Example 1: Simple usage with default parameters
    """
    print("\n" + "="*60)
    print("Example 1: Simple usage with default parameters")
    print("="*60)
    
    # Create sample data
    image_dir, mask_dir = create_sample_data()
    
    # Get image and mask paths
    images = sorted([os.path.join(image_dir, f) for f in os.listdir(image_dir)])
    masks = sorted([os.path.join(mask_dir, f) for f in os.listdir(mask_dir)])
    
    # Generate GIF with default settings
    create_segmentation_gif(
        images=images,
        masks=masks,
        output_path="output_simple.gif"
    )
    
    print("\nOutput: output_simple.gif")


def example_2_custom_settings():
    """
    Example 2: Custom timing and appearance
    """
    print("\n" + "="*60)
    print("Example 2: Custom timing and appearance")
    print("="*60)
    
    image_dir = "sample_data/images"
    mask_dir = "sample_data/masks"
    
    # Get image and mask paths
    images = sorted([os.path.join(image_dir, f) for f in os.listdir(image_dir)])
    masks = sorted([os.path.join(mask_dir, f) for f in os.listdir(mask_dir)])
    
    # Generate GIF with custom settings
    create_segmentation_gif(
        images=images,
        masks=masks,
        output_path="output_custom.gif",
        image_duration=300,          # Show image for 300ms
        mask_duration=700,            # Show mask overlay for 700ms
        mask_alpha=0.6,               # More opaque mask
        mask_color=(0, 255, 0),       # Green mask instead of red
        resize=(320, 240)             # Resize to smaller dimensions
    )
    
    print("\nOutput: output_custom.gif")
    print("Settings: Green mask, 300ms image / 700ms overlay, resized to 320x240")


def example_3_class_usage():
    """
    Example 3: Using the class for more control
    """
    print("\n" + "="*60)
    print("Example 3: Using the class for more control")
    print("="*60)
    
    image_dir = "sample_data/images"
    mask_dir = "sample_data/masks"
    
    # Get image and mask paths
    images = sorted([os.path.join(image_dir, f) for f in os.listdir(image_dir)])
    masks = sorted([os.path.join(mask_dir, f) for f in os.listdir(mask_dir)])
    
    # Create generator with specific settings
    generator = SegmentationGifGenerator(
        image_duration=400,
        mask_duration=800,
        mask_alpha=0.7,
        mask_color=(255, 165, 0),     # Orange mask
        loop=0                         # Infinite loop
    )
    
    # Generate the GIF
    generator.generate_gif(
        images=images,
        masks=masks,
        output_path="output_orange.gif",
        resize=(400, 300)
    )
    
    print("\nOutput: output_orange.gif")
    print("Settings: Orange mask with 70% opacity")


def example_4_numpy_arrays():
    """
    Example 4: Using numpy arrays directly (useful for inference pipelines)
    """
    print("\n" + "="*60)
    print("Example 4: Using numpy arrays directly")
    print("="*60)
    
    # Simulate having images and masks as numpy arrays (from model inference)
    images = []
    masks = []
    
    for i in range(3):
        # Simulate loading image
        img_path = f"sample_data/images/image_{i:03d}.png"
        img = Image.open(img_path)
        images.append(img)
        
        # Simulate model prediction (binary mask as numpy array)
        mask_path = f"sample_data/masks/mask_{i:03d}.png"
        mask = np.array(Image.open(mask_path))
        # Normalize to 0 and 1
        mask = (mask > 128).astype(np.uint8)
        masks.append(mask)
    
    # Generate GIF
    create_segmentation_gif(
        images=images,
        masks=masks,
        output_path="output_numpy.gif",
        mask_color=(255, 0, 255),     # Magenta mask
        mask_alpha=0.5
    )
    
    print("\nOutput: output_numpy.gif")
    print("Used PIL Images and numpy arrays directly (no file paths)")


if __name__ == "__main__":
    print("Segmentation GIF Generator - Examples")
    print("This script demonstrates various ways to use the tool\n")
    
    # Run examples
    example_1_simple()
    example_2_custom_settings()
    example_3_class_usage()
    example_4_numpy_arrays()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)
    print("\nGenerated GIFs:")
    print("  - output_simple.gif (default settings)")
    print("  - output_custom.gif (green mask, custom timing)")
    print("  - output_orange.gif (orange mask)")
    print("  - output_numpy.gif (magenta mask, from arrays)")
    print("\nOpen these files to see the results!")
