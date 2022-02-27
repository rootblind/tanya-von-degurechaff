import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CommandNotFound
import os

def im_owner(ctx):
    return ctx.message.author.id == 224131162996473856
cogsloaded = []
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        cogsloaded.append(f'{filename[:-3]}')

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(pass_context=True)
    @commands.check(im_owner)
    async def load(self, ctx, extencion):
        global cogsloaded
        self.client.load_extension(f'cogs.{extencion}')
        await ctx.send(f'```Modulul {extencion} a fost încărcat cu succes.```')
        cogsloaded.append(f'{extencion}')

    @commands.command(pass_context=True)
    @commands.check(im_owner)
    async def unload(self, ctx, extencion):
        if  extencion.startswith('owner'):
            await ctx.send(f'<@{ctx.message.author.id}> Nu iti este permis sa dezactivezi modulul `{extencion}`.')
        else:
            self.client.unload_extension(f'cogs.{extencion}')
            await ctx.send(f'```Modulul {extencion} a fost descarcat cu succes.```')
            global cogsloaded
            cogsloaded.remove(f'{extencion}')


    @commands.command(pass_context=True)
    @commands.check(im_owner)
    async def reload(self, ctx, extencion):
        if extencion.startswith('owner'):
            await ctx.send(f'<@{ctx.message.author.id}> Nu iti este permis sa reincarci modulul `{extencion}`.')
        else:
            self.client.unload_extension(f'cogs.{extencion}')
            self.client.load_extension(f'cogs.{extencion}')
            await ctx.send(f'```Modulul {extencion} a fost reincarcat cu succes.```')


    @commands.command(pass_context=True)
    @commands.check(im_owner)
    async def reloadall(self, ctx):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('owner'):
                self.client.unload_extension(f'cogs.{filename[:-3]}')
                self.client.load_extension(f'cogs.{filename[:-3]}')
        await ctx.send(f'```Toate modulele au fost reincarcate cu succes.```')
        global cogsloaded
        cogsloaded.clear()
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                cogsloaded.append(f'{filename[:-3]}')


    @commands.command()
    @commands.check(im_owner)
    async def allmodules(self, ctx):
        global cogsloaded
        embed = discord.Embed(
            color= discord.Color.green(),
            title= 'Toate modulele'
        )

        embed.set_author(name='Owner: Blind#1115' ,icon_url= 'https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024'.format(ctx.message.author))
        counter = int(0)
        for x in cogsloaded:
            counter += 1
            embed.add_field(name = f'{counter}', value=f'{x}', inline= False)
        await ctx.send(embed=embed)


    @load.error
    async def load_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send(f'<@{ctx.message.author.id}> doar Ownerul meu poate folosi aceasta comanda.')
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f'<@{ctx.message.author.id}> trebuie sa oferi si un argument.')
        elif isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(
                f'<@{ctx.message.author.id}> modulul `{ctx.message.content.split(" ")[1]}` nu exista sau are erori.')

    @unload.error
    async def unload_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send(f'<@{ctx.message.author.id}> doar Ownerul meu poate folosi aceasta comanda.')
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f'<@{ctx.message.author.id}> trebuie sa oferi si un argument.')
        elif isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(
                f'<@{ctx.message.author.id}> modulul `{ctx.message.content.split(" ")[1]}` nu exista sau are erori.')

    @reload.error
    async def reload_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send(f'<@{ctx.message.author.id}> doar Ownerul meu poate folosi aceasta comanda.')
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f'<@{ctx.message.author.id}> trebuie să oferi și un argument.')
        elif isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(
                f'<@{ctx.message.author.id}> modulul `{ctx.message.content.split(" ")[1]}` nu exista sau are erori.')

    @reloadall.error
    async def reload_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send(f'<@{ctx.message.author.id}> doar Ownerul meu poate folosi aceasta comanda.')


    @allmodules.error
    async def allmodules_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send(f'<@{ctx.message.author.id}> doar Ownerul meu poate folosi aceasta comanda.')
        else:
            await ctx.send(f'<@{ctx.message.author.id}> a aparut o eroare.')

def setup(client):
    client.add_cog(Owner(client))