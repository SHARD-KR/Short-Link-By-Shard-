from flask import render_template, jsonify, Flask, request, redirect
import sqlite3
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route("/short/<url>")
def url(url):
    try:
        con = sqlite3.connect("C:/Users/1/Downloads/discord_short_url/urls" + ".db")
        cur = con.cursor()
        cur.execute("SELECT * FROM url WHERE url == ?;", (url,))
        rows = cur.fetchone()
        current_time = datetime.now()
        nowdate = f"{current_time.year}년 {current_time.month}월 {current_time.day}일 {current_time.hour}시 {current_time.minute}분 {current_time.second}초"
        cur.execute("UPDATE url SET users = ?, joinedate = ? WHERE url == ?;", (int(rows[1]) + 1, str(nowdate), str(url)))
        con.commit()
        con.close()
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)[:-4] + "XXXX"
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/892710959892799518/cECOxIK_J_2pC0hilV0IrQv32bI4e9jfOmjpLrplQjKXMiSifJhmDNHMY3uuhnnVMFcE')
        embed = DiscordEmbed(title='단축링크 접속로그', description='User IP : ' + ip + ', Url : [바로 접속하기](https://shard.kr/short/' + url + '), Redirect : ' + rows[3], color='03b2f8')
        embed.set_footer(text=nowdate + " | " + rows[1] + "번 접속됨 | "+ "https://shard.kr/short/" + url)
        webhook.add_embed(embed)
        webhook.execute()
        return redirect(rows[3])  
    except:
        return render_template("error.html")   

@app.route("/logs")
def urllog():
    con = sqlite3.connect("C:/Users/1/Downloads/discord_short_url/urls" + ".db")
    cur = con.cursor()
    cur.execute("SELECT * FROM url")
    logs = cur.fetchall()
    con.close()
    return render_template("index.html", logs=logs)



app.run()