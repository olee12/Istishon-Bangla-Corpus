
import requests;
from astropy.extern.bundled.six import print_
from bs4 import BeautifulSoup;
from builtins import print
import os
import errno

def make_sure_path_exists(path):
    try:
        os.makedirs(path);
        return 1;
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return 0;
        else:
            return 1;

file_names = dict();

def validate(ulr):
    if ulr[0]=='h':
        return ulr;
    else :
        return "https://www.istishon.com"+ulr;
def fixTitle(title):
    #print("title : "+title);
    title = title.replace("“","_");
    title = title.replace("”","_");
    title = title.replace("\\","_");
    title = title.replace("/","_");
    title = title.replace(":","_");
    title = title.replace("*","_");
    title = title.replace("?","_");
    title = title.replace("\"","_");
    title = title.replace("<","_");
    title = title.replace(">","_");
    title = title.replace("|","_");
    title = title.replace(".","_");
    #print("after : "+title);
    return title;



def goo_for_it(max_page):
    make_sure_path_exists("Data")
    page = 399;
    cnt = 0;
    page_error = 0;

    while page <= max_page :
        print("page : "+str(page));
        print("Cnt : "+str(cnt));
        url = "https://www.istishon.com/?q=node&page="+str(page);
        print("my link to new page : "+url)
        try:
            source_code = requests.get(url);
        except Exception as e:
            page_error+=1;
            if page_error > 10:
                page+=15;
                page_error = 0;
            continue;
        plain_text = source_code.text;
        #print(plain_text);
        soup = BeautifulSoup(plain_text,'lxml');

        for link in soup.findAll('div', {'class': 'node node-blog node-promoted node-teaser '}):
            #title = link.string;
            #href = link.findall('a');
            #print(title);
            #print(href[0].get('href'));
            #print(link);
            mysoup = BeautifulSoup(str(link), 'lxml');
            post_link = "";
            post_name = "";
            author = "";
            post_date = "";
            for link1 in mysoup.findAll('h2', {"class": "title"}):
                tolink = BeautifulSoup(str(link1), 'lxml');
                ll = tolink.findAll('a');
                post_name = str(tolink.find('a').string);
                print("my link to post "+post_name);
                post_link = str(validate(ll[0].get('href')));
                print(post_link);
            for link1 in mysoup.findAll('span', {'class': 'username'}):
                #print(link1);
                tolink = BeautifulSoup(str(link1), 'lxml');
                author = str(tolink.get_text());
                print("author " + author);
            for link1 in mysoup.findAll('span', {'property': 'dc:date dc:created'}):
                # print(link1);
                tolink = BeautifulSoup(str(link1), 'lxml');
                post_date = str(tolink.get_text());
                print("date " + post_date);
            print("---------------");
            print(post_name+" " + post_link +" "+ author);
            print("********************");
            post_name = fixTitle(post_name);
            author = fixTitle(author);
            post_date = fixTitle(post_date);
            get_single_item_data(post_link,post_name,author,post_date);
            cnt+=1;
        page+=1;

def get_single_item_data(item_url,title,author,date=""):

    mystring = "";
    try :
        source_code = requests.get(item_url);
    except Exception as e:
        return ;
    plain_text = source_code.text;
    soup = BeautifulSoup(plain_text, 'lxml');

    for link in soup.findAll('div', {"class": "field-item even"}):
        text = BeautifulSoup(str(link), 'lxml').get_text();
        lines = text.split("\\n");
        #print(text);

        leng = len(lines);
        if leng <= 0 :
            return ;
        now = 0;
        while now < leng :
            mystring+=lines[now];
            mystring+="\n"
            now+=1;
        break;

    folder = author;

    root_path = "Data" + "\\" + folder
    if make_sure_path_exists(root_path)==0:
        return ;
    #try:
        #file_names[folder] = file_names[folder] + 1;
    #except KeyError:
        #file_names[folder] = 1;
    number = len(os.listdir("./"+root_path)) + 1;
    import random;
    rndNumber = random.randint(1,10000);
    file_name = title+"_"+folder+"_"+str(rndNumber)+"_"+"["+date+"]"+"_"+str(number) + ".doc";
    print("File name" + file_name);
    path = root_path+"\\" + file_name;
    try:
        fw = open(path, 'w', encoding='utf8');
    except :
        return ;
    try:
        fw.write(title);
        fw.write("\n");
        fw.write("\n");
        fw.write("\n");
        fw.write(mystring);
    except :
        fw.close();
    fw.close();


make_sure_path_exists("./Data");
goo_for_it(500);
