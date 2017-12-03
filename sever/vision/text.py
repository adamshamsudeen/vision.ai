import io
from google.cloud import vision
# from malayalam import mallu

def get_text(filename):

        vision_client = vision.Client()
        file_name = 'images/'+filename

        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
            image = vision_client.image(
                content=content, )

        text=image.detect_full_text().text
        return(text)