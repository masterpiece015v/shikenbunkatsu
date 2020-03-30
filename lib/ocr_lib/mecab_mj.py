#import MeCab
from natto import MeCab
#m=MeCab("-Owakati")
#m=MeCab("-Odump")   #全情報
m=MeCab("-Ochasen")
#m = MeCab()

def get_text_mecab(text):
    return m.parse(text)

def get_text_mecab_ippan( text ):
    text1 = get_text_mecab(text)
    text2 = ""
    flg = True
    for r in text1.split("\n"):
        r_list = r.split("\t")
        if len(r_list) > 1:
            if r.split("\t")[3] == "名詞-一般":
                if flg:
                    text2 = r_list[0]
                    flg = False
                else:
                    text2 = text2 + " " + r_list[0]
    return text2

if __name__ == "__main__":
    text = get_text_mecab("浮動小数点数は小数")
    print( text )

