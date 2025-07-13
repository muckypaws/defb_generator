"""Amstrad CPC screen decoding and processing utilities."""
import png
from .helpers import load_palette_json, make_ink_palette

def get_default_ink_palette():
    """
    Return the CPC firmware's default 16-ink to greyscale colour mapping.

    For flashing colours, only the first (static) colour is returned, since PNG cannot flash.

    Returns:
        dict: {ink_number: greyscale_index}
    """
    return {
        -1: 1,    # Border: Blue
         0: 1,    # Blue
         1: 24,   # Bright Yellow
         2: 20,   # Bright Cyan
         3: 6,    # Bright Red
         4: 26,   # Bright White
         5: 0,    # Black
         6: 2,    # Bright Blue
         7: 8,    # Bright Magenta
         8: 10,   # Cyan
         9: 12,   # Yellow
        10: 14,   # Pastel Blue
        11: 16,   # Pink
        12: 18,   # Bright Green
        13: 22,   # Pastel Green
        14: 1,    # Flashing Blue / Bright Yellow → use Blue
        15: 11    # Flashing Sky Blue / Pink → use Sky Blue
    }

def convert_hw_to_greyscale(hw_value):
    """
    Convert Amstrad CPC hardware colour number to firmware greyscale index (0-26).

    Args:
        hw_value (int): CPC hardware colour code (0-31, usually 0-31 but only 27 used)

    Returns:
        int: Greyscale index (0-26), or None if invalid
    """
    hw_to_greyscale = {
        20: 0,   # Black
        4:  1,   # Blue
        21: 2,   # Bright Blue
        28: 3,   # Red
        24: 4,   # Magenta
        29: 5,   # Mauve
        12: 6,   # Bright Red
        5:  7,   # Purple
        13: 8,   # Bright Magenta
        22: 9,   # Green
        6:  10,  # Cyan
        23: 11,  # Sky Blue
        30: 12,  # Yellow
        0:  13,  # White
        31: 14,  # Pastel Blue
        14: 15,  # Orange
        7:  16,  # Pink
        15: 17,  # Pastel Magenta
        18: 18,  # Bright Green
        2:  19,  # Sea Green
        19: 20,  # Bright Cyan
        26: 21,  # Lime
        25: 22,  # Pastel Green
        27: 23,  # Pastel Cyan
        10: 24,  # Bright Yellow
        3:  25,  # Pastel Yellow
        11: 26   # Bright White
    }
    return hw_to_greyscale.get(hw_value)

def default_cpc_palette():
    """
    Firmware-accurate Amstrad CPC 27-colour palette.

    Indexed by greyscale value (0-26) as used by INK n,x.
    """
    return {
        "0":  [0, 0, 0],         # Black
        "1":  [0, 0, 128],       # Blue
        "2":  [0, 0, 255],       # Bright Blue
        "3":  [128, 0, 0],       # Red
        "4":  [128, 0, 128],     # Magenta
        "5":  [192, 0, 192],     # Mauve
        "6":  [255, 0, 0],       # Bright Red
        "7":  [128, 0, 255],     # Purple
        "8":  [255, 0, 255],     # Bright Magenta
        "9":  [0, 128, 0],       # Green
        "10": [0, 128, 128],     # Cyan
        "11": [0, 255, 255],     # Sky Blue
        "12": [255, 255, 0],     # Yellow
        "13": [255, 255, 255],   # White
        "14": [128, 128, 255],   # Pastel Blue
        "15": [255, 128, 0],     # Orange
        "16": [255, 128, 128],   # Pink
        "17": [255, 128, 255],   # Pastel Magenta
        "18": [0, 255, 0],       # Bright Green
        "19": [0, 255, 128],     # Sea Green
        "20": [0, 255, 255],     # Bright Cyan
        "21": [128, 255, 0],     # Lime
        "22": [128, 255, 128],   # Pastel Green
        "23": [128, 255, 255],   # Pastel Cyan
        "24": [255, 255, 64],    # Bright Yellow
        "25": [255, 255, 128],   # Pastel Yellow
        "26": [255, 255, 255],   # Bright White
    }

def calculate_bytes_per_line(mode, screen_chars):
    """Calculate the number of bytes per scanline for a given CPC mode."""
    if mode == 2:
        return screen_chars * 1
    elif mode == 1:
        return screen_chars * 2
    elif mode == 0:
        return screen_chars * 4
    else:
        raise ValueError("Unsupported CPC mode")


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
    # Coming soon, cater for Amstrad Screen Sizes affected by 
    # CRTC Registers, i.e. create a Spectrum Size Screen
    # for Lazy conversions.
    #bytes_per_line = calculate_bytes_per_line(mode, screen_chars)

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
    """
    Decode Mode 2 (1bpp, 2 colours) CPC screen data.

    Each byte encodes 8 horizontal pixels.
    Each visual line is repeated to simulate correct pixel aspect ratio.
    """
    pixels = []

    for i in range(0, len(data), 80):  # 80 bytes per scanline
        line = []
        chunk = data[i:i+80]

        for byte in chunk:
            for bit in range(7, -1, -1):
                index = (byte >> bit) & 1
                line.append(palette.get(str(index), [0, 0, 0]))

        # Repeat line to simulate taller pixels
        pixels.append(line)
        pixels.append(line[:])  # Deep copy to prevent reference duplication

    return pixels



def decode_mode_1(data, palette):
    """
    Decode Mode 1 (2bpp, 4 colours) CPC screen data.

    Each byte encodes 4 pixels.
    PEN 1 = #F0 = 11110000
    PEN 2 = #0F = 00001111
    PEN 3 = #FF = 11111111
    """
    pixels = []

    for i in range(0, len(data), 80):  # 80 bytes per scanline
        line = []
        chunk = data[i:i+80]

        for byte in chunk:
            # Extract pixels: bit pairs are (7&3), (6&2), (5&1), (4&0)
            # Correct Mode 1 pixel bit extraction:
            p1 = ((byte >> 3) & 1) << 1 | ((byte >> 7) & 1)  # Leftmost pixel
            p2 = ((byte >> 2) & 1) << 1 | ((byte >> 6) & 1)
            p3 = ((byte >> 1) & 1) << 1 | ((byte >> 5) & 1)
            p4 = ((byte >> 0) & 1) << 1 | ((byte >> 4) & 1)  # Rightmost pixel

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

    Each byte encodes 2 pixels using interleaved bits: 
    - Left Pixel: bits 1,5,3,7
    - Right Pixel: bits 0,4,2,6
    Each pixel is doubled horizontally for display accuracy.
    """
    pixels = []

    for i in range(0, len(data), 80):
        line = []
        chunk = data[i:i+80]

        for byte in chunk:
            # Extract left pixel (bits 1,5,3,7)
            p1 = (
                ((byte >> 1) & 0x01) << 3 |
                ((byte >> 5) & 0x01) << 2 |
                ((byte >> 3) & 0x01) << 1 |
                ((byte >> 7) & 0x01)
            )
            # Extract right pixel (bits 0,4,2,6)
            p2 = (
                ((byte >> 0) & 0x01) << 3 |
                ((byte >> 4) & 0x01) << 2 |
                ((byte >> 2) & 0x01) << 1 |
                ((byte >> 6) & 0x01)
            )

            colour1 = palette.get(str(p1), [0, 0, 0])
            colour2 = palette.get(str(p2), [0, 0, 0])

            # Double horizontally for CPC-style wide pixels
            line.extend([colour1, colour1, colour2, colour2])

        pixels.append(line)

    return pixels


def detect_embedded_palette(data):
    """Detect and extract embedded hardware palette data from Advanced Art Studio files.

    This is currently a placeholder. Some screen files may contain hidden colour
    definitions stored in unused memory areas. This function will eventually scan
    for those and convert them to greyscale indices or INK mappings.

    Args:
        data (bytes): Raw binary screen data to analyse.

    Returns:
        dict or None: Extracted palette mapping if found, otherwise None.
    """
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



# modules/amstrad.py

def process_amstrad(args):
    """
    Handle all Amstrad CPC-specific processing and PNG output.

    Expects args to come directly from argparse.
    """
    # Step 1: Load raw data
    with open(args.filename, "rb") as f:
        raw_data = f.read()

    print(f"\n📂 Processing file: {args.filename}")
    print(f"🖼️  Mode: {args.Mode} | Screen dump: {args.screen_dump} | Detect HW colours: {args.detect_hw_colours}")

    # Step 2: Load full CPC palette
    full_palette = default_cpc_palette()

    # Step 3: Load custom palette JSON if provided
    palette = full_palette
    if args.palette:
        try:
            palette = load_palette_json(args.palette)
            print(f"🎨 Loaded custom palette from: {args.palette}")
        except Exception as e:
            print(f"⚠️  Failed to load custom palette: {e} — using default CPC palette")

    # Step 4: Load default INK mapping
    logical_to_ink = get_default_ink_palette()

    # Step 5: Override with user --inks values
    if args.inks:
        try:
            ink_values = [int(i.strip()) for i in args.inks.split(",")]
            if not all(0 <= i <= 26 for i in ink_values):
                raise ValueError
            for i, val in enumerate(ink_values):
                logical_to_ink[i] = val
            print(f"🧪 Custom ink overrides applied: {ink_values}")
        except Exception:
            print("❌ Error: --inks must be a comma-separated list of values between 0 and 26 (e.g. 0,26,6,18)")
            sys.exit(1)
    else:
        print("🎨 Using default firmware ink palette")

    # Step 6: Apply INK mapping
    palette = make_ink_palette(logical_to_ink, full_palette)

    if args.show_inks:
        print("🖍 Final INK → RGB Mapping:")
        for ink in sorted(logical_to_ink.keys()):
            rgb = palette.get(str(ink))
            if rgb:
                print(f"  INK {ink:>2}: {rgb}")

    # Step 7: Decode image
    from modules.amstrad import decode_amstrad  # avoid circular if defined in same file
    image_data = decode_amstrad(
        raw_data,
        mode=args.Mode,
        palette=palette,
        screen_dump=args.screen_dump,
        detect_hw_colours=args.detect_hw_colours
    )

    # Step 8: Save to PNG
    output_file = args.output if args.output else "output.png"
    width = len(image_data[0])
    height = len(image_data)
    flat_rows = [[value for pixel in row for value in pixel] for row in image_data]

    with open(output_file, "wb") as f:
        writer = png.Writer(
            width=width,
            height=height,
            bitdepth=8,
            greyscale=False,
            planes=3
        )
        writer.write(f, flat_rows)

    print(f"✅ PNG written to: {output_file}\n")
