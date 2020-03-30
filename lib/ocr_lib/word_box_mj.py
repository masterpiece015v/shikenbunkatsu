import pyocr
import pyocr.builders
import cv2
import sys
from PIL import Image

def get_word_box(src_file_path):
    tools = pyocr.get_available_tools()
    if len( tools ) == 0:
        print("No OCR tool found")
        sys.exeit(1)
    tool = tools[0]
    res = tool.image_to_string(Image.open(src_file_path),lang="jpn",builder=pyocr.builders.WordBoxBuilder(tesseract_layout=1))
    #res = tool.image_to_string(Image.open(src_file_path),lang="jpn",builder=pyocr.builders.TextBuilder(tesseract_layout=6))
    #res = tool.image_to_string(Image.open(src_file_path),lang="jpn",builder=pyocr.builders.BaseBuilder())
    print( res )
    return res

if __name__ == "__main__":
    src_file_path = "../image/fe/h21a/h21a03.png"
    res = get_word_box(src_file_path)
    out = cv2.imread(src_file_path)
    for d in res:
        print( d.content )
        print( d.position )
        cv2.rectangle(out,d.position[0],d.position[1],(0,0,255),2)

    cv2.imshow('image',out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
