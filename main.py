import discord, config
from discord import utils
from discord.ext.commands import Bot
import asyncio

intents = discord.Intents.default()
intents.members = True

client = Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def create(ctx, name):
    category = ctx.channel.category
    member = ctx.message.author
    guild = ctx.guild

    if name == None: return

    _role = await guild.create_role(name=f"{name}_channel")

    await member.add_roles(_role)

    channel = await category.create_text_channel(name=str(name))

    for role in guild.roles:
        if role == _role: 
            await channel.set_permissions(role, read_messages=True, send_messages=True)
            continue

        await channel.set_permissions(role, read_messages=False, send_messages=False)

    await asyncio.sleep(5)

    await role.delete()
    await channel.delete()

if __name__ == "__main__":
    client.run(config.TOKEN)