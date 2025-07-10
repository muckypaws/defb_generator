## Monochrome Bitmap DEFB Generator – User Manual

**Version:** Refer to in-app banner
**Author:** Jason Brooks
**Script:** `DEFB_GeneratorV3.py`

---

### 🧩 Overview

A command-line Python tool that converts monochrome sprite sheets (PNG format) into compact 1-bit-per-pixel representations. Originally built with ZX Spectrum `DEFB` assembly output in mind, the tool is now suitable for a wide range of retro, embedded, or emulator-based graphics workflows. It supports exporting as `DEFB` listings, raw binary, ASCII previews, and reverse reconstruction from binary back to PNG.

---

### ⚙️ Command-Line Arguments

#### 🎯 Input

* `filename` – *(optional)* Path to PNG input file. Required unless using `--sprite_data`.

#### 🖼️ Sprite Layout

* `--sprite_width` – Width of each sprite in pixels (default: `8`)
* `--sprite_height` – Height of each sprite in pixels (default: `8`)
* `--gap_x` – Horizontal gap between sprites (default: `0`)
* `--gap_y` – Vertical gap between sprites (default: `0`)
* `--offset_x` – Horizontal pixel offset from top-left (default: `0`)
* `--offset_y` – Vertical pixel offset from top-left (default: `0`)

#### 🎨 Colour Handling

* `--exclude_colour` – Background colour in hex (default: `#000000`)
* `--exclude_tolerance` – RGB tolerance for exclusion (default: `8`)
* `--alpha_threshold` – Ignore pixels with alpha below threshold (default: `254`)

#### 🧾 Output Options

* `--hex` – Output `DEFB` lines in hexadecimal
* `--bin` – Output `DEFB` lines in binary
* `--labels` – Add assembler-style labels (e.g., `sprite_1_2:`)
* `--binfile` – Output raw sprite binary to a `.bin` file
* `--preview` – Render ASCII preview of each sprite in terminal
* `--output` / `-o` – Output `.asm` file path (stdout if omitted)

#### 🔄 Sprite Transformations

* `--inverse` – Invert logic (exclude colour becomes foreground)
* `--mirror` – Mirror sprite bits horizontally
* `--mirror-align` – Reverse byte order as well as bits
* `--flip-vertical` – Vertically flip sprite rows

#### 🎞️ Animation & Timing

* `--animate` – Run ASCII animation of all sprites in loop
* `--delay` – Time delay between frames in seconds (default: `0.2`)

#### 📤 Alternative Input (BIN Decode Mode)

* `--sprite_data` – Input binary sprite data (instead of PNG)
* `--bin_output_png` – Output PNG reconstruction of sprite data
* `--max_texture_width` – Max width of reconstructed image (used for layout)

---

### 🔧 Example Usages

#### Convert PNG to DEFB (Hex, with labels)

```bash
python3 DEFB_GeneratorV3.py sprites.png --sprite_width 8 --sprite_height 8 --hex --labels -o output.asm
```

#### Generate Binary Sprite File

```bash
python3 DEFB_GeneratorV3.py sprites.png --binfile sprites.bin
```

#### Preview Sprites in Terminal

```bash
python3 DEFB_GeneratorV3.py TestData/SpriteSheet.png --preview --sprite_width 10 --sprite_height 16
```

#### Animate Sprites (Linux/macOS only)

```bash
python3 DEFB_GeneratorV3.py sprites.png --animate
```

#### Decode BIN File into PNG

```bash
python3 DEFB_GeneratorV3.py --sprite_data sprites.bin --bin_output_png --sprite_width 8 --sprite_height 8 --max_texture_width 128
```

---

### 🧮 How Image Pixels Translate to Bytes

Sprites are encoded row-by-row, left to right, top to bottom. Each row is packed into bytes, where 1 bit = 1 pixel. Pixels are considered "on" or "off" depending on whether they match or differ from the `--exclude_colour`.

#### Example (8×8 Sprite):

```
Input Image:
⬜⬛⬛⬜⬜⬜⬛⬛   (⬜ = background / excluded, ⬛ = sprite pixel)
⬜⬛⬛⬜⬜⬜⬛⬛
⬜⬛⬛⬜⬜⬜⬛⬛
⬜⬛⬛⬜⬜⬜⬛⬛
⬜⬛⬛⬜⬜⬜⬛⬛
⬜⬛⬛⬜⬜⬜⬛⬛
⬜⬛⬛⬜⬜⬜⬛⬛
⬜⬛⬛⬜⬜⬜⬛⬛

Binary encoding (row-wise):
  01100011   -> 0x63
  01100011   -> 0x63
  01100011   -> 0x63
  01100011   -> 0x63
  01100011   -> 0x63
  01100011   -> 0x63
  01100011   -> 0x63
  01100011   -> 0x63

DEFB Output:
  DEFB 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63, 0x63
```

This simple layout ensures the binary and DEFB outputs are predictable and match the sprite visually, especially when viewed in horizontal byte-aligned grids.

---

### 🔄 Transformation Examples

#### `--inverse`

Reverses which pixels are treated as 'on'. Useful for PNGs with light foreground on dark background.

```
Original Row:  ⬜⬛⬛⬜⬜⬜⬛⬛  → 01100011
Inverse Logic: ⬛⬜⬜⬛⬛⬛⬜⬜  → 10011100
```

#### `--mirror`

Each row's bits are reversed (horizontal mirror).

```
Original Row:     01100011 → 0x63
Mirrored Bits:    11000110 → 0xC6
```

#### `--mirror-align`

Same as `--mirror`, but byte order is also reversed for multi-byte sprites.

#### `--flip-vertical`

Rows are reversed (top-to-bottom flip).

```
Before Flip:
  Row 0 → 01100011
  Row 7 → 01100011

After Flip:
  Row 0 → 01100011 (was Row 7)
  Row 7 → 01100011 (was Row 0)
```

Combined options can produce mirrored + flipped + inverted variants for various platforms.

---

### 📦 Dependencies

* Python 3.7+
* `pypng` (Install via `pip install pypng`)

---

### ⚠️ Notes

* Input PNG must be 1-bit (black/white) or greyscale.
* Animation mode uses ANSI control sequences and is Unix-only.
* Ensure dimensions divide evenly across the source image.
* Output is ZX Spectrum-friendly but also suitable for general retro, embedded, and emulator graphics workflows.

---

### 👤 Credits

Written by Jason Brooks, 2025
Terminal banner artwork included for nostalgic ZX-era flair.
