import discord
from discord.ext import commands
import asyncio
import random
import time
import datetime
import sqlite3

bot = commands.Bot(command_prefix = 'dl ')
bot.remove_command('help') # removed the shitty default help command

conn = sqlite3.connect('DiscordLibrary.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Guilds(GuildID TEXT, LatestBump TEXT, Description TEXT, BannerURL TEXT)")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------')
    time.sleep(1)
    game = discord.Game(name = 'dl help')
    await bot.change_presence(status = discord.Status.online, game = game)

@bot.event
async def on_guild_join(guild): # logs when a guild was added
	try:
		await guild.text_channels[0].create_invite(reason = 'Used for bumping server.', unique = False)
	except:
		pass

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
async def on_guild_remove(guild): # logs when a guild was removed
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

	help_embed = discord.Embed(title = 'DiscordLibrary', color = 0x00EFEB)
	help_embed.add_field(name = 'Commands', value = '`dl help` - Shows this message.\n`dl links` - Provides useful links.\n`dl bump` - Bumps the server on the list.')
	help_embed.set_thumbnail(url = str(bot.user.avatar_url))

	try:
		await ctx.send(embed = help_embed)
	except:
		try:
			await ctx.send(':x: **I don\'t seem to have `Embed Links` permission.**')
		except:
			return

@bot.command()
async def ping(ctx):
	pingtime = time.time()
	pingms = await ctx.send('*Pinging...*')
	ping = (time.time() - pingtime) * 1000
	await pingms.edit(content = ':ping_pong: **{} ms**'.format(int(ping)))

@bot.command(pass_context = True)
async def links(ctx):
	guild = bot.get_guild(ctx.guild.id)
	print(str(ctx.author.name) + ' [' + str(ctx.author.id) + ']: ' + str(ctx.guild.name) + ' [' + str(ctx.guild.id) + ']: links')

	if ctx.author.bot == True:
		return

	links = discord.Embed(description = '[Add Me](https://discord.gg/achfbu4)\n[Official Discord](https://discord.gg/achfbu4)', color = 0x00EFEB)

	try:
		await ctx.send(embed = links)
	except:
		try:
			await ctx.send(':x: **I don\'t seem to have `Embed Links` permission. Please fix my permissions and try again.**')
		except:
			return

@bot.command(pass_context = True)
async def bump(ctx):
	guild = bot.get_guild(ctx.guild.id)
	print(str(ctx.author.name) + ' [' + str(ctx.author.id) + ']: ' + str(ctx.guild.name) + ' [' + str(ctx.guild.id) + ']: bump')

	if ctx.author.bot == True: # avoiding automated bumps
		return await ctx.send(':warning: **Please don\'t automate bumps, otherwise I will be permanentaly blacklisted from this server.**')

	if isinstance(ctx.channel, discord.DMChannel): # can't bump DMs, cause why would you even...
		return await ctx.send(':thinking: **Hmmm... Bumping DMs? This doesn\'t seem right...**')

	try: # shows "typing" in a called channel if it has send messages permission in it
		await ctx.trigger_typing()
	except:
		pass

	if not ctx.author.guild_permissions.manage_guild: # only members with manage server permission can bump servers
		try:
			await ctx.send(':x: **You need to have `Manage Server` permission in order to bump.**')
		except:
			return
	else:
		#try:
			# creates an invite of the top most text channel
		c_invite = await guild.text_channels[0].create_invite(reason = 'Used for bumping server.', unique = False)

		bump_bump = discord.Embed(color = 0x00EFEB)
		bump_bump.add_field(name = 'Guild Name', value = '`' + str(guild.name) + '`')
		bump_bump.add_field(name = 'Guild Owner', value = '`' + str(guild.owner) + '`')
		bump_bump.add_field(name = 'Members', value = str(len(guild.members)))
		bump_bump.add_field(name = 'Invite Link', value = str(c_invite), inline = False)
		bump_bump.set_thumbnail(url = str(guild.icon_url))
		bump_bump.set_footer(text = 'Guild ID: ' + str(guild.id))

		try:
			channel = bot.get_channel(390204229987336193)
			await channel.send(embed = bump_bump)
		except:
			user = bot.get_user(140898654180474882)
			await user.send(':warning: **I can\'t bump servers anymore!**')
			return await ctx.send(':warning: **An error occured while bumping the server. I have sent the error notification to my owner.**')

		cursor.execute("INSERT INTO Guilds(GuildID, LatestBump) VALUES('" + str(guild.id) + "', '" + str(datetime.datetime.now()) + "')")
		conn.commit()

		try:
			await ctx.send('**Bumped!** :thumbsup:')
		except:
			return
		#except:
		#	await ctx.send(':x: **I need the `Create Instant Invite` permission of the top most text channel that I\'m able to reach with my current permissions.**')

# owner only command: bot leaves a server specified by it's id
@bot.command()
async def leave(ctx, server):
	if ctx.author.id != 140898654180474882:
		return

	guild = bot.get_guild(int(server))

	try:
		await guild.leave()
		await ctx.send(':white_check_mark: **Left the guild.**')
	except TypeError:
		await ctx.send(':x: **Invalid syntax.**')
	except:
		await ctx.send(':x: **Couldn\'t leave the guild.**')


bot.run('TOKEN')
