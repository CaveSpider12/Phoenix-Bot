# Phoenix Bot - Official Bot of Phoenix Chat
# FEATURE: Combines everything from older bots

import discord
from discord.ext import commands, tasks
import time


# GENERAL BOT SETTINGS
client = commands.Bot(command_prefix = "p/")
client.remove_command("help")


# ROLE SETTINGS
admin = None
modlog = None
muted = None
welcome = None


# HELP
@client.command()
async def help(ctx): # sends an embedded list of all commands
    embed = discord.Embed(title = "Phoenix Bot Commands", description = "Commands for Phoenix Bot ALPHA", color = discord.Color.red())

    embed.add_field(name = "p/help", value = "Sends this message", inline = False)
    
    embed.add_field(name = "p/setadminrole (OWNER ONLY)", value = "Sets the admin role for them to use moderation commands", inline = False)
    embed.add_field(name = "p/adminrole (ADMINS ONLY", value = "Checks the admin role", inline = False)
    
    embed.add_field(name = "p/setmodlog (OWNER ONLY)", value = "Sets the moderator logging channel", inline = False)
    embed.add_field(name = "p/modlog (ADMINS ONLY)", value = "Checks the moderator logging channel", inline = False)
    
    embed.add_field(name = "p/setmutedrole (OWNER ONLY)", value = "Sets the muted role", inline = False)
    embed.add_field(name = "p/mutedrole (ADMINS ONLY)", value = "Checks the muted role", inline = False)
    
    embed.add_field(name = "p/setwelcomechannel (OWNER ONLY)", value = "Sets the welcome channel for the server", inline = False)
    embed.add_field(name = "p/welcomechannel (ADMINS ONLY)", value = "Checks the welcome channel", inline = False)
    
    embed.add_field(name = "p/kick {member mention} {reason} (ADMINS ONLY)", value = "Kicks a member from the server", inline = False)
    embed.add_field(name = "p/ban {member mention} {reason} (ADMINS ONLY)", value = "Bans a member from the server", inline = False)
    embed.add_field(name = "p/unban {name and discriminator} {reason} (ADMINS ONLY)", value = "Unbans a member", inline = False)
                    
    embed.add_field(name = "p/clear {amount} (ADMINS ONLY)", value = "Clears a set amount of messages", inline = False)
    
    embed.add_field(name = "p/mute {member mention} (ADMINS ONLY)", value = "Mutes a member", inline = False)
    embed.add_field(name = "p/unmute {member mention} (ADMINS ONLY)", value = "Unmutes a member", inline = False)

    await ctx.send(embed = embed)


# MODERATION
@client.command()
async def setadminrole(ctx, role): # sets the admin role
    if ctx.message.author == ctx.guild.owner:
        if role == None:
            await ctx.send("sir/ma'am please put a role along with the command (like just say it)")
        else:
            global admin
            admin = discord.utils.get(ctx.guild.roles, name = role) 
            await ctx.send("Set admin role to " + str(admin))
    else:
        await ctx.send("bruh you don't own the server what are you doing???")

@client.command()
async def adminrole(ctx): # checks the admin role
    global admin
    
    if admin in ctx.author.roles or ctx.message.author == ctx.guild.owner:
        await ctx.send("The admin role for this server is " + str(admin))
    else:
        await ctx.send("You're not an admin!")

@client.command()
async def setmodlog(ctx, channel): # sets the moderator logging channel
    if ctx.message.author == ctx.guild.owner:
        if channel == None:
            await ctx.send("sir/ma'am please put a channel along with the command")
        else:
            global modlog
            modlog = discord.utils.get(ctx.guild.channels, name = channel)
            await ctx.send("Set moderator logging channel to " + str(modlog))
    else:
        await ctx.send("bruh you don't own the server what are you doing???")

@client.command()
async def modlog(ctx): # checks the moderator logging channel
    global modlog

    if admin in ctx.author.roles or ctx.message.author == ctx.guild.owner:
        await ctx.send("The moderator logging channel for this server is " + str(modlog))
    else:
        await ctx.send("You're not an admin!")

@client.command()
async def setmutedrole(ctx, role): # sets the muted role
    if ctx.message.author == ctx.guild.owner:
        if role == None:
            await ctx.send("sir/ma'am please put a role along with the command (like just say it)")
        else:
            global muted
            muted = discord.utils.get(ctx.guild.roles, name = role) 
            await ctx.send("Set muted role to " + str(muted))
    else:
        await ctx.send("bruh you don't own the server what are you doing???")

@client.command()
async def mutedrole(ctx): # checks the muted role
    global muted

    if admin in ctx.author.roles or ctx.message.author == ctx.guild.owner:
        await ctx.send("The muted role for this server is " + str(muted))
    else:
        await ctx.send("You're not an admin!")

@client.command()
async def setwelcomechannel(ctx, channel): # sets the welcome channel
    if ctx.message.author == ctx.guild.owner:
        if channel == None:
            await ctx.send("sir/ma'am please put a channel along with the command (like just say it)")
        else:
            global welcome
            welcome = discord.utils.get(ctx.guild.channels, name = channel)
            await ctx.send("Set welcome channel to " + str(welcome))
    else:
        await ctx.send("bruh you don't own the server what are you doing???")

@client.command()
async def welcomechannel(ctx): # checks the welcome channel
    global welcome

    if admin in ctx.author.roles or ctx.message.author == ctx.guild.owner:
        await ctx.send("The welcome channel for this server is " + str(welcome))
    else:
        await ctx.send("You're not an admin!")
    
@client.command()
async def kick(ctx, member : discord.Member = None, *, reason = None): # kicks a mentioned member
    global admin

    if admin in ctx.author.roles or ctx.message.author == ctx.guild.owner:
        if member == None:
            await ctx.send("bro you gotta mention someone to actually kick them")
        elif admin in member.roles:
            await ctx.send("you can't kick an admin")
        else:
            await member.kick(reason = reason)
            
            if reason == None:
                await ctx.send(str(member.mention) + " has been kicked")

                global modlog
                embed = discord.Embed(title = (str(member) + " has been kicked"), color = discord.Color.blue())
                await modlog.send(embed = embed)
            else:
                await ctx.send(str(member.mention) + " has been kicked for " + reason)

                if modlog == None:
                    return
                else:
                    embed = discord.Embed(title = (str(member) + " has been kicked"), description = ("Reason: " + str(reason)), color = discord.Color.blue())
                    await modlog.send(embed = embed)
    else:
        await ctx.send("you're not an admin")

@client.command()
async def ban(ctx, member : discord.Member = None, *, reason = None): # bans a mentioned member
    global admin

    if admin in ctx.author.roles or ctx.message.author == ctx.guild.owner:
        if member == None:
            await ctx.send("bro you gotta mention someone to actually ban them")
        elif admin in member.roles:
            await ctx.send("you can't ban an admin")
        else:
            await member.ban(reason = reason)

            if reason == None:
                await ctx.send(str(member.mention) + " has been banned")

                global modlog
                embed = discord.Embed(title = (str(member) + " has been banned"), color = discord.Color.blue())
                await modlog.send(embed = embed)                
            else:
                await ctx.send(str(member.mention) + " has been banned for " + reason)

                if modlog == None:
                    return
                else:
                    embed = discord.Embed(title = (str(member) + " has been banned"), description = ("Reason: " + str(reason)), color = discord.Color.blue())
                    await modlog.send(embed = embed)
    else:
        await ctx.send("you're not an admin")
        
@client.command()
async def unban(ctx, *, member): # unbans a specified member
    global admin

    if admin in ctx.author.roles or ctx.message.author == ctx.guild.owner:
        if member == None:
            await ctx.send("bro you gotta add a member to unban to actually unban them, ya know?")
        else:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split("#")

            for ban_entry in banned_users:
                user = ban_entry.user
                
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send("Unbanned " + str(user.mention))
                    
                    global modlog
                    if modlog == None:
                        return
                    else:
                        if modlog == None:
                            return
                        else:
                            embed = discord.Embed(title = (str(member) + " has been unbanned"), color = discord.Color.blue())
                            await modlog.send(embed = embed)
                else:
                    await ctx.send("bruh they're not even banned")
    else:
        await ctx.send("you're not an admin")

@client.command()
async def clear(ctx, amount : int): # clears a specified amount of messages
    global admin

    if admin in ctx.author.roles or ctx.message.author == ctx.guild.owner:
        if amount < 1:
            await ctx.send("sir/ma'am please type in an actual number greater than 0 to clear messages")
        elif amount == None:
            await ctx.send("bro you gotta put in a number of messages to clear to actually clear them, ya know?")
        else:
            await ctx.channel.purge(limit = amount + 1)
            await ctx.send("Cleared " + str(amount) + " message(s)")
            time.sleep(2)
            await ctx.channel.purge(limit = 1)
    else:
        await ctx.send("you're not an admin")

@client.command()
async def mute(ctx, member : discord.Member = None): # mutes a mentioned member
    global admin

    if admin in ctx.author.roles or ctx.message.author == ctx.guild.owner:
        if member == None:
            await ctx.send("bro you gotta mention someone to actually mute them")
        elif admin in member.roles:
            await ctx.send("you can't mute an admin")
        else:
            global muted
            await member.add_roles(muted)
            
            await ctx.send(str(member.mention) + " has been muted")

            global modlog
            if modlog == None:
                return
            else:
                embed = discord.Embed(title = (str(member) + " has been muted"), color = discord.Color.blue())
                await modlog.send(embed = embed)
    else:
        await ctx.send("you're not an admin")

@client.command()
async def unmute(ctx, member : discord.Member = None): # unmutes a mentioned member
    global admin

    if admin in ctx.author.roles or ctx.message.author == ctx.guild.owner:
        if member == None:
            await ctx.send("bro you gotta mention someone to actually unmute them")
        elif admin in member.roles:
            await ctx.send("you can't unmute an admin, cause they can't be muted anyways")
        else:
            global muted
            await member.remove_roles(muted)
            
            await ctx.send(str(member.mention) + " has been unmuted")

            global modlog
            if modlog == None:
                return
            else:
                embed = discord.Embed(title = (str(member) + " has been unmuted"), color = discord.Color.blue())
                await modlog.send(embed = embed)
    else:
        await ctx.send("you're not an admin")


# EVENTS
@client.event
async def on_ready(): # done when the bot is ready
    print("Ready")
    await client.change_presence(activity = discord.Game("Phoenix Chat | p/help"))

@client.event
async def on_member_join(ctx): # done when a member joins the server
    global welcome
    if welcome == None:
        return
    else:
        await welcome.send(str(ctx.mention) + " HAS JOINED THE CHAT")

    await ctx.create_dm()

    embed = discord.Embed(title = "Phoenix Chat", description = "SERVING THE PEOPLE SINCE JULY 15, 2019", color = discord.Color.red())
    embed.add_field(name = "*", value = "Hello, and welcome to Phoenix Chat, our community's central hub of gaming, anime, memes, tech, and more! If you're new here, all you have to do is:", inline = False)
    embed.add_field(name = "*", value = "1. Read the rules (please do or you're gonna have a bad time)", inline = False)
    embed.add_field(name = "*", value = "2. Check out channel-help and react if you need to", inline = False)
    embed.add_field(name = "*", value = "...and then you'll have access to the rest of the server! Once, you do so, then have fun!", inline = False)
    embed.set_footer(text = "Enjoy!! - Phoenix Bot")

    await ctx.dm_channel.send(embed = embed)

@client.event
async def on_member_remove(ctx): # done when a member leaves the server
    global welcome
    if welcome == None:
        return
    else:
        await welcome.send(str(ctx.mention) + " has left the chat...sucks to suck")


# CLIENT TOKEN
# REDACTED



# Current Version: ALPHA 1.0



# HISTORY:
# 4/11/20: Update ALPHA 1.0 deployed



# UPDATE LOG:
# ALPHA 1.0: Included basic moderation commands (kick, ban, unban, clear, mute, and unmute), created join messages in a channel and in DM, as well as leave messages, and added role and channel settings
