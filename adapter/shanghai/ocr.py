# coding=utf-8
import os
import random
from PIL import Image

src = "./codes/"
dest = "./"
out = "./out/"

size = {"w":10, "h":10}
position = ({"x":0, "y":0}, {"x":10, "y":0}, {"x":20, "y":0}, {"x":30, "y":0})

def build():
    for f in os.listdir(src):
        img = Image.open(src + f)
        img = img.convert("RGBA")
        img.save(out + '_' + f, "JPEG", quality = 100)
        pixdata = img.load()

        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x, y][0] < 90:
                    pixdata[x, y] = (0, 0, 0, 255)
        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x, y][1] < 90:
                    pixdata[x, y] = (0, 0, 0, 255)
        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x, y][2] > 0:
                    pixdata[x, y] = (255, 255, 255, 255)

        img.save(out + f, "JPEG", quality = 100)

        for i in xrange(len(position)):
          digital = img.crop((position[i]["x"], position[i]["y"],\
              position[i]["x"]+size["w"], position[i]["y"]+size["h"]))
          digital.save(out + f.split('.')[0] + "_" + str(i) + '.jpg', "JPEG",
                  quality = 100)

def convert(img):
    img = img.convert("RGBA")
    pixdata = img.load()

    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][0] < 90:
                pixdata[x, y] = (0, 0, 0, 255)
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][1] < 90:
                pixdata[x, y] = (0, 0, 0, 255)
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][2] > 0:
                pixdata[x, y] = (255, 255, 255, 255)

    digitals = []
    for i in xrange(len(position)):
        digital = img.crop((position[i]["x"], position[i]["y"],\
                position[i]["x"]+size["w"], position[i]["y"]+size["h"]))
        digitals.append(digital)
    return digitals

def get_fonts():
    fonts_name = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    fonts = []
    for f in fonts_name:
        img = Image.open(dest + 'fonts/' + f + ".jpg")
        img = img.convert("RGBA")
        fonts.append(img)
    return fonts

fonts = get_fonts()

def read(fp):
    img = Image.open(fp)
    digitals = convert(img)
    chars = []
    for digital in digitals:
        diffs = []
        for i in xrange(len(fonts)):
            row_diffs = []
            for x in xrange(digital.size[1]):
                diff = 0
                for y in xrange(digital.size[0]):
                    if digital.getpixel((x,y)) != fonts[i].getpixel((x,y)):
                        diff += 1
                row_diffs.append(diff)
            diffs.append(row_diffs)

        min_diffs = []
        for m in xrange(len(diffs[0])):
            min_diff = None
            for n in xrange(10):
                if min_diff is None:
                    min_diff = dict(val=diffs[n][m],idx=[n])
                else:
                    if min_diff['val'] == diffs[n][m]:
                        min_diff['idx'].append(n)
                    if min_diff['val'] > diffs[n][m]:
                        min_diff = dict(val=diffs[n][m],idx=[n])
            min_diffs = min_diffs + min_diff['idx']
        counter = {}
        for pos in min_diffs:
            if counter.get(str(pos), None) is None:
                counter[str(pos)] = 0
            else:
                counter[str(pos)] = counter[str(pos)] + 1
        min_item = None
        for k,v in counter.items():
            if min_item is None:
                min_item = dict(k=k,v=v)
            elif min_item['v'] < v:
                min_item = dict(k=k,v=v)
        chars.append(min_item['k'])
    return "".join(chars)

def test():
  for f in os.listdir(src):
    code = read(src + f)
    print code
    os.rename(src + f, src + code + "_%s" % random.randrange(10000)  + ".jpg")

if __name__ == "__main__":
  test()
