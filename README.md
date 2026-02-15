# AxonGIFSeg

Generate animated GIFs to visualize axon and myelin segmentation results.

## Requirements

- Python 3.7+
- Pillow
- NumPy

## Installation

```bash
git clone https://github.com/yolaatar/AxonGIFSeg.git
cd AxonGIFSeg
pip install -r requirements.txt
```

## Data Structure

Organize your images and masks with matching filenames:

```
your_data/
├── images/
│   ├── image_001.png
│   ├── image_002.png
│   └── image_003.png
└── masks/
    ├── image_001.png
    ├── image_002.png
    └── image_003.png
```

**Important:** Image and mask files must have the same name.

## Mask Format

Masks should be 2D grayscale images with pixel values:
- `0` (black): Background - displayed as transparent
- `126-127` (gray): Myelin - displayed in red
- `255` (white): Axon - displayed in blue

## Usage

```python
from multiclass_segmentation_gif import create_multiclass_segmentation_gif
import glob

images = sorted(glob.glob("your_data/images/*.png"))
masks = sorted(glob.glob("your_data/masks/*.png"))

class_colors = {
    255: (0, 0, 255),    # Axon -> Blue
    126: (255, 0, 0),    # Myelin -> Red
    127: (255, 0, 0),
}

create_multiclass_segmentation_gif(
    images=images,
    masks=masks,
    output_path="results.gif",
    class_colors=class_colors,
    mask_alpha=0.4,           # Overlay transparency (0.0 to 1.0)
    image_duration=400,       # Show image alone (ms)
    mask_duration=1200        # Show overlay (ms)
)
```

See `generate_my_gif.py` for a complete example.

## License

MIT
