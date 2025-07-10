# ZX Spectrum Sprite Sheet to DEFB Converter

![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey)
![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-v0.4-orange)

> Monochrome bitmap to DEFB/HEX/BIN sprite converter with preview and animation support.

---

## ✅ Features

* 🔲 Convert PNG sprite sheets to `.DEFB` output
* 🧱 Binary `.bin` export for sprite data
* 🔁 Horizontal mirror, vertical flip, inverse logic
* 🔍 ASCII preview of sprites in terminal
* 🖼️ PNG output from `.BIN` sprite data
* 🕹️ Animated ASCII preview (looping, key to exit)
* Customisable sprite width/height and spacing
* Pixel offset support (cropping)
* Alpha channel filtering and background colour exclusion
* Outputs in decimal, hexadecimal, or binary
* Optional assembler-style `sprite_X_Y:` labels

---

## ⚙️ Setup Instructions

### 📦 Requirements

* Python 3.7+
* `pypng` library

### 🪟 Windows / 🍎 macOS / 🐧 Linux

```bash
# Clone or download the script
cd <project-folder>

# Create and activate a virtual environment
python -m venv venv
# Windows
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🎮 Usage Examples

### 🔄 Convert Sprite Sheet (with gaps and offset)

```bash
python DEFB_GeneratorV3.py TestData/SpriteSheetTest1.png \
  --sprite_width 10 --sprite_height 16 \
  --gap_x 1 --gap_y 1 \
  --offset_x 1 --offset_y 1 \
  --exclude_colour "#000000" --exclude_tolerance 8 \
  --labels --preview --hex \
  --output output.asm --binfile sprites.bin
```

### 🔄 Convert Non-Byte-Aligned Width (e.g. 10px)

```bash
python DEFB_GeneratorV3.py TestData/SpriteSheet.png \
  --sprite_width 10 --sprite_height 16 \
  --exclude_colour "#000000" --exclude_tolerance 8 \
  --labels --preview \
  --output outputTest.asm --binfile spritesTest.bin
```

### 🔳 PNG to DEFB or Binary

```bash
python DEFB_GeneratorV3.py assets/spritesheet.png --sprite_width 8 --sprite_height 16 \
  --output sprites.asm --binfile sprites.bin
```

### 🔍 PNG to ASCII Preview

```bash
python DEFB_GeneratorV3.py assets/spritesheet.png --sprite_width 16 --sprite_height 16 --preview
```

### 🧩 BIN to PNG + Preview

```bash
python DEFB_GeneratorV3.py dummy.png --sprite_data chumper-bear.bin \
  --sprite_width 16 --sprite_height 16 --bin_output_png output.png --preview
```

> `dummy.png` is ignored when `--sprite_data` is used.

### 🎞️ Animated Preview

```bash
python DEFB_GeneratorV3.py assets/spritesheet.png --sprite_width 8 --sprite_height 16 --animate
```

```bash
python DEFB_GeneratorV3.py dummy.png --sprite_data chumper-bear.bin --sprite_width 16 --sprite_height 16 --animate
```

> Press any key to stop animation.

---

## 🧠 Command Line Parameters

| Parameter                  | Description                                                       |
| -------------------------- | ----------------------------------------------------------------- |
| `filename`                 | Optional path to PNG file (required unless using `--sprite_data`) |
| `--sprite_width`           | Width of each sprite in pixels (multiple of 8 recommended)        |
| `--sprite_height`          | Height of each sprite in pixels                                   |
| `--gap_x`, `--gap_y`       | Horizontal and vertical spacing between sprites                   |
| `--offset_x`, `--offset_y` | Pixel offset into the sheet                                       |
| `--exclude_colour`         | Background colour in hex (default `#000000`)                      |
| `--exclude_tolerance`      | RGB tolerance (default `8`)                                       |
| `--alpha_threshold`        | Ignore pixels below this alpha value (default `254`)              |
| `--hex`, `--bin`           | Output in hexadecimal or binary format                            |
| `--labels`                 | Include sprite labels in DEFB output                              |
| `--preview`                | ASCII preview in terminal                                         |
| `--inverse`                | Invert logic (exclude becomes encoded pixel)                      |
| `--mirror`                 | Flip bits horizontally                                            |
| `--mirror-align`           | Reverse byte order too                                            |
| `--flip-vertical`          | Vertically flip each sprite                                       |
| `--animate`                | ASCII animation preview                                           |
| `--delay`                  | Frame delay in seconds (default `0.2`)                            |
| `--sprite_data`            | Input raw sprite `.bin` file                                      |
| `--bin_output_png`         | Reconstruct `.PNG` from binary                                    |
| `--max_texture_width`      | Max width of reconstructed PNG layout                             |
| `--binfile`                | Output binary file (.bin)                                         |
| `-o`, `--output`           | Output `.asm` file                                                |

---

## 📝 Example Workflow

```bash
python DEFB_GeneratorV3.py player.png --sprite_width 8 --sprite_height 16 \
  --mirror --flip-vertical --binfile player.bin --output player.asm --preview
```

---

## 🔧 Output Formats

* **DEFB statements**: Z80-ready, like `DEFB 255, 129, 165, ...`
* **Binary file output**: Usable in emulators or embedded loaders
* **ASCII preview**: Quick visualisation in terminal
* **PNG export**: Reconstructed from binary input

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

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🧑‍💻 Author

Created by [Jason Brooks](https://muckypaws.com)
