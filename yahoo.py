from bs4 import BeautifulSoup as bs 
import requests
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import discord
import os
from discord.ext import commands
class Stonk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        help = 
        '''
        印出護國神跡台灣第一權值股更動一點大盤更動八點的tsmc或是他的小夥伴的簡易當日股價走勢圖
        note: some graph's line may be inconsistent due to the fact that that the stock is really unpopular QQ 
        ''', 
        brief = "Print current day's simple stock price diagram"
    )
    async def stonk(self, ctx):
        await ctx.send("請輸入股票代碼")
        t= await self.bot.wait_for('message', timeout= 300.0)
        if t.content== '2330':
            await ctx.send("TSMC!!!")
        try:
            r= requests.get(f'https://tw.stock.yahoo.com/_td-stock/api/resource/FinanceChartService.ApacLibraCharts;symbols=%5B%22{t.content}.TW%22%5D;type=tick?bkt=%5B%22tw-qsp-exp-no2-1%22%2C%22test-es-module-production%22%2C%22test-portfolio-stream%22%5D&device=desktop&ecma=modern&feature=ecmaModern%2CshowPortfolioStream&intl=tw&lang=zh-Hant-TW&partner=none&prid=2h3pnulg7tklc&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.902&returnMeta=true')
            jd =r.json()['data']
        except Exception as CommandInvokeError:
            await ctx.send("沒這股不然就是這股沒了貼壁紙QQ")
        close = jd[0]['chart']['indicators']['quote'][0]['close']
        timestamp = jd[0]['chart']['timestamp']
        df = pd.DataFrame({'timestamp': timestamp, 'close':close})
        df['dt'] = pd.to_datetime(df['timestamp'] + 3600 * 8, unit = 's')
        plt.plot(df['dt'], df['close']) 
        plt.title("stonk {}".format(t.content), fontsize=24) #圖表標題
        plt.xlabel("time", fontsize=16) #x軸標題
        plt.ylabel("price", fontsize=20) 
        plt.savefig(os.path.join("..", "storage",'stonk.png'), bbox_inches='tight') 
        plt.close() 
        await ctx.send("done!")  
        try:
            with open(os.path.join("..", "storage", "stonk.png"), "rb") as f:
                picture = discord.File(f) # 把檔案內容轉成 discord 上可以傳送的格式
                await ctx.send(file = picture) # Bot 傳送圖片
        except FileNotFoundError:
            await ctx.send('Saved image not found!')
    @commands.command(
        help= "得到大盤的資訊, note: 絕對不是滑水exceed the minimum lines limitation用><",
        brief= "get the overall info of Taiwan's stock market"
    )
    async def tmarket(self, ctx):
        r= requests.get('https://tw.stock.yahoo.com/')
        soup= bs(r.text, "html.parser")
        z= soup.select('#main-0-ComponentGrid-Proxy > div > div.grid-item.item-span-8.default-row-gap > div > div > div.D\(f\).Mt\(8px\).Bd.Bdc\(\$bd-primary-divider\).Ov\(h\) > div > div.D\(f\).Ai\(fe\).Jc\(fe\) > span')
        c= soup.select('#main-0-ComponentGrid-Proxy > div > div.grid-item.item-span-8.default-row-gap > div > div > div.D\(f\).Mt\(8px\).Bd.Bdc\(\$bd-primary-divider\).Ov\(h\) > div > div.D\(f\).Ai\(fe\).Jc\(fe\) > div > span')
        v= soup.select('#main-0-ComponentGrid-Proxy > div > div.grid-item.item-span-8.default-row-gap > div > div > div.D\(f\).Mt\(8px\).Bd.Bdc\(\$bd-primary-divider\).Ov\(h\) > div > div.D\(f\).Ai\(fe\).Jc\(fe\) > div > div')
        vv= soup.select('#main-0-ComponentGrid-Proxy > div > div.grid-item.item-span-8.default-row-gap > div > div > div.D\(f\).Mt\(8px\).Bd.Bdc\(\$bd-primary-divider\).Ov\(h\) > div > div.D\(f\).Mt\(12px\) > div:nth-child(1)')
        vvv= soup.select('#main-0-ComponentGrid-Proxy > div > div.grid-item.item-span-8.default-row-gap > div > div > div.D\(f\).Mt\(8px\).Bd.Bdc\(\$bd-primary-divider\).Ov\(h\) > div > div.D\(f\).Mt\(12px\) > div:nth-child(2)')
        cc= soup.select('#main-0-ComponentGrid-Proxy > div > div.grid-item.item-span-8.default-row-gap > div > div > div.D\(f\).Mt\(8px\).Bd.Bdc\(\$bd-primary-divider\).Ov\(h\) > div > div.D\(f\).Mt\(12px\) > div:nth-child(3)')
        ccc= soup.select('#main-0-ComponentGrid-Proxy > div > div.grid-item.item-span-8.default-row-gap > div > div > div.D\(f\).Mt\(8px\).Bd.Bdc\(\$bd-primary-divider\).Ov\(h\) > div > div.D\(f\).Mt\(12px\) > div:nth-child(4)')
        await ctx.send("台灣加權指（上市: ")
        await ctx.send(z[0].text)
        await ctx.send(c[0].text)
        await ctx.send("漲跌與percentage: ")
        await ctx.send(v[0].text)
        await ctx.send(vv[0].text)
        await ctx.send(vvv[0].text)
        await ctx.send(cc[0].text)
        await ctx.send(ccc[0].text)


def setup(bot):
    bot.add_cog(Stonk(bot))