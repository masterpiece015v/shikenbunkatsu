#問題を切り取るプログラム
import cv2
import math
import numpy as np
from PIL import Image
import os ,pyocr , pyocr.builders , sys
import csv

#pilで読込cv2に吐き出す
def pilread(file_path):
    img = Image.open( file_path )
    return np.asarray( img )

#numpyで渡して画像保存する。
def pilwrite( numpy_image , file_path ):
    img = Image.fromarray(np.uint8(numpy_image))
    img.save( file_path )

# img_in( directory path) , img_out( directory path )  , file_name 'feh29h'
def cut_mondai(img_in , img_out , file_name , freq=2 ):
    img_no = 1
    for f in os.listdir( img_in ):
        #img = cv2.imread()
        img = pilread( "%s/%s"%(img_in,f) )
        img = cv2.resize(img,(920,1300))
        img = img[20:1220,20:900]
        #サイズを変更する
        img2 = img

        #img2を2値化
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        thresh = 100
        max_pixel = 250
        ret, img2 = cv2.threshold(img2, thresh, max_pixel, cv2.THRESH_BINARY)

        #特徴量を取得する
        #detector = cv2.ORB_create()
        detector = cv2.AgastFeatureDetector_create()
        #detector = cv2.FastFeatureDetector_create()

        #特徴量のkeyを取得する
        keypoints = detector.detect(img2)

        #ノイズを消去する
        keypoints = noize_cut(keypoints,900,1280, freq )

        #x,yの配列
        px = []
        py = []
        for key in keypoints:
            px.append( key.pt[0])
            py.append( key.pt[1] )

        #xの最小値と最大値を取得
        max_x = math.floor( max(px) )
        min_x = math.floor( min(px) )

        #keyの高さの間隔を取得
        interval = []
        spt = py[0]
        old_y = py[0]
        for y in py:
            dy = y - old_y
            if dy > 80:
                interval.append((math.floor(spt), math.floor(old_y)))
                spt = y
            old_y = y

        if old_y - spt > 50:
            interval.append((math.floor(spt), math.floor(old_y)))

        for m in interval:
            print( m )

        out = img

        #特徴をマークする
        #out = cv2.drawKeypoints(img2,keypoints,None)

        for dect in interval:
            #out = cv2.rectangle(out,(min_x, y1 ),(max_x, dect[0]),(0,0,0),2)
            path = img_out+"/%s"
            if img_no < 10:
                path = path%"%s0%s.png"%(file_name,img_no)
            else:
                path = path % "%s%s.png"%(file_name,img_no)

            #ファイルを保存する
            # cv2.imwrite(path,out[dect[0]-15:dect[1]+15,min_x-15:max_x+15])
            pilwrite(out[dect[0]-15:dect[1]+15,min_x-15:max_x+15],path)
            img_no = img_no + 1

        print( str(img_no - 1) + "問")

# img_in( directory path) , img_out( directory path )  , file_name 'feh29h'
def cut_mondai_bk(img_in , img_out , file_name , freq=2 ):
    img_no = 1
    toi1 = pilread("marker\\toi1.png")
    toi2 = pilread("marker\\toi2.png")
    toi3 = pilread("marker\\toi3.png")
    toi4 = pilread("marker\\toi4.png")
    toi5 = pilread("marker\\toi5.png")
    dai1mon = pilread("marker\\dai1mon.png")
    toi_list =[toi1,toi2,toi3,toi4,toi5]

    #どのページにどの第●問が含まれるかチェックする
    page_cnt = 1
    dai_dict = {}
    check_dict ={'第1問':['第1問','第1間'],'第2問':['第2問','第2間'],'第3問':['第3問','第3間'],'第4問':['第4問','第4間'],'第5問':['第5問','第5間']}
    for f in os.listdir( img_in ):
        text1 = get_text_ocr("%s/%s"%(img_in,f),50,50,250,1200)
        text2 = get_text_ocr("%s/%s"%(img_in,f),1290,50,1490,1200)
        print( text1 )
        print( text2 )
        for key in check_dict.keys():
            if check_dict[key][0] in text1 or check_dict[key][1] in text1:
                dai_dict[(page_cnt-1)*2+1] = key
            if check_dict[key][0] in text2 or check_dict[key][1] in text2:
                dai_dict[(page_cnt-1)*2+2] = key
        page_cnt = page_cnt + 1
        if page_cnt > 4:
            break

    # 問題を切り取る
    page = 1
    for f in os.listdir( img_in ):
        print( os.path.join(img_in,f) )
        #img_s = cv2.imread(os.path.join(img_in,f))
        img_s = pilread( os.path.join(img_in,f) )
        img_s1 = img_s[50:1700,50:1190]
        img_s2 = img_s[50:1700,1290:2430]

        img_list = [ img_s1 , img_s2 ]
        for img in img_list:
            if page in dai_dict.keys():
                daimon = dai_dict[page]
                # 第1問の時
                if daimon == "第1問":
                    toi_cnt = 0
                    log0,max_val0 = cv2MatchTemplate(img,dai1mon,0.8)
                    min_y0 = min(log0[0])

                    while toi_cnt < len(toi_list):
                        log1, max_val1 = cv2MatchTemplate(img, toi_list[toi_cnt],0.8)
                        print( log1 )
                        #print( max_val1 )
                        min_x = min(log1[1])
                        min_y = min(log1[0])
                        #if toi_cnt == 0:
                        #    f_min_y = min_y

                        if toi_cnt < len(toi_list) - 1:
                            log2, max_val2 = cv2MatchTemplate(img, toi_list[toi_cnt + 1],0.8)
                            # 1～4まで
                            max_x = min(log2[1])
                            max_y = min(log2[0])
                            filename = "%s\\%s%s.png" % (img_out, file_name, "_1_%s" % str(toi_cnt + 1))
                            #cv2.imwrite(filename, img[min_y:max_y, min_x:img.shape[1]])
                            pilwrite( img[min_y:max_y, min_x:img.shape[1]],filename )
                            if toi_cnt == 0:
                                #許容勘定科目
                                filename = "%s\\%s%s.png" % (img_out,file_name,"_1_0")
                                # cv2.imwrite(filename,img[min_y0+150:min_y, min_x:img.shape[1]])
                                pilwrite( img[min_y0+150:min_y, min_x:img.shape[1]], filename )
                        else:
                            # 5
                            img_temp = img[min_y:img.shape[0], min_x:img.shape[1]]
                            img5, rect = tokucyou_cut(img_temp)
                            filename = "%s\\%s%s.png" % (img_out, file_name, "_1_%s" % str(toi_cnt + 1))
                            #cv2.imwrite(filename, img[min_y:min_y + rect[3] + 15, min_x:img.shape[1]])
                            pilwrite(img[min_y:min_y + rect[3] + 15, min_x:img.shape[1]],filename)
                        toi_cnt = toi_cnt + 1
                elif daimon == '第2問':
                    # 第2問の時
                    #showimage( img )
                    img2, rect = tokucyou_cut(img)
                    #showimage( img2 )
                    #print(rect)
                    if len(rect) > 0:
                        # showimage( img2 )
                        filename = "%s\\%s%s.png" % (img_out, file_name, "_2_1")
                        #cv2.imwrite(filename, img2)
                        pilwrite( img2 , filename )
                elif daimon == '第3問':
                    # 第3問の時
                    img2, rect = tokucyou_cut(img)
                    if len(rect) > 0:
                        # showimage( img2 )
                        filename = "%s\\%s%s.png" % (img_out, file_name, "_3_1")
                        # cv2.imwrite(filename, img2)
                        pilwrite( img2 , filename )
                elif daimon == '第4問':
                    # 第4問の時
                    img2, rect = tokucyou_cut(img)
                    if len(rect) > 0:
                        # showimage( img2 )
                        filename = "%s\\%s%s.png" % (img_out, file_name, "_4_1")
                        #cv2.imwrite(filename, img2)
                        pilwrite( img2 , filename )
                elif daimon == '第5問':
                    # 第5問の時
                    img2, rect = tokucyou_cut(img)
                    if len(rect) > 0:
                        # showimage( img2 )
                        filename = "%s\\%s%s.png" % (img_out, file_name, "_5_1")
                        # cv2.imwrite(filename, img2)
                        pilwrite( img2 , filename )
                else:
                    # 第問以外
                    img2, rect = tokucyou_cut(img)
                    if len(rect) > 0:
                        # showimage( img2 )
                        filename = "%s\\%s%s.png" % (img_out, file_name, "_3_2")
                        # cv2.imwrite(filename, img2)
                        pilwrite( img2 , filename )
                print( "%s:%s"%(page,daimon) )
            else:
                img2,rect = tokucyou_cut(img)
                print( len(rect) )
                if len( rect) >= 4 :
                    if len( file_name ) >= 6:
                        if page >= 10:
                            filename = "%s\\%s.png" % (img_out,"%s2%s%s"%(file_name[0:2],file_name[3:6],"00%s"%page))
                        else:
                            filename = "%s\\%s.png" % (img_out, "%s2%s%s" % (file_name[0:2], file_name[3:6],"000%s" % page))
                    else:
                        if page >= 10:
                            filename = "%s\\00%s.png"%(img_out,page)
                        else:
                            filename ="%s\\000%s.png"%(img_out,page)
                    # cv2.imwrite(filename, img[rect[2]-15:rect[3]+15 , rect[0]-15:rect[1]+15])
                    pilwrite(img[rect[2]-15:rect[3]+15 , rect[0]-15:rect[1]+15] ,filename )
                print("第問ではない。")
            page = page + 1

# img_in( directory path) , img_out( directory path )  , file_name 'feh29h'
def cut_mondai_hj(img_in , img_out , file_name , freq=2 ):
    #mondai = cv2.imread("marker\\mondai.png")
    mondai = pilread("marker\\mondai.png")
    # 問題を切り取る
    page = 1
    for f in os.listdir( img_in ):
        #img_s = cv2.imread("%s\\%s"%(img_in,f))
        img_s = pilread("%s\\%s"%(img_in,f))
        # [問題]の場所を見つける
        log, max_val = cv2MatchTemplate(img_s, mondai ,0.8)
        #print( log )
        #print( max_val )

        if len( log[1] ) > 0 and len( log[0] ) > 0:
            top_x = min(log[1])

            top_list_y = [ item for i,item in enumerate(log[0]) if i == 0 or i > 0 and log[0][i] - log[0][i-1] > 100 ]
            # [問題]から始まらない場合

            flg = 0
            if top_list_y[0] > 200:
                top_list_y.insert( 0 , 100)
                flg = 1

            print( top_list_y )

            img_list = []

            if len( top_list_y) == 1:
                img_list.append( img_s[top_list_y[0] - 10 :img_s.shape[0] - 30 ,top_x - 20 :img_s.shape[1]] )
            else:
                for i , item in enumerate( top_list_y ):
                    if len( top_list_y )-1 > i:
                        print( top_list_y[i+1] - 10 )
                        img_list.append( img_s[ item -10 :top_list_y[i+1] - 30 , top_x - 20 :img_s.shape[1] ])
                    else:
                        img_list.append(img_s[ item - 10 :img_s.shape[0] -30, top_x - 20 :img_s.shape[1]])

            for i,img in enumerate( img_list ):
                # 特徴量抽出
                img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                thresh = 100
                max_pixel = 250
                ret, img3 = cv2.threshold(img2, thresh, max_pixel, cv2.THRESH_BINARY)

                #特徴量を取得する
                #detector = cv2.ORB_create()
                detector = cv2.AgastFeatureDetector_create()
                #detector = cv2.FastFeatureDetector_create()

                #特徴量のkeyを取得する
                keypoints = detector.detect(img3)

                #ノイズを消去する
                keypoints = noize_cut(keypoints,img3.shape[1],img3.shape[0], freq )

                #x,yの配列
                px = []
                py = []
                for key in keypoints:
                    px.append( key.pt[0])
                    py.append( key.pt[1] )

                #xの最小値と最大値を取得
                max_x = math.floor( max(px) ) + 20
                min_x = math.floor( min(px) ) - 20
                max_y = math.floor( max(py) ) + 20
                min_y = math.floor( min(py) ) - 20

                # ファイルネーム
                if i == 0 and flg == 1:
                    filename = "%s\\%s%s.png" % (img_out, file_name, "010%s%s" % (str(page-1), str(1)))
                else:
                    filename = "%s\\%s%s.png" % (img_out, file_name, "010%s%s" % (str(page),str(0)))
                    page = page + 1

                #cv2.imwrite(filename, img[0:max_y , 0:max_x])
                pilwrite(img[0:max_y , 0:max_x],filename )
        else:
            # [問題]がない場合
            # 特徴量抽出
            img2 = cv2.cvtColor(img_s, cv2.COLOR_BGR2GRAY)
            thresh = 100
            max_pixel = 250
            ret, img3 = cv2.threshold(img2, thresh, max_pixel, cv2.THRESH_BINARY)

            # 特徴量を取得する
            # detector = cv2.ORB_create()
            detector = cv2.AgastFeatureDetector_create()
            # detector = cv2.FastFeatureDetector_create()

            # 特徴量のkeyを取得する
            keypoints = detector.detect(img3)

            # ノイズを消去する
            keypoints = noize_cut(keypoints, img3.shape[1], img3.shape[0], freq)

            # x,yの配列
            px = []
            py = []
            for key in keypoints:
                px.append(key.pt[0])
                py.append(key.pt[1])

            # xの最小値と最大値を取得
            max_x = math.floor(max(px)) + 20
            min_x = math.floor(min(px)) - 20
            max_y = math.floor(max(py)) + 20
            min_y = math.floor(min(py)) - 20
            filename = "%s\\%s%s.png" % (img_out, file_name, "010%s%s" % (str(page),str(1)))
            #cv2.imwrite( filename, img_s[min_y:max_y , min_x: max_x ] )
            pilwrite( img_s[min_y:max_y , min_x: max_x ] , filename )

# img_in( directory path) , img_out( directory path )  , file_name 'feh29h'
# 余白を削除するのみ
def cut_mondai_margin(img_in ,img_out, freq=2 ):
    for i,f in enumerate(os.listdir( img_in )):
        if ".png" in f:
            # img = cv2.imread("%s/%s"%(img_in,f))
            img = pilread( "%s/%s"%(img_in,f) )
            print("%s/%s"%(img_in,f))
            #showimage( img )
            # 特徴量抽出
            #img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            thresh = 100
            max_pixel = 250
            ret, img3 = cv2.threshold(img, thresh, max_pixel, cv2.THRESH_BINARY)

            #特徴量を取得する
            #detector = cv2.ORB_create()
            detector = cv2.AgastFeatureDetector_create()
            #detector = cv2.FastFeatureDetector_create()

            #特徴量のkeyを取得する
            keypoints = detector.detect(img3)

            #ノイズを消去する
            keypoints = noize_cut(keypoints,img3.shape[1],img3.shape[0], freq )

            #x,yの配列
            px = []
            py = []
            for key in keypoints:
                px.append( key.pt[0])
                py.append( key.pt[1] )

            #xの最小値と最大値を取得
            max_x = math.floor( max(px) ) + 20
            min_x = math.floor( min(px) ) - 20
            max_y = math.floor( max(py) ) + 20
            min_y = math.floor( min(py) ) - 20

            # ファイルネーム
            if i < 10:
                filename = "%s/%s.png" % (img_out, f[0:len(f)-4].replace("-","_") )
            else:
                filename = "%s/%s.png" % (img_out, f[0:len(f)-4].replace("-","_") )

            # cv2.imwrite(filename, img[min_y:max_y , min_x:max_x])
            pilwrite( img[min_y:max_y,min_x:max_x] , filename )
            # os.remove( "%s/%s"%(img_in,f) )

# 画像を2値化
def conv_binary(img):
    img_gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = 100
    max_pixel = 250
    ret, img_gry = cv2.threshold(img_gry, thresh, max_pixel, cv2.THRESH_BINARY)
    return img_gry

# 画像をグレーアウト
def conv_gray(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img_gray

#特徴量で切り取る
def tokucyou_cut(img , freq=2 ):
    # img1を2値化
    img_gry = conv_binary( img )
    # 特徴量を取得する
    # detector = cv2.ORB_create()
    detector = cv2.AgastFeatureDetector_create()
    # detector = cv2.FastFeatureDetector_create()

    # 特徴量のkeyを取得する
    kp = detector.detect(img_gry)
    # ノイズを消去する
    kp = noize_cut(kp, 1080, 1590, freq)

    # 特徴をマークする
    #out = cv2.drawKeypoints(img,kp,None)
    #cv2.imwrite("cut_image/t.png",out)
    #showimage(out)
    if len(kp) > 0:
        # x,yの配列
        px = []
        py = []
        for key in kp:
            px.append(key.pt[0])
            py.append(key.pt[1])

        # xの最小値と最大値を取得
        max_x = math.floor(max(px))
        min_x = math.floor(min(px))
        max_y = math.floor(max(py))
        min_y = math.floor(min(py))

        #showimage(img[min_y-15:max_y+15,min_x-15:max_x+15])
        rect = (min_x,max_x,min_y,max_y)
        return img[min_y-30:max_y+30,min_x-30:max_x+30],rect
    else:
        return img_gry,()

# 画像同士の類似度
def cv2MatchTemplate2(image , marker ):
    res = cv2.matchTemplate(image, marker, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
    #loc = np.where(res >= threshold)
    return {'minVal':minVal,'maxVal':maxVal,'minLoc':minLoc,'maxLoc':maxLoc}

# 画像同士の類似度
def cv2MatchTemplate(image , marker,threshold ):
    res = cv2.matchTemplate(image, marker, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
    loc = np.where(res >= threshold)
    return loc,maxVal

def check( m , x ,y ):
    i = 0
    while i < len( m ):
        list = m[i]
        if list[0] == x and list[1] == y:
            return i
        i = i + 1
    return -1

def noize_cut( keypoints ,x_size , y_size ,power ):
    maplist = []
    # [ [ x , y , [ key ]] , [ x, y , [ key ,key ] ]
    for key in keypoints:
        x = math.floor( key.pt[0] / 15)
        y = math.floor( key.pt[1] / 15)
        i = check( maplist,x,y)
        if i >= 0:
            maplist[i][2].append( key )
        else:
            list = []
            list.append(x)
            list.append(y)
            keys = []
            keys.append( key )
            list.append(keys)
            maplist.append(list)

    for list in maplist:
        if len(list[2]) < power:
            for key in list[2]:
                keypoints.remove( key )

    return keypoints

def showimage(img):
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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

def png_to_ocr( src_dir_name,des_dir_name,des_file_name):
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    tool = tools[0]

    for fileName in os.listdir( src_dir_name):
        im = Image.open( "%s/%s"%(src_dir_name,fileName ))

        res = tool.image_to_string(
            im,
            lang="jpn",
            builder=pyocr.builders.TextBuilder(tesseract_layout=6)
        )

        res = res.replace(" ","")
        res = res.replace("\n","")

        new_file_name = "%s/%s.csv"%(des_dir_name,des_file_name)

        with open(new_file_name,mode='a',newline='') as f:
            writer = csv.writer(f)
            writer.writerow([fileName[0:len(fileName)-4],res])

def main():
    cut_mondai_hj(img_in='C:\\Users\\mnt\\Desktop\\png',img_out='C:\\Users\\mnt\\Desktop\\png_cut',file_name='148')

if __name__ == '__main__':
    main()