import os

NO_IMG = 'images/no_img.png'

class ImageHandler(object):
    # Default file image
    def build_image_path(self,objectRef,objectType):
        img_path = f'images/{objectType}/{objectRef}.png'
        if not os.path.exists(f'./static/{img_path}'):
            img_path = NO_IMG
        return img_path