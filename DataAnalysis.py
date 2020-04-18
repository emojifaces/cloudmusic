import db
import jieba.analyse
import collections
import csv
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image
from SaveChart import save_to_bar,save_to_pie





jieba.load_userdict('./dict.txt')
stopwords = [line.strip() for line in open('./stopwords.txt',encoding='utf-8').readlines()]

def count_word():
    all_lyric = ""
    words = []
    lyric_tuple = db.get_all_lyric()
    for item in lyric_tuple:
        all_lyric += item[0]
    word_list = jieba.cut(all_lyric)
    for word in word_list:
        if len(word) >= 2 and word not in stopwords:
            words.append(word)
    content = ' '.join(words)
    mycount = collections.Counter(words)
    with open('./result/count_word_EN.csv','a',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['word', 'frequency'])
        for key, val in mycount.most_common(300):
            writer.writerow([key, val])
            print(key, val)
    save_to_bar('./result/count_word_EN.csv','国外rapper常用词汇','./result/国外rapper常用词汇条形图.html',11)
    save_to_pie('./result/count_word_EN.csv', '国外rapper常用词汇', './result/国外rapper常用词汇饼状图.html', 31)
    return content


def count_artist_word(artist_name):
    lyric_tuple = db.get_lyric(artist_name)
    all_lyric = ""
    words = []
    for item in lyric_tuple:
        all_lyric += item[0]
    word_list = jieba.cut(all_lyric)
    for word in word_list:
        if len(word) >= 2 and word not in stopwords:
            words.append(word)
    content = ' '.join(words)
    mycount = collections.Counter(words)
    with open(f'./result/artist_EN/{artist_name}.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['word', 'frequency'])
        for key, val in mycount.most_common(100):
            writer.writerow([key, val])
            print(key, val)

    save_to_bar(f'./result/artist_EN/{artist_name}.csv', f'{artist_name}常用词汇',
                f'./result/artist_EN/{artist_name}常用词汇条形图.html', 11)
    save_to_pie(f'./result/artist_EN/{artist_name}.csv', f'{artist_name}常用词汇',
                f'./result/artist_EN/{artist_name}常用词汇饼状图.html', 11)

    return content


def get_wordcloud(content,background,res):
    content_all = content
    img = Image.open(background)  # 打开图片
    img_array = np.array(img)  # 将图片装换为数组

    cloud = WordCloud(
        font_path="STXINWEI.TTF",
        background_color='white',
        mask=img_array,
        max_words=100,
        max_font_size=80,
        min_font_size=20,
        width=1200,
        height=720
    )
    word_cloud = cloud.generate(content_all)
    word_cloud.to_file(res)
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()

    pass

if __name__ == '__main__':

    artist_tuple = db.get_all_artist()
    for artist in artist_tuple:
        artist_name = artist[0]
        content = count_artist_word(artist_name)
        back = 'image/x.png'
        res = f'./result/wordcloud/{artist_name}.png'
        get_wordcloud(content,back,res)

    content_all = count_word()
    get_wordcloud(content_all,'image/2.jpg','./result/wordcloud/EN.png')

    pass