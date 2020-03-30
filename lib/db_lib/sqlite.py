#coding: utf-8
import sqlite3

def execute(db_name,sql_str ):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    #print( sqlStr%(tbl,cols))
    cur.execute( sql_str )
    con.commit()
    cur.close()
    con.close()

def create(db_name, tbl_name , fields ):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    sqlStr = "create table %s (%s)"
    #print( sqlStr%(tbl,cols))
    cur.execute( sqlStr%(tbl_name,fields))
    con.commit()
    cur.close()
    con.close()

def insert(db_name,tbl_name,values ):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    sqlStr = "insert into %s values ( %s )"
    cur.execute( sqlStr%(tbl_name,values))
    con.commit()
    cur.close()
    con.close()

def select( db_name,sql_str ):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    return cur.execute( sql_str )

def delete( self, tbl_name, criteria ):
    sql_str = "delete from %s where %s"%(tbl_name,criteria)
    con = sqlite3.connect( self.db_name )
    cur = con.cursor()
    cur.execute( sql_str )
    con.commit()

def update( db_name,tbl_name, values , keys ):
    con = sqlite3.connect( db_name )
    cur = con.cursor()
    cur.execute( "update %s set %s where %s"%(tbl_name,values,keys) )
    con.commit()

def getKeys( db_name , sql_str ):
    con = sqlite3.connect( db_name )
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute( sql_str )
    r = cur.fetchone()
    return r.keys()
