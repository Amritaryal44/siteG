from PIL import Image, ImageSequence
from pilkit.processors import ProcessorPipeline, ResizeToFit, SmartResize
import os

class HandleImage:
    def load(image):
        img = Image.open(image)
        if not img.format == 'GIF':
            if img.mode in ("RGBA", "P"): 
                img = img.convert("RGB")
        return img

    def save(image, save_as):
        if not image.format == 'GIF':
            image.save(save_as)
        else:
            if save_as.endswith(".gif"):
                HandleImage._save_animated(image, save_as)

    def reduce_size(image):
        if not image.format == 'GIF':
            w, h = image.size
            newSize = image.size
            ar = w/h
            if w>3000 or h>3000:
                if w>h:
                    nw = 3000
                    nh = int(nw/ar)
                    newSize = (nw, nh)
                else:
                    nw = 3000
                    nh = int(nw/ar)
                    newSize = (nw, nh)
                return image.resize(newSize)
            else:
                return image
        else:
            return image

    def _save_animated(image, save_as):
        frames = ImageSequence.Iterator(image)
        newFrames = []
        for frame in frames:
            thumbnail = frame.copy()
            newFrames.append(thumbnail)
        newImage = newFrames[0]
        newImage.info = image.info
        newImage.save(save_as, save_all=True, append_images=newFrames, loop=0)

    def faviconGenerator(originalImage, save_to):
        index = 0

        sizes = [
        #
        #	FileName		LogoSize		BoxSize
        #
            ["favicon-32",		[32,32],		[32,32]],
            ["favicon-57",		[57,57],		[57,57]],
            ["favicon-76",		[76,76],		[76,76]],
            ["favicon-96",		[96,96],		[96,96]],
            ["favicon-120",		[120,120],		[120,120]],
            ["favicon-128",		[128,128],		[128,128]],
            ["smalltile",		[128,128],		[128,128]],
            ["favicon-144",		[144,144],		[144,144]],
            ["favicon-152",		[152,152],		[152,152]],
            ["favicon-180",		[180,180],		[180,180]],
            ["favicon-196",		[196,196],		[196,196]],
            ["favicon-228",		[228,228],		[228,228]],
            ["mediumtile",		[270,270],		[270,270]],
            ["widetile",		[270,270],		[558,270]],
            ["largetile",		[558,558],		[558,558]],
        ]

        outfile = os.path.splitext(originalImage)[0] + ".png"

        for size in sizes:
            im = Image.open(originalImage)
            processor = ProcessorPipeline([ResizeToFit(size[1][0], size[1][1])])
            result = processor.process(im)
            background = Image.new('RGBA', size[2], (255, 255, 255, 0))
            background.paste(
                result, (int((size[2][0] - result.size[0]) / 2), int((size[2][1] - result.size[1]) / 2))
            )
            background.save(os.path.normpath(save_to + "/" + size[0] + ".png"))
            print("{}.png generated".format(size[0]))

