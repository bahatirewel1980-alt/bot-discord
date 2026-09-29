import discord
from discord.ext import commands
import os
from datetime import timedelta

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Liste des mauvais mots à surveiller (à adapter)
BAD_WORDS = ["mot1", "mot2", "insulte1", "insulte2"]

# Dictionnaire pour compter les avertissements (infractions) par utilisateur
warnings = {}

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

@bot.event
async def on_message(message):
    # Ignorer les messages envoyés par le bot lui-même
    if message.author == bot.user:
        return

    # --- 1. SYSTÈME DE MODÉRATION AUTOMATIQUE ---
    if not message.author.bot:
        content_lower = message.content.lower()
        if any(word in content_lower for word in BAD_WORDS):
            try:
                await message.delete()
            except discord.Forbidden:
                pass

            author_id = message.author.id
            warnings[author_id] = warnings.get(author_id, 0) + 1
            fault_count = warnings[author_id]

            if fault_count >= 5:
                try:
                    duration = timedelta(minutes=30)
                    await message.author.timeout(duration, reason="Utilisation répétée de mauvais mots (5 infractions)")
                    await message.channel.send(f"{message.author.mention} a été mis en sourdine (mute) pendant 30 minutes pour récidive d'insultes.")
                    warnings[author_id] = 0
                except discord.Forbidden:
                    await message.channel.send("Je n'ai pas les permissions pour mute cet utilisateur.")
            else:
                await message.channel.send(f"{message.author.mention} Attention, ce mot est interdit ! ({fault_count}/5 avant un mute de 30 min).", delete_after=5)
            
            return # On arrête le traitement ici pour le message insultant

    # --- 2. INTERACTION TYPE IA LORSQU'ON LE MENTIONNE ---
    # Si le bot est mentionné dans le message
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        # Enlever la mention du texte pour récupérer ce que l'utilisateur a dit
        clean_content = message.content.replace(f"<@!{bot.user.id}>", "").replace(f"<@{bot.user.id}>", "").strip()
        
        # Exemple de réponse interactive de type IA (tu pourras connecter une API externe comme OpenAI/Gemini plus tard si tu veux)
        if "bonjour" in clean_content.lower() or "salut" in clean_content.lower():
            await message.channel.send(f"Salut {message.author.mention} ! Je suis le gardien de ce serveur et ton assistant TCG. Comment puis-je t'aider aujourd'hui ?")
        elif "carte" in clean_content.lower():
            await message.channel.send(f"Tu t'intéresses aux cartes mèmes ? N'hésite pas à consulter les salons dédiés pour voir les dernières pépites créées !")
        else:
            await message.channel.send(f"J'ai bien reçu ton message, {message.author.mention} ! Je discute avec tout le monde comme un humain (ou presque 😉).")

    # Traitement classique des commandes du bot (ex: préfixe !)
    await bot.process_commands(message)

# Lancement du bot avec le token sécurisé sur Railway
bot.run(os.getenv("TOKEN"))
