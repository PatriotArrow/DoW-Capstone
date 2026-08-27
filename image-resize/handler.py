from PIL import Image
import io
import base64

def handle(event, context):
    image_data = base64.b64decode(event.body)

    img = Image.open(io.BytesIO(image_data))

    img = img.resize((2000, 2000))

    return f"Image resized: {img.width}x{img.height}"
