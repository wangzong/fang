#!C:\Program Files\Python35\python.exe
import requests
from bs4 import BeautifulSoup
import re
import chardet


def trim(string):
    string = string.strip()
    string = re.sub('\s+', '', string)
    return (string)


def get_house_links(uni_html):
    soup = BeautifulSoup(uni_html,"lxml")

    houseitems = soup.find_all(name="dd",attrs={"class":"info rel floatr"})

    house_links = []

    for houseitem in houseitems:
        house_links.append("http://esf.suzhou.fang.com" + houseitem.p.a["href"])

    return(house_links)


def get_house_detail(uni_html):
    soup = BeautifulSoup(uni_html,"lxml")


    mainbox = soup.find_all(name="div", attrs={"class": "main clearfix"})

    title = mainbox[0].find("h1")
    title_str = trim(title.text)
    print("title",title_str)

    train_note = mainbox[0].find(name = "span", attrs = {"class":"train note"})
    train_note_str = train_note.text
    print("train_note",train_note_str)

    id = mainbox[0].find(name="span",attrs={"class":"mr10"})
    id_str = id.text
    print("id",id_str)

    # publish_time = mainbox[0].find(name = "p", attrs = {"class":"gray9"})
    # publish_time_str = publish_time.contents[7]
    # publish_time_str = trim(publish_time_str)
    # print("发布时间：",publish_time_str)

    price = mainbox[0].find(name="dt", attrs={"class": "gray6 zongjia1"})
    price_str = price.contents[3].text
    print("总价:", price_str)

    l = mainbox[0].find_all(name="dd", attrs={"class": "gray6"})
    layout_str = l[1].contents[1]
    print("户型:", layout_str)

    area_str = l[2].contents[1].text
    print("面积：", area_str)

    phone_number = mainbox[0].find(name="label", attrs={"id": "mobilecode"})
    phone_number_str = phone_number.text
    print("联系电话：", phone_number_str)

    house_info = soup.find(name="div", attrs={"class": "inforTxt"})

    dd = house_info.find_all("dd")
    # print(dd)
    year_str = dd[4].contents[2]
    print(year_str)

    direction_str = dd[5].contents[2]
    print(direction_str)

    layer_str = dd[6].contents[2]
    print(layer_str)

    deco_str = dd[7].contents[2]
    print(deco_str)

    type_str = dd[8].contents[2]
    print(type_str)

    property_type = dd[9].contents[2]
    print(property_type)

    dt = house_info.find_all("dt")

    community_name = dt[1].contents[1].text
    print(community_name)

    school = soup.find(name="div", attrs={"class": "schoolLinkWrap"})
    school_str = trim(school.text)
    print(school_str)


def page2unicode(html):
    charset = chardet.detect(html)
    chartype = charset['encoding']
    # print(chartype)

    if chartype.find("UTF") >= 0:
        unicode_html = html
    else:
        unicode_html = html.decode('gbk')
    return(unicode_html)

# index_page_url = "http://esf.suzhou.fang.com/house-a0277-b03996/i31-j340/"

index_page_url_prefix = "http://esf.suzhou.fang.com/house-a0277-b03996/i3"
index_page_url_postfix = "-j340/"

out_file = r"houselist.txt"
writer = open(out_file, 'w', encoding='utf-8')

page_links=[]

urls = {}
urls['http://esf.suzhou.fang.com/house/i31/']=1

try:
    h_links = []
    for i in range(1,2,1):
        index_page_url = index_page_url_prefix + str(i) + index_page_url_postfix
        print(index_page_url)

        response = requests.get(index_page_url)
        page = response.content

        unicode_page = page2unicode(page)

        new_h_links = get_house_links(unicode_page)
        for new_h_link in new_h_links:
            h_links.append(new_h_link)
        # print(h_link)

    # print(soup)
except Exception as e:
    print(e)

for h_link in h_links:
    print(h_link)
    response = requests.get(h_link)
    page = response.content
    unicode_page = page2unicode(page)
    house_detail_str = get_house_detail(unicode_page)
    # print(house_detail_str)

writer.close()