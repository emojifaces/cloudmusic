# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Request
import re
import json
from Lyric.items import LyricItem
import copy



class TestSpider(Spider):
    name = 'test'
    allowed_domains = ['music.163.com']
    artist_id = ['31055', '13145283']

    def start_requests(self):

        for id in self.artist_id:
            url = f'https://music.163.com/artist/album?id={id}&limit=9999'
            yield Request(url=url, callback=self.parse,meta={"id":id})


    def parse(self, response):

        artist_name = response.xpath('//*[@id="artist-name"]/text()').extract_first()
        item = LyricItem()
        item['artist_id'] = response.meta.get("id")
        item['artist_name'] = artist_name
        print(f'正在爬取------{artist_name}')

        album_url_list = response.xpath('//ul[@id="m-song-module"]/li/div/a[@class="msk"]/@href').extract()
        album_id_list = [re.search(r'id=(\d+)', album_url).group(1) for album_url in album_url_list]
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
