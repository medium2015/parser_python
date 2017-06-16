#-*- coding:utf-8 -*-
import pycurl
from io import BytesIO
import re
import tkinter.ttk as ttk
import tkinter
from PIL import Image, ImageTk

item_count=4
main_dict={\
2:{'name':'Плитка','url':'http://keramasvit.com.ua/plitka','parent_id':''},\
3:{'name':'Сантехника','url':'http://keramasvit.com.ua/cantexnika','parent_id':''},\
4:{'name':'Акции','url':'http://keramasvit.com.ua/akciyi','parent_id':''}\
}
check_dict={\
2:True,\
3:True,\
4:True\
}
word_list1={}

def main_event(el_id):
    global im
    text.delete(1.0,'end')
    global word_list
    buf = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, main_dict[el_id]['url'])
    print(main_dict[el_id]['url'])
    c.setopt(c.WRITEDATA,buf)
    c.perform()
    buf1= buf.getvalue().decode('utf-8')
    title_tag=re.compile('<title>(.+?)</title>')
    meta_tag=re.compile('<meta name="description" content=" (.+?)" />')
    meta2_tag=re.compile('<meta name="keywords" content=" (.+?)" />')
    h1_tag=re.compile('<h1>(.+?)</h1>')
    h3_tag=re.compile('<h3>(.+?)</h3>')
    h4_tag=re.compile('<h4>(.+?)</h4>')
    span_tag=re.compile('<span itemprop="title">(.+?)</span>')
    span2_tag=re.compile('<font color="#444">(.+?)</font>')
    name_tag=re.compile('<h1>(.+?)</h1>')
    whomade_tag=re.compile('Виробник:.(.+?)<')
    model_tag=re.compile('К.лекція: (.+?)<')
    articul_tag=re.compile('.+Артикул виробника:.(.+?)<')
    price_tag=re.compile('                (.+?).грн\n')
    opis_tag=re.compile('<strong>Опис.+?\n.+?\n.+?\n.+?\n(.+?)<')
    haract_tag=re.compile('<strong>Характеристики([\s\S]+?[^</div>\n\t]?)<div id="tab-attribute" class="tab-content">')
    vidguk_tag=re.compile('<img src="catalog/view/theme/default/image/stars-5.png" alt=".+?" /><br />\n(.+?)</p>')
    zobragh_tag=re.compile('<img src="(.+?)" width="330" height="275"')
    dop_zobragh_tag=re.compile('class="fancybox" rel="fancybox"><img src="(.+?)"')
    posul_tag=re.compile('<div class="name"><a href="(.+?)">')
    word_list={}
    
    word_list['title']=re.findall(title_tag,buf1)[0]
    word_list['meta_tag']=re.findall(meta_tag,buf1)
    word_list['keywords']=re.findall(meta2_tag,buf1)
    word_list['h1']=re.findall(h1_tag,buf1)
    word_list['h3']=re.findall(h3_tag,buf1)
    word_list['h4']=re.findall(h4_tag,buf1)
    
    word_list['span']=re.findall(span_tag,buf1)
    word_list['span2']=re.findall(span2_tag,buf1)
    word_list['name']=re.findall(name_tag,buf1)
    word_list['virobnik']=re.findall(whomade_tag,buf1)
    word_list['model']=re.findall(model_tag,buf1)
    word_list['articul']=re.findall(articul_tag,buf1)   
    word_list['price']=re.findall(price_tag,buf1)
    word_list['price']=word_list['price'][0].replace(" ","",1).replace(",", ".", 1)
    word_list['description']=re.findall(opis_tag,buf1)
    l=word_list.get('description')
    if len(word_list.get('description')) != 0:        
        m=l[0]
        m=m.replace("<div>",'')
        m=m.replace("</div>",'')
        m=m.replace("<strong>",'')
        m=m.replace("</strong>",'')
        m=m.replace('\n',' ')
        m=m.replace('\t','')
        m=m.replace("&nbsp;",'')
        m=m.replace("(<a href=\"http://keramasvit.com.ua/krishka-opoczno-bilbao-slow-closing-ok-98-0003.html\">","")
        word_list['description']=m
    word_list['haracteristika']=re.findall(haract_tag,buf1)
    l=word_list.get('haracteristika')
    if len(word_list.get('haracteristika')) != 0:
        m=l[0]
        m=m.replace('<br />','')   
        m=m.replace('</div>','')
        m=m.replace('<div>','')
        m=m.replace(';','')
        m=m.replace('\n',' ')
        m=m.replace('\t','')
        m=m.replace('<span>','')
        m=m.replace('</span>','')
        m=m.replace('</strong>','')
        m=m.replace('&nbsp','')
        m=m.replace('<strong>','')
        word_list['haracteristika']=m
    word_list['otzuvu']=re.findall(vidguk_tag,buf1)
    word_list['image']=re.findall(zobragh_tag,buf1)
    word_list['dop image']=re.findall(dop_zobragh_tag,buf1)
    word_list['links']=re.findall(posul_tag,buf1)
    izobr = ''
    izobr = word_list['image'][0]
    added_pict=word_list['dop image']
    title = word_list['title']
    buf2 = BytesIO()
    c1 = pycurl.Curl()
    izobr=str(izobr)
    izobr=izobr.encode('utf8')
    izobr=str(izobr)
    izobr=izobr.replace('\\x','%').replace(' ','%20')
    izobr=izobr[2:-1]
    print(izobr)
    c1.setopt(c1.URL,izobr)   
    c1.setopt(c1.FOLLOWLOCATION, True)
    #c.setopt(c.PROXY,'ekit-proxy:8080')
    c1.setopt(c1.WRITEDATA,buf2)
    c1.perform() 
    f = open('D:\VisualStudioProjects\\'+title+'.jpg','wb')
    f.write(buf2.getvalue())
    f.close()
    buf2.close()
    buf.close()
    for i in word_list:
        print(i,word_list[i])
    for i in word_list:
        text.insert('end', u"\n"+str(i)+' '+str(word_list[i])+"\n")
    im = ImageTk.PhotoImage(Image.open('D:\VisualStudioProjects\\'+title+'.jpg'))
    text.image_create('end', image=im)
    for j in range(len(added_pict)):
        buf2 = BytesIO()
        c1.setopt(c1.URL, added_pict[j])
        c1.setopt(c1.FOLLOWLOCATION, True)
        c1.setopt(c1.WRITEDATA,buf2)
        c1.perform()
        f = open('D:\VisualStudioProjects\\'+title+str(j)+'.jpg','wb')
        f.write(buf2.getvalue())
        f.close()
        buf2.close()
    buf2.close()

def privet():
    print('Hello')
    text.insert('end', u"\nHello")  
def poka():
    text.insert('end', u"\nGoodbye")
    print('Goodbye')
def quit1():
    root.destroy()
def help1():
    text.insert('end', u"\nGod will help you")
    print("God will help you")

def Get(event):
    item=tree.focus()
    if item:
        id = int(item)
        print(str(id))
        getChildren(id)

def getChildren(el_id):
    global check_dict
    global main_dict
    global item_count
    buffer = BytesIO()
    c = pycurl.Curl()
    print(el_id)
    url = main_dict[el_id]['url']
    print(url)
    print(check_dict[el_id])
    if check_dict[el_id] == True:
        check_dict[el_id] = False
        c.setopt(c.URL, main_dict[el_id]['url'])
        c.setopt(c.WRITEDATA, buffer)
        print('start grabber')
        c.perform()
        print('finish grabber')
        buf = buffer.getvalue().decode('utf-8')
        all_sant=re.compile('<div class="category_name"><a href="(.+?)">(.+?)</a>',re.DOTALL)
        all_results=re.findall(all_sant, buf)
        print('01')
        if not all_results:
            all_proizv=re.compile('<li class="category-.+?"><a href="(.+?)"><span></span>(.+?)</a></li>',re.DOTALL) #проверяем, если был выбран производитель
            all_results=re.findall(all_proizv, buf)
            print('02')
            if not all_results:
                all_proizv=re.compile('<a href="(.+?brand.+?)"><span>(.+?)\s</span></a>',re.DOTALL) #заполняем производителями
                all_results=re.findall(all_proizv, buf)
                print('03')
            else:
                all_pages=re.compile('</div><div class="results">Показано 1 по 21 із .+? \(всього сторінок: (.+?)\)</div></div>', re.DOTALL) #ищем количество страниц
                all_results=re.findall(all_pages, buf)
                print(all_results)
                if all_results:         
                    i=int(all_results[0])
                    last_page = i
                    print(last_page)
                    all_results = []
                    for i in range(int(last_page)):
                        buffer = BytesIO()
                        c.setopt(c.URL, main_dict[el_id]['url']+'?page='+str(i+1))
                        print(main_dict[el_id]['url']+'?page='+str(i+1))
                        c.setopt(c.WRITEDATA, buffer)
                        c.perform()
                        buf = buffer.getvalue().decode('utf-8')
                        all_tovari=re.compile('</a></div>\n.+?<div class="name"><a href="(.+?)">(.+)</a></div>\n.+?"description') #имя и ссылка на товар на странице
                        all_results+=re.findall(all_tovari, buf)
                else:
                    all_tovari=re.compile('</a></div>\n.+?<div class="name"><a href="(.+?)">(.+)</a></div>\n.+?"description') #имя и ссылка на товар на странице
                    all_results=re.findall(all_tovari, buf)
            obj_opis=[]
            obj_opis = re.compile('class="fancybox" rel="fancybox"><img src="(.+?)"')
            print('smotri suda'+str(re.findall(obj_opis, buf)))
            if re.findall(obj_opis, buf):
                main_event(el_id)
            else:
                print('ne rabotaet')
        for result in all_results:
            item_count+=1
            main_dict[item_count]={'name':result[1],'url':result[0],'parent_id':str(el_id)}
            check_dict[item_count]=True
            tree.insert(str(main_dict[item_count]['parent_id']), item_count, str(item_count), text=main_dict[item_count]['name'])
    else:
        print('ne vishlo')

root=tkinter.Tk()
menubar = tkinter.Menu(root)
tree= ttk.Treeview(root)
for el_id in main_dict.keys():
    tree.insert(str(main_dict[el_id]['parent_id']), int(el_id), str(el_id), text=main_dict[el_id]['name'])
tree.bind('<Button-1>', Get)
text = tkinter.Text(root)
text.pack(side = 'right')
tree.pack(side = 'left')
filemenu = tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label="Hello", command=privet)
filemenu.add_command(label="Goodbye", command=poka)
menubar.add_cascade(label="File", menu=filemenu)
menubar.add_command(label='Exit',command=quit1)
menubar.add_command(label='Help',command=help1)
root.config(menu=menubar)
xscrollbar = tkinter.Scrollbar(root, orient="horizontal",command=tree.xview)
xscrollbar.pack(side='bottom',fill='x')
yscrollbar = tkinter.Scrollbar(root, orient="vertical",command=tree.yview)
yscrollbar.pack(side='right',fill='y')
tree.configure(xscrollcommand=xscrollbar.set)
tree.configure(yscrollcommand=yscrollbar.set)
root.mainloop()
