from PIL import Image , ImageDraw
import numpy ,os ,pyocr , pyocr.builders , re , sys

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]

def get_text_ocr(src_file_name):

    #print("%s"%tool.get_name())

    #langs = tool.get_available_languages()
    #print("%s"%langs)

    res = tool.image_to_string(
        Image.open(src_file_name),
        lang="jpn",
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )

    #print( res )
    res = res.replace(" ","")
    res = res.replace("\n","")
    return res

if __name__ == "__main__":
    print( get_text_ocr("../png/2009h21h_fe_am_qs-4.jpg") )