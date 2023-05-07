import pymysql
from wordcloud import WordCloud
import jieba


def remove_stop_words(f):
    stop_words = [k.strip() for k in open('./stopword.txt', encoding='utf8').readlines() if k.strip() != '']

    for stop_word in stop_words:
        f = f.replace(stop_word, '')
    return f

# 生成词云
def create_word_cloud(name,f):
	print('根据词频，开始生成词云!')
	f = remove_stop_words(f)
	cut_text = " ".join(jieba.cut(f,cut_all=False, HMM=True))
	wc = WordCloud(
        background_color='white',
		font_path="./text.ttf",
		max_words=100,
		width=2000,
		height=1200,
    )
	print(cut_text)
	wordcloud = wc.generate(cut_text)
	# 写词云图片
	wordcloud.to_file('D:\\projs\\scrapy\\mymusic\\public\\'+name+'.jpg')

if __name__=='__main__':
     conn = pymysql.connect(
        host='localhost',
        user='root',
        password='952088z,',
        db='music',
        charset='utf8mb4',
        # autocommit=True,   
    ) 
     with conn:	
        cur = conn.cursor()
        sql_info = "select * from info;"
        cur.execute(sql_info)  

        all=cur.fetchall()
        song=''
        for i in all:
            songid = i[0]
            text = i[4]
            
            if text=='':
                sql = "delete from info where songid=%s"
                arg = (songid)
                cur.execute(sql,arg)
                conn.commit()
                continue
            text=text.replace(u'<br>', u' ')
            song = song + ' '+ text
            create_word_cloud(songid,text)

            fin = open('D:\\projs\\scrapy\\mymusic\\public\\'+songid+'.jpg','rb')
            img = fin.read()
            fin.close()
            # img = pymysql.Binary(img)

            sql="update info set img=%s where songid=%s"
            arg = (img,songid) 
            cur.execute(sql,arg)
            conn.commit()

        create_word_cloud("mymusic",song)

        sql_singer = "select singer from info group by singer order by count(*) desc limit 10;"
        cur.execute(sql_singer)
        singers=cur.fetchall()
        for singer in singers:
            sql = "select * from info where singer='%s'" % (singer)
            cur.execute(sql)
            info = cur.fetchall()
            texts=''
            name=info[0][2]
            for i in info:
                text = i[4]
                text=text.replace(u'<br>', u' ')
                texts=texts+' '+text
            create_word_cloud(name,texts)

        sql_belong = "select belong from info group by belong order by count(*) desc limit 10;"
        cur.execute(sql_belong)
        belongs=cur.fetchall()
        for belong in belongs:
            sql = "select * from info where belong='%s'" % (belong)
            cur.execute(sql)
            info = cur.fetchall()
            texts=''
            name=info[0][3]
            for i in info:
                text = i[4]
                text=text.replace(u'<br>', u' ')
                texts=texts+' '+text
            create_word_cloud(name,texts)

        cur.close()