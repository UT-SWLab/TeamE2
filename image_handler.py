import os

class ImageHandler(object):
    # Default file image
    NO_IMG = 'images/no_img.png'

    def build_image_path(self,objectRef):
        img_path = f'images/constructors/{objectRef}.png'
        if not os.path.exists(f'./static/{img_path}'):
            img_path = NO_IMG
        return img_path