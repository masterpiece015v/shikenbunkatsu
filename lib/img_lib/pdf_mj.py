import os
import os.path
import fnmatch
import subprocess

def pdf_to_png(src_dir,dst_path):
    for dirpath,_,filenames in os.walk(src_dir):
        for filename in filenames:
            if fnmatch.fnmatch(filename,u"*.pdf"):
                org_path = os.path.join(dirpath,filename)

                #list =["magick",org_path,"-resize","2148x3039",png_path]
                for i in range(40):
                    f = ""
                    if i < 10:
                        f = "0" + str(i) + ".png"
                    else:
                        f = str(i) + ".png"

                    # 年度のフォルダを作成
                    png_path = os.path.join(dst_path,filename[4:8])
                    if os.path.exists(png_path)==False:
                        os.makedirs(png_path)

                    # 書き込み先のファイル名作成
                    png_path = os.path.join(png_path, filename.replace(".pdf", f))

                    print("convert {0} to {1}".format(org_path, png_path))

                    list = ["magick","convert","-density","400",org_path+"[%s]"%str(i),png_path]

                    if subprocess.call(list):
                        print("failed:{0}".format(org_path))
                        break


if __name__ == "__main__":
    pdf_to_png("../image/pdf","../image/png")

