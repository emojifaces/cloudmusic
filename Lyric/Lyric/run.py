from scrapy import cmdline

name = 'cloudmusic'
# name = 'test'

cmd = f'scrapy crawl {name}'
cmdline.execute(cmd.split())