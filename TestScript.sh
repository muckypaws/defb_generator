python DEFB_GeneratorV3.py --sprite_width 10 --sprite_height 16 --exclude_colour #000000  TestData/SpriteSheet.png --output TestOutput/output_with_offset.asm --inverse --animate
python DEFB_GeneratorV3.py --sprite_width 10 --sprite_height 16 --exclude_colour #000000  TestData/SpriteSheet.png --output TestOutput/output_with_offset.asm --animate
python DEFB_GeneratorV3.py --sprite_width 10 --sprite_height 16 --exclude_colour #000000  TestData/SpriteSheet.png --output TestOutput/output_with_offset_mirror.asm --mirror-align --animate
python DEFB_GeneratorV3.py --sprite_width 10 --sprite_height 16 --exclude_colour #000000  TestData/SpriteSheet.png --output TestOutput/output_with_offset.asm --flip-vertical --animate
python DEFB_GeneratorV3.py --sprite_width 10 --sprite_height 16 --exclude_colour #000000  TestData/SpriteSheet.png --output TestOutput/output_with_offset_mirror.asm --inverse --mirror-align --animate
python DEFB_GeneratorV3.py --sprite_width 10 --sprite_height 16 --exclude_colour #000000  TestData/SpriteSheet.png --output TestOutput/output_with_offset_mirror.asm --inverse --mirror-align --flip-vertical --animate

python DEFB_GeneratorV3.py --sprite_width 10 --sprite_height 16 --exclude_colour #000000 --offset_x 1 --offset_y 1 --gap_x 1 --gap_y 1 TestData/SpriteSheetTest1.png --animate
python DEFB_GeneratorV3.py --sprite_width 16 --sprite_height 16 TestData/SpriteSheetTest1.png --sprite_data TestData/HornBears.bin --bin_output_png TestOutput/HornBears.png --animate
