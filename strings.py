import discord
import re
import string
from unidecode import unidecode

def create_message(title, desc, color=discord.Embed.Empty):
    message = discord.Embed(
        title=title,
        description=desc,
        color=color
    )
    return message

def create_error(desc):
    return create_message('Error', desc, discord.Color.red())

def create_desc(round_info):
    desc = ''
    for target in round_info['targets']:
        data = round_info['targets'][target]
        line = f"**{data['type']}** : {data['print']}"
        if data['guessed_by']:
            line += f" - guessed by {data['guessed_by'].mention}"
        desc += f'{line}\n'
    return desc + '\u200B'

def start_message(playlist_info, points_to_win, rounds):
    desc = f"**Playlist** : {playlist_info['name']}\n"
    desc += f'**Rounds** : {rounds}\n\u200B'
    message = discord.Embed(
        title='Starting a game!',
        description=desc,
        color=discord.Color.blue()
    )
    message.set_thumbnail(url=playlist_info['thumbnail'])
    message.add_field(name='Whats the win con?', value=f'Playing first to {points_to_win} points!', inline=False)
    return message

def round_message(round_info, scoreboard):
    print(round_info)
    title = f"Round {round_info['round_no']} - Summary"
    desc = create_desc(round_info)
    color = discord.Color.green()

    if round_info['skipped']:
        title += ' (Skipped)'
        color = discord.Embed.Empty

    message = create_message(title, desc, color)
    message.set_thumbnail(url=round_info['thumbnail'])
    value = scoreboard if scoreboard else 'No scores yet.'
    message.add_field(name='Leaderboard', value=value)

    return message

def end_message(playlist_info, scoreboard):
    desc = f"**Playlist** : {playlist_info['name']}"
    title = f'Game Summary'
    message = create_message(title, desc, discord.Color.blue())
    message.set_thumbnail(url=playlist_info['thumbnail'])
    value = scoreboard if scoreboard else 'No scores yet.'
    message.add_field(name='Leaderboard', value=value, inline=False)
    print(message)

    return message

def guess_message(round_info):
    desc = ''
    targets = round_info['targets']
    for i, target in enumerate(targets):
        data = targets[target]
        target_type = f"**{data['type']}"
        if len(targets) > 2 and i > 0:
            target_type += f' {i}'

        guessed_by = '???'
        if data['guessed_by']:
            guessed_by = f"{data['print']} - guessed by {data['guessed_by'].mention}"
        desc += f'{target_type}** : {guessed_by}\n'

    message = create_message(f"Round {round_info['round_no']} - Scoreboard", desc, discord.Color.dark_gray())
    return message

def normalise(s, target=False):
    s = s.lower()
    s = re.sub(r'&', 'and', s)
    if target:
        s = hide_details(s)
        s = unidecode(s)
    # s = re.sub(r'[\!\?][^w]', ' ', s)
    s = re.sub(r' +', ' ', s)
    s = s.translate(str.maketrans('', '', string.punctuation))
    s = s.strip()
    return s

def hide_details(s):
    s = re.sub(r'[\(\[].+[\)\]]', '', s)
    s = re.sub(r' - .*', '', s)
    s = s.strip()
    return s
