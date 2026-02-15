"""
Multi-class Segmentation GIF Generator

Generates animated GIFs to visualize multi-class segmentation results.
Each frame shows the original image followed by the segmentation overlay.
Designed for axon and myelin segmentation visualization.
"""

import numpy as np
from PIL import Image
from typing import List, Union, Tuple, Optional, Dict
import os


class MultiClassSegmentationGifGenerator:
    """Creates GIFs to visualize multi-class segmentation with custom colors."""
    
    def __init__(
        self,
        image_duration: int = 500,
        mask_duration: int = 1000,
        class_colors: Optional[Dict[int, Tuple[int, int, int]]] = None,
        mask_alpha: float = 0.5,
        loop: int = 0
    ):
        """
        Args:
            image_duration: Duration to show image alone (ms)
            mask_duration: Duration to show overlay (ms)
            class_colors: Dict mapping pixel values to RGB colors
            mask_alpha: Overlay transparency (0.0 to 1.0)
            loop: Loop count (0 = infinite)
        """
        self.image_duration = image_duration
        self.mask_duration = mask_duration
        self.mask_alpha = mask_alpha
        self.loop = loop
        
        # Default color mapping: white->blue, gray->red
        if class_colors is None:
            self.class_colors = {
                255: (0, 0, 255),    # White (Axon) -> Blue
                128: (255, 0, 0),    # Gray (Myelin) -> Red
            }
        else:
            self.class_colors = class_colors
    
    def create_multiclass_overlay(
        self,
        image: Image.Image,
        mask: np.ndarray
    ) -> Image.Image:
        """
        Create an image with multi-class mask overlay.
        
        Args:
            image: PIL Image object
            mask: 2D grayscale mask (HxW)
        
        Returns:
            PIL Image with colored mask overlay
        """
        image = image.convert('RGBA')
        overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
        overlay_array = np.array(overlay)
        
        # Convert to int16 to avoid uint8 underflow
        mask = mask.astype(np.int16)
        alpha_value = int(self.mask_alpha * 255)
        
        # Apply colors for each class
        for pixel_value, color in self.class_colors.items():
            class_mask = np.abs(mask - pixel_value) <= 10
            if np.any(class_mask):
                overlay_array[class_mask] = (*color, alpha_value)
        
        overlay = Image.fromarray(overlay_array, 'RGBA')
        result = Image.alpha_composite(image, overlay)
        return result.convert('RGB')
    
    def load_image(self, image_path: Union[str, Image.Image]) -> Image.Image:
        """Load image from path or return if already PIL Image."""
        if isinstance(image_path, Image.Image):
            return image_path
        return Image.open(image_path)
    
    def load_mask(self, mask_path: Union[str, np.ndarray]) -> np.ndarray:
        """Load 2D mask from path or return if already numpy array."""
        if isinstance(mask_path, np.ndarray):
            return mask_path
        return np.array(Image.open(mask_path))
    
    def generate_gif(
        self,
        images: List[Union[str, Image.Image]],
        masks: List[Union[str, np.ndarray, Image.Image]],
        output_path: str,
        resize: Optional[Tuple[int, int]] = None
    ):
        """Generate segmentation GIF from images and masks."""
        if len(images) != len(masks):
            raise ValueError(
                f"Number of images ({len(images)}) must match number of masks ({len(masks)})"
            )
        
        if len(images) == 0:
            raise ValueError("At least one image-mask pair is required")
        
        frames = []
        durations = []
        
        print(f"Generating multi-class segmentation GIF with {len(images)} image-mask pairs...")
        print(f"Class color mapping: {self.class_colors}")
        
        for i, (img_path, mask_path) in enumerate(zip(images, masks)):
            print(f"Processing pair {i+1}/{len(images)}...")
            
            # Load image and mask
            image = self.load_image(img_path)
            mask = self.load_mask(mask_path)
            
            # Resize if specified
            if resize is not None:
                image = image.resize(resize, Image.Resampling.LANCZOS)
                mask_img = Image.fromarray(mask.astype(np.uint8))
                mask_img = mask_img.resize(resize, Image.Resampling.NEAREST)
                mask = np.array(mask_img)
            
            # Convert to RGB for GIF
            image_rgb = image.convert('RGB')
            
            # Create frame with just the image
            frames.append(image_rgb)
            durations.append(self.image_duration)
            
            # Create frame with mask overlay
            overlaid = self.create_multiclass_overlay(image, mask)
            frames.append(overlaid)
            durations.append(self.mask_duration)
        
        # Save as GIF
        print(f"Saving GIF to {output_path}...")
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=self.loop,
            optimize=False
        )
        
        print(f"GIF successfully created: {output_path}")
        print(f"  Total frames: {len(frames)}")
        print(f"  Total duration: {sum(durations)/1000:.2f} seconds")


def create_multiclass_segmentation_gif(
    images: List[Union[str, Image.Image]],
    masks: List[Union[str, np.ndarray]],
    output_path: str,
    image_duration: int = 500,
    mask_duration: int = 1000,
    class_colors: Optional[Dict[int, Tuple[int, int, int]]] = None,
    mask_alpha: float = 0.5,
    resize: Optional[Tuple[int, int]] = None,
    loop: int = 0
):
    """
    Create a multi-class segmentation GIF.
    
    Args:
        images: List of image paths or PIL Images
        masks: List of 2D mask paths or numpy arrays
        output_path: Output GIF file path
        image_duration: Duration to show image alone (ms)
        mask_duration: Duration to show overlay (ms)
        class_colors: Dict mapping pixel values to RGB colors
        mask_alpha: Overlay transparency (0.0 to 1.0)
        resize: Optional (width, height) to resize frames
        loop: Loop count (0 = infinite)
    """
    generator = MultiClassSegmentationGifGenerator(
        image_duration=image_duration,
        mask_duration=mask_duration,
        class_colors=class_colors,
        mask_alpha=mask_alpha,
        loop=loop
    )
    
    generator.generate_gif(images, masks, output_path, resize=resize)


if __name__ == "__main__":
    print("Multi-class Segmentation GIF Generator")
    print("Import this module and use create_multiclass_segmentation_gif()")
