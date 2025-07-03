# ZX Spectrum Sprite Sheet to DEFB Converter

A command-line tool to convert ZX Spectrum-compatible sprite sheets into `.DEFB` assembler statements or raw binary sprite data. Supports previewing in ASCII art, PNG export, flipping, mirroring, and inverse rendering. Also allows loading binary `.BIN` sprite data and converting it into visual PNG or ASCII output.

---

## ✅ Features

- 🔲 Convert PNG sprite sheets to `.DEFB` output
- 🧱 Binary `.bin` export for ZX Spectrum sprite data
- 🔁 Horizontal mirror, vertical flip, inverse logic
- 🔍 ASCII preview of sprites in terminal
- 🖼️ PNG output from `.BIN` sprite data
- 🕹️ Animated ASCII preview (looping, key to exit)
- Supports sprites of arbitrary size (width × height)
- Handles horizontal/vertical gaps between sprites
- Optional bounding box offset for inner sprite cropping
- Detects alpha transparency (ignores pixels with low alpha)
- Excludes a specific RGB background colour (with optional tolerance)
- Outputs in decimal, hexadecimal, or binary DEFB format
- Optionally adds assembler-style `sprite_X_Y:` labels
- ASCII art preview of each sprite in the terminal
- Raw binary output of sprite data

---

## ⚙️ Setup Instructions

### 📦 Requirements

- Python 3.7+
- `pypng` library

### 🪟 Windows / 🍎 macOS / 🐧 Linux

```bash
# Clone or download the script and enter the folder
cd <project-folder>

# Create and activate a virtual environment
python -m venv venv
# Windows
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

---

## 🎮 Usage

### 🔄 Sprite Sheet with Bounding Box Export as HEX Example
```bash
python DEFB_Generator.py SpriteSheetTest1.png \
    --sprite_width 10 \
    --sprite_height 16 \
    --gap_x 1 --gap_y 1 \
    --offset_x 1 --offset_y 1 \
    --exclude_colour "#000000" \
    --exclude_tolerance 8 \
    --labels --preview_ascii --hex \
    --output output.asm --binfile sprites.bin
```
### 🔄 Sprite Sheet not byte aligned (10 Pixels Width) Example
```bash
python DEFB_Generator.py SpriteSheet.png \
    --sprite_width 10 \
    --sprite_height 16 \
    --exclude_colour "#000000" \
    --exclude_tolerance 8 \
    --labels --preview_ascii \
    --output outputTest.asm --binfile spritesTest.bin
```

## Output Format

Each sprite block in the `.asm` file looks like:

```asm
; Sprite 0 ; (X=0, Y=0)
sprite_0_0:
    DEFB $3C, $42, $A5, $81, $A5, $99, $42, $3C
    ; ASCII Preview:
    ;   ████    
    ;  █    █   
    ; █ █  █ █  
    ; █      █  
    ; █ █  █ █  
    ; █  ██  █  
    ;  █    █   
    ;   ████    
```

### 🔄 PNG to DEFB or Binary

```bash
python DEFB_GeneratorV3.py assets/spritesheet.png --sprite_width 8 --sprite_height 16 --output sprites.asm --binfile sprites.bin
```

### 🔳 PNG to ASCII Preview

```bash
python DEFB_GeneratorV3.py assets/spritesheet.png --sprite_width 16 --sprite_height 16 --preview
```

### 🧩 BIN to PNG + ASCII Preview

```bash
python DEFB_GeneratorV3.py dummy.png --sprite_data chumper-bear.bin --sprite_width 16 --sprite_height 16 --bin_output_png output.png --preview
```

> `dummy.png` is still required to satisfy the positional argument for legacy mode. It is ignored if `--sprite_data` is used.

### 🎞️ Animated Preview (from PNG or BIN)

```bash
python DEFB_GeneratorV3.py assets/spritesheet.png --sprite_width 8 --sprite_height 16 --animate
```

```bash
python DEFB_GeneratorV3.py dummy.png --sprite_data chumper-bear.bin --sprite_width 16 --sprite_height 16 --animate
```

Press any key to stop animation.

---

## 🧠 Command Line Parameters

| Parameter             | Description |
|----------------------|-------------|
| `--sprite_width`      | Width of each sprite in pixels (must be multiple of 8) |
| `--sprite_height`     | Height of each sprite in pixels |
| `--gap_x`, `--gap_y`  | Horizontal/vertical gap between sprites |
| `--offset_x`, `--offset_y` | Pixel offset into the sheet |
| `--exclude_colour`    | Hex colour to treat as transparent (default `#000000`) |
| `--exclude_tolerance` | Tolerance in colour matching (default `8`) |
| `--alpha_threshold`   | Ignore pixels with alpha below this value |
| `--hex`, `--bin`      | Output in hexadecimal or binary format |
| `--labels`            | Add labels to DEFB output (e.g., `sprite_0_1:`) |
| `--preview`           | Show ASCII preview of each sprite |
| `--inverse`           | Invert logic (treat exclude as 'on') |
| `--mirror`            | Horizontally mirror each sprite |
| `--mirror-align`      | Right-align mirrored image (reverses byte order too) |
| `--flip-vertical`     | Vertically flip the sprite |
| `--animate`           | Loop ASCII animation of extracted sprites |
| `--delay`             | Frame delay for animation (default `0.2` sec) |
| `--sprite_data`       | Path to a `.bin` file containing ZX sprite data |
| `--bin_output_png`    | PNG output path when reading `.bin` sprite data |
| `--binfile`           | Write raw binary sprite data to `.bin` |
| `-o`, `--output`      | Output DEFB listing to file |

---

## 📝 Example Workflow

```bash
python DEFB_GeneratorV3.py player.png --sprite_width 8 --sprite_height 16 --mirror --flip-vertical --binfile player.bin --output player.asm --preview
```

---

## 🔧 Output Formats

- **DEFB statements** like:
  ```
  sprite_0_0:
      DEFB 255, 129, 165, ...
  ```
- **Binary file output**: can be used directly in ZX Spectrum loaders or emulators
- **ASCII preview**: for visual debugging in terminal
- **PNG export**: from `.BIN` to visual sprite sheet

---

## 🧑‍💻 Author

Created by Jason Brooks (https://muckypaws.com)  

---