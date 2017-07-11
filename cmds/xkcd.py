from bs4 import BeautifulSoup
from random import choice
import requests
import aiohttp


def is_int(a):
    try:
        int(a)
        return True
    except ValueError:
        return False


# xkcd command
async def ex(dclient, channel, mention, a, cmd_char):
    if len(a) > 0:
        a = a.split(' ')[0]
        if a == 'latest':
			try:
				async with aiohttp.ClientSession() as s:
					async with s.get('https://xkcd.com/info.0.json') as r:
						d = await r.json()
						await dclient.send_message(channel, '''Title: {}
Comic ID: {}
{}'''.format(d['safe_title'], d['num'], d['img']))
			except Exception ex:
				embed=discord.Embed(title="Error", description="Error when trying to retrieve data from https://xkcd.com/info.0.json", color=0xff0000)
				embed.set_thumbnail(url='http://i.imgur.com/dx87cAe.png')
				embed.add_field(name="Reason", value=ex, inline=False)
				await dclient.say(embed=embed)
        elif is_int(a):
            comic_id = a
            try:
                async with aiohttp.ClientSession() as s:
                    async with s.get('https://xkcd.com/{}/info.0.json'.format(comic_id)) as r:
                        d = await r.json()
                        await dclient.send_message(channel, '''Title: {}
Comic ID: {}
{}'''.format(d['safe_title'], d['num'], d['img']))
            except Exception:
                await dclient.send_message(channel, "{}, unable to retrieve a specific comic! Perhaps it doesn't "
                                                    "exist?".format(mention, cmd_char))
        else:
            await dclient.send_message(channel,
                                       '{}, **USAGE:** {}xkcd <latest OR comic_ID>'.format(mention, cmd_char))
    else:
        b = BeautifulSoup(requests.get('https://xkcd.com/archive/').text, 'html.parser')
        ids = b.find('div', id='middleContainer').find_all('a')
        idr = choice(ids)['href']
        idr.replace('/', '')
		try:
			async with aiohttp.ClientSession() as s:
				async with s.get('https://xkcd.com/{}/info.0.json'.format(idr)) as r:
					d = await r.json()
					await dclient.send_message(channel, '''Title: {}
Comic ID: {}
{}'''.format(d['safe_title'], d['num'], d['img']))
		except Exception ex:
			embed=discord.Embed(title="Error", description="Error when trying to retrieve data from https://xkcd.com/info.0.json", color=0xff0000)
			embed.set_thumbnail(url='http://i.imgur.com/dx87cAe.png')
			embed.add_field(name="Reason", value=ex, inline=False)
			await dclient.say(embed=embed)
