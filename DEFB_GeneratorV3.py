"""
ZX Spectrum Sprite Sheet to DEFB Converter.

This module reads a PNG sprite sheet and converts each sprite into
ZX Spectrum-compatible assembler output using DEFB statements.

Supports output in decimal, hexadecimal, and binary formats, as well as raw binary file export.

Author: Jason Brooks - muckypaws.com
Version: 0.3c - Windows is Feckin' shite edition... 
Date: 3rd July 2025
"""
import sys
print("DEBUG: Python path is", sys.executable)

import os
import sys
import time
import math
import argparse
import platform
import png

if platform.system() == "Windows":
    import msvcrt
else:
    import termios
    import tty
    import select

print("Interpreter path:", sys.executable)

def key_pressed():
    """
    Check if a key has been pressed (cross-platform, no admin rights).
    """
    if platform.system() == "Windows":
        return msvcrt.kbhit()
    else:
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        return bool(dr)

def render_spectrum_bin_to_frames(sprite_data, sprite_width, sprite_height):
    """
    Convert ZX Spectrum sprite binary data into a list of individual sprite frames.

    Args:
        sprite_data (bytes): Raw ZX Spectrum sprite data.
        sprite_width (int): Width of a single sprite in pixels.
        sprite_height (int): Height of a single sprite in pixels.

    Returns:
        list of list of list of int: Each frame is a 2D array of greyscale pixel values.
    """
    bytes_per_row = (sprite_width + 7) // 8
    bytes_per_sprite = bytes_per_row * sprite_height
    total_sprites = len(sprite_data) // bytes_per_sprite

    frames = []
    for sprite_index in range(total_sprites):
        base = sprite_index * bytes_per_sprite
        frame = []
        for row in range(sprite_height):
            row_pixels = []
            row_offset = base + row * bytes_per_row
            for byte_index in range(bytes_per_row):
                byte = sprite_data[row_offset + byte_index]
                for bit in range(8):
                    pixel_x = byte_index * 8 + bit
                    if pixel_x >= sprite_width:
                        continue
                    pixel_on = (byte & (1 << (7 - bit))) != 0
                    row_pixels.append(255 if pixel_on else 0)
            frame.append(row_pixels)
        frames.append(frame)
    return frames


def render_spectrum_bin_to_image(sprite_data, sprite_width, sprite_height, sprites_per_row=None):
    """
    Convert ZX Spectrum sprite binary data into a 2D greyscale image array.

    Args:
        sprite_data (bytes): Raw ZX Spectrum sprite data.
        sprite_width (int): Width of a single sprite in pixels.
        sprite_height (int): Height of a single sprite in pixels.
        sprites_per_row (int, optional): Number of sprites per row in the output image.

    Returns:
        list of list of int: 2D greyscale image data (0 = background, 255 = pixel on).
    """
    bytes_per_row = (sprite_width + 7) // 8
    bytes_per_sprite = bytes_per_row * sprite_height
    total_sprites = len(sprite_data) // bytes_per_sprite

    if sprites_per_row is None:
        sprites_per_row = math.ceil(math.sqrt(total_sprites))

    sprites_per_column = math.ceil(total_sprites / sprites_per_row)

    image_width = sprites_per_row * sprite_width
    image_height = sprites_per_column * sprite_height

    image_data = [[0 for _ in range(image_width)] for _ in range(image_height)]

    for sprite_index in range(total_sprites):
        base = sprite_index * bytes_per_sprite
        x_offset = (sprite_index % sprites_per_row) * sprite_width
        y_offset = (sprite_index // sprites_per_row) * sprite_height

        for row in range(sprite_height):
            row_offset = base + row * bytes_per_row
            for byte_index in range(bytes_per_row):
                byte = sprite_data[row_offset + byte_index]
                for bit in range(8):
                    pixel_x = byte_index * 8 + bit
                    if pixel_x >= sprite_width:
                        continue
                    pixel_on = (byte & (1 << (7 - bit))) != 0
                    image_data[y_offset + row][x_offset + pixel_x] = 255 if pixel_on else 0

    return image_data

def write_image_to_png(image_data, output_filename):
    """
    Write a 2D greyscale pixel array to a PNG file using pypng.

    Args:
        image_data (list of list of int): 2D array of greyscale pixel values.
        output_filename (str): Path to save PNG file.
    """
    height = len(image_data)
    width = len(image_data[0])
    with open(output_filename, "wb") as f:
        writer = png.Writer(width=width, height=height, greyscale=True, bitdepth=8)
        writer.write(f, image_data)

def ascii_preview_from_image(image_data):
    """
    Generate an ASCII preview of a greyscale image using full blocks for white pixels.

    Args:
        image_data (list of list of int): 2D array of greyscale pixel values.

    Returns:
        str: Multi-line string preview of the image.
    """
    preview = []
    for row in image_data:
        line = ''.join('█' if px > 0 else ' ' for px in row)
        preview.append(line)
    return '\n'.join(preview)

def ascii_preview_from_image(image_data):
    """
    Generate an ASCII preview of a greyscale image using full blocks for white pixels.

    Args:
        image_data (list of list of int): 2D array of greyscale pixel values.

    Returns:
        str: Multi-line string preview of the image.
    """
    preview = []
    for row in image_data:
        line = ''.join('█' if px > 0 else ' ' for px in row)
        preview.append(line)
    return '\n'.join(preview)

def animate_ascii_preview(frames, delay=0.25):
    """
    Animate a sequence of sprite frames or ASCII art frames with key interrupt support.

    Args:
        frames (list): Either 2D pixel frames or pre-rendered ASCII string frames.
        delay (float): Time in seconds between frames.
    """
    if platform.system() != "Windows":
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)
    else:
        old_settings = None  # no-op for Windows

    try:
        while True:
            for frame in frames:
                print("\033[H\033[J", end="") if platform.system() != "Windows" else os.system("cls")
                if isinstance(frame, list) and all(isinstance(line, str) for line in frame):
                    print('\n'.join(frame))
                else:
                    print(ascii_preview_from_image(frame))
                time.sleep(delay)
                if key_pressed():
                    #read_key()
                    raise KeyboardInterrupt
    except KeyboardInterrupt:
        print("\nAnimation stopped.")
    finally:
        if platform.system() != "Windows":
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def flip_sprite_vertically(sprite_rows):
    """
    Flip the entire sprite vertically (top-to-bottom).

    Args:
        sprite_rows (list of list of int): Each sublist is a row of bytes.

    Returns:
        list of list of int: Vertically flipped sprite.
    """
    return sprite_rows[::-1]

def reverse_bits(byte):
    """Reverse the bits of a single byte using bit manipulation."""
    byte = (byte & 0xF0) >> 4 | (byte & 0x0F) << 4
    byte = (byte & 0xCC) >> 2 | (byte & 0x33) << 2
    byte = (byte & 0xAA) >> 1 | (byte & 0x55) << 1
    return byte

def mirror_sprite_bytes(sprite_bytes, bytes_per_row, mirror_align):
    """
    Mirror the sprite horizontally either in-place (bitwise mirror per byte).

    Or with alignment (bitwise mirror and reverse byte order).

    Args:
        sprite_bytes (list): The raw sprite byte list.
        bytes_per_row (int): Number of bytes per row.
        mirror_align (bool): If True, also reverse the byte order per row.

    Returns:
        list: Transformed list of bytes.
    """
    mirrored = []
    for i in range(0, len(sprite_bytes), bytes_per_row):
        row = sprite_bytes[i:i+bytes_per_row]
        flipped = [reverse_bits(b) for b in row]
        if mirror_align:
            flipped = flipped[::-1]
        mirrored.extend(flipped)
    return mirrored

def convert_png_to_zx_defb_pypng(
    png_file,
    exclude_colour="#000000",
    sprite_width=10,
    sprite_height=16,
    gap_x=0,
    gap_y=0,
    offset_x=0,
    offset_y=0,
    use_hex=False,
    use_bin=False,
    use_labels=False,
    alpha_threshold=254,
    preview_ascii=False,
    exclude_tolerance=8,
    inverse=False,
    mirror=False,
    mirror_align=False,
    flip_vertical=False
):
    """
    Convert a PNG sprite sheet to ZX Spectrum DEFB output with options for inversion, mirroring and preview.

    Args:
        png_file (str): Path to the input PNG file.
        exclude_colour (str): Colour in hex to treat as background.
        sprite_width (int): Width of each sprite in pixels.
        sprite_height (int): Height of each sprite in pixels.
        gap_x (int): Horizontal gap between sprites in pixels.
        gap_y (int): Vertical gap between sprites in pixels.
        offset_x (int): Horizontal offset in pixels.
        offset_y (int): Vertical offset in pixels.
        use_hex (bool): Output DEFB values in hexadecimal format.
        use_bin (bool): Output DEFB values in binary format.
        use_labels (bool): Add sprite labels in the output.
        alpha_threshold (int): Ignore pixels below this alpha threshold.
        preview_ascii (bool): Include ASCII preview in output.
        exclude_tolerance (int): Colour match tolerance.
        inverse (bool): Invert logic to encode the exclude colour instead.
        mirror (bool): Mirror sprites horizontally.
        mirror_align (bool): Also align mirrored sprite bytes.
        flip_vertical (bool): Flip the sprite vertically.

    Returns:
        tuple: Assembler output string, raw binary output, optional ASCII block list.
    """
    exclude_rgb = tuple(int(exclude_colour[i:i+2], 16) for i in (1, 3, 5))
    reader = png.Reader(png_file)
    width, height, pixels, meta = reader.read()
    pixel_rows = list(pixels)
    channels = 4 if meta.get('alpha', False) else 3

    def get_pixel(x, y):
        row = pixel_rows[y]
        start = x * channels
        return tuple(row[start:start + channels])

    def colour_close(a, b, tolerance=8):
        return all(abs(a[i] - b[i]) <= tolerance for i in range(3))

    defb_output = []
    binary_output = bytearray()
    sprite_index = 0

    all_ascii_blocks = []  # <- NEW

    full_width = sprite_width + gap_x
    full_height = sprite_height + gap_y
    bytes_per_row = math.ceil(sprite_width / 8)

    max_x = width - ((width - offset_x) % full_width)
    max_y = height - ((height - offset_y) % full_height)

    for y_sprite_index, y_sprite in enumerate(range(offset_y, max_y, full_height)):
        if y_sprite + sprite_height > height:
            break
        for x_sprite_index, x_sprite in enumerate(range(offset_x, max_x, full_width)):
            if x_sprite + sprite_width > width:
                break

            defb_output.append(f"; Sprite {sprite_index} ; (X={x_sprite_index}, Y={y_sprite_index})")
            if use_labels:
                defb_output.append(f"sprite_{x_sprite_index}_{y_sprite_index}:")

            sprite_rows = []
            ascii_lines = []

            for y in range(sprite_height):
                row_bytes = []
                ascii_row = ""
                for byte_index in range(bytes_per_row):
                    byte_val = 0
                    visual_bits = []
                    for bit in range(8):
                        pixel_x = x_sprite + byte_index * 8 + bit

                        if pixel_x >= x_sprite + sprite_width:
                            if inverse:
                                byte_val |= 1 << (7 - bit)
                                visual_bits.append("█")
                            else:
                                visual_bits.append(" ")
                            continue

                        pixel = get_pixel(pixel_x, y_sprite + y)
                        r, g, b = pixel[:3]
                        alpha_ok = True
                        if channels == 4:
                            alpha_ok = pixel[3] >= alpha_threshold

                        match = colour_close((r, g, b), exclude_rgb, exclude_tolerance)
                        pixel_on = (match if inverse else not match) and alpha_ok

                        if pixel_on:
                            byte_val |= 1 << (7 - bit)
                            visual_bits.append("█")
                        else:
                            visual_bits.append(" ")

                    row_bytes.append(byte_val)
                    ascii_row += "".join(visual_bits)
                sprite_rows.append(row_bytes)
                ascii_lines.append(ascii_row)
                
            if flip_vertical:
                sprite_rows = flip_sprite_vertically(sprite_rows)
                ascii_lines = ascii_lines[::-1]

            flat_bytes = [b for row in sprite_rows for b in row]

            if mirror:
                flat_bytes = mirror_sprite_bytes(flat_bytes, bytes_per_row, mirror_align)
                if mirror_align:
                    ascii_lines = [line[::-1] for line in ascii_lines]
                else:
                    ascii_lines = [
                        ''.join(
                            ''.join(line[j:j+8][::-1]) for j in range(0, len(line), 8)
                        )
                        for line in ascii_lines
                    ]
            
            if preview_ascii:
                    all_ascii_blocks.append(ascii_lines)

            binary_output.extend(flat_bytes)

            for i in range(0, len(flat_bytes), 8):
                chunk = flat_bytes[i:i+8]
                if use_bin:
                    formatted = ", ".join(f"%{b:08b}" for b in chunk)
                elif use_hex:
                    formatted = ", ".join(f"${b:02X}" for b in chunk)
                else:
                    formatted = ", ".join(str(b) for b in chunk)
                defb_output.append("    DEFB " + formatted)

            if preview_ascii:
                defb_output.append("    ; ASCII Preview:")
                for line in ascii_lines:
                    defb_output.append("    ; " + line)

            defb_output.append("")
            sprite_index += 1

    #return "\n".join(defb_output), bytes(binary_output)
    return "\n".join(defb_output), bytes(binary_output), all_ascii_blocks


def main():
    """
    Entry point for the ZX Spectrum sprite tool.

    Parses command-line arguments and executes the appropriate rendering logic.
    """
    parser = argparse.ArgumentParser(
        description="Convert a PNG sprite sheet into ZX Spectrum DEFB statements."
    )
    parser.add_argument("filename", help="Path to input PNG file")
    parser.add_argument("--sprite_width", type=int, default=8, help="Width of each sprite in pixels")
    parser.add_argument("--sprite_height", type=int, default=8, help="Height of each sprite in pixels")
    parser.add_argument("--gap_x", type=int, default=0, help="Horizontal gap between sprites (default: 0)")
    parser.add_argument("--gap_y", type=int, default=0, help="Vertical gap between sprites (default: 0)")
    parser.add_argument("--offset_x", type=int, default=0, help="Horizontal offset in pixels (default: 0)")
    parser.add_argument("--offset_y", type=int, default=0, help="Vertical offset in pixels (default: 0)")
    parser.add_argument("--exclude_colour", default="#000000", help="Exclude/background colour in hex (default: #000000)")
    parser.add_argument("--exclude_tolerance", type=int, default=8, help="Tolerance when matching exclude colour")
    parser.add_argument("--alpha_threshold", type=int, default=254, help="Ignore pixels with alpha below this value (default: 254)")
    parser.add_argument("--hex", action="store_true", help="Output DEFB values in hexadecimal")
    parser.add_argument("--bin", action="store_true", help="Output DEFB values in binary format")
    parser.add_argument("--labels", action="store_true", help="Add sprite_X_Y: label above each sprite")
    parser.add_argument("--binfile", help="Output raw binary sprite data to .bin file")
    parser.add_argument("--preview", action="store_true", help="Print ASCII preview of each sprite to terminal")
    parser.add_argument("--inverse", action="store_true", help="Invert logic: treat exclude colour as pixel to encode")
    parser.add_argument("--mirror", action="store_true", help="Mirror sprites horizontally")
    parser.add_argument("--mirror-align", action="store_true", help="Right-align mirrored sprite by reversing byte order")
    parser.add_argument("--flip-vertical", action="store_true", help="Flip sprite vertically (top-to-bottom)")
    parser.add_argument("--animate", action="store_true", help="Animate ASCII preview of each sprite")
    parser.add_argument("--delay", type=float, default=0.2, help="Delay in seconds between frames (default: 0.2)")
    parser.add_argument("--sprite_data", help="Path to .BIN file containing ZX Spectrum sprite data")
    parser.add_argument("--bin_output_png", help="Filename to write rendered PNG output from .BIN file")
    parser.add_argument("-o", "--output", help="Output filename for DEFB listing (stdout if not specified)")

    args = parser.parse_args()

    if not os.path.isfile(args.filename):
        print(f"❌ Error: File not found - '{args.filename}'")
        sys.exit(1)

    if not args.filename.lower().endswith(".png"):
        print(f"⚠️ Warning: '{args.filename}' does not appear to be a .png file.")

    if args.mirror_align:
        args.mirror = True

    if args.sprite_data:
        if not os.path.isfile(args.sprite_data):
            print(f"\u274c Error: BIN file not found - '{args.sprite_data}'")
            sys.exit(1)
        with open(args.sprite_data, "rb") as f:
            sprite_bytes = f.read()
        
        if args.sprite_width % 8 != 0:
            adjusted_width = ((args.sprite_width + 7) // 8) * 8
            print(f"\u26A0\ufe0f Warning: Sprite width {args.sprite_width} not byte-aligned. Adjusted to {adjusted_width}.")
            args.sprite_width = adjusted_width

        image = render_spectrum_bin_to_image(
            sprite_data=sprite_bytes,
            sprite_width=args.sprite_width,
            sprite_height=args.sprite_height
        )
        if args.bin_output_png:
            write_image_to_png(image, args.bin_output_png)
            print(f"\u2705 PNG image written to {args.bin_output_png}")
        if args.preview:
            print("\nASCII Preview:\n")
            print(ascii_preview_from_image(image))

        if args.animate:
            frames = render_spectrum_bin_to_frames(
                sprite_data=sprite_bytes,
                sprite_width=args.sprite_width,
                sprite_height=args.sprite_height
            )
            animate_ascii_preview(frames, delay=args.delay)
            #animate_ascii_frames(frames)
            return
    else:
        asm_output, binary_data, ascii_blocks = convert_png_to_zx_defb_pypng(
            png_file=args.filename,
            exclude_colour=args.exclude_colour,
            sprite_width=args.sprite_width,
            sprite_height=args.sprite_height,
            gap_x=args.gap_x,
            gap_y=args.gap_y,
            offset_x=args.offset_x,
            offset_y=args.offset_y,
            use_hex=args.hex,
            use_bin=args.bin,
            use_labels=args.labels,
            alpha_threshold=args.alpha_threshold,
            preview_ascii=args.preview,
            exclude_tolerance=args.exclude_tolerance,
            inverse=args.inverse,
            mirror=args.mirror,
            mirror_align=args.mirror_align,
            flip_vertical=args.flip_vertical
        )

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(asm_output)
            print(f"DEFB output written to {args.output}")
        else:
            print(asm_output)

        if args.binfile:
            with open(args.binfile, "wb") as bf:
                bf.write(binary_data)
            print(f"Binary output written to {args.binfile}")

        if args.animate:
            animate_ascii_preview(ascii_blocks, delay=args.delay)
            #preview_animated_ascii(ascii_blocks, delay=args.delay)

if __name__ == "__main__":
    
    main()
