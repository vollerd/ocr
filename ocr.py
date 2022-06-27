import io
from google.cloud import vision
from google.oauth2 import service_account
from pdf2image import convert_from_path
import os, time
from PIL import Image


# 身元証明書のjson読み込み
credentials = service_account.Credentials.from_service_account_file('key.json')
client = vision.ImageAnnotatorClient(credentials=credentials)
 
print("1")

pages = convert_from_path('in-501-599.pdf', 500)
count = 0
for page in pages:
    print("2")
    count += 1
    page.save('pyoutx.png','PNG')
    img = Image.open('pyoutx.png')
    print("3")
    img_resize_lanczos = img.resize((int(img.width * 1.5), int(img.height * 1.5)), Image.LANCZOS)
    img_resize_lanczos.save('pyout.png')
    time.sleep(10)
    # OCR対象の画像パス
    input_file = "pyout.png"
     
    with io.open(input_file, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
     
    # OCRした結果を表示
    print(response.full_text_annotation.text)
    os.remove("pyout.png")
    os.remove("pyoutx.png")

    text_file = open(f"data_{count+500}.txt", "w")
 
    #write string to file
    text_file.write(response.full_text_annotation.text)
    #close file
    text_file.close()