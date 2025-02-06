import discord
from discord.ext import commands
from mcrcon import MCRcon
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
MCRCON_HOST = os.getenv("MCRCON_HOST")
MCRCON_PORT = int(os.getenv("MCRCON_PORT"))
MCRCON_PASSWORD = os.getenv("MCRCON_PASSWORD")

# Vérification des variables d'environnement
if not TOKEN or not MCRCON_HOST or not MCRCON_PORT or not MCRCON_PASSWORD:
    print("❌ Erreur : Une ou plusieurs variables d'environnement sont manquantes.")
    exit(1)

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True  # Important pour lire les commandes !
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")

@bot.command()
async def mc(ctx, *, commande):
    """Exécute une commande sur le serveur Minecraft via RCON."""
    
    # Vérifier si l'utilisateur a le rôle "Admin" ou un rôle spécifique
    if not any(role.name == "» H. Administration" for role in ctx.author.roles):  # Remplace "Admin" par le rôle voulu
        await ctx.send("❌ Vous devez avoir le rôle Admin pour utiliser cette commande.")
        return
    
    print(f"📩 Commande Discord reçue : {commande}")  # Log dans la console
    
    try:
        print("🔌 Tentative de connexion à RCON...")
        with MCRcon(MCRCON_HOST, MCRCON_PASSWORD, MCRCON_PORT) as mcr:
            print("✅ Connexion RCON réussie !")
            response = mcr.command(commande)
            print(f"📝 Réponse du serveur : {response}")
        await ctx.send(f"✅ Commande exécutée : `{commande}`\n📝 Réponse: {response}")
    except Exception as e:
        print(f"❌ Erreur : {e}")  # Voir l'erreur exacte dans la console
        await ctx.send(f"❌ Erreur lors de l'exécution : {e}")

bot.run(TOKEN)
