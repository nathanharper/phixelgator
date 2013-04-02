<h1>Phixelgator</h1>
Sorry for the dumb title! I couldn't think of anything. This is a command line utility that converts a photo to "pixel art", i.e. a lower resolution version of the same image with a custom color palette.

Dependencies are python and the python imaging library "PIL". If you are running a python version less than 2.7, you may need to install argparse as well. This should be enough:

<pre>sudo easy_install PIL argparse</pre>

I'm lazy, so here's a dump of the help printout from when you run `./phixelgator -h` at the CLI.

<pre>
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
</pre>

As I said above, you can see all this from using the help flag when invoking the script. Just do:

<pre>
chmod +x phixelgator.py
./phixelgator.py -h
</pre>

Here's an example usage:

<pre>./phixelgator.py -p nes -t jpeg -b 16 -d 1600x1600 ~/input.png output.jpeg</pre>

That would take the file `~/input.png` and make a new file name `output.jpeg` that is a JPEG file made from 16x16-pixel chunks and then resized to 1600x1600 pixels using the NES color palette.

You can also create custom palette files manually and load them into Phixelgator. The files should be formatted like so:

<pre>
[
[0,0,0],
[255,255,255]
]
</pre>

Each integer triplet represents an RGB color value (in that order) ranging from 0 to 255. If you had that saved to a file name `custom.json`, you could use it in your image translation like so: `./phixelgator.py -c custom.json ~/input.png output.png`

This tool is *heavily* inspired by this site: http://superpixeltime.com/
One might even say that I just ported it to Python! So, many thanks to the creators.
