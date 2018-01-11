import discord
from discord.ext import commands
import asyncio
import random
import time
import datetime
import sqlite3

'''
In this code I'm always trying to catch as many "bugs" as possible to prevent users from spamming lots of errors into my console
This bot's code is just so cheap and poor, that I don't even care leaking it
'''

conn = sqlite3.connect('DiscordLibrary.db')
cursor = conn.cursor()

bot = commands.Bot(command_prefix = 'dl ')
bot.remove_command('help') # removed the shitty default help command

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------')
    game = discord.Game(name = 'dl help')
    await bot.change_presence(status = discord.Status.online, game = game)

@bot.event
async def on_guild_join(guild):
	bot_join = discord.Embed(title = 'Joined guild', color = 0x8DFF50)
	bot_join.add_field(name = 'Guild Name', value = '`' + str(guild.name) + '`')
	bot_join.add_field(name = 'Guild Owner', value = '`' + str(guild.owner) + '|' + str(guild.owner.id) + '`')
	bot_join.add_field(name = 'Members', value = str(len(guild.members)))
	bot_join.add_field(name = 'Current Guild Count', value = str(len(bot.guilds)), inline = False)
	bot_join.set_thumbnail(url = str(guild.icon_url))
	bot_join.set_footer(text = 'Guild ID: ' + str(guild.id))

	channel = bot.get_channel(398214258019532804)
	await channel.send(embed = bot_join)

@bot.event
async def on_guild_remove(guild):
	bot_leave = discord.Embed(title = 'Left guild', color = 0xCD0000)
	bot_leave.add_field(name = 'Guild Name', value = '`' + str(guild.name) + '`')
	bot_leave.add_field(name = 'Guild Owner', value = '`' + str(guild.owner) + '|' + str(guild.owner.id) + '`')
	bot_leave.add_field(name = 'Members', value = str(len(guild.members)))
	bot_leave.add_field(name = 'Current Guild Count', value = str(len(bot.guilds)), inline = False)
	bot_leave.set_thumbnail(url = str(guild.icon_url))
	bot_leave.set_footer(text = 'Guild ID: ' + str(guild.id))

	channel = bot.get_channel(398214258019532804)
	await channel.send(embed = bot_leave)

# created an own help command instead
@bot.command(pass_context = True)
async def help(ctx):
	guild = bot.get_guild(ctx.guild.id)
	print(str(ctx.author.name) + ' [' + str(ctx.author.id) + ']: ' + str(ctx.guild.name) + ' [' + str(ctx.guild.id) + ']: help')

	if ctx.author.bot == True:
		return

	help_embed = discord.Embed(title = 'DiscordLibrary', description = 'I\'m a bot dedicated to bumping servers on their staff behalfs.', color = 0x00EFEB)
	help_embed.add_field(name = 'Written in', value = 'Python3.6.2')
	help_embed.add_field(name = 'Library', value = 'discord.py-rewrite')
	help_embed.add_field(name = 'Commands', value = '`dl help` - shows this message.\n`dl bump` - bumps the server on the list.\n`dl links` - provides useful links.', inline = False)

	try:
		await ctx.send(embed = help_embed)
	except:
		try:
			await ctx.send(':x: **I don\'t seem to have `Embed Links` permission. Please fix my permissions and try again.**')
		except:
			try:
				if ctx.author.guild_permissions.manage_roles:
					await ctx.message.author.send('**I don\'t seem to have `Send Messages` permission in that channel. Please fix my permissions and try again.**')
				else:
					await ctx.message.author.send('**I don\'t seem to have `Send Messages` permission in that channel. Please ask the server administrator to fix my permissions.**')
			except:
				return

@bot.command(pass_context = True)
async def links(ctx):
	guild = bot.get_guild(ctx.guild.id)
	print(str(ctx.author.name) + ' [' + str(ctx.author.id) + ']: ' + str(ctx.guild.name) + ' [' + str(ctx.guild.id) + ']: links')

	if ctx.author.bot == True:
		return

	invite_link = discord.Embed(description = '[Add Me](https://discord.gg/achfbu4)\n[Official Discord](https://discord.gg/achfbu4)', color = 0x00EFEB)

	try:
		await ctx.send(embed = invite_link)
	except:
		try:
			await ctx.send(':x: **I don\'t seem to have `Embed Links` permission. Please fix my permissions and try again.**')
		except:
			try:
				if ctx.author.guild_permissions.manage_roles:
					await ctx.message.author.send('**I don\'t seem to have `Send Messages` permission in that channel. Please fix my permissions and try again.**')
				else:
					await ctx.message.author.send('**I don\'t seem to have `Send Messages` permission in that channel. Please ask the server administrator to fix my permissions.**')
			except:
				return

@bot.command(pass_context = True)
async def bump(ctx):
	guild = bot.get_guild(ctx.guild.id)
	print(str(ctx.author.name) + ' [' + str(ctx.author.id) + ']: ' + str(ctx.guild.name) + ' [' + str(ctx.guild.id) + ']: bump')

	if ctx.author.bot == True:
		return await ctx.send(':warning: **Please don\'t automate bumps, otherwise I will be permanentaly blacklisted from this server.**')

	if isinstance(ctx.channel, discord.DMChannel):
		return await ctx.send(':thinking: **Hmmm... Bumping DMs? This doesn\'t seem right...**')

	if not ctx.author.guild_permissions.manage_guild:
		try:
			await ctx.send(':x: **You need to have `Manage Server` permission in order to bump.**')
		except:
			return
	else:
		try:
			c_invite = await guild.text_channels[0].create_invite(max_age = 21600, reason = 'Bumped the guild.', unique = False)

			try:
				await ctx.trigger_typing()
			except:
				pass

			bump_bump = discord.Embed(color = 0x00EFEB)
			bump_bump.add_field(name = 'Guild Name', value = '`' + str(guild.name) + '`')
			bump_bump.add_field(name = 'Guild Owner', value = '`' + str(guild.owner) + '`')
			bump_bump.add_field(name = 'Members', value = str(len(guild.members)))
			bump_bump.add_field(name = 'Invite Link', value = str(c_invite), inline = False)
			bump_bump.set_thumbnail(url = str(guild.icon_url))
			bump_bump.set_footer(text = 'Guild ID: ' + str(guild.id))

			channel = bot.get_channel(390204229987336193)
			await channel.send(embed = bump_bump)
			await ctx.send('**Bumped!** :thumbsup:')
		except:
			await ctx.send(':x: **I don\'t seem to have `Create Instant Invite` permission.**')

@bot.command()
async def leave(ctx, *args):
	if ctx.author.id != 140898654180474882:
		return

	try:
		guild = bot.get_guild(int(' '.join(args)))
		try:
			await guild.leave()
			await ctx.send(':white_check_mark: **Successfully left the guild.**')
		except HTTPException:
			await ctx.send(':x: **Leaving the guild failed.**')
		except:
			await ctx.send(':x: **Something went wrong...**')
	except:
		await ctx.send(':x: **Invalid syntax.**')


bot.run('TOKEN')