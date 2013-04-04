#!/usr/bin/env python
import sys, argparse, math, json, os
from PIL import Image

def getHex(color):
  "Get color hex value from rgb (or rgba)"
  return ''.join(map(lambda t: hex(t).split('x',1)[1], color[:3]))

def colorDiff(c1, c2):
  "Calculates difference betwixt two colors: Euclidean Distance"
  return math.sqrt(((c1[0] - c2[0])**2) + ((c1[1] - c2[1])**2) + ((c1[2] - c2[2])**2))

def averagePixel(data):
  "Takes a list of pixel data tuples -- (r,g,b,a) -- and finds average. one-liners are fucken sweet!"
  return tuple(map(lambda x: int(round(sum(x) / len(data))), zip(*data)))

def getClosestColor(color, palette, hexdict):
  "Find the closest color in the current palette. TODO: optimize!"
  hexval = getHex(color)
  if hexval not in hexdict:
    r,g,b = min(palette, key=lambda c: colorDiff(color, c))
    hexdict[hexval] = [r,g,b]
  else:
    r,g,b = hexdict[hexval]
  return (r,g,b,color[3]) # maintain original alpha channel

def phixelate(img, palette, blockSize):
  "Takes a PIL image object, a palette, and a block-size and alters colors in-place. no return val."
  width, height = img.size
  rgb = img.load()
  blockWidth = int(math.ceil(width / blockSize))
  blockHeight = int(math.ceil(height / blockSize))
  hexdict = {} # store "closest" colors to avoid repeat computations.
  for x in range(blockWidth):
    xOffset = x * blockSize
    for y in range(blockHeight):
      yOffset = y * blockSize
      container = []
      for xi in range(blockSize):
        if (xi + xOffset) >= width: break
        for yi in range(blockSize):
          if (yi + yOffset) >= height: break
          container.append(rgb[xi+xOffset,yi+yOffset])

      color = averagePixel(container)
      if palette: color = getClosestColor(color, palette, hexdict)

      for xi in range(blockSize):
        if (xi + xOffset) >= width: break
        for yi in range(blockSize):
          if (yi + yOffset) >= height: break
          rgb[xi+xOffset,yi+yOffset] = color

def generatePalette(img):
  "Generate a palette json file from an image. Image should NOT have an alpha value!"
  rgb = img.load()
  width,height = img.size
  return json.dumps(map(lambda (_,(r,g,b)): [r,g,b], img.getcolors(width*height)))

def exitScript(args, code):
  args.infile.close()
  args.outfile.close()
  sys.exit(code)

if __name__=="__main__":
  parse = argparse.ArgumentParser( \
      description='Create "pixel art" from a photo', prog='phixelgator', \
      epilog="Disclaimer: this does not *really* make pixel art, it just reduces the image resolution with preset color palettes.")
  parse.add_argument('-b', '--block', type=int, default=8, \
      help="Block size for phixelization. Default is 8 pixels.")
  parse.add_argument('-p', '--palette', \
      choices=['mario','flashman','hyrule','kungfu','tetris','contra','appleii', \
      'atari2600','commodore64','gameboy','grayscale','intellivision','nes','sega'], \
      help="The color palette to use.")
  parse.add_argument('-c', '--custom', type=argparse.FileType('r'), \
      help="A custom palette file to use instead of the defaults. Should be plain JSON file with a single array of color triplets.")
  parse.add_argument('-d', '--dimensions', \
      help="The dimensions of the new image (format: 10x10)")
  parse.add_argument('-t', '--type', choices=['png','jpeg','gif','bmp'], default='png', \
      help="Output file type.")
  parse.add_argument('-x', '--crop', choices=['tl','tr','bl','br'], \
      help="If this flag is set, the image will be cropped to conform to the Block Size. \
      The argument passed describes what corner to crop from.")
  parse.add_argument('-g', '--generate', action='store_true', \
      help="This flag overrides the default behaviour of infile and outfile options -- instead \
      of converting the input to a new image, a custom palette file will be generated from all colors \
      used in the infile photo. Other options are ignored.")
  parse.add_argument('infile', nargs='?', type=argparse.FileType('rb'), default=sys.stdin, \
      help="the input file (defaults to stdin)")
  parse.add_argument('outfile', nargs='?', type=argparse.FileType('wb'), default=sys.stdout, \
      help="the output file (defaults to stdout)")
  args = parse.parse_args()

  """ If the -g flag is set, the behaviour of the utility is
      completely altered -- instead of generating a new image,
      a new color-palette json file is generated from the colors
      of the input file. """
  if args.generate is True:
    img = Image.open(args.infile).convert('RGB')
    palette = generatePalette(img)
    args.outfile.write(palette)
    exitScript(args, 0)

  """ Try to load the custom palette if provided:
      Should be formatted as json similar to the
      default palette definitions in this script. """
  palette = False
  if args.custom is not None:
    palette = json.loads(args.custom.read())
    args.custom.close()
  elif args.palette is not None: 
    try:
      path = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'palettes' + os.sep
      with open(path + args.palette + '.json', 'r') as f:
        palette = json.loads(f.read())
    except Exception, e:
      sys.stderr.write("No palette loaded")
      palette = False

  img = Image.open(args.infile).convert('RGBA')

  """ Crop the image so that it fits the block size evenly """
  if args.crop:
    width,height = img.size
    newWidth = math.floor(width / args.block) * args.block
    newHeight = math.floor(height / args.block) * args.block
    if 'tl' == args.crop: img = img.crop((0,0,newWidth,newHeight))
    elif 'tr' == args.crop: img = img.crop((width-newWidth,0,width,newHeight))
    elif 'bl' == args.crop: img = img.crop((0,height-newHeight,newWidth,height))
    elif 'br' == args.crop: img = img.crop((width-newWidth,height-newHeight,width,height))

  phixelate(img, palette, args.block)

  """ Try to resize the image and fail gracefully """
  if args.dimensions:
    try:
      imgWidth, imgHeight = map(int, args.dimensions.split('x',1))
      resized_img = img.resize((imgWidth, imgHeight))
      resized_img.save(args.outfile, args.type)
    except Exception, e:
      sys.stderr.write("Failed to resize image")
      img.save(args.outfile, args.type)
  else:
    img.save(args.outfile, args.type)

  exitScript(args, 0)
