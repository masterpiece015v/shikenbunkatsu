#問題を切り取るプログラム
import cv2
import math
import os
import numpy as np

# img_in( directory path) , img_out( directory path )  , file_name 'feh29h'
def cut_mondai(img_in , img_out , file_name , freq=2 ):
    img_no = 1
    for f in os.listdir( img_in ):
        img = cv2.imread("%s/%s"%(img_in,f))
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
            cv2.imwrite(path,out[dect[0]-15:dect[1]+15,min_x-15:max_x+15])
            img_no = img_no + 1

        print( str(img_no - 1) + "問")

# img_in( directory path) , img_out( directory path )  , file_name 'feh29h'
def cut_mondai_bk(img_in , img_out , file_name , freq=2 ):
    img_no = 1
    toi1 = cv2.imread("marker\\toi1.png")
    toi2 = cv2.imread("marker\\toi2.png")
    toi3 = cv2.imread("marker\\toi3.png")
    toi4 = cv2.imread("marker\\toi4.png")
    toi5 = cv2.imread("marker\\toi5.png")
    toi_list =[toi1,toi2,toi3,toi4,toi5]

    dai1mon = cv2.imread("marker\\dai1mon.png")
    dai2mon = cv2.imread("marker\\dai2mon.png")
    dai3mon = cv2.imread("marker\\dai3mon.png")
    dai4mon = cv2.imread("marker\\dai4mon.png")
    dai5mon = cv2.imread("marker\\dai5mon.png")

    # 画像を切り取る
    page = 1
    for f in os.listdir( img_in ):
        img_s = cv2.imread("%s/%s"%(img_in,f))

        img_s1 = img_s[80:1670,80:1160]
        img_s2 = img_s[80:1670,1320:2400]

        img_list = [ img_s1 , img_s2 ]

        for img in img_list:
            # 第1問
            log,max_val = cv2MatchTemplate(img,dai1mon,0.9)
            if max_val > 0.9:
                # 第1問の時
                toi_cnt = 0
                while toi_cnt < len(toi_list):
                    log1,max_val1 = cv2MatchTemplate(img,toi_list[toi_cnt],0.8)
                    min_x = min(log1[1])
                    min_y = min(log1[0])
                    if toi_cnt < len(toi_list)-1:
                        log2,max_val2 = cv2MatchTemplate(img,toi_list[toi_cnt+1],0.8)
                        # 1～4まで
                        max_x = min(log2[1])
                        max_y = min(log2[0])
                        filename = "%s\\%s%s.png"%(img_out,file_name,"010%s"%str(toi_cnt+1))
                        cv2.imwrite(filename,img[min_y:max_y,min_x:img.shape[1] ])
                    else:
                        # 5
                        img_temp = img[min_y:img.shape[0], min_x:img.shape[1]]
                        img5,rect = tokucyou_cut( img_temp )
                        filename = "%s\\%s%s.png" % (img_out, file_name, "010%s" % str(toi_cnt + 1))
                        cv2.imwrite(filename, img[min_y:min_y+rect[3]+15,min_x:img.shape[1]] )
                    toi_cnt = toi_cnt + 1
            else:
                #第1問以外の時
                img2,rect = tokucyou_cut(img)
                if len(rect) > 0:
                    #showimage( img2 )
                    filename = "%s\\%s%s.png" % (img_out, file_name, "000%s" % str(page))
                    cv2.imwrite(filename, img2 )
            page = page + 1

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
        return img[min_y-15:max_y+15,min_x-15:max_x+15],rect
    else:
        return img_gry,()

# 画像同士の類似度
def cv2MatchTemplate(image , marker , threshold):
    res = cv2.matchTemplate(image, marker, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    loc = np.where(res >= threshold)
    return loc , max_val

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
