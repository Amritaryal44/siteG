from PIL import Image, ImageSequence

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

