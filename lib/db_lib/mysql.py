#coding:utf-8
import MySQLdb

def execute(db_name,sql_str ):
    con = get_con(db_name)
    cur = con.cursor()
    #print( sqlStr%(tbl,cols))
    cur.execute( sql_str )
    con.commit()
    cur.close()
    con.close()

def create(db_name,tbl_name,fields):
    con = get_con( db_name )
    sql_str = "create table %s ( %s )"%(tbl_name,fields)
    cur = con.cursor()
    cur.execute( sql_str )
    con.commit()
    cur.close()
    con.close()

def select(db_name,sql_str):
    con = get_con(db_name)
    #con.execute("SET NAMES utf8")
    cur = con.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SET NAMES utf8")
    cur.execute(sql_str)
    fetch = cur.fetchall()
    return fetch

def insert(db_name,tbl_name,values ):
    con = get_con(db_name)
    cur = con.cursor()
    sqlStr = "insert into %s values ( %s )"
    cur.execute( sqlStr%(tbl_name,values))
    con.commit()
    cur.close()
    con.close()

def delete( db_name, sql_str ):
    con = get_con( db_name )
    cur = con.cursor()
    cur.execute( sql_str )
    con.commit()
    cur.close()
    con.close()

def update( db_name,tbl_name, values , keys ):
    con = get_con( db_name )
    cur = con.cursor()
    cur.execute( "update %s set %s where %s"%(tbl_name,values,keys) )
    con.commit()
    cur.close()
    con.close()

def get_con(db_name):
    con = MySQLdb.connect(host="localhost" , db=db_name , user="mp015v", passwd="wtbtsy5701",charset="utf8")
    con.cursorclass =MySQLdb.cursors.DictCursor

    return con