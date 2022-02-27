import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound
import json
import os

if os.path.exists('settings.json') and os.stat('settings.json').st_size != 0:
    with open('settings.json') as fileSettings:
        botSettings = json.load(fileSettings)
else:
    with open('settings.json', 'w') as fileSettings:
        botSettings = {
            'prefix':',',
            'status':'DMs Open'
        }
        json.dump(botSettings, fileSettings, indent=2)


intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = commands.Bot(intents=intents, command_prefix=botSettings['prefix'])

def im_owner(ctx):
    return ctx.message.author.id == 224131162996473856

@client.event
async def on_ready():
    print(f"Botul este online!\nPing:{round(client.latency * 1000)}ms")

@client.event
async def on_disconnect():
    print("Botul este offline!")




#cogs owner command
@commands.command(pass_context=True)
@commands.check(im_owner)
async def reloado(ctx):
    client.unload_extension(f'cogs.owner')
    client.load_extension(f'cogs.owner')
    await ctx.send(f'```Owner reloaded.```')
client.add_command(reloado)


@reloado.error
async def reloado_error(ctx, error):
   if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(f'<@{ctx.message.author.id}> doar Ownerul meu poate folosi aceasta comanda.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(f'Comanda invalida.')
        return 0
    raise error

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


if os.path.exists('token.json'):
    with open('token.json') as fileToken:
        botToken = json.load(fileToken)['token']

client.run(botToken)
