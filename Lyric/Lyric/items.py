# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from scrapy import Item,Field

class LyricItem(Item):

    artist_id = Field()    # 歌手ID
    artist_name = Field()    # 歌手名
    img_url = Field()       # 歌手图片
    album_num = Field()     # 专辑数量
    album_size = Field()    # 专辑歌曲数量
    song_name = Field()      # 歌曲名
    song_id = Field()   # 歌曲ID
    album_name = Field()     # 所属专辑名
    album_id = Field()      # 专辑ID
    publish_time = Field()      # 发布时间
    lyric = Field()     # 歌词
