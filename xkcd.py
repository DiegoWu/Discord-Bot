import requests 
from bs4 import BeautifulSoup as bs
import random as rd
import re
from PIL import Image
import matplotlib.pyplot as plt
import os
import string 
import discord
from discord.ext import commands
class Xkcd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(help = "get five interesting comics", brief = "comics from xkcd")
    async def comics(self, ctx):
        await ctx.send("five amzuing comics!!!")
        lt = rd.sample(range(1, 2471), 6)
        r= requests.get('https://xkcd.com/'+str(lt[0])+'/')
        for v in range(1, 6):
            try: 
                soup= bs(r.text, "html.parser")
                fi= soup.select('#middleContainer > ul:nth-child(2) > li:nth-child(4) > a')
                img= soup.select('#comic > img')
                z= 'https:'+img[0].attrs['src']
                print(fi[0].attrs['href'])
                res= requests.get(z)
                b= str(lt[v])+'.png'
                file= open(os.path.join("..", "storage",b), "wb")
                file.write(res.content)  
                file.close()
                with open(os.path.join("..", "storage", b), "rb") as f:
                    picture = discord.File(f) # 把檔案內容轉成 discord 上可以傳送的格式
                    await ctx.send(file = picture) # Bot 傳送圖片
                temp= 'https://xkcd.com/'+str(lt[v])+'/'
                r= requests.get(temp)
            except:
                temp= 'https://xkcd.com/'+str(lt[v-1])+'/'
                r= requests.get(temp)
    @commands.command(help = "輸入單一數字，代表下載一則, 輸入 r 和 random 代表隨機下載一則,輸入以 , 分隔的多個數字，代表下載多則, 輸入一個 數字-數字 的範圍，代表下載多則, 輸入漫畫名會下載它並跳出漫畫", brief = "get specific xkcd comics")
    async def xkcd(self, ctx):
        await ctx.send("輸入單一數字，代表下載一則, 輸入 r 和 random 代表隨機下載一則,輸入以 , 分隔的多個數字，代表下載多則, 輸入一個 數字-數字 的範圍，代表下載多則, 輸入漫畫名會下載它並跳出漫畫： ")
        p= await self.bot.wait_for("message", timeout= 300.0)
        p= p.content
        await ctx.send("processing------------------------------------------------------")
        if p==('r'or 'random'): 
            try:
                lt = rd.sample(range(1, 2471), 50)
                r= requests.get('https://xkcd.com/'+str(lt[0])+'/')
                soup= bs(r.text, "html.parser")
                fi= soup.select('#middleContainer > ul:nth-child(2) > li:nth-child(3) > a')
                z= 'https:'+fi[0].attrs['href']
                res= requests.get(z)
                soup1=bs(res.text, "html.parser")
                img= soup1.select('#comic > img')
                res= requests.get('https:'+img[0].attrs['src'])
                file= open(os.path.join("..", "storage",'random.png'), "wb")
                file.write(res.content)
                file.close()
                with open(os.path.join("..", "storage", "random.png"), "rb") as f:
                    picture = discord.File(f) # 把檔案內容轉成 discord 上可以傳送的格式
                    await ctx.send(file = picture) # Bot 傳送圖片
            except:
                ctx.send('unexpected error!')
        elif p.find("-")!= -1:   
            l= list(p.split('-'))
            l= sorted(l, key= int)  
            for i in range(int(l[0]), int(l[1])+1):
                r= requests.get('https://xkcd.com/'+str(i)+'/')
                soup= bs(r.text, "html.parser")
                img= soup.select('#comic > img')
                z= 'https:'+img[0].attrs['src']
                res= requests.get(z)
                file= open(os.path.join("..", "storage", str(i)+'.png'), "wb")
                file.write(res.content)
                file.close()
                with open(os.path.join("..", "storage", str(i)+".png"), "rb") as f:
                    picture = discord.File(f) # 把檔案內容轉成 discord 上可以傳送的格式
                    await ctx.send(file = picture) # Bot 傳送圖片
        elif p.find(',')!= -1 or p.isdigit()== True:
            l= list(p.split(','))
            for i in range(len(l)):
                try:
                    r= requests.get('https://xkcd.com/'+l[i]+'/')
                    soup= bs(r.text, "html.parser")
                    img= soup.select('#comic > img')
                    z= 'https:'+img[0].attrs['src']
                    res= requests.get(z)
                    file= open(os.path.join("..", "storage" , l[i]+'.png'), 'wb')
                    file.write(res.content)
                    file.close()
                    with open(os.path.join("..", "storage", l[i]+".png"), "rb") as f:
                        picture = discord.File(f) # 把檔案內容轉成 discord 上可以傳送的格式
                        await ctx.send(file = picture) # Bot 傳送圖片
                except:
                    await ctx.send( "sorry {intt} comic's 404 not found :( ".format(intt= l[i]))
                    continue
        else: #bonus
            try:
                pp= p.lower()
                pp = pp.translate(str.maketrans('', '', string.punctuation))
                pp=pp.replace(' ', '_')
                z= 'https://imgs.xkcd.com/comics/'+pp+'.png'
                res= requests.get(z)
                file = open(os.path.join("..", "storage", pp+".png"), "wb")
                file.write(res.content)
                file.close()
                '''
                with open(pp+'.png', 'wb') as f:
                    f.write(res.content)
                '''
                img=Image.open(os.path.join("..", "storage", pp+".png"))
            except:
                open(os.path.join("..", "storage", pp+".png"), 'w').close()
                await ctx.send( "sorry {intt} comic's 404 not found :( ".format(intt= p))
            plt.imshow(img)
            plt.title(p) 
            plt.axis('off')
            plt.savefig(os.path.join("..", "storage",pp+'.png'), bbox_inches='tight') 
            plt.close() 
            with open(os.path.join("..", "storage", pp+".png"), "rb") as f:
                picture = discord.File(f) # 把檔案內容轉成 discord 上可以傳送的格式
                await ctx.send(file = picture) # Bot 傳送圖片
def setup(bot):
    bot.add_cog(Xkcd(bot))

