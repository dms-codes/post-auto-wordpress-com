from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from conf import *
import pandas as pd 
import time

HASHTAG_REPLACE_CHARS = ['(',')',':',';','!','#','%','^','&','*','{','}',
                         '[',']','<','>',',','.','?','/','-',' ']
COLUMNS = ['Error Message', 'Product ID', 'Nama Produk', 'URL', 'Deskripsi Produk',
       'Minimum Pemesanan *', 'Etalase Kode', 'Waktu Proses Preorder',
       'Kondisi*', 'Asuransi Pengiriman*', 'Gambar 1*', 'Gambar 2', 'Gambar 3',
       'Gambar 4', 'Gambar 5', 'URL Video Produk 1', 'URL Video Produk 2',
       'URL Video Produk 3', 'Kurir Pengiriman', 'Unnamed: 19']

def read_xlsx():
    df = pd.read_excel('data.xlsx',skiprows=2)
    df.columns = COLUMNS
    return df
    
def get_wp_client():
    wp = Client(f'{HOME_URL}/xmlrpc.php',USERNAME,PASSWORD)
    return wp

def get_user_info(wp):
    return wp.call(GetUserInfo())

def create_wp_post(wp,title, content,post_tags=' ', categories=' '):
    post = WordPressPost()
    post.title = title
    post.content = content
    #post.terms_names = {
     #   'post_tag' : ,
     #   'category' : categories
    #}
    post.post_status = 'publish'
    wp.call(NewPost(post))
    #print(post.link)
    #return post.link

def get_hashtag(title):
    checkwords = ['by','dalam','in','untuk','for','kepada','to','ke','from','pada','above','on','into',
                  'di','dan','and','or','through',
                  'atau','lewat','melalui','terhadap',
                  'para','oleh','yang',
                  'sekitar','dengan','seputar']
    try:
        title = title.replace(':','')
        hashtag = ''
        for t in title.lower().split(' '):
            if t not in HASHTAG_REPLACE_CHARS:
                if t[0] not in '0123456789':
                    if t not in checkwords:
                        hashtag +=f'#{t} '
        return hashtag
    except:
        return ''
    
def get_content(title,url,deskripsi,img):
    hashtag = get_hashtag(title)
    html = f'<h1>{title} {hashtag}</h1><br>'
    html += f'<a href="{url}>{url}</a><br>'
    html += f'<p>{hashtag}</p><br><br>'
    html += f'<p>{deskripsi}</p><br>'
    html += f'<img src="{img}"></img>'
    return html, hashtag

def run(startfrom):
    wp = get_wp_client()
    df = read_xlsx()
    df = df[startfrom-1:]
    for index,data in df.iterrows():
        title = data['Nama Produk']
        url = data['URL']
        deskripsi = data['Deskripsi Produk']
        img = data['Gambar 1*']
        content,hashtag = get_content(title,url,deskripsi,img)
        start_to_finish_time = (len(df)+startfrom-1) * 2.0000 * 60 
        passed_time = (startfrom+index) * 2.0000 * 60
        seconds = start_to_finish_time - passed_time
        #print(start_to_finish_time,passed_time,seconds)
        min,sec = divmod(seconds,60)
        hour,min = divmod(min,60)
        print(f'{index+1}/{(len(df)+startfrom-1)} {title} {hour} hours and {min} minutes to go.')
        create_wp_post(wp,f'{title} {hashtag}',content)
        time.sleep(2*60)
        
if __name__ == '__main__':
    #read_xlsx()
    run(107)
