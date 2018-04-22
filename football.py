# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 14:16:50 2018

@author: Roy Lee
"""
import requests, re, csv, datetime
from lxml import html
from bs4 import BeautifulSoup




def boring(url):
    global data_at, data_og, data_df, data_view
    global name_list, df_list,og_list, at_list
    global info_key,info_value,player_name, final_data, final_list
    data_view = []
    data_at = []
    data_df = []
    data_og = []
    name_list = []
    df_list = []
    at_list = []
    og_list = []
    info_value = []
    info_key = []
    player_name = []
    final_data = []
    final_list = []
    
    
    def get_data(url): 
        # 获取数据
        try:
            data = requests.get(url)
            data.raise_for_status()
        except:
            return "check your network" 
        
        # 解析页面
        sl = html.fromstring(data.text)
        soup = BeautifulSoup(data.text, "html.parser")
        
        
        # 匹配数据lalala
        dtimes = len(sl.xpath('//*[@id="summaryTable"]/tbody/tr'))#获取tr标签数量
     
        # 数据路径
        dpath  = '//*[@id="summaryTable"]/tbody/tr[{}]/td/text()'.format(dtimes) # view
        dpath2 = '//*[@id="summaryTable"]/tbody/tr[{}]/td/span/text()'.format(dtimes)# tag
        dtimes_at  = '//*[@id="offensiveTable"]/tbody/tr[{}]/td/text()'.format(dtimes) 
        dtimes_df  = '//*[@id="defensiveTable"]/tbody/tr[{}]/td/text()'.format(dtimes)
        dtimes_og  = '//*[@id="passTable"]/tbody/tr[{}]/td/text()'.format(dtimes)
        
        # 解析
        d1 = sl.xpath(dpath)
        d2 = sl.xpath(dpath2)
        d3 = sl.xpath(dtimes_at)
        d4 = sl.xpath(dtimes_df)
        d5 = sl.xpath(dtimes_og)
         
        
        # 数据归表
        data_view.append(re.findall(r"\d+\.?\d*|[-]+",str(d1)))
        data_view.append(re.findall(r"\d+\.?\d*",str(d2)))
        data_at.append(re.findall(r"\d+\.?\d*|[-]+",str(d3)))
        data_df.append(re.findall(r"\d+\.?\d*|[-]+",str(d4)))
        data_og.append(re.findall(r"\d+\.?\d*|[-]+",str(d5)))
        
            
        # 匹配行（column)名字 lalala
        view_name_path  = '//*[@id="summaryTable"]/thead/tr/th/text()'
        at_name_path = '//*[@id="offensiveTable"]/thead/tr/th/text()'
        df_name_path = '//*[@id="defensiveTable"]/thead/tr/th/text()'
        og_name_path = '//*[@id="passTable"]/thead/tr/th/text()'
        
        n  = sl.xpath(view_name_path)
        df  = sl.xpath(df_name_path)
        og  = sl.xpath(og_name_path)
        at = sl.xpath(at_name_path)
        
        name_list.append(n)
        df_list.append(df)
        og_list.append(og)
        at_list.append(at)
            
        # 
        p_info = soup.find_all("div", class_='player-info')
        p_soup = BeautifulSoup(str(p_info), "html.parser")
        for tag in p_soup.find_all(re.compile('^th')):
            info_key.append(tag.string)
        for tag in p_soup.find_all(re.compile('^td')):
            a = tag.stripped_strings
            for i in a:
                info_value.append(i)
        

        # 中文名
        player_path = '/html/body/div[3]/div[1]/div[1]/div[1]/div/h1/text()'
        nb = sl.xpath(player_path)
        
        pm =''.join(re.findall(r'[\u4e00-\u9fa5]', nb[0]))
        player_name.append(pm)
        # clean data  PROBLEM!!!!!
        return
           
    
    get_data(url)
    
    
    
        # DATA CLEANING IN STUPID WAY, SO WHAT, BITE ME?
    def cl(data):
        data = data[0]
        return data
    data_at = cl(data_at)
    data_df = cl(data_df)
    data_og = cl(data_og)
    name_list = cl(name_list)
    at_list  =  cl(at_list)
    og_list  = cl(og_list)
    df_list  = cl(df_list)      
        
             
    for a in(data_at, data_og, data_df):
        del a[0]
        del a[0]
    for i in ( df_list, og_list, at_list ):
        del i[-1]
        for x in range(3):
            del i[0] 
        
    shit = data_view.pop(1)
    data_view = data_view[0]
    dd = str(shit[1]),str(shit[0])
    data_view.insert(4, '/'.join(dd))
    data_view.insert(len(data_view), shit[-1])
        
    name_list.remove('赛事')  
    
    # INFO
    info_value[2] = ''.join(re.findall(r'[^\s]', info_value[2]))
    info_value[5] = ''.join(re.findall(r'[^\s]', info_value[5]))
    jj = info_value.pop(-2)    
    info_value[-2] = info_value[-2],jj      
    
    
        # CONCAT DATA
    fl = ['姓名']+ at_list + df_list + og_list + info_key     
    fd = player_name + data_at + data_df + data_og + info_value
    def uu(data_big, data_small):   # 避免重复数据
        for i in range(len(data_small)):
            if i not in [2,3,5]:
                data_big.append(data_small[i])
    uu(fd, data_view)
    uu(fl, name_list)
    final_data.append(fd)
    final_list.append(fl)
    final_data = cl(final_data)
    final_list = cl(final_list)    
        
    
    return 
    

if __name__ == "__main__":
    url = 'http://www.tzuqiu.cc/players/527/show.do'
    boring(url)
    
    
 #Get all players
try:
    start = datetime.datetime.now()
    for pl in range(35000,40001): 
        try:
            url = 'http://www.tzuqiu.cc/players/{}/show.do'.format(pl)
            boring(url)
            if pl == 1:
                with open('wenzi.csv', mode='w',encoding='utf_8_sig',newline='') as f:
                    writer = csv.DictWriter(f, final_list)
                    writer.writeheader()
            with open('wenzi.csv', mode='a',encoding='utf_8_sig',newline='' ) as f:
                writer = csv.writer(f)
                writer.writerow(final_data)
            print('%s players completed'%(pl))
        except:
            pass
    end = datetime.datetime.now()
    print(end-start)
except:
    pass
        




        


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        