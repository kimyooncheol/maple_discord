# -*- coding:utf-8 -*- 
import discord
import os
from discord.ext.commands import bot
import asyncio
import requests
import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from urllib import parse
from zeep import Client

client = discord.Client()
accese_token = os.environ["BOT_TOKEN"]
#팅패 정보
def get_InspectionInfo() :
    wsdl = 'http://api.maplestory.nexon.com/soap/maplestory.asmx?wsdl'
    client = Client(wsdl=wsdl)
    soapDate = client.service.GetInspectionInfo()
    a = str(soapDate)
    b = a.split('InspectionInfo')[1]
    c = str(b)
    strObstacleContents = str(c.split('strObstacleContents')[1])
    strObstacleContent = repo(strObstacleContents)
    DateTimes = str(c.split('startDateTime')[1]).replace(strObstacleContents,'')
    DateTime = re.findall(r"\d+", DateTimes)
    return strObstacleContent, DateTime
def repo(lists) :
    rep1 = str(lists)
    rep2 = rep1.replace("[","")
    rep3 = rep2.replace("]","")
    rep4 = rep3.replace("'","")
    rep5 = rep4.replace("{","")
    rep6 = rep5.replace("}","")
    rep7 = rep6.replace("\\n","")
    rep8 = rep7.replace(":","")
    return rep8
def DateTimeRe(DateTime) :
    startDate = []
    endDate = []
    startDate.append(DateTime[0]+'년')
    startDate.append(DateTime[1]+'월')
    startDate.append(DateTime[2]+'일')
    startDate.append(DateTime[3]+'시')
    startDate.append(DateTime[4]+'분')
    endDate.append(DateTime[7]+'년')
    endDate.append(DateTime[8]+'월')
    endDate.append(DateTime[9]+'일')
    endDate.append(DateTime[10]+'시')
    endDate.append(DateTime[11]+'분')
    return startDate, endDate
#이벤트 정보
def get_event() :
    event_data = []
    event_date = []
    event_url = []
    url = "https://maplestory.nexon.com/News/Event"
    req = requests.get(url)
    html = req.text
    bs = BeautifulSoup(html, 'html.parser')
    tags = bs.find_all('dd',{'class':'data'})
    if tags:
        for tag in tags:
            events = tag.text
            event_data.append(events.strip('\n'))
    else :
        event_data.append("진행중인 이벤트가 없습니다")
    tags = bs.find_all('dd',{'class':'date'})
    if tags:
        for tag in tags:
            events = tag.text
            event_date.append(events.strip('\n'))
    else :
        event_date.append(None)
    tags = bs.find_all('div',{'class':'event_list_wrap'})
    for tag in tags :
        dt = tag.find('dt')
        a = dt.find('a')["href"]
        url = "https://maplestory.nexon.com/" + a
        event_url.append(url)
    return event_data ,event_date, event_url
#html
def get_UserInfohtml(userName) :
    word = userName
    url_tmp = "www.maple.gg/u/" + word
    url = "http://" + parse.quote(url_tmp)
    req = requests.get(url)
    html = req.text
    return html
#층수
def get_UserFloor(html) :
    userFloor = []
    err = 'X'
    bs = BeautifulSoup(html, 'html.parser')
    tags = bs.find_all('div',{'class':'user-summary-box-content text-center position-relative'})
    if tags:
        for tag in tags:
            floor = (" ".join(tag.h1.text.split()))
            userFloor.append(floor)
    else :
        userFloor.append(err)
    return userFloor
#레벨
def get_UserLevel(html) :
    userLevel = []
    bs = BeautifulSoup(html, 'html.parser')
    lis = bs.find_all('li',{'class':'user-summary-item'})
    for li in lis:
        if 'Lv' in li.text :
            level = re.findall(r"\d+",(" ".join(li.text.split())))
            userLevel.append(level)
    return userLevel
#마지막 접속일
def get_UserDate(html) :
    userDate = []
    err = 'X'
    bs = BeautifulSoup(html, 'html.parser')
    spans = bs.find_all('span',{'class':'font-size-12 text-white'})
    if spans :
        for span in spans:
            date = re.findall(r"\d+",(" ".join(span.text.split())))
            userDate.append(date)
    else :
        userDate.append(err)
    return userDate
#직업
def get_UserJob(html) :
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    userJob = []
    bs = BeautifulSoup(html, 'html.parser')
    lis2 = bs.find_all('li',{'class':'user-summary-item'})
    for li2 in lis2:
        job = (li2.text)
        result = hangul.sub('', job)
        userJob.append(result.replace("인기도",""))
    userJobs = [x for x in userJob if x]     
    return userJobs
#아바타
def get_UserAvatar(html) :
    bs = BeautifulSoup(html, 'html.parser')
    metas = bs.find('meta',{'property':'og:image'})
    meta = metas['content']   
    return meta
#[]'제거
def rep(lists) :
    rep1 = str(lists)
    rep2 = rep1.replace("[","")
    rep3 = rep2.replace("]","")
    rep4 = rep3.replace("'","")
    if re.findall(r'\d+', rep4):
        return(int(re.findall(r'\d+', rep4)[0]))
    return rep4


#봇 시작
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(status=discord.Status.online, activity=discord.Game('재획'))
    print('------')
#새로운 멤버
@client.event
async def on_member_join(member):
    embed = discord.Embed(title="[길드 ** 공지]",description=':one: 서로 존중하는 채팅\n:two: 기타 내용',color=0xFF0000)
    embed.set_thumbnail(url="https://ssl.nx.com/s2/game/maplestory/renewal/common/logo.png")
    await member.send(embed=embed)
@client.event
async def on_message(message):
    if message.author.bot: #봇 일경우
        return None 
    elif message.content == "!명령어":
        embed = discord.Embed(title="명령어 목록" ,color=0x62c1cc)
        embed.add_field(name="FredBoat♪♪", value="`;;p word` , `;;p url`: 음악 재생 \n`;;q`: 대기열 표시 \n`;;np`: 재생중인 트랙 표시 \n`;;s`: 재생중인 트렉 건너뛰기 \n`;;st`: 플레이어를 중지", inline=True)
        embed.add_field(name="** 봇", value="`!정보 닉네임`: 해당 유저의 레벨, 직업, 무릉, 마지막 접속일을 조회 \n`!이벤트`: 현제 진행중인 이벤트를 표시\n`!팅패`: 팅패 정보를 표시\n`!공지`: 길드 공지사항을 표시",inline=True)
        embed.set_footer(text="Made By 김윤철",icon_url="https://ssl.nx.com/s2/game/maplestory/renewal/common/logo.png")
        await message.channel.send(embed=embed) 
    elif message.content == "!이벤트":
        event_data = []
        event_date = []
        event_url = []
        event_data, event_date, event_url = get_event()
        embed = discord.Embed(title="이벤트 정보",color=0x62c1cc)
        embed.set_thumbnail(url="https://ssl.nx.com/s2/game/maplestory/renewal/common/logo.png")
        for i in range(len(event_date)):
            embed.add_field(name=i+1 ,value='[%s](%s)' % (event_data[i], event_url[i])+'\n'+ event_date[i], inline=True)
        embed.set_footer(text="Made By 김윤철",icon_url="https://ssl.nx.com/s2/game/maplestory/renewal/common/logo.png")
        await message.channel.send(embed=embed) 
    elif message.content.startswith('!정보'):
        message_replaced = message.content.replace("!정보 ", "")
        html = get_UserInfohtml(message_replaced)
        get_UserAvatar(html)
        userDate = rep(get_UserDate(html))
        userFloor = rep(get_UserFloor(html))
        userJob = rep(get_UserJob(html))
        userLevel = rep(get_UserLevel(html))
        urls = str(get_UserAvatar(html))
        embed = discord.Embed(color=0x62c1cc)
        embed.set_author(name=message_replaced + ' ' + "님의 정보", icon_url=urls, url=urls)
        embed.add_field(name="레벨", value=userLevel, inline=True)
        embed.add_field(name="직업", value=userJob, inline=True)
        embed.add_field(name="무릉", value=str(userFloor) + "층", inline=True)
        embed.add_field(name="마지막 접속일", value=str(userDate) + "일", inline=True)
        embed.set_footer(text="Made By 김윤철",icon_url="https://ssl.nx.com/s2/game/maplestory/renewal/common/logo.png")
        await message.channel.send(embed=embed) 
    elif message.content == "!팅패":
        strObstacleContent = []
        DateTime = []
        strObstacleContent, DateTime = get_InspectionInfo()
        startDates, endDates = DateTimeRe(DateTime)
        startDate = ''.join(startDates)
        endDate = ''.join(endDates)
        embed = discord.Embed(title="팅패 정보",description=strObstacleContent+'\n'+startDate+'~'+endDate,color=0xFF0000)
        embed.set_image(url="https://ssl.nx.com/s2/game/maplestory/renewal/common/logo.png")
        embed.set_thumbnail(url="https://ssl.nx.com/s2/game/maplestory/renewal/common/logo.png")
        embed.set_footer(text="Made By 김윤철",icon_url="https://ssl.nx.com/s2/game/maplestory/renewal/common/logo.png")
        await message.channel.send(embed=embed) 
    elif message.content == "!공지":
        embed = discord.Embed(title="[길드 ** 공지]",description=':one: 서로 존중하는 채팅\n:two: 기타 내용',color=0xFF0000)
        embed.set_thumbnail(url="https://ssl.nx.com/s2/game/maplestory/renewal/common/logo.png")
        await message.author.send(embed=embed)  
client.run(accese_token)


