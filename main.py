import subprocess
import os
from PIL import Image
from PIL import ImageEnhance
import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import StringVar
from tkinter import messagebox
import threading
from lib import cut_mj

class MyFram():
    def __init__(self):
        # フォント
        font = ("",12)
        # カレントディレクトリ
        self.cur_dir = os.getcwd()
        # メインウィンドウ
        self.main_win = tkinter.Tk()
        self.main_win.title('PDFをPNGに変換する')
        self.main_win.geometry('640x480')
        # スタイルの設定
        style = ttk.Style()
        style.configure(".",font=font)

        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        # タブの設定
        nb = ttk.Notebook(width=630, height=440)
        self.tab1 = ttk.Frame(nb)
        self.tab2 = ttk.Frame(nb)
        self.tab3 = ttk.Frame(nb)
        self.tab4 = ttk.Frame(nb)
        nb.add(self.tab1,text=u'PDFtoPNG',padding=3)
        nb.add(self.tab2,text=u'JH_CutPNG',padding=3)
        nb.add(self.tab3,text=u'明暗',padding=3)
        nb.add(self.tab4,text=u'BK_CutPNG',padding=3)
        nb.place(x=5,y=5)

        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        # タブ1
        # 読み込みPDFファイルの選択
        self.tab1_src_file_var = StringVar()
        self.tab1_src_file_label = ttk.Label(self.tab1, text=u'PDFファイル')
        self.tab1_src_file_entry = ttk.Entry(self.tab1, textvariable=self.tab1_src_file_var, width=50)
        self.tab1_src_file_btn = ttk.Button(self.tab1, text=u'参照', command=self.tab1_src_file_btn_click)
        # 読み込みPDFファイル選択のレイアウト
        self.tab1_src_file_label.place(x=5,y=5,width=130,height=30)
        self.tab1_src_file_entry.place(x=155,y=5,width=300,height=30)
        self.tab1_src_file_btn.place(x=475,y=5,width=80,height=30)

        # 保存先フォルダの選択
        self.tab1_dst_folder_var = StringVar()
        self.tab1_dst_folder_label = ttk.Label(self.tab1, text=u'保存先フォルダ')
        self.tab1_dst_folder_entry = ttk.Entry(self.tab1, textvariable=self.tab1_dst_folder_var, width=50)
        self.tab1_dst_folder_btn = ttk.Button(self.tab1, text=u'参照', command=self.tab1_dst_folder_btn_click)
        # 保存先選択のレイアウト
        self.tab1_dst_folder_label.place(x=5,y=45,width=130,height=30)
        self.tab1_dst_folder_entry.place(x=155,y=45,width=300,height=30)
        self.tab1_dst_folder_btn.place(x=475,y=45,width=80,height=30)

        # 保存先のファイルを表示するリスト
        self.tab1_file_list_var = StringVar(value=())
        self.tab1_file_list = ttk.Treeview(self.tab1)
        self.tab1_file_list.bind('<Double-1>', lambda event: self.tab1_file_list_double_click())
        # 保存先ファイルのリストのレイアウト
        self.tab1_file_list.place(x=5,y=85,width=250,height=200)

        # スクロールバー
        self.tab1_file_list_scr = ttk.Scrollbar( self.tab1,orient=tkinter.VERTICAL,command=self.tab1_file_list.yview)
        self.tab1_file_list['yscrollcommand'] = self.tab1_file_list_scr.set
        # スクロールバーのレイアウト
        self.tab1_file_list_scr.place(x=255,y=85,width=10,height=200)

        # ファイルを削除するボタン
        self.tab1_file_select_del_btn = ttk.Button(self.tab1,text=u'選択削除',command=self.tab1_file_select_del_btn_click)
        # ファイルを削除するボタンのレイアウト
        self.tab1_file_select_del_btn.place(x=275,y=85,width=100,height=30)

        # ファイルを全て削除するボタン
        self.tab1_file_all_del_btn = ttk.Button(self.tab1, text=u'全削除', command=self.tab1_file_all_del_btn_click)
        # ファイルを全て削除するボタンのレイアウト
        self.tab1_file_all_del_btn.place(x=275,y=125,width=100,height=30)

        # コントラスト
        self.tab1_cont_box_var = StringVar()
        self.tab1_cont_label = ttk.Label(self.tab1, text=u'コントラスト')
        self.tab1_cont_entry = ttk.Entry(self.tab1, textvariable=self.tab1_cont_box_var ,width=5)
        self.tab1_cont_entry.bind('<KeyPress-Return>',lambda event:self.tab1_cont_box_callback())
        self.tab1_cont_entry.insert(tkinter.END, '1.5')
        # コントラストのレイアウト
        self.tab1_cont_label.place(x=5,y=295,width=130,height=30)
        self.tab1_cont_entry.place(x=145,y=295,width=60,height=30)
        # コントラストのスケール
        self.tab1_cont_scale_var = tkinter.DoubleVar()
        self.tab1_cont_scale_var.set(2.0)
        self.tab1_cont_scale = ttk.Scale(self.tab1,from_=0,to=5,variable=self.tab1_cont_scale_var,command=self.tab1_cont_scale_callback )
        # コントラストスケールのレイアウト
        self.tab1_cont_scale.place(x=215,y=295,width=200,height=30)

        # ファイル名
        self.tab1_file_name_var = StringVar()
        self.tab1_file_name_label = ttk.Label(self.tab1,text=u'ファイル名')
        self.tab1_file_name_entry = ttk.Entry(self.tab1,width=10,textvariable=self.tab1_file_name_var)
        # ファイル名のレイアウト
        self.tab1_file_name_label.place(x=5,y=335,width=130,height=30)
        self.tab1_file_name_entry.place(x=145,y=335,width=120,height=30)

        # プログレスバー
        self.tab1_prog_bar = ttk.Progressbar(self.tab1, orient=tkinter.HORIZONTAL, length=200, mode='indeterminate')
        self.tab1_prog_bar.configure(maximum=100, value=0)
        # プログレスバーのレイアウト
        self.tab1_prog_bar.place(x=5,y=375,width=260,height=30)

        # PDFをPNGに変換するボタン
        self.tab1_convert_btn = ttk.Button(self.tab1, text=u'変換', command=self.tab1_convert_btn_pdf)
        # PDFをPNGに変換するボタンのレイアウト
        self.tab1_convert_btn.place(x=275,y=335,width=80,height=30)

        #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
        # tab2
        # タブ1
        # 文字列のバインド

        # ソースフォルダの選択
        self.tab2_src_folder_label = ttk.Label(self.tab2, text=u'ソースフォルダ')
        self.tab2_src_folder_var = StringVar()
        self.tab2_src_folder_entry = ttk.Entry(self.tab2, textvariable=self.tab2_src_folder_var, width=50)
        self.tab2_src_folder_btn = ttk.Button(self.tab2, text=u'参照', command=self.tab2_src_folder_btn_click)
        # ソースフォルダのレイアウト
        self.tab2_src_folder_label.place(x=5, y=5, width=130, height=30)
        self.tab2_src_folder_entry.place(x=155, y=5, width=300, height=30)
        self.tab2_src_folder_btn.place(x=475, y=5, width=80, height=30)

        # 保存先フォルダの選択
        self.tab2_dst_folder_label = ttk.Label(self.tab2, text=u'保存先フォルダ')
        self.tab2_dst_folder_var = StringVar()
        self.tab2_dst_folder_entry = ttk.Entry(self.tab2, textvariable=self.tab2_dst_folder_var, width=50)
        self.tab2_dst_folder_btn = ttk.Button(self.tab2, text=u'参照', command=self.tab2_dst_folder_btn_click)
        # 保存先選択のレイアウト
        self.tab2_dst_folder_label.place(x=5, y=45, width=130, height=30)
        self.tab2_dst_folder_entry.place(x=155, y=45, width=300, height=30)
        self.tab2_dst_folder_btn.place(x=475, y=45, width=80, height=30)

        # 保存先のファイルを表示するリスト
        self.tab2_file_list = ttk.Treeview(self.tab2)
        self.tab2_file_list.bind('<Double-1>', lambda event: self.tab2_file_list_double_click())
        # 保存先ファイルのリストのレイアウト
        self.tab2_file_list.place(x=5, y=85, width=250, height=200)

        # スクロールバー
        self.tab2_file_list_scr = ttk.Scrollbar(self.tab2, orient=tkinter.VERTICAL, command=self.tab2_file_list.yview)
        self.tab2_file_list['yscrollcommand'] = self.tab2_file_list_scr.set
        # スクロールバーのレイアウト
        self.tab2_file_list_scr.place(x=255, y=85, width=10, height=200)

        # ファイルを削除するボタン
        self.tab2_file_select_del_btn = ttk.Button(self.tab2, text=u'選択削除', command=self.tab2_file_select_del_btn_click)
        # ファイルを削除するボタンのレイアウト
        self.tab2_file_select_del_btn.place(x=275, y=85, width=100, height=30)

        # ファイルを全て削除するボタン
        self.tab2_file_all_del_btn = ttk.Button(self.tab2, text=u'全削除', command=self.tab2_file_all_del_btn_click)
        # ファイルを全て削除するボタンのレイアウト
        self.tab2_file_all_del_btn.place(x=275, y=125, width=100, height=30)

        # リネーム
        self.tab2_file_rename_btn = ttk.Button( self.tab2,text=u'リネーム',command=self.tab2_file_rename_btn_click)
        self.tab2_file_rename_btn.place(x=275,y=165,width=100,height=30)

        # ファイル名
        self.tab2_file_name_label = ttk.Label(self.tab2, text=u'ファイル名')
        self.tab2_file_name_var = StringVar()
        self.tab2_file_name_entry = ttk.Entry(self.tab2, width=10, textvariable=self.tab2_file_name_var)
        # ファイル名のレイアウト
        self.tab2_file_name_label.place(x=5,y=335,width=130,height=30)
        self.tab2_file_name_entry.place(x=145,y=335,width=120,height=30)

        # プログレスバー
        self.tab2_prog_bar = ttk.Progressbar(self.tab2, orient=tkinter.HORIZONTAL, length=200, mode='indeterminate')
        self.tab2_prog_bar.configure(maximum=100, value=0)
        # プログレスバーのレイアウト
        self.tab2_prog_bar.place(x=5, y=375, width=260, height=30)

        # PDFをPNGに変換するボタン
        self.tab2_convert_btn = ttk.Button(self.tab2, text=u'変換', command=self.tab2_convert_btn_click)
        # PDFをPNGに変換するボタンのレイアウト
        self.tab2_convert_btn.place(x=275,y=335,width=80,height=30)

        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
        # タブ3
        # ソースフォルダの選択
        self.tab3_src_folder_label = ttk.Label(self.tab3, text=u'ソースフォルダ')
        self.tab3_src_folder_var = StringVar()
        self.tab3_src_folder_entry = ttk.Entry(self.tab3, textvariable=self.tab3_src_folder_var, width=50)
        self.tab3_src_folder_btn = ttk.Button(self.tab3, text=u'参照', command=self.tab3_src_folder_btn_click)
        # ソースフォルダのレイアウト
        self.tab3_src_folder_label.place(x=5, y=5, width=130, height=30)
        self.tab3_src_folder_entry.place(x=155, y=5, width=300, height=30)
        self.tab3_src_folder_btn.place(x=475, y=5, width=80, height=30)

        # 保存先のファイルを表示するリスト
        self.tab3_file_list = ttk.Treeview(self.tab3)
        self.tab3_file_list.bind('<Double-1>', lambda event: self.tab3_file_list_double_click())
        # 保存先ファイルのリストのレイアウト
        self.tab3_file_list.place(x=5, y=85, width=250, height=200)

        # スクロールバー
        self.tab3_file_list_scr = ttk.Scrollbar(self.tab3, orient=tkinter.VERTICAL, command=self.tab3_file_list.yview)
        self.tab3_file_list['yscrollcommand'] = self.tab3_file_list_scr.set
        # スクロールバーのレイアウト
        self.tab3_file_list_scr.place(x=255, y=85, width=10, height=200)

        # ファイルを削除するボタン
        self.tab3_file_select_del_btn = ttk.Button(self.tab3, text=u'選択削除', command=self.tab3_file_select_del_btn_click)
        # ファイルを削除するボタンのレイアウト
        self.tab3_file_select_del_btn.place(x=275, y=85, width=100, height=30)

        # ファイルを全て削除するボタン
        self.tab3_file_all_del_btn = ttk.Button(self.tab3, text=u'全削除', command=self.tab3_file_all_del_btn_click)
        # ファイルを全て削除するボタンのレイアウト
        self.tab3_file_all_del_btn.place(x=275, y=125, width=100, height=30)

        # コントラスト
        self.tab3_cont_box_var = StringVar()
        self.tab3_cont_label = ttk.Label(self.tab3, text=u'コントラスト')
        self.tab3_cont_entry = ttk.Entry(self.tab3, textvariable=self.tab3_cont_box_var ,width=5)
        self.tab3_cont_entry.bind('<KeyPress-Return>',lambda event:self.tab3_cont_box_callback())
        self.tab3_cont_entry.insert(tkinter.END, '2.0')
        # コントラストのレイアウト
        self.tab3_cont_label.place(x=5,y=295,width=130,height=30)
        self.tab3_cont_entry.place(x=145,y=295,width=60,height=30)
        # コントラストのスケール
        self.tab3_cont_scale_var = tkinter.DoubleVar()
        self.tab3_cont_scale_var.set(2.0)
        self.tab3_cont_scale = ttk.Scale(self.tab3,from_=0,to=5,variable=self.tab3_cont_scale_var,command=self.tab3_cont_scale_callback )
        # コントラストスケールのレイアウト
        self.tab3_cont_scale.place(x=215,y=295,width=200,height=30)

        # プログレスバー
        self.tab3_prog_bar = ttk.Progressbar(self.tab3, orient=tkinter.HORIZONTAL, length=200, mode='indeterminate')
        self.tab3_prog_bar.configure(maximum=100, value=0)
        # プログレスバーのレイアウト
        self.tab3_prog_bar.place(x=5, y=375, width=260, height=30)

        # PDFをPNGに変換するボタン
        self.tab3_convert_btn = ttk.Button(self.tab3, text=u'変換', command=self.tab3_convert_btn_click)
        # PDFをPNGに変換するボタンのレイアウト
        self.tab3_convert_btn.place(x=275, y=335, width=80, height=30)

        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
        # tab2
        # タブ1
        # 文字列のバインド

        # ソースフォルダの選択
        self.tab4_src_folder_label = ttk.Label(self.tab4, text=u'ソースフォルダ')
        self.tab4_src_folder_var = StringVar()
        self.tab4_src_folder_entry = ttk.Entry(self.tab4, textvariable=self.tab4_src_folder_var, width=50)
        self.tab4_src_folder_btn = ttk.Button(self.tab4, text=u'参照', command=self.tab4_src_folder_btn_click)
        # ソースフォルダのレイアウト
        self.tab4_src_folder_label.place(x=5, y=5, width=130, height=30)
        self.tab4_src_folder_entry.place(x=155, y=5, width=300, height=30)
        self.tab4_src_folder_btn.place(x=475, y=5, width=80, height=30)

        # 保存先フォルダの選択
        self.tab4_dst_folder_label = ttk.Label(self.tab4, text=u'保存先フォルダ')
        self.tab4_dst_folder_var = StringVar()
        self.tab4_dst_folder_entry = ttk.Entry(self.tab4, textvariable=self.tab4_dst_folder_var, width=50)
        self.tab4_dst_folder_btn = ttk.Button(self.tab4, text=u'参照', command=self.tab4_dst_folder_btn_click)
        # 保存先選択のレイアウト
        self.tab4_dst_folder_label.place(x=5, y=45, width=130, height=30)
        self.tab4_dst_folder_entry.place(x=155, y=45, width=300, height=30)
        self.tab4_dst_folder_btn.place(x=475, y=45, width=80, height=30)

        # 保存先のファイルを表示するリスト
        self.tab4_file_list = ttk.Treeview(self.tab4)
        self.tab4_file_list.bind('<Double-1>', lambda event: self.tab4_file_list_double_click())
        # 保存先ファイルのリストのレイアウト
        self.tab4_file_list.place(x=5, y=85, width=250, height=200)

        # スクロールバー
        self.tab4_file_list_scr = ttk.Scrollbar(self.tab4, orient=tkinter.VERTICAL, command=self.tab4_file_list.yview)
        self.tab4_file_list['yscrollcommand'] = self.tab4_file_list_scr.set
        # スクロールバーのレイアウト
        self.tab4_file_list_scr.place(x=255, y=85, width=10, height=200)

        # ファイルを削除するボタン
        self.tab4_file_select_del_btn = ttk.Button(self.tab4, text=u'選択削除', command=self.tab4_file_select_del_btn_click)
        # ファイルを削除するボタンのレイアウト
        self.tab4_file_select_del_btn.place(x=275, y=85, width=100, height=30)

        # ファイルを全て削除するボタン
        self.tab4_file_all_del_btn = ttk.Button(self.tab4, text=u'全削除', command=self.tab4_file_all_del_btn_click)
        # ファイルを全て削除するボタンのレイアウト
        self.tab4_file_all_del_btn.place(x=275, y=125, width=100, height=30)

        # リネーム
        self.tab4_file_rename_btn = ttk.Button(self.tab4, text=u'リネーム', command=self.tab4_file_rename_btn_click)
        self.tab4_file_rename_btn.place(x=275, y=165, width=100, height=30)

        # ファイル名
        self.tab4_file_name_label = ttk.Label(self.tab4, text=u'ファイル名')
        self.tab4_file_name_var = StringVar()
        self.tab4_file_name_entry = ttk.Entry(self.tab4, width=10, textvariable=self.tab4_file_name_var)
        # ファイル名のレイアウト
        self.tab4_file_name_label.place(x=5, y=335, width=130, height=30)
        self.tab4_file_name_entry.place(x=145, y=335, width=120, height=30)

        # プログレスバー
        self.tab4_prog_bar = ttk.Progressbar(self.tab4, orient=tkinter.HORIZONTAL, length=200, mode='indeterminate')
        self.tab4_prog_bar.configure(maximum=100, value=0)
        # プログレスバーのレイアウト
        self.tab4_prog_bar.place(x=5, y=375, width=260, height=30)

        # PDFをPNGに変換するボタン
        self.tab4_convert_btn = ttk.Button(self.tab4, text=u'変換', command=self.tab4_convert_btn_click)
        # PDFをPNGに変換するボタンのレイアウト
        self.tab4_convert_btn.place(x=275, y=335, width=80, height=30)

    def mainloop(self):
        self.main_win.mainloop()

    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    # タブ1のイベント
    # pdfファイルを選択するボタンのイベント
    def tab1_src_file_btn_click(self):
            file_type = [(u'PDFファイル', '*.pdf')]
            path = filedialog.askopenfilename(filetypes=file_type, initialdir=self.cur_dir)
            file = path.split("/")
            self.tab1_src_file_var.set(path)
            self.tab1_file_name_var.set(file[len(file) - 1].split(".")[0])

    # pngファイルを保存するフォルダを選択するボタンのイベント
    def tab1_dst_folder_btn_click(self):
        path = filedialog.askdirectory(initialdir=self.cur_dir)
        self.tab1_file_list_show(path)
        self.tab1_dst_folder_var.set(path)

    # パラメータ（パス）内のファイルをfile_listに表示する
    def tab1_file_list_show(self, path):
        # リスト内をクリアする
        self.tab1_file_list.delete(*self.tab1_file_list.get_children())
        for file in os.listdir(path):
            sub_path = os.path.join(path, file)
            if (os.path.isdir(sub_path)):
                # フォルダの場合
                folder = self.tab1_file_list.insert("", "end", text=file)
                for file2 in os.listdir(sub_path):
                    if '.png' in file2:
                        self.tab1_file_list.insert(folder, "end", text=file2)

    # コンバートボタンのイベント
    def tab1_convert_btn_pdf(self):
        os.makedirs(os.path.join(self.tab1_dst_folder_entry.get(), self.tab1_file_name_entry.get()), exist_ok=True)
        self.tab1_prog_bar.start(interval=10)
        th = threading.Thread(target=self.pdftopng_callback)
        th.start()

    # pdftopngのコールバック
    def pdftopng_callback(self):
        self.pdftopng(self.tab1_src_file_entry.get(),
                      os.path.join(self.tab1_dst_folder_entry.get(), self.tab1_file_name_entry.get()),
                      self.tab1_cont_entry.get())
        self.tab1_prog_bar.stop()
        messagebox.showinfo("終了", "変換が終了しました。")
        # ファイル名を表示する
        self.tab1_file_list_show(self.tab1_dst_folder_entry.get())

    # 選択したファイルを削除するボタンのイベント
    def tab1_file_select_del_btn_click(self):
        file_name = self.get_treeview_file_path(self.tab1_file_list)
        # print(os.path.join(self.folder_box.get(),file_name ) )
        file_path = os.path.join(self.tab1_dst_folder_entry.get(), file_name)
        if '.png' in file_name:
            os.remove(file_path)
            self.tab1_file_list.delete(self.tab1_file_list.focus())
        elif os.path.isdir(os.path.join(self.tab1_dst_folder_entry.get(), file_name)):
            try:
                print(file_path)
                os.rmdir(file_path)
                self.tab1_file_list.delete(self.tab1_file_list.focus())
            except OSError:
                messagebox.showerror("削除できません", "フォルダが空ではないため削除できません。")

    # ファイルを全て削除する
    def tab1_file_all_del_btn_click(self):
        for child in self.tab1_file_list.get_children(self.tab1_file_list.focus()):
            file = self.tab1_file_list.item(child)['text']
            if '.png' in file:
                parent = self.tab1_file_list.item(self.tab1_file_list.focus())['text']
                file_path = os.path.join(self.tab1_dst_folder_entry.get(), parent, file)
                os.remove(file_path)
                self.tab1_file_list.delete(child)

    # リストボックスをダブルクリックすると画像を表示する
    def tab1_file_list_double_click(self):
        focus_file_path = self.get_treeview_file_path(self.tab1_file_list)
        file_path = os.path.join(self.tab1_dst_folder_entry.get(), focus_file_path)
        if '.png' in file_path:
            im = Image.open(file_path)
            im.show()

    # フォーカスされたツリービューのパスを返す
    def get_treeview_file_path(self, tv):
        file_name = tv.item(tv.focus())['text']
        parent_name = tv.item(tv.parent(tv.focus()))['text']
        return os.path.join(parent_name, file_name)

    # コントラストスライダーのコールバック
    def tab1_cont_scale_callback(self, value):
        self.tab1_cont_box_var.set(round(float(value) * 10) / 10)

    # コントラストボックスのコールバック
    def tab1_cont_box_callback(self):
        self.tab1_cont_scale_var.set(float(self.tab1_cont_entry.get()))

    # pdfをpngに変換するメソッド
    def pdftopng(self, pdf_file_path, image_file_path, contrast=1):
        poppler_dir = os.path.join(self.cur_dir, 'poppler-0.51', 'bin', 'pdftocairo')
        src_path = pdf_file_path
        dst_path = os.path.join(image_file_path, self.tab1_file_name_entry.get())

        cmd = '%s -png %s %s' % (poppler_dir, src_path, dst_path)

        returncode = subprocess.Popen(cmd, shell=True)
        returncode.wait()

        print(returncode)

        for file in os.listdir(image_file_path):
            if '.png' in file:
                im1 = Image.open(os.path.join(image_file_path, file))
                con = ImageEnhance.Contrast(im1)
                im2 = con.enhance(float(contrast))

                im1.close()

                os.remove(os.path.join(image_file_path, file))

                file_name = file[0:len(file) - 4] + "-conv.png"
                im2.save(os.path.join(image_file_path, file_name))
                im2.close()

    #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    #タブ2のイベント
    #tab2の保存先フォルダ選択
    def tab2_dst_folder_btn_click(self):
        path = filedialog.askdirectory(initialdir=self.cur_dir)
        self.tab2_file_list_show(path)
        self.tab2_dst_folder_var.set(path)

    # パラメータ（パス）内のファイルをfile_listに表示する
    def tab2_file_list_show(self,path):
        # リスト内をクリアする
        self.tab2_file_list.delete( *self.tab2_file_list.get_children() )
        for file in os.listdir(path):
            sub_path = os.path.join( path , file )
            if( os.path.isdir(sub_path) ):
                #フォルダの場合
                folder = self.tab2_file_list.insert("","end",text=file)
                for file2 in os.listdir(sub_path):
                    if '.png' in file2:
                        self.tab2_file_list.insert(folder,"end",text=file2)

    #tab2のカットもとフォルダの選択
    def tab2_src_folder_btn_click(self):
        path = filedialog.askdirectory(initialdir=self.cur_dir)
        self.tab2_file_list_show(path)
        self.tab2_src_folder_var.set(path)

    # 選択したファイルを削除する
    def tab2_file_select_del_btn_click(self):
        file_name = self.get_treeview_file_path(self.tab2_file_list)
        # print(os.path.join(self.folder_box.get(),file_name ) )
        file_path = os.path.join(self.tab2_dst_folder_entry.get(), file_name)
        if '.png' in file_name:
            os.remove(file_path)
            self.tab2_file_list.delete(self.tab2_file_list.focus())
        elif os.path.isdir(os.path.join(self.tab2_dst_folder_entry.get(), file_name)):
            try:
                print(file_path)
                os.rmdir(file_path)
                self.tab2_file_list.delete(self.tab2_file_list.focus())
            except OSError:
                messagebox.showerror("削除できません", "フォルダが空ではないため削除できません。")
    #
    def tab2_file_all_del_btn_click(self):
        for child in self.tab2_file_list.get_children(self.tab2_file_list.focus()):
            file = self.tab2_file_list.item(child)['text']
            if '.png' in file:
                parent = self.tab2_file_list.item(self.tab2_file_list.focus())['text']
                file_path = os.path.join(self.tab2_dst_folder_entry.get(), parent, file)
                os.remove(file_path)
                self.tab2_file_list.delete(child)

    #
    def tab2_file_rename_btn_click(self):
        dir_path = os.path.join(self.tab2_dst_folder_entry.get(),self.tab2_file_list.item(self.tab2_file_list.focus())['text'])
        num = 1
        for file in os.listdir(dir_path):
            if num < 10:
                new_file_name = file[:7] + '0' + str(num) + '.png'
                os.rename(os.path.join(dir_path,file),os.path.join(dir_path,new_file_name))
                # print( new_file_name )
            else:
                new_file_name = file[:7] + str(num) + '.png'
                os.rename(os.path.join(dir_path, file), os.path.join(dir_path, new_file_name))
                # print( new_file_name )
            num = num + 1
        self.tab2_file_list_show(self.tab2_dst_folder_entry.get())

    def tab2_file_list_double_click(self):
        print("")

    # tab2のコンバートボタン
    def tab2_convert_btn_click(self):
        dst_path = os.path.join(self.tab2_dst_folder_entry.get(),self.tab2_file_name_entry.get())
        os.makedirs(dst_path, exist_ok=True)
        self.tab2_prog_bar.start(interval=10)
        th = threading.Thread(target=self.cut_mondai_callback,args=(dst_path,))
        th.start()
    # tab2コンバートボタンのコールバック
    def cut_mondai_callback(self ,dst_path ):
        #dst_path = os.path.join(self.tab2_dst_folder_entry.get(), self.tab2_file_name_entry.get())
        cut_mj.cut_mondai(self.tab2_src_folder_entry.get(), dst_path, self.tab2_file_name_entry.get(), 2)
        self.tab2_prog_bar.stop()
        self.tab2_file_list_show(self.tab2_dst_folder_entry.get())

    #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    # タブ3のイベント
    # 変換元フォルダを選択するボタンのイベント
    def tab3_src_folder_btn_click(self):
        path = filedialog.askdirectory(initialdir=self.cur_dir)
        self.tab3_file_list_show(path)
        self.tab3_src_folder_var.set(path)

    # パラメータ（パス）内のファイルをfile_listに表示する
    def tab3_file_list_show(self, path):
        # リスト内をクリアする
        self.tab3_file_list.delete(*self.tab3_file_list.get_children())
        for file in os.listdir(path):
            sub_path = os.path.join(path, file)
            print( sub_path )
            if (os.path.isdir(sub_path)):
                # フォルダの場合
                folder = self.tab3_file_list.insert("", "end", text=file)
                for file2 in os.listdir(sub_path):
                    if '.png' in file2:
                        self.tab3_file_list.insert(folder, "end", text=file2)
            elif '.png' in file:
                self.tab3_file_list.insert("","end",text=file)

    # コンバートボタンのイベント
    def tab3_convert_btn_click(self):
        self.tab3_prog_bar.start(interval=10)
        th = threading.Thread(target=self.contrast_callback)
        th.start()

    # pdftopngのコールバック
    def contrast_callback(self):
        self.contrast(self.tab3_src_folder_entry.get(),self.tab3_cont_box_var.get())
        self.tab3_prog_bar.stop()
        messagebox.showinfo("終了", "変換が終了しました。")
        # ファイル名を表示する
        self.tab3_file_list_show(self.tab3_src_folder_entry.get())

        # pdfをpngに変換するメソッド
    def contrast(self, src_folder_path, contrast=1):
        for file in os.listdir(src_folder_path):
            if '.png' in file:
                im1 = Image.open(os.path.join(src_folder_path, file))
                con = ImageEnhance.Contrast(im1)
                im2 = con.enhance(float(contrast))

                im1.close()

                os.remove(os.path.join(src_folder_path, file))

                im2.save(os.path.join(src_folder_path, file))
                im2.close()

    # 選択したファイルを削除するボタンのイベント
    def tab3_file_select_del_btn_click(self):
        file_name = self.get_treeview_file_path(self.tab3_file_list)
        # print(os.path.join(self.folder_box.get(),file_name ) )
        file_path = os.path.join(self.tab3_src_folder_entry.get(), file_name)
        if '.png' in file_name:
            os.remove(file_path)
            self.tab3_file_list.delete(self.tab3_file_list.focus())
        elif os.path.isdir(os.path.join(self.tab3_src_folder_entry.get(), file_name)):
            try:
                print(file_path)
                os.rmdir(file_path)
                self.tab3_file_list.delete(self.tab3_file_list.focus())
            except OSError:
                messagebox.showerror("削除できません", "フォルダが空ではないため削除できません。")

    # ファイルを全て削除する
    def tab3_file_all_del_btn_click(self):
        for child in self.tab3_file_list.get_children(self.tab3_file_list.focus()):
            file = self.tab3_file_list.item(child)['text']
            if '.png' in file:
                parent = self.tab3_file_list.item(self.tab3_file_list.focus())['text']
                file_path = os.path.join(self.tab3_src_folder_entry.get(), parent, file)
                os.remove(file_path)
                self.tab3_file_list.delete(child)

    # リストボックスをダブルクリックすると画像を表示する
    def tab3_file_list_double_click(self):
        focus_file_path = self.get_treeview_file_path(self.tab3_file_list)
        file_path = os.path.join(self.tab3_src_folder_entry.get(), focus_file_path)
        if '.png' in file_path:
            im = Image.open(file_path)
            im.show()

    # コントラストスライダーのコールバック
    def tab3_cont_scale_callback(self, value):
        self.tab3_cont_box_var.set(round(float(value) * 10) / 10)

    # コントラストボックスのコールバック
    def tab3_cont_box_callback(self):
        self.tab1_cont_scale_var.set(float(self.tab1_cont_entry.get()))
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    #タブ4のイベント
    #tab4の保存先フォルダ選択
    def tab4_dst_folder_btn_click(self):
        path = filedialog.askdirectory(initialdir=self.cur_dir)
        self.tab4_file_list_show(path)
        self.tab4_dst_folder_var.set(path)

    # パラメータ（パス）内のファイルをfile_listに表示する
    def tab4_file_list_show(self,path):
        # リスト内をクリアする
        self.tab4_file_list.delete( *self.tab4_file_list.get_children() )
        for file in os.listdir(path):
            sub_path = os.path.join( path , file )
            if( os.path.isdir(sub_path) ):
                #フォルダの場合
                folder = self.tab4_file_list.insert("","end",text=file)
                for file2 in os.listdir(sub_path):
                    if '.png' in file2:
                        self.tab4_file_list.insert(folder,"end",text=file2)

    #tab4のカットもとフォルダの選択
    def tab4_src_folder_btn_click(self):
        path = filedialog.askdirectory(initialdir=self.cur_dir)
        self.tab4_file_list_show(path)
        self.tab4_src_folder_var.set(path)

    # 選択したファイルを削除する
    def tab4_file_select_del_btn_click(self):
        file_name = self.get_treeview_file_path(self.tab4_file_list)
        # print(os.path.join(self.folder_box.get(),file_name ) )
        file_path = os.path.join(self.tab4_dst_folder_entry.get(), file_name)
        if '.png' in file_name:
            os.remove(file_path)
            self.tab4_file_list.delete(self.tab4_file_list.focus())
        elif os.path.isdir(os.path.join(self.tab4_dst_folder_entry.get(), file_name)):
            try:
                print(file_path)
                os.rmdir(file_path)
                self.tab4_file_list.delete(self.tab4_file_list.focus())
            except OSError:
                messagebox.showerror("削除できません", "フォルダが空ではないため削除できません。")
    #
    def tab4_file_all_del_btn_click(self):
        for child in self.tab4_file_list.get_children(self.tab4_file_list.focus()):
            file = self.tab4_file_list.item(child)['text']
            if '.png' in file:
                parent = self.tab4_file_list.item(self.tab4_file_list.focus())['text']
                file_path = os.path.join(self.tab4_dst_folder_entry.get(), parent, file)
                os.remove(file_path)
                self.tab4_file_list.delete(child)

    #
    def tab4_file_rename_btn_click(self):
        dir_path = os.path.join(self.tab4_dst_folder_entry.get(),self.tab4_file_list.item(self.tab4_file_list.focus())['text'])
        num = 1
        for file in os.listdir(dir_path):
            if num < 10:
                new_file_name = file[:7] + '0' + str(num) + '.png'
                os.rename(os.path.join(dir_path,file),os.path.join(dir_path,new_file_name))
                # print( new_file_name )
            else:
                new_file_name = file[:7] + str(num) + '.png'
                os.rename(os.path.join(dir_path, file), os.path.join(dir_path, new_file_name))
                # print( new_file_name )
            num = num + 1
        self.tab4_file_list_show(self.tab4_dst_folder_entry.get())

    def tab4_file_list_double_click(self):
        print("")

    # tab4のコンバートボタン
    def tab4_convert_btn_click(self):
        dst_path = os.path.join(self.tab4_dst_folder_entry.get(),self.tab4_file_name_entry.get())
        os.makedirs(dst_path, exist_ok=True)
        self.tab4_prog_bar.start(interval=10)
        th = threading.Thread(target=self.cut_mondai_callback,args=(dst_path,))
        th.start()

    # tab4コンバートボタンのコールバック
    def cut_mondai_callback(self ,dst_path ):
        #dst_path = os.path.join(self.tab2_dst_folder_entry.get(), self.tab2_file_name_entry.get())
        cut_mj.cut_mondai_bk(self.tab4_src_folder_entry.get(), dst_path, self.tab4_file_name_entry.get(), 2)
        self.tab4_prog_bar.stop()
        self.tab4_file_list_show(self.tab4_dst_folder_entry.get())

if __name__ == "__main__":
    frame = MyFram()
    frame.mainloop()