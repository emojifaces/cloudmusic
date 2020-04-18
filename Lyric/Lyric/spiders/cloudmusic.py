# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.utils.project import get_project_settings
from scrapy import Request
from urllib.parse import quote
import re
import json
from Lyric.items import LyricItem
import copy




class CloudmusicSpider(Spider):
    name = 'cloudmusic'
    allowed_domains = ['music.163.com']
    base_urls = 'http://localhost:3000/search?keywords=%s&type=100'


    def start_requests(self):
        # 获取配置文件
        settings = get_project_settings()
        for keyword in settings.get('KEYWORDS_EN'):
            # 拼接url地址并返回Request对象
            url = self.base_urls % (quote(keyword))
            yield Request(url=url, callback=self.parse)


    def parse(self, response):

        item = LyricItem()
        artist_json = json.loads(response.text)
        artist_id = artist_json.get('result').get('artists')[0].get('id')
        artist_name = artist_json.get('result').get('artists')[0].get('name')
        print(f'正在爬取------歌手ID：{artist_id}，歌手名字：{artist_name}')
        albums_url = f'https://music.163.com/artist/album?id={artist_id}&limit=9999'
        item['artist_id'] = artist_id
        item['artist_name'] = artist_name
        yield Request(url=albums_url, callback=lambda rsp, it=item: self.parse_albums(response=rsp, item=it))


    def parse_albums(self,response,item):

        album_url_list = response.xpath('//ul[@id="m-song-module"]/li/div/a[@class="msk"]/@href').extract()
        album_id_list = [re.search(r'id=(\d+)',album_url).group(1) for album_url in album_url_list]
        album_num = len(album_url_list)
        img_url = response.xpath('//div[@class="n-artist f-cb"]/img/@src').extract_first()
        item['album_num'] = album_num
        item['img_url'] = img_url
        for album_id in album_id_list:
            album_url = f'http://music.163.com/api/album/{album_id}'
            yield Request(url=album_url,callback=lambda rsp, it=item: self.parse_album(response=rsp, item=it))

    def parse_album(self,response,item):

        album_json = json.loads(response.text)
        songs_list = album_json.get('album').get('songs')

        for song in songs_list:
            it = copy.deepcopy(item)
            song_name = song.get('name')
            song_id = song.get('id')
            publish_time = song.get('album').get('publishTime')
            album_name = song.get('album').get('name')
            album_id = song.get('album').get('id')
            album_size = song.get('album').get('size')
            print(f'正在爬取------歌曲名：{song_name}，发布时间：{publish_time}，所属专辑：{album_name}，所属专辑ID：{album_id}，所属专辑歌曲数量：{album_size}')
            it['song_name'] = song_name
            it['song_id'] = song_id
            it['publish_time'] = publish_time
            it['album_name'] = album_name
            it['album_id'] = album_id
            it['album_size'] = album_size
            lyric_url = f'http://music.163.com/api/song/lyric?id={song_id}&lv=1&kv=1&tv=1'
            yield Request(url=lyric_url,callback=lambda rsp, it=it: self.parse_lyric(response=rsp, item=it))

    def parse_lyric(self,response,item):

        lyric_json = json.loads(response.text)
        try:
            lyric = lyric_json.get('lrc').get('lyric')
            item['lyric'] = lyric
            print(f'正在爬取------{item["artist_name"]}《{item["song_name"]}》歌词')
            yield item
        except:
            print('暂无歌词')
            return None

