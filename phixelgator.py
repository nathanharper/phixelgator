#!/usr/bin/env python
import os, sys, argparse, math, json
from PIL import Image

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

if __name__=="__main__":
  parse = argparse.ArgumentParser( \
      description='Create "pixel art" from a photo', prog='phixel', \
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
      help="The dimensions of the new image (format: /\d+x\d+/)")
  parse.add_argument('-t', '--type', choices=['png','jpeg','gif','bmp'], default='png', \
      help="Output file type.")
  # parse.add_argument('-l', '--no-lock', metavar="nolock", help="Don't preserve image ratio when resizing.")
  parse.add_argument('infile', nargs='?', type=argparse.FileType('rb'), default=sys.stdin, \
      help="the input file (defaults to stdin)")
  parse.add_argument('outfile', nargs='?', type=argparse.FileType('wb'), default=sys.stdout, \
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
    try:
      with open('palettes/' + args.palette + '.json', 'r') as f:
        palette = json.loads(f.read())
    except Exception, e:
      sys.stderr.write("No palette loaded: " + e)
      palette = False

  img = Image.open(args.infile).convert('RGBA')
  phixelate(img, palette, args.block)

  if args.dimensions:
    try:
      imgWidth, imgHeight = map(int, args.dimensions.split('x', 1))
      resized_img = img.resize((imgWidth, imgHeight))
      resized_img.save(args.outfile, args.type)
    except Exception, e:
      sys.stderr.write("Failed to resize image: " + e)
      img.save(args.outfile, args.type)
  else:
    img.save(args.outfile, args.type)

  args.infile.close()
  args.outfile.close()
  sys.exit(0)
