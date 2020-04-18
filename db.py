import pymysql

db = pymysql.connect(host='localhost',
                     user='root',
                     password='root',
                     db='cloudmusic',
                     port=3306,
                     charset='utf8')


def get_all_lyric():

    with db.cursor() as cursor:
        sql = "select lyric from music_en"
        cursor.execute(sql)
        res = cursor.fetchall()
        return res

def get_lyric(artist_name):
    with db.cursor() as cursor:
        sql = f'''select lyric from music_en where artist_name="{artist_name}"'''
        cursor.execute(sql)
        res = cursor.fetchall()
        return res

def get_all_artist():
    with db.cursor() as cursor:
        sql = "select distinct artist_name from music_en"
        cursor.execute(sql)
        res = cursor.fetchall()
        return res

if __name__ == '__main__':
    pass

