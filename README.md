usage: phixel [-h] [-b BLOCK]
              [-p {mario,flashman,hyrule,kungfu,tetris,contra,appleii,atari2600,commodore64,gameboy,grayscale,intellivision,nes,sega}]
              [-c CUSTOM] [-d DIMENSIONS] [-t {png,jpeg,gif,bmp}]
              [infile] [outfile]

Create "pixel art" from a photo

positional arguments:
  infile                the input file (defaults to stdin)
  outfile               the output file (defaults to stdout)

optional arguments:
  -h, --help            show this help message and exit
  -b BLOCK, --block BLOCK
                        Block size for phixelization. Default is 8 pixels.
  -p {mario,flashman,hyrule,kungfu,tetris,contra,appleii,atari2600,commodore64,gameboy,grayscale,intellivision,nes,sega}, --palette {mario,flashman,hyrule,kungfu,tetris,contra,appleii,atari2600,commodore64,gameboy,grayscale,intellivision,nes,sega}
                        The color palette to use.
  -c CUSTOM, --custom CUSTOM
                        A custom palette file to use instead of the defaults.
                        Should be plain JSON file with a single array of color
                        triplets.
  -d DIMENSIONS, --dimensions DIMENSIONS
                        The dimensions of the new image (format: /\d+x\d+/i)
  -t {png,jpeg,gif,bmp}, --type {png,jpeg,gif,bmp}
                        Output file type.

Disclaimer: this does not *really* make pixel art, it just reduces the image

This tool is *heavily* inspired by this site: http://superpixeltime.com/
One might even say that I just ported it to Python! So, many thanks to the creators.
