from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from conf import *
import pandas as pd 
import time

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
    hashtag = ''
    for t in title.lower().split(' '):
        if t[0] not in '0123456789':
            hashtag +=f'#{t} '
    return hashtag
    
def get_content(title,url,deskripsi,img):
    html = f'<h1>{title}</h1><br>'
    html += f'<a href="{url}>{url}</a><br>'
    hashtag = get_hashtag(title)
    html += f'<p>{hashtag}</p><br><br>'
    html += f'<p>{deskripsi}</p><br>'
    html += f'<img src="{img}"></img>'
    return html

def run():
    wp = get_wp_client()
    df = read_xlsx()
    for index,data in df.iterrows():
        title = data['Nama Produk']
        url = data['URL']
        deskripsi = data['Deskripsi Produk']
        img = data['Gambar 1*']
        content = get_content(title,url,deskripsi,img)
        print(content)
        create_wp_post(wp,title,content)
        time.sleep(5*60)
        
if __name__ == '__main__':
    #read_xlsx()
    run()
