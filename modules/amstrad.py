import struct
#from .helpers import load_palette_json



def default_cpc_palette():
    """
    Full Amstrad CPC 27-colour palette with RGB values and colour names for reference.
    """
    return {
        "0":  [0, 0, 0],         # Black
        "1":  [0, 0, 128],       # Blue
        "2":  [0, 0, 255],       # Bright Blue
        "3":  [0, 128, 0],       # Green
        "4":  [0, 128, 128],     # Cyan
        "5":  [0, 128, 255],     # Bright Cyan
        "6":  [0, 255, 0],       # Bright Green
        "7":  [0, 255, 128],     # Spring Green
        "8":  [0, 255, 255],     # Aqua / Light Cyan

        "9":  [128, 0, 0],       # Red
        "10": [128, 0, 128],     # Magenta
        "11": [128, 0, 255],     # Purple
        "12": [128, 128, 0],     # Olive
        "13": [128, 128, 128],   # Grey
        "14": [128, 128, 255],   # Periwinkle
        "15": [128, 255, 0],     # Chartreuse
        "16": [128, 255, 128],   # Light Green
        "17": [128, 255, 255],   # Sky Blue

        "18": [255, 0, 0],       # Bright Red
        "19": [255, 0, 128],     # Rose
        "20": [255, 0, 255],     # Bright Magenta
        "21": [255, 128, 0],     # Orange
        "22": [255, 128, 128],   # Salmon
        "23": [255, 128, 255],   # Orchid
        "24": [255, 255, 0],     # Yellow
        "25": [255, 255, 128],   # Lemon
        "26": [255, 255, 255],   # White
    }

def decode_amstrad(data, mode=2, palette=None, screen_dump=False, detect_hw_colours=False):
    """
    Decode Amstrad CPC screen data into an RGB image buffer.

    Args:
        data (bytes): Raw CPC binary screen data
        mode (int): Graphics mode (0, 1, or 2)
        palette (dict): Colour palette mapping indexes to [R, G, B]
        screen_dump (bool): Whether to apply line interleave layout
        detect_hw_colours (bool): Parse embedded colour attribute data

    Returns:
        List of list of RGB tuples: 2D pixel grid
    """
    if screen_dump:
        data = reorder_cpc_screen_dump(data, mode)

    if mode == 2:
        return decode_mode_2(data, palette)
    elif mode == 1:
        return decode_mode_1(data, palette)
    elif mode == 0:
        return decode_mode_0(data, palette)
    else:
        raise ValueError(f"Unsupported CPC mode: {mode}")

# Mode decoders (simplified stubs)
def decode_mode_2(data, palette):
    # 1bpp, 2 colours, 1 byte = 8 pixels
    pixels = []
    for byte in data:
        row = []
        for bit in range(8):
            index = (byte >> (7 - bit)) & 1
            row.append(palette.get(str(index), [0, 0, 0]))
        pixels.append(row)
    return pixels

def decode_mode_1(data, palette):
    """
    Decode Mode 1 (2bpp, 4 colours) CPC screen data.
    Each byte encodes 4 pixels.
    """
    pixels = []

    for i in range(0, len(data), 80):  # 80 bytes per scanline
        line = []
        chunk = data[i:i+80]

        for byte in chunk:
            # Extract pixels: bit pairs are (7&3), (6&2), (5&1), (4&0)
            p1 = ((byte >> 7) & 1) << 1 | ((byte >> 3) & 1)
            p2 = ((byte >> 6) & 1) << 1 | ((byte >> 2) & 1)
            p3 = ((byte >> 5) & 1) << 1 | ((byte >> 1) & 1)
            p4 = ((byte >> 4) & 1) << 1 | ((byte >> 0) & 1)

            line.extend([
                palette.get(str(p1), [0, 0, 0]),
                palette.get(str(p2), [0, 0, 0]),
                palette.get(str(p3), [0, 0, 0]),
                palette.get(str(p4), [0, 0, 0])
            ])
        pixels.append(line)

    for y, row in enumerate(pixels):
        if len(row) != len(pixels[0]):
            print(f"❌ Row {y} has length {len(row)}, expected {len(pixels[0])}")

    return pixels

def decode_mode_0(data, palette):
    """
    Decode Mode 0 (4bpp, 16 colours) CPC screen data.
    Each byte encodes 2 pixels.
    """
    pixels = []

    for i in range(0, len(data), 80):  # Always 80 bytes per line
        line = []
        chunk = data[i:i+80]

        for byte in chunk:
            # Extract bits by their positions (odd/even masks interleaved)
            # Pixel 1
            p1 = ((byte >> 7) & 1) << 3 | ((byte >> 5) & 1) << 2 | ((byte >> 3) & 1) << 1 | ((byte >> 1) & 1)
            # Pixel 2
            p2 = ((byte >> 6) & 1) << 3 | ((byte >> 4) & 1) << 2 | ((byte >> 2) & 1) << 1 | ((byte >> 0) & 1)

            line.extend([
                palette.get(str(p1), [0, 0, 0]),
                palette.get(str(p2), [0, 0, 0])
            ])
        pixels.append(line)

    return pixels

def detect_embedded_palette(data):
    # TO DO: Implement detection of Advanced Art Studio colour info if present
    return None

def reorder_cpc_screen_dump(data, mode):
    """
    Rearranges CPC screen dump memory layout into linear scanlines.

    Args:
        data (bytes): Raw CPC screen dump
        mode (int): CPC mode (affects bytes per line)

    Returns:
        bytes: Reordered screen data
    """
    if mode == 2:
        # Mode 2: 1bpp = 80 bytes per line (640px wide)
        bytes_per_line = 80
    elif mode == 1:
        # Mode 1: 2bpp = 40 bytes per line (320px wide)
        bytes_per_line = 80
    elif mode == 0:
        # Mode 0: 4bpp = 20 bytes per line (160px wide)
        bytes_per_line = 80
    else:
        raise ValueError("Unsupported CPC graphics mode")

    reordered = bytearray()
    total_lines = 200  # All CPC modes are 200 lines tall
    block_size = 0x0800  # Each vertical slice is 2KB

    for line in range(total_lines):
        block = line % 8
        y = line // 8
        src_offset = (block * block_size) + (y * bytes_per_line)
        reordered.extend(data[src_offset:src_offset + bytes_per_line])

    return bytes(reordered)
