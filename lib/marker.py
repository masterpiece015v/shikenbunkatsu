import os
import cv2
import numpy as np

STATIC_PATH = os.curdir()

def get_answer_list(filename):
    #マーカーの読み込み

    #django用設定
    #path = settings.BASE_DIR
    #ローカル実行用設定

    path = os.path.join( STATIC_PATH , "marker.png" )

    marker = cv2.imread(path, 0)

    #画像ファイルの読み込みとサイズ調整
    img = cv2.imread(filename, 0)
    img = cv2.resize(img, (2100, 2964))

    #img = cv2.resize(img, (1000, 1500))
    # markeと同じ画像の位置を取得する
    res_gaku = cv2.matchTemplate(img, marker, cv2.TM_CCOEFF_NORMED)
    threshold = 0.6
    loc = np.where(res_gaku >= threshold)
    x = min(loc[1])
    y = min(loc[0])
    mark_area = { 'x' : x , 'y' : y }
    mark_list =[]
    mark_list.append( mark_area )
    for pt in zip(*loc[::-1]):
        nx = pt[0]
        ny = pt[1]
        if y + 80 < ny:
            mark_area = {}
            mark_area['x'] = nx
            mark_area['y'] = ny
            mark_list.append( mark_area )
            y = ny

    #組織ID、テストID、ユーザIDを取得する
    img_info = img[mark_list[0]['y']-25: mark_list[0]['y']+140, mark_list[0]['x']+90: mark_list[0]['x']+1805]
    img_info = cv2.resize(img_info, (1400, 200))
    #imgshow( img_info )
    org_id = img_info[0:100, 348:695]
    test_id = img_info[0:100, 1050:1400]
    user_id = img_info[104:200, 348:695]
    org_id = cv2.resize(org_id,(350,100))
    test_id = cv2.resize(test_id,(350,100))
    user_id = cv2.resize(user_id,(350,100))

    ainum = Ainum()
    #白黒チェンジ
    res , org_id = bwchange( org_id )
    o_n = ""

    #imgshow( org_id )
    for c in range(4):
        o_num = org_id[10:90 , (c*42)+15:(c*42)+57]
        o_num = cv2.resize(o_num,(28,28))
        o_num = img_center( o_num )
        #imgshow(o_num)
        o_n = o_n + str( ainum.get_num( o_num ) )

    res,test_id = bwchange( test_id )
    t_n = ""

    #imgshow( test_id )
    for c in range(4):
        test_num = test_id[10:90 ,(c*42)+15:(c*42)+57]
        test_num = cv2.resize(test_num,(28,28))
        test_num = img_center( test_num )
        #imgshow(test_num)
        t_n = t_n + str( ainum.get_num(test_num) )

    res,user_id = bwchange( user_id )

    u_n = ""

    #imgshow( user_id )
    for c in range(8):
        user_num = user_id[10:90 , (c*40)+15:(c*40)+55 ]
        user_num = cv2.resize( user_num , (28,28) )
        user_num = img_center( user_num )
        #imgshow(user_num)
        u_n = u_n + str( ainum.get_num(user_num) )

    # 列数
    n_col = 20
    #結果を入れる配列
    result = [[],[],[],[]]
    # マークシート
    # 全ての行が終わるまで
    for r in range(len( mark_list) ):
        if r >= 3:
            img_ans = img[ mark_list[r]['y']-15:mark_list[r]['y']+55 , mark_list[r]['x']+85: 1950]
            # リサイズ
            img_ans = cv2.resize(img_ans, (n_col * 30, 30))
            #img_ans = cv2.cvtColor( img_ans,cv2.COLOR_GRAY2RGBA)

            # 黒白に変換
            res_gaku, img_ans = bwchange(img_ans)
            #imgshow( img_ans )
            img_ans = 255 - img_ans
            #imgshow( img_ans )
            #1～20の答え
            area_sum1 = []
            for col in range(1,5):
                tmp_img = img_ans[5:90 , col * 30 : col * 30 + 30 ]
                #print( col )
                #imgshow( tmp_img )
                val = np.sum(tmp_img)
                if val > 35000:
                    area_sum1.append(val)
                else:
                    area_sum1.append(0)
            result[0].append( area_sum1 > np.median(area_sum1) * 3)

            #21～40の答え
            area_sum2 = []
            for col in range(6,10):
                tmp_img = img_ans[5:90, col * 30: col * 30 + 30 ]
                #print( col )
                #imgshow( tmp_img )
                val = np.sum(tmp_img)
                if val > 35000:
                    area_sum2.append(val)
                else:
                    area_sum2.append(0)

            result[1].append( area_sum2 > np.median(area_sum2) * 3 )

            #41～60の答え
            area_sum3 = []
            for col in range(11,15):
                tmp_img = img_ans[5:90, col * 30: col * 30 + 30 ]
                #print( col )
                #imgshow( tmp_img )
                val = np.sum(tmp_img)
                if val > 35000:
                    area_sum3.append(val)
                else:
                    area_sum3.append(0)
            result[2].append( area_sum3 > np.median(area_sum3) * 3 )

            #61～80の答え
            area_sum4 = []
            for col in range(16,20):
                tmp_img = img_ans[5:90, col * 30: col * 30 +30 ]
                #print( col )
                #imgshow( tmp_img )
                val = np.sum(tmp_img)
                if val > 35000:
                    area_sum4.append(val)
                else:
                    area_sum4.append(0)
            result[3].append( area_sum4 > np.median(area_sum4) * 3 )

    answer = ['ア', 'イ', 'ウ', 'エ']
    answerlist = []
    # y=1→1～30 y=2→31～60 y=3→61～90
    for y in range(4):
        for x in range(len(result[y])):
            res = np.where(result[y][x] == True)[0]
            q = []
            if len(res) > 1:
                q.append(y * 20 + x + 1)
                q.append('複数回答')
            elif len(res) == 1:
                q.append(y * 20 + x + 1)
                q.append(answer[res[0]])

            else:
                q.append(y * 20 + x + 1)
                q.append('未回答')
            answerlist.append(q)

    return o_n,t_n,u_n, answerlist
