import discord
import json
import openai as ai

from discord.ext import commands

with open("config.json", "r") as f:
    config = json.load(f)
    
    botconfig = config["bot"]
    prefix = botconfig["prefix"]
    token = botconfig["token"]
    
    openAIconfig = config["openAI"]
    key = openAIconfig["key"]

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
bot.remove_command("help")

ai_key = ai.api_key = key

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        raise e
    print("Ready, logged in as {0.user}".format(bot))

@bot.tree.command(name="invite", description="Invite bot to a server OWNER ONLY")
@commands.is_owner()
async def invite(interaction):
    embed = discord.Embed(title="Invite", description="Invite me to your server!", color=discord.Color.blurple())
    embed.set_author(name="Invite", url="https://discord.com/api/oauth2/authorize?client_id=CLIENTID&permissions=277025704000&scope=bot")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="completion", description="Get a completion from OpenAI")
async def completion(interaction, *, prompt:str):
    
    await interaction.response.defer()
    
    reponse = ai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=100, temperature=0.9)
    
    embed = discord.Embed(title="Completion", description="Requested by %s" % interaction.user.mention, color=discord.Color.blurple())
    
    embed.add_field(name="Prompt", value=prompt, inline=False)
    embed.add_field(name="Response", value=reponse["choices"][0]["text"], inline=False)
    
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="generate_image", description="Generate an image from OpenAI")
async def image(interaction, *, prompt:str):
    await interaction.response.defer()
    
    reponse = ai.Image.create(prompt=prompt, n=1, size="1024x1024")
    
    embed = discord.Embed(title=prompt, description=f"Prompt: {prompt}\nRequested by: {interaction.user.mention}",  color=discord.Color.blurple())
    embed.set_image(url=reponse["data"][0]["url"])
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="help", description="Help command")
async def help(interaction):
    embed = discord.Embed(title="Help", description="Help command", color=discord.Color.blurple())
    embed.add_field(name="Commands", value="`/completion` - API respond with a completion that attempts to match the context or pattern you provided.\n`/generate_image` - Allows you to create an original image given a text prompt", inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

bot.run(token)
