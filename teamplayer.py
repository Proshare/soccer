import os

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import csv
from bs4 import BeautifulSoup


# 负责每个页面的内容抓取
def get_page_source(url):
    # 设置头部访问信息
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable--gpu')
    browser = webdriver.Chrome(options=chrome_options)

    browser.get(url)
    page_source = browser.page_source
    # yield page_source 生成器
    return page_source

# def get_page_source(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.text
#         return None
#     except ConnectionError:
#         print('Error occurred')
#         return None

def get_page_list():
    page_source = get_page_source('https://soccer.hupu.com/')
    # 通过soup解析所有球队网页信息
    soup = BeautifulSoup(page_source, 'lxml')
    # 获取每个球队的网址
    team_player_list = soup.find_all('li', attrs={'class': 'hp-dropDownMenu'})
    for hrefs in team_player_list[2:6]:
        href = hrefs.find('a')

        print("访问" + href['title'] + '网址：' + href['href'])

        get_player_list(href['href'], href['title'])


# 获取每个足球联盟的足球队员页面的list
def get_player_list(url, league):
    page_source = get_page_source(url)
    # 清理一下html数据
    soup = BeautifulSoup(page_source, 'lxml')
    teamlist = soup.find('ul', attrs={'class': 'england-list-item'})
    teams = teamlist.find_all('li')
    # 爬取页面
    for team in teams:
        # 每一个足球队
        hrefs = team.find('a')
        print('正在爬取', hrefs['title'], '网址：', hrefs['href'])
        teamname = hrefs.get_text()
        # print(league)
        get_player_info(hrefs['href'], league, teamname)


# 获取球员详细信息
def get_player_info(url, league, team):
    page_source = get_page_source(url)
    # 清理一下html页面数据
    soup = BeautifulSoup(page_source, 'lxml')
    # 创建一个字典
    teamplayerscore = []
    tables = soup.find_all('table', attrs={'class': 'team_player'})

    for table in tables:
        trs = table.find_all('tr')
        for tr in trs[1:]:
            item = {}
            # 获取每个比赛的相关信息
            tdsc = tr.find_all('td')
            item['number'] = tdsc[0].get_text()
            item['name'] = tdsc[1].get_text()
            item['Ename'] = tdsc[2].get_text()
            item['age'] = tdsc[3].get_text()
            item['national'] = tdsc[4].get_text()
            item['position'] = tdsc[5].get_text()
            item['first_start'] = tdsc[6].get_text()
            item['alternate'] = tdsc[7].get_text()
            item['rescue'] = tdsc[8].get_text()
            item['assists'] = tdsc[9].get_text()
            item['yellow'] = tdsc[10].get_text()
            item['red'] = tdsc[11].get_text()

            teamplayerscore.append(item)

    filenames = ["number", "name", "Ename", "age", "national",
                 "position", "first_start", "alternate", "rescue", "assists", "yellow", "red"]
    print('开始保存' + team + '足球队比赛信息')

    if not os.path.exists(league):
        os.makedirs(league)
    root_path = os.getcwd()
    # 获取目前的路径
    os.chdir(root_path)
    for list in teamplayerscore:
        # 以字典的形式写入文件

        with open(league + '/' + team + ".csv", "a", errors="ignore", newline='') as fp:
            f_csv = csv.DictWriter(fp, fieldnames=filenames)
            f_csv.writerow(list)
        os.chdir(root_path)
    print('结束保存' + team + '足球队比赛信息')


def main():
    # get_player_list('https://soccer.hupu.com/england/')
    get_page_list()

    # get_player_info('https://soccer.hupu.com/teams/135', '英超', '曼城')


if __name__ == '__main__':
    main()
