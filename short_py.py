

import sqlite3
import randomstring
import discord
client = discord.Client()


@client.event
async def on_message(message):
    if isinstance(message.channel, discord.channel.DMChannel):
        con = sqlite3.connect("C:/Users/1/Downloads/discord_short_url/urls" + ".db")
        cur = con.cursor()
        if (message.content.startswith("u!short ")):
            shorts = message.content.split(" ")[1]
            idlink = randomstring.pick(6)
            cur.execute("INSERT INTO url VALUES(?, ?, ?, ?, ?, ?);", (idlink, 0, "접속 기록이 없음", shorts, message.author.name, message.author.id))
            con.commit()
            con.close()  
            embed=discord.Embed(color=0x00ff00)
            embed.add_field(name="제작이 완료되었습니다.", value="다음 링크로 접속해주세요. https://shard.kr/short/" + idlink + "/" , inline=False)
            await message.author.send(embed=embed)
    else:
        return 

            
client.run("ODkxNTU5MDM2MTc1MTMwNjY0.YVAHDg.mYsTxbUquJMrE7BVk2Ok5JUh4dI")