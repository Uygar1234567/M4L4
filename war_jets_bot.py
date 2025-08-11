import discord
from discord.ext import commands
import sqlite3
from config import token

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

DB_NAME = "war_jets.db"

@bot.event
async def on_ready():
    print(f"Bot giriş yaptı: {bot.user}")

@bot.command()
async def jet(ctx, *, jet_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT jet_id FROM jets WHERE jet_name = ?", (jet_name,))
    result = cursor.fetchone()

    if not result:
        await ctx.send(f"{jet_name} could not be found.")
        return

    jet_id = result[0]

    cursor.execute("SELECT kd_ratio FROM stats WHERE jet_id = ?", (jet_id,))
    kd = cursor.fetchone()[0]

    cursor.execute("SELECT max_speed, turn_ratio, max_takeoff_weight FROM abilities WHERE jet_id = ?", (jet_id,))
    speed, turn, weight = cursor.fetchone()

    conn.close()

    embed = discord.Embed(
        title=f"{jet_name} information:",
        color=discord.Color.blue()
    )
    embed.add_field(name="K/D ratio", value=kd, inline=False)
    embed.add_field(name="Max speed", value=f"{speed} km/h", inline=False)
    embed.add_field(name="Turn rate", value=str(turn), inline=False)
    embed.add_field(name="Max T/O weight", value=weight, inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def best(ctx):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT jets.jet_name FROM abilities
        JOIN jets ON jets.jet_id = abilities.jet_id
        ORDER BY max_speed DESC LIMIT 1
    ''')
    best_speed = cursor.fetchone()[0]

    cursor.execute('''
        SELECT jets.jet_name FROM abilities
        JOIN jets ON jets.jet_id = abilities.jet_id
        ORDER BY turn_ratio DESC LIMIT 1
    ''')
    best_turn = cursor.fetchone()[0]

    cursor.execute('''
        SELECT jets.jet_name FROM abilities
        JOIN jets ON jets.jet_id = abilities.jet_id
        ORDER BY max_takeoff_weight + 0 DESC LIMIT 1
    ''')
    best_weight = cursor.fetchone()[0]

    cursor.execute('''
        SELECT jets.jet_name FROM stats
        JOIN jets ON jets.jet_id = stats.jet_id
        ORDER BY kd_ratio + 0 DESC LIMIT 1
    ''')
    best_kd = cursor.fetchone()[0]

    conn.close()

    embed = discord.Embed(
        title="Best jets",
        color=discord.Color.green()
    )
    embed.add_field(name="Fastest", value=best_speed, inline=False)
    embed.add_field(name="Best turn speed", value=best_turn, inline=False)
    embed.add_field(name="Heaviest T/O weight", value=best_weight, inline=False)
    embed.add_field(name="Best K/D ratio", value=best_kd, inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def fav(ctx):
    await ctx.send("Mine is F14, what's your fav?")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)
        fav_jet = msg.content.strip()

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT jet_id, jet_name FROM jets WHERE jet_name LIKE ?", (f"%{fav_jet}%",))
        result = cursor.fetchone()

        if not result:
            await ctx.send(f"{fav_jet} could not be found.")
            conn.close()
            return

        jet_id, jet_name = result

        cursor.execute("SELECT kd_ratio FROM stats WHERE jet_id = ?", (jet_id,))
        kd = cursor.fetchone()[0]

        cursor.execute("SELECT max_speed, turn_ratio, max_takeoff_weight FROM abilities WHERE jet_id = ?", (jet_id,))
        speed, turn, weight = cursor.fetchone()

        conn.close()

        embed = discord.Embed(
            title=f"{jet_name} information:",
            color=discord.Color.blue()
        )
        embed.add_field(name="K/D ratio", value=kd, inline=False)
        embed.add_field(name="Max speed", value=f"{speed} km/h", inline=False)
        embed.add_field(name="Turn rate", value=str(turn), inline=False)
        embed.add_field(name="Max T/O weight", value=weight, inline=False)

        await ctx.send(embed=embed)

    except TimeoutError:
        await ctx.send("Took too long.")

bot.run(token)
