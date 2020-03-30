#coding: utf-8
import sqlite3

class SqlLite:
    def __init__(self , db_name ):
        self.db_name = db_name

    def execute(self,sql_str ):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        #print( sqlStr%(tbl,cols))
        cur.execute( sql_str )
        con.commit()
        cur.close()
        con.close()

    def create(self, tbl_name , fields ):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        sqlStr = "create table %s (%s)"
        #print( sqlStr%(tbl,cols))
        cur.execute( sqlStr%(tbl_name,fields))
        con.commit()
        cur.close()
        con.close()

    def insert(self,tbl_name,fields,values ):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        sqlStr = "insert into %s (%s) values ( %s )"
        cur.execute( sqlStr%(tbl_name,fields,values))
        con.commit()
        cur.close()
        con.close()

    def select( self ,sql_str ):
        con = sqlite3.connect(self.db_name )
        cur = con.cursor()
        return cur.execute( sql_str )

    def delete( self, tbl_name, criteria ):
        sql_str = "delete from %s where %s"%(tbl_name,criteria)
        con = sqlite3.connect( self.db_name )
        cur = con.cursor()
        cur.execute( sql_str )
        con.commit()

    def update( self ,tbl_name, values , keys ):
        con = sqlite3.connect( self.db_name )
        cur = con.cursor()
        cur.execute( "update %s set %s where %s"%(tbl_name,values,keys) )
        con.commit()

    def getKeys( self , sql_str ):
        con = sqlite3.connect( self.db_name )
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute( sql_str )
        r = cur.fetchone()
        return r.keys()
