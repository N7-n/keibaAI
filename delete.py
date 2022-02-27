import sqlite3

try:
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    cur.execute('DELETE FROM data')
    con.commit()
    print('処理が完了しました')
except:
    print('処理が失敗しました') 
