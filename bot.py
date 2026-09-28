import os
import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Liste des événements aléatoires de combat
evenements = [
    "💥 Coup critique ! Tu perds **15 PV** !",
    "🛡️ Parade parfaite ! Tu gagnes **+10 de bouclier** !",
    "⚡ Attaque surprise ! Tout le monde perd **20 PV** !",
    "✨ Jackpot de l'Arène ! Tu gagnes **+25 PV** de soin !",
    "🌀 Confusion totale ! Rien ne se passe ce tour-ci.",
    "🔥 Frappe fatale ! Tu perds **30 PV** !",
]

@bot.event
async def on_ready():
    print(f"Bot connectée en tant que {bot.user}")

@bot.command(name="cartes")
async def cartes(ctx):
    await ctx.send("🃏 **Cartes disponibles :** Poutine Vmax, Donald Trump, Macron, Gi-Hun, Mr. Propre, Ronaldo, Cébedouze ex, God TK, Kilogram Mbappé !")

@bot.command(name="tour")
async def tour(ctx, joueur: discord.Member):
    action = random.choice(evenements)
    
    embed = discord.Embed(
        title="⚔️ L'ARÈNE A TRANCHÉ !",
        description=f"Action pour {joueur.mention} :\n\n{action}",
        color=discord.Color.red()
    )
    embed.set_footer(text="Arbitre Automatique — Meme TCG Arena")
    
    await ctx.send(embed=embed)

# Remplace 'TON_TOKEN_SECRET' par le véritable token de ton bot bot.run(os.getenv("TOKEN"))
bot.run(os.getenv("TOKEN"))
