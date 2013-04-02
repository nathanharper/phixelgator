#!/usr/bin/env python
import os, sys, argparse, math, json
from PIL import Image

PALETTES = {
  'tetris' : [
    [50,194,255],
    [160,26,204],
    [20,18,167],
    [66,64,255],
    [21,95,217],
    [100,176,255],
    [192,223,255],
    [72,205,222],
    [228,229,148],
    [255,129,112],
    [255,255,255],
    [0,0,0]
  ],
  'mario' : [
    [146,144,255],
    [13,147,0],
    [136,216,0],
    [107,109,0],
    [234,158,34],
    [153,78,0],
    [255,204,197],
    [181,49,32],
    [255,255,255],
    [0,0,0]
  ],
  'sega' : [
    [0,0,0],
    [85,0,0],
    [170,0,0],
    [255,0,0],
    [0,0,85],
    [85,0,85],
    [170,0,85],
    [255,0,85],
    [0,85,0],
    [85,85,0],
    [170,85,0],
    [255,85,0],
    [0,85,85],
    [85,85,85],
    [170,85,85],
    [255,85,85],
    [0,170,0],
    [85,170,0],
    [170,170,0],
    [255,170,0],
    [0,170,85],
    [85,170,85],
    [170,170,85],
    [255,170,85],
    [0,255,0],
    [85,255,0],
    [170,255,0],
    [255,255,0],
    [0,255,85],
    [85,255,85],
    [170,255,85],
    [255,255,85],
    [0,0,170],
    [85,0,170],
    [170,0,170],
    [255,0,170],
    [0,0,255],
    [85,0,255],
    [170,0,255],
    [255,0,255],
    [0,85,170],
    [85,85,170],
    [170,85,170],
    [255,85,170],
    [0,85,255],
    [85,85,255],
    [170,85,255],
    [255,85,255],
    [0,170,170],
    [85,170,170],
    [170,170,170],
    [255,170,170],
    [0,170,255],
    [85,170,255],
    [170,170,255],
    [255,170,255],
    [0,255,170],
    [85,255,170],
    [170,255,170],
    [255,255,170],
    [0,255,255],
    [85,255,255],
    [170,255,255],
    [255,255,255]
  ],
  'nes' : [
    [124, 124, 124],
    [0, 0, 252],
    [0, 0, 188],
    [68, 40, 188],
    [148, 0, 132],
    [168, 0, 32],
    [168, 16, 0],
    [136, 20, 0],
    [80, 48, 0],
    [0, 120, 0],
    [0, 104, 0],
    [0, 88, 0],
    [0, 64, 88],
    [0, 0, 0],
    [188, 188, 188],
    [0, 120, 248],
    [0, 88, 248],
    [104, 68, 252],
    [216, 0, 204],
    [228, 0, 88],
    [248, 56, 0],
    [228, 92, 16],
    [172, 124, 0],
    [0, 184, 0],
    [0, 168, 0],
    [0, 168, 68],
    [0, 136, 136],
    [248, 248, 248],
    [60, 188, 252],
    [104, 136, 252],
    [152, 120, 248],
    [248, 120, 248],
    [248, 88, 152],
    [248, 120, 88],
    [252, 160, 68],
    [248, 184, 0],
    [184, 248, 24],
    [88, 216, 84],
    [88, 248, 152],
    [0, 232, 216],
    [120, 120, 120],
    [252, 252, 252],
    [164, 228, 252],
    [184, 184, 248],
    [216, 184, 248],
    [248, 184, 248],
    [248, 164, 192],
    [240, 208, 176],
    [252, 224, 168],
    [248, 216, 120],
    [216, 248, 120],
    [184, 248, 184],
    [184, 248, 216],
    [0, 252, 252],
    [216, 216, 216]
  ],
  'kungfu' : [
    [160,26,204],
    [146,144,255],
    [192,223,255],
    [189,244,171],
    [56,135,0],
    [136,216,0],
    [234,158,34],
    [247,216,165],
    [181,49,32],
    [255,255,255],
    [0,0,0]
  ],
  'intellivision' : [
    [0,0,0],
    [164,150,255],
    [255,61,16],
    [181,26,88],
    [84,110,0],
    [0,167,86],
    [255,180,31],
    [201,207,171],
    [0,45,255],
    [36,184,255],
    [255,78,87],
    [189,172,200],
    [56,107,63],
    [117,204,128],
    [250,234,80],
    [255,255,255]
  ],
  'hyrule' : [
    [66,64,255],
    [146,144,255],
    [13,147,0],
    [136,216,0],
    [234,158,34],
    [247,216,165],
    [153,78,0],
    [255,204,197],
    [181,49,32],
    [255,255,255],
    [102,102,102],
    [0,0,0]
  ],
  'grayscale' : [
    [0, 0, 0],
    [20, 20, 20],
    [40, 40, 40],
    [60, 60, 60],
    [80, 80, 80],
    [100, 100, 100],
    [120, 120, 120],
    [140, 140, 140],
    [160, 160, 160],
    [180, 180, 180],
    [200, 200, 200],
    [220, 220, 220],
    [240, 240, 240],
    [255, 255, 255]
  ],
  'gameboy' : [
    [15,56,15],
    [48,98,48],
    [139,172,15],
    [155,188,15]
  ],
  'flashman' : [
    [50,194,255],
    [160,26,204],
    [20,18,167],
    [66,64,255],
    [21,95,217],
    [100,176,255],
    [192,223,255],
    [72,205,222],
    [228,229,148],
    [255,129,112],
    [255,255,255],
    [0,0,0]
  ],
  'contra' : [
    [66,64,255],
    [21,95,217],
    [100,176,255],
    [56,135,0],
    [136,216,0],
    [51,53,0],
    [188.190,0],
    [107,109,0],
    [247,216,165],
    [255,129,112],
    [255,204,197],
    [181,49,32],
    [255,255,255],
    [173,173,173],
    [0,0,0]
  ],
  'commodore64' : [
    [0,0,0],
    [255,255,255],
    [136,57,50],
    [103,182,189],
    [139,63,150],
    [85,160,73],
    [64,49,141],
    [191,206,114],
    [139,84,41],
    [87,66,0],
    [184,105,98],
    [80,80,80],
    [120,120,120],
    [148,224,137],
    [120,105,196],
    [159,159,159]
  ],
  'atari2600' : [
    [0,0,0],
    [68,68,0],
    [112,40,0],
    [132,24,0],
    [136,0,0],
    [120,0,92],
    [72,0,120],
    [20,0,132],
    [0,0,136],
    [0,24,124],
    [0,44,92],
    [0,64,44],
    [0,60,0],
    [20,56,0],
    [44,48,0],
    [68,40,0],
    [64,64,64],
    [100,100,16],
    [132,68,20],
    [152,52,24],
    [156,32,32],
    [140,32,116],
    [96,32,144],
    [48,32,152],
    [28,32,156],
    [28,56,144],
    [28,76,120],
    [28,92,72],
    [32,92,32],
    [52,92,28],
    [76,80,28],
    [100,72,24],
    [108,108,108],
    [132,132,36],
    [152,92,40],
    [172,80,48],
    [176,60,60],
    [160,60,136],
    [120,60,164],
    [76,60,172],
    [56,64,176],
    [56,84,168],
    [56,104,144],
    [56,124,100],
    [64,124,64],
    [80,124,56],
    [104,112,52],
    [132,104,48],
    [144,144,144],
    [160,160,52],
    [172,120,60],
    [192,104,72],
    [192,88,88],
    [176,88,156],
    [140,88,184],
    [104,88,192],
    [80,92,192],
    [80,112,188],
    [80,132,172],
    [80,156,128],
    [92,156,92],
    [108,152,80],
    [132,140,76],
    [160,132,68],
    [176,176,176],
    [184,184,64],
    [188,140,76],
    [208,128,92],
    [208,112,112],
    [192,112,176],
    [160,112,204],
    [124,112,208],
    [104,116,208],
    [104,136,204],
    [104,156,192],
    [104,180,148],
    [116,180,116],
    [132,180,104],
    [156,168,100],
    [184,156,88],
    [200,200,200],
    [208,208,80],
    [204,160,92],
    [224,148,112],
    [224,136,136],
    [208,132,192],
    [180,132,220],
    [148,136,224],
    [124,140,224],
    [124,156,220],
    [124,180,212],
    [124,208,172],
    [140,208,140],
    [156,204,124],
    [180,192,120],
    [208,180,108],
    [220,220,220],
    [232,232,92],
    [220,180,104],
    [236,168,128],
    [236,160,160],
    [220,156,208],
    [196,156,236],
    [168,160,236],
    [144,164,236],
    [144,180,236],
    [144,204,232],
    [144,228,192],
    [164,228,164],
    [180,228,144],
    [204,212,136],
    [232,204,124],
    [236,236,236],
    [252,252,104],
    [232,204,124],
    [252,188,148],
    [252,180,180],
    [236,176,224],
    [212,176,252],
    [188,180,252],
    [164,184,252],
    [164,200,252],
    [164,224,252],
    [164,252,212],
    [184,252,184],
    [200,252,164],
    [224,236,156],
    [252,224,140]
  ],
  'appleii' : [
    [0,0,0],
    [108,41,64],
    [64,53,120],
    [217,60,240],
    [19,87,64],
    [128,128,128],
    [38,151,240],
    [191,180,248],
    [64,75,7],
    [217,104,15],
    [236,168,191],
    [38,195,15],
    [191,202,135],
    [147,214,191],
    [255,255,255]
  ]
}

def colorDiff(c1, c2):
  "Calculates difference betwixt two colors"
  return math.sqrt(((c1[0] - c2[0])**2) + ((c1[1] - c2[1])**2) + ((c1[2] - c2[2])**2))

def averagePixel(data):
  "Takes a list of pixel data tuples -- (r,g,b,a) -- and finds average "
  numPixels = len(data)
  r,g,b,a = 0,0,0,0
  for i in range(numPixels):
    r += data[i][0]
    g += data[i][1]
    b += data[i][2]
    a += data[i][3]
  return (int(round(r/numPixels)),
      int(round(g/numPixels)),
      int(round(b/numPixels)),
      int(round(a/numPixels)))

def getClosestColor(color, palette):
  "Find the closest color in the current palette. TODO: optimize!"
  minDelta = 255*3
  closestColor = (0,0,0)
  for c in palette:
    delta = colorDiff(color, c)
    if delta < minDelta:
      minDelta = delta
      closestColor = c
  # preserve the alpha value from the original color, and convert list to tuple
  return (closestColor[0], closestColor[1], closestColor[2], color[3])

def phixelate(img, palette, blockSize):
  "initiate conversion"
  width, height = img.size
  rgb = img.load()
  blockWidth = int(math.ceil(width / blockSize))
  blockHeight = int(math.ceil(height / blockSize))
  for x in range(blockWidth):
    xOffset = x * blockSize
    for y in range(blockHeight):
      yOffset = y * blockSize
      container = []
      for xi in range(blockSize):
        for yi in range(blockSize):
          if (xi + xOffset) < width and (yi + yOffset) < height:
            container.append(rgb[xi+xOffset,yi+yOffset])
      color = averagePixel(container)
      if palette: color = getClosestColor(color, palette)
      # TODO: make averagePixel and getClosestColor update rgb by ref
      # so that we don't have to loop again
      for xi in range(blockSize):
        for yi in range(blockSize):
          if (xi + xOffset) < width and (yi + yOffset) < height:
            rgb[xi+xOffset,yi+yOffset] = color
      # processBlock(x + (x * blockWidth), y + (y * blockHeight), width, height, blockSize)

if __name__=="__main__":
  parse = argparse.ArgumentParser( \
      description='Create "pixel art" from a photo', prog='phixel', \
      epilog="Disclaimer: this does not *really* make pixel art, it just reduces the image resolution with preset color palettes.")
  parse.add_argument('-b', '--block', type=int, default=8, \
      help="Block size for phixelization.")
  parse.add_argument('-p', '--palette', choices=['mario','flashman','zelda','kungfu','tetris','contra'], \
      help="The color palette to use.")
  parse.add_argument('-c', '--custom', type=argparse.FileType('r'), \
      help="A custom palette file to use instead of the defaults.")
  # parse.add_argument('-d', '--dimensions', \
  #     help="The dimensions of the new image (format: /\d+x\d+/i)")
  parse.add_argument('-t', '--type', choices=['png','jpg','gif','bmp'], default='png', \
      help="Output file type.")
  # parse.add_argument('-l', '--no-lock', metavar="nolock", help="Don't preserve image ratio when resizing.")
  parse.add_argument('infile', nargs='?', type=argparse.FileType('rb'), default=sys.stdin, \
      help="the input file (defaults to stdin)")
  parse.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, \
      help="the output file (defaults to stdout)")
  args = parse.parse_args()

  """ Try to load the custom palette if provided:
      Should be formatted as json similar to the
      default palette definitions in this script. """
  palette = False
  if args.custom is not None:
    palette = json.loads(args.custom.read())
    args.custom.close()
  elif args.palette is not None: 
    palette = PALETTES[args.palette]

  img = Image.open(args.infile).convert('RGBA')
  phixelate(img, palette, args.block)

  img.save(args.outfile, args.type)
  args.infile.close()
  args.outfile.close()
  sys.exit(0)
