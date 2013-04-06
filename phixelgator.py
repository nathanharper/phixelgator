#!/usr/bin/env python
from __future__ import division # this lets us get decimal results from the '/' operator.
import sys, argparse, math, json, os, colorsys
from PIL import Image

def getHex(color, mode='rgb'):
  "Get color hex value from rgb (or rgba)"
  if 'hsv' == mode:
    rgb = colorsys.hsv_to_rgb(*(color[:3]))
  elif 'hls' == mode:
    rgb = colorsys.hls_to_rgb(*(color[:3]))
  else:
    rgb = color[:3]
  return ''.join(map(lambda t: hex(int(t)).split('x',1)[1], rgb))

def colorDiff(c1, c2):
  "Calculates difference betwixt two colors."
  return sum(map(lambda (x,y): abs(x-y), zip(c1[:3],c2[:3])))

def colorDiffWheighted(c1, c2, mode='hsv'):
  "HSV and HLS should have different weights... TODO: decide what they are :P"
  diff_pix = map(lambda (x,y): abs(x-y), zip(c1[:3],c2[:3]))
  return diff_pix[0] + diff_pix[1] + diff_pix[2]

def averagePixel(data, mode='rgb'):
  "Takes a list of pixel data tuples and finds average."
  if 'rgb' == mode:
    return map(lambda x: int(round(sum(x) / len(data))), zip(*data)[:3])
  else:
    return map(lambda x: sum(x) / len(data), zip(*data)[:3])

def getClosestColor(color, palette, hexdict, mode='rgb'):
  "Find the closest color in the current palette. TODO: optimize!"
  hexval = getHex(color, mode)
  if hexval not in hexdict:
    if mode != 'rgb': diff_func = colorDiffWheighted
    else: diff_func = colorDiff
    hexdict[hexval] = min(palette, key=lambda c: diff_func(color, c))
  return list(hexdict[hexval]) # "list" looks redundant, but we want a *copy* of the color

""" TODO: There's probably a more efficient way to convert rgb => hsv and hls,
    perhaps with numpy """
def phixelate(img, palette, blockSize, mode='rgb'):
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

      container = [] # represents one monochrome "block" of the image
      for xi in range(blockSize):
        if (xi + xOffset) >= width: break
        for yi in range(blockSize):
          if (yi + yOffset) >= height: break
          container.append(rgb[xi+xOffset,yi+yOffset])

      # alpha isn't used in finding the color so just pop it off for later
      avg_alpha = int(round(sum(zip(*container)[3]) / len(container)))

      """ TODO: store converted RGB values to prevent duplicate
          calls to colorsys """
      if 'hsv' == mode:
        container = map(lambda co: colorsys.rgb_to_hsv(*(co[:3])), container)
      if 'hls' == mode:
        container = map(lambda co: colorsys.rgb_to_hls(*(co[:3])), container)

      # Convert a block to one color -- take the average, and find closest palette color
      color = averagePixel(container, mode)
      if palette: color = getClosestColor(color, palette, hexdict, mode)

      # Convert back to rgb if we're in hsv or hls mode
      if 'hsv' == mode:
        color = list(colorsys.hsv_to_rgb(*color))
      if 'hls' == mode:
        color = list(colorsys.hls_to_rgb(*color))

      # stick alpha channel back on and convert to tuple
      color.append(avg_alpha)
      color = tuple(map(lambda co: int(round(co)), color))

      for xi in range(blockSize):
        if (xi + xOffset) >= width: break
        for yi in range(blockSize):
          if (yi + yOffset) >= height: break
          rgb[xi+xOffset,yi+yOffset] = color

def generatePalette(img, mode='rgb'):
  "Generate a palette json file from an image. Image should NOT have an alpha value!"
  if 'hsv' == mode:
    transform = lambda (_,rgb): list(colorsys.rgb_to_hsv(*rgb))
  elif 'hls' == mode:
    transform = lambda (_,rgb): list(colorsys.rgb_to_hls(*rgb))
  else:
    transform = lambda (_,rgb): list(rgb)
  return json.dumps(map(transform, img.getcolors(img.size[0]*img.size[1])))

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
      choices=['mario','hyrule','kungfu','tetris','contra','appleii', \
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
  parse.add_argument('-m', '--mode', choices=['rgb','hsv','hls'], default='rgb', \
      help="The color mode to use. hsv or hls may produce more desirable results than the default rgb \
      but the process will take longer.")
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
    # To simplify things, the custom palette generator only makes rgb files,
    # so it's fairly safe to assume that's what we're getting.
    if 'hsv' == args.mode:
      palette = map(lambda rgb: colorsys.rgb_to_hsv(*rgb), palette)
    elif 'hls' == args.mode:
      palette = map(lambda rgb: colorsys.rgb_to_hls(*rgb), palette)
  elif args.palette is not None: 
    try:
      path = os.sep.join([os.path.dirname(os.path.realpath(__file__)),'palettes',args.mode,args.palette])
      with open(path + '.json', 'r') as f:
        palette = json.loads(f.read())
    except Exception, e:
      sys.stderr.write("No palette loaded")
      palette = False

  img = Image.open(args.infile).convert('RGBA')

  """ Crop the image so that it fits the block size evenly """
  if args.crop:
    width,height = img.size
    newWidth = int(math.floor(width / args.block) * args.block)
    newHeight = int(math.floor(height / args.block) * args.block)
    if 'tl' == args.crop: cropsize = (0,0,newWidth,newHeight)
    elif 'tr' == args.crop: cropsize = (width-newWidth,0,width,newHeight)
    elif 'bl' == args.crop: cropsize = (0,height-newHeight,newWidth,height)
    elif 'br' == args.crop: cropsize = (width-newWidth,height-newHeight,width,height)
    img = img.crop(cropsize)

  phixelate(img, palette, args.block, args.mode)

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
