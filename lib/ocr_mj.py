from PIL import Image
import os ,pyocr , pyocr.builders , sys

def get_text_ocr(src_file_name,left,upper,right,lower):
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    tool = tools[0]

    im = Image.open(src_file_name)
    im = im.crop( ( left,upper ,right,lower) )
    res = tool.image_to_string(
        im,
        lang="jpn",
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )

    res = res.replace(" ","")
    res = res.replace("\n","")
    return res

if __name__ == "__main__":
    os.environ['PATH'] = "%s;%s"%(os.environ['PATH'],'C:/pythonproject/shikenbunkatsu/Tesseract-OCR')
    os.environ['TESSDATA_PREFIX'] = 'c:/pythonproject/shikenbunkatsu/Tesseract-OCR/tessdata'
    print( get_text_ocr("c:/pythonproject/shikenbunkatsu/image/148/148-1-conv.png" , 80 , 80 , 280 , 280) )
    print( get_text_ocr("c:/pythonproject/shikenbunkatsu/image/148/148-1-conv.png", 1320, 80, 1520, 280))
