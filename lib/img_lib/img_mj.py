import cv2
import os
import math

#問題を切り取るプログラム
def img_cut(src_dir , dst_dir, dst_file_name):
    img_no = 1
    file_list = os.listdir( src_dir )
    # file_list.sort()
    for f in file_list:
        img = cv2.imread(src_dir+"/%s"%f)
        print( src_dir+"/%s"%f)

        #img = cv2.resize(img,(920,1300))
        img = img[200:3800,200:2650]
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
        keypoints = noize_cut(keypoints,60,60, 3 )

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
            if dy > 230:
                interval.append((math.floor(spt), math.floor(old_y)))
                spt = y
            old_y = y

        if old_y - spt > 150:
            interval.append((math.floor(spt), math.floor(old_y)))

        for m in interval:
            print( m )

        out = img

        #特徴をマークする
        #out = cv2.drawKeypoints(img2,keypoints,None)

        for dect in interval:
            #out = cv2.rectangle(out,(min_x, y1 ),(max_x, dect[0]),(0,0,0),2)
            path = dst_dir+"/%s"
            if img_no < 10:
                path = path%"%s0%s.png"%(dst_file_name,img_no)
            else:
                path = path % "%s%s.png"%(dst_file_name,img_no)

            print( path )

            #ファイルを保存する
            cv2.imwrite(path,out[dect[0]-15:dect[1]+15,min_x-15:max_x+15])
            img_no = img_no + 1

# m[]内のxとyの個数を数える
def check( m , x ,y ):
    i = 0
    while i < len( m ):
        list = m[i]
        if list[0] == x and list[1] == y:
            return i
        i = i + 1
    return -1

# x_size , y_sizeの範囲にkeyがpower以上あるか調べる
def noize_cut( keypoints ,x_size , y_size ,power ):
    maplist = []
    # [ [ x , y , [ key ]] , [ x, y , [ key ,key ] ]
    for key in keypoints:
        x = math.floor( key.pt[0] / x_size)
        y = math.floor( key.pt[1] / y_size)

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

if __name__ == "__main__":
    img_cut("../image/png","../image/img_out")
