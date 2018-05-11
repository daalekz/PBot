from pbot_utils import *

#Member join event
@client.event
async def on_member_join(member):
    server = member.server
    srv = Utils.get_server(server.id)
    unverified = discord.utils.get(server.roles, name="Unverified")
    await client.add_roles(member, unverified)
    await client.send_message(client.get_channel(str(srv.welcome_channel)),srv.entry_text.format(**{'member_name':member.name,'server_name':server.name}))
    msg = await client.send_message(member,srv.entry_text_pm.format(**{'member_name':member.name,'server_name':server.name}))
    await client.add_reaction(msg,'👍')
    await asyncio.sleep(1)
    res = await client.wait_for_reaction(message=msg)
    usr = srv.make_member(member.id)
    if res.reaction.emoji == '👍':
        await client.remove_roles(member,unverified)
        await client.send_message(member,':white_check_mark: You have been verified. Enjoy your stay :champagne:')
        usr.verified = 1
        usr.update()


#Member leave event
@client.event
async def on_member_remove(member):
    srv = Utils.get_server(member.server.id)
    db.update(table='members',values={'in_server':'0'},params={'id':member.id,'server_id':member.server.id})
    await client.send_message(client.get_channel(str(srv.goodbye_channel)),srv.goodbye_text.format(member.name+'#'+member.discriminator))