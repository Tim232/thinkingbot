#모듈 임포트

from discord import *
from random import randint
import asyncio
from discord.ext import commands
from os.path import isdir
import time
import os
from os.path import isfile
import datetime
from pytz import timezone
from datetime import timedelta

#기본 변수 설정

prefix ="''"

app = commands.Bot(command_prefix=["''", '"'])

a = open('token.txt', 'r')
token = a.read()
a.close()

category_list = [
    '지원',
    '일반',
    '관리자',
    '수학',
    '포인트'
]

category_explain = [
    '`도움`, `봇정보`, `핑`',
    '`정보`, `출석`, `소개설정`, `파일생성`, `찬반투표`',
    '`밴`, `언밴`, `관리자송금`, `공지`, `공지설정`',
    '`사칙연산`, `일차풀기`',
    '`도박`, `송금`'
]

func_list = [
    '도움',
    '봇정보',
    '출석',
    '정보',
    '소개설정',
    '밴',
    '언밴',
    '파일생성',
    '사칙연산',
    '일차풀기',
    '도박',
    '핑',
    '송금',
    '관리자송금',
    '공지',
    '찬반투표',
    '공지설정'
]

func_footer = [
    '도움',
    '봇정보',
    '출석',
    '정보',
    '소개설정 (소개말)',
    '밴 (멤버 멘션)',
    '언밴 (멤버 멘션)',
    '파일생성 (제목) (내용)',
    '사칙연산 (수) (연산자) (수)',
    '일차풀기 (미지수 단위) (a) (b) (c)',
    '도박 (걸 포인트 / 올인)',
    '핑',
    '송금 (멤버 멘션) (송금할 포인트)',
    '관리자송금 (멤버 멘션) (송금할 포인트)',
    '공지 (내용)'
    '찬반투표 (내용)',
    '공지설정',
    '도박 (포인트/올인)'
]

func_explain = [
    '쓸 수 있는 명령어 확인',
    '봇 정보 확인',
    '출석하기',
    '포인트 및 정보 확인',
    '소개말 설정',
    '봇 사용 금지 (관리자 전용)',
    '봇 사용 금지 해제 (관리자 전용)',
    '파일 만들어서 올려줌 (파일명 한글은 미적용)',
    '사칙연산 수행(+, -, *, /)',
    '일차방정식의 해 구하기 (ax+b=c)',
    '50% 확률로 건 돈을 더 얻음 (아니면 건돈 × -1배)',
    '핑을 측정',
    '돈을 송금함',
    '돈 송금 - 관리자용',
    '공지하기',
    '찬성/반대 투표 생성',
    '공지설정',
    '도박'
]

embedcolor = 0x00ffff
errorcolor = 0xff0000

KST = timezone('Asia/Seoul')

#함수 처리

def is_owner():
    async def predicate(ctx):
        return ctx.author.id in [745848200195473490, 557119176590884864, 594183416266752000]
    return commands.check(predicate)

def can_use():
    async def predicate(ctx):
        return not isbanned(ctx.author.id)
    return commands.check(predicate) 

def isbanned(id):
    if isfile('ban.txt'):
        return (str(id) in open('ban.txt', 'r').read())
    open('ban.txt', 'x')
    return False

def readpoint(id):
    pointroute = f'{id}.txt'
    try:
        a = open(pointroute, 'r')
        b = a.read()
    except FileNotFoundError:
        a = open(pointroute, 'w')
        a.write('0')
        b = 0
    a.close()
    b = int(b)
    return b

def writepoint(id, addpoint):
    pointroute = f'{id}.txt'
    a = open(pointroute, 'w')
    a.write(str(addpoint))
    a.close()

#이벤트 처리

@app.event
async def on_ready():
    print('구동 시작')
    game = Game(f'{prefix}도움')
    await app.change_presence(status=Status.online, activity=game)
    

@app.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        pass

#커맨드 처리

#일반 카테고리
@app.command(name='출석')
@can_use()
async def _chulseok(ctx):
    utcnow= datetime.datetime.utcnow()
    time_gap= datetime.timedelta(hours=9)
    kor_time= utcnow+ time_gap
    date = str(kor_time.strftime('%Y%m%d'))
    ifyouchulseoked = f'{date}/{ctx.author.id}.txt'
    b = True
    if not isdir(f'{date}/'):
        os.makedirs(f'{date}/')
    try:
        a = open(ifyouchulseoked, 'r')
    except FileNotFoundError:
        b = False
        a = open(ifyouchulseoked, 'w')
        point = readpoint(ctx.author.id)
        writepoint(ctx.author.id, 1+point)
        point += 1
        msgembed = Embed(title='출석 완료', description=f'출석이 완료되었습니다. \n 현재 포인트: {point}', color=embedcolor)
    a.close()
    if b:
        msgembed = Embed(title='🚫에러🚫', description='이미 출석했습니다', color=errorcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

@app.command(name='소개설정')
@can_use()
async def _setInfo(ctx, *, content):
    pointroute = f'{ctx.author.id}_info.txt'
    a = open(pointroute, 'w', encoding='utf-8')
    a.write(content)
    a.close()
    msgembed = Embed(title='변경 완료', description=f'소개말이 {content} (으)로 변경되었습니다', color=embedcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(Embed=msgembed)
    
@app.command(name='정보')
@can_use()
async def _info(ctx):
    pointroute = f'{ctx.author.id}_info.txt'
    b = True
    try:
        a = open(pointroute, 'r')
    except FileNotFoundError:
        b = False
        userinfo = f'내용이 없습니다. `{prefix}소개설정` 명령어로 소개말을 설정하세요.'
    if b:
        a.close()
        a = open(pointroute, 'r', encoding='utf-8')
        userinfo = a.read()
        a.close()
    pointroute = f'{ctx.author.id}.txt'
    msgembed = Embed(title=str(ctx.author), description=userinfo, color=embedcolor)
    msgembed.set_thumbnail(url=str(ctx.author.avatar_url))
    msgembed.add_field(name='유저 ID', value=f'{ctx.author.id}')
    point = readpoint(ctx.author.id)
    msgembed.add_field(name='💵유저 포인트💵', value=point)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

@app.command(name='파일생성')
@can_use()
async def _makefile(ctx, filename, *, content):
    a = open(filename, 'w')
    a.write(content)
    a.close()
    file1 = File(filename)
    await ctx.send(file=file1)
    os.remove(filename)

@app.command(name='찬반투표')
@can_use()
async def _devote_tof(ctx, *, content):
    msgembed = Embed(title='투표', description=content, color=embedcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    a = await ctx.send(embed=msgembed)
    await a.add_reaction('❌')
    await a.add_reaction('✅')

#수학 카테고리

@app.command(name='사칙연산')
@can_use()
async def _calcul(ctx, n1, operator, n2):
    b = True
    msgembed = Embed(title='사칙연산', description='', color=embedcolor)
    msgembed.add_field(name='**Input**', value=f'```{n1}{operator}{n2}```', inline=False)
    if operator == '+':
        a = float(n1)+float(n2)
    elif operator == '-':
        a = float(n1)-float(n2)
    elif operator == '/' or operator == '÷':
        a = float(n1)/float(n2)
    elif operator == '*' or operator == '×':
        a = float(n1)*float(n2)
    else:
        b = False
    if float(int(a)) == a:
        a = int(a)
    msgembed.add_field(name='**Output**', value=f'```{a}```', inline='True')
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    if b:
        await ctx.send(embed=msgembed)

@app.command(name='일차풀기')
@can_use()
async def _calcul(ctx, operator, a, b, c):
    msgembed = Embed(title='일차풀기', description='', color=embedcolor)
    if b[0] == '-':
        msgembed.add_field(name='**Input**', value=f'```{a}{operator}{b}={c}```', inline=False)
    else:
        msgembed.add_field(name='**Input**', value=f'```{a}{operator}+{b}={c}```', inline=False)
    answer = (float(c)-float(b)) / float(a)
    if float(int(answer)) == answer:
        answer = int(answer)
    msgembed.add_field(name='**Output**', value=f'```{answer}```', inline=False)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

#지원 카테고리

@app.command(name='봇정보')
@can_use()
async def _botinfo(ctx):
    msgembed = Embed(title='ThinkingBot Beta#7894',description='', color=embedcolor)
    msgembed.add_field(name='개발자', value='yswysw#9328')
    msgembed.add_field(name='도움을 주신 분들', value='`huntingbear21#4317`님, `Decave#9999`님, `koder_ko#8504`님, `Scott7777#5575`님 , `Minibox#3332`님 등 많은 분들께 감사드립니다.', inline=False)
    msgembed.add_field (name='상세정보', value='2020년에 만들어진 봇이며, 수학과 다른 봇에서는 볼 수 없는 독특한 기능들이 많이 있음', inline=False)
    msgembed.add_field(name='버전', value='1.2.3 - 20201106 릴리즈', inline=False)
    msgembed.add_field(name='개발언어 및 라이브러리', value='파이썬, discord.py', inline=False)
    msgembed.add_field(name='깃허브', value='https://github.com/sw08/thinkingbot', inline=False)
    msgembed.add_field(name='공식 홈페이지', value='http://thinkingbot.kro.kr')
    msgembed.add_field(name='개발환경', value='윈도우10, Visual Studio Code', inline=False)
    msgembed.add_field(name='공식 서포트 서버', value='https://discord.gg/ASvgRjX', inline=False)
    msgembed.add_field(name='봇 초대 링크', value='https://discord.com/api/oauth2/authorize?client_id=750557247842549871&permissions=0&scope=bot', inline=False)
    msgembed.set_thumbnail(url="https://sw08.github.io/cloud/profile.png")
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

@app.command(name='도움')
@can_use()
async def _help(ctx, what_you_look_for):
    if what_you_look_for in func_list:
        msgembed = Embed(title=f'도움 - {what_you_look_for}', description=func_explain[func_list.index(what_you_look_for)], color=embedcolor)
        msgembed.set_footer(text=f'{ctx.author} | {prefix}{func_footer[func_list.index(what_you_look_for)]}', icon_url=ctx.author.avatar_url)

    elif what_you_look_for in category_list:
        msgembed = Embed(title=f'도움 - {what_you_look_for}', description=category_explain[category_list.index(what_you_look_for)], color=embedcolor)
        msgembed.set_footer(text=f'{ctx.author} | {prefix}도움 {what_you_look_for}', icon_url=ctx.author.avatar_url)
    
    else:
        msgembed = Embed(title='🚫에러🚫', description='음.... 아직 그런 카테고리는 없습니다.', color=errorcolor)
        msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

@app.command(name='핑')
@can_use()
async def _ping(ctx):
    la = app.latency
    msgembed = Embed(title='핑', description=f'{str(round(la * 1000))}ms', color=embedcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

#관리자 카테고리

@app.command(name='밴')
@can_use()
@is_owner()
async def _ban(ctx, member: Member):
    if isbanned(member.id):
        await ctx.send('이미 차단당했습니다')
    else:
        b = True
        try:
            a = open('ban.txt', 'r')
        except FileNotFoundError:
            a = open('ban.txt', 'w')
            a.write(str(member.id))
            b = False
        a.close()
        if b:
            a = open('ban.txt', 'r')
            banned_members = a.read()
            a.close()
            a = open('ban.txt', 'w')
            a.write(f'{banned_members}\n{member.id}')
            a.close()
            await ctx.send(f'{member.mention} 님은 ThinkingBot에게서 차단되었습니다. 이의는 ThinkingBot 관리자에게 제출해 주십시오.')

@app.command(name='언밴')
@can_use()
@is_owner()
async def _ban(ctx, member: Member):
    if isbanned(member.id):
        b = True
        try:
            a = open('ban.txt', 'r')
        except FileNotFoundError:
            a = open('ban.txt', 'w')
            a.write('')
            b = False
        a.close()
        if b:
            a = open('ban.txt', 'r')
            banned_members = a.read().replace(f'\n{member.id}', '')
            a.close()
            a = open('ban.txt', 'w')
            a.write(banned_members)
            a.close()
            await ctx.send(f'{member.mention} 님은 ThinkingBot에게서 차단이 풀렸습니다.')
    else:
        await ctx.send('차단당한적이 없습니다')

@app.command(name='관리자송금')
@can_use()
@is_owner()
async def _sendmoney(ctx, member: Member, money):
    point = readpoint(member.id)
    writepoint(member.id, point+int(money))
    msgembed = Embed(title='관리자송금', description=f'{member.mention}님께 {money}원이 송금되었습니다', color=embedcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

@app.command(name='공지')
@can_use()
@is_owner()
async def _공지(ctx, *, msg):
    utcnow= datetime.datetime.utcnow()
    time_gap= datetime.timedelta(hours=9)
    kor_time= utcnow+ time_gap
    time1 = kor_time.strftime('%Y/%m/%d %H:%M')
    a = True
    msgembed = Embed(title='📢봇공지📢', description=msg, color=embedcolor)
    msgembed.set_footer(text=f'{ctx.author} | {time1}', icon_url=ctx.author.avatar_url)
    msgembed.set_thumbnail(url="https://sw08.github.io/cloud/profile.png")
    try:
        b = open('notice.txt', 'r')
    except FileNotFoundError:
        b = open('notice.txt', 'w').close()
        a = False
        await ctx.send('공지채널없음')
    if a:
        c = b.read().split('\n')
        print(c)
        c.remove('')
        for i in range(len(c)):
            await app.get_channel(int(c[i].replace('\n', ''))).send(embed=msgembed)
    b.close()

@app.command('공지설정')
@can_use()
async def _공지설정(ctx):
    try:
        a = open('notice.txt', 'r')
        b = a.read()
    except FileNotFoundError:
        a = open('notice.txt', 'w')
        b = ''
    a.close()
    if str(ctx.channel.id) in b:
        msgembed = Embed(title='🚫에러🚫', description='이미 등록되어 있음', color=errorcolor)
    else:
        os.remove('notice.txt')
        a = open('notice.txt', 'w')
        a.write(b + f'\n{ctx.channel.id}')
        a.close()
        msgembed = Embed(title='🔔공지설정🔔', description='완료', color=embedcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)


@app.command('공지취소')
@can_use()
async def _공지취소(ctx):
    try:
        a = open('notice.txt', 'r')
        b = a.read()
    except FileNotFoundError:
        a = open('notice.txt', 'w')
        b = ''
    a.close()
    if not str(ctx.channel.id) in b:
        msgembed = Embed(title='🚫에러🚫', description='등록되어 있지 않음', color=errorcolor)
    else:
        os.remove('notice.txt')
        a = open('notice.txt', 'w')
        a.write(b.replace(f'{ctx.channel.id}\n', ''))
        a.close()
        msgembed = Embed(title='🔕공지취소🔕', description='완료', color=embedcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

#포인트 카테고리

@app.command(name='도박')
@can_use()
async def _dobac(ctx, don1):
    point = readpoint(ctx.author.id)
    if don1 == '올인':
        don = point
    else:
        don = don1
    if float(don) > point:
        msgembed = Embed(title='🚫에러🚫', description='돈이 부족합니다', color=errorcolor)
    elif float(don) <= 0:
        msgembed = Embed(title='🚫에러🚫', description='돈은 1 이상부터 걸 수 있습니다', color=errorcolor)
    else:
        if randint(0,1):
            writepoint(ctx.author.id, point+int(don))
            msgembed = Embed(title='와아아', description='이겼습니다!', color=embedcolor)
            msgembed.add_field(name='원래 있던 돈', value=str(point), inline=False)
            msgembed.add_field(name='번 돈', value=don, inline=False)
            msgembed.add_field(name='현재 가진 돈', value=str(point+int(don)), inline=False)
        else:
            writepoint(ctx.author.id, point-int(don))
            msgembed = Embed(title='으아악', description='졌습니다...', color=errorcolor)
            msgembed.add_field(name='원래 있던 돈', value=str(point), inline=False)
            msgembed.add_field(name='번 돈', value=don, inline=False)
            msgembed.add_field(name='현재 가진 돈', value=str(point-int(don)), inline=False)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

@app.command(name='송금')
@can_use()
async def _sendmoney(ctx, member: Member, money):
    point = readpoint(ctx.author.id)
    if point < int(money):
        await ctx.send('돈이 부족합니다....')
    else:
        writepoint(ctx.author.id, point-int(money))
        point = readpoint(member.id)
        writepoint(member.id, point+int(money))
        msgembed = Embed(title='송금', description=f'{member.mention}님께 {money}원이 송금되었습니다', color=embedcolor)
        msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=msgembed)

#에러 처리

@_help.error
async def _help_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        msgembed = Embed(title='도움', description='도움말', color=embedcolor)
        msgembed.set_thumbnail(url='https://thinkingbot.kro.kr/profile.png')
        msgembed.add_field(name='일반', value='`일반 명령어들`', inline=False)
        msgembed.add_field(name='포인트', value='`포인트 관련 명령어들`', inline=False)
        msgembed.add_field(name='수학', value='`수학 관련 명령어들`', inline=False)
        msgembed.add_field(name='지원', value='`봇 관련 지원 명령어들`', inline=False)
        msgembed.add_field(name='관리자', value='`관리자 전용 명령어들`', inline=False)
        msgembed.set_footer(text=f'{ctx.author} | {prefix}도움 (명령어/카테고리)', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=msgembed)

app.remove_command("help")
app.run(token)