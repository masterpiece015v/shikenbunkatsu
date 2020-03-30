#coding:utf-8
import MySQLdb
import cgitb

cgitb.enable()

class MySql:
    def __init__(self , host="localhost" , db="mp015v" , user="mp015v", passwd="wtbtsy5701"):
        self.host = host
        self.db_name = db
        self.user = user
        self.passwd = passwd

    def execute(self,sql_str ):
        con = self.get_con(  )
        cur = con.cursor()
        #print( sqlStr%(tbl,cols))
        cur.execute( sql_str )
        con.commit()
        cur.close()
        con.close()

    def create( self ,tbl_name,fields):
        con = self.get_con(  )
        sql_str = "create table %s ( %s )"%(tbl_name,fields)
        cur = con.cursor()
        cur.execute( sql_str )
        con.commit()
        cur.close()
        con.close()

    def select( self ,sql_str):
        con = self.get_con(  )
        #con.cursorclass = MySQLdb.cursors.DictCursor
        cur = con.cursor(MySQLdb.cursors.DictCursor)
        #cur.execute("set names utf8")
        #cur.execute = con.cursor()
        cur.execute(sql_str)
        fetch = cur.fetchall()
        return fetch

    def insert(self,tbl_name,fields,values):
        con = self.get_con()
        cur = con.cursor()
        sqlStr = "insert into %s ( %s ) values ( %s )"
        try:
            cur.execute( sqlStr%(tbl_name,fields,values))
            con.commit()
        except:
            cur.close()
            con.close()
            return False
        else:
            cur.close()
            con.close()
            return True

    def insert_table(self,tbl_name,select_str):
        con = self.get_con()
        cur = con.cursor()
        sqlStr = "insert into %s %s"%(tbl_name,select_str)
        try:
            cur.execute( sqlStr )
            con.commit()
        except:
            cur.close()
            con.close()
            return False
        else:
            cur.close()
            con.close()
            return True


    def delete( self, tbl_name, criteria ):
        sql_str = "delete from %s where %s"%(tbl_name,criteria)
        con = self.get_con()
        cur = con.cursor()
        cur.execute( sql_str )
        con.commit()

    def update( self ,tbl_name, values , keys ):
        con = self.get_con(  )
        cur = con.cursor()
        cur.execute( "update %s set %s where %s"%(tbl_name,values,keys) )
        con.commit()
        cur.close()
        con.close()

    def get_con(self):
        con = MySQLdb.connect(host=self.host , db=self.db_name , user=self.user, passwd=self.passwd,charset="utf8")
        return con