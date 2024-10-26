import discord
import os
from discord.ext import tasks
from dotenv import load_dotenv
from googleapiclient.discovery import build
from db_man import get_id, add_id, connectdb

load_dotenv()

bot_token = os.getenv("TOKEN")
utube_api = os.getenv("UAPI")
val_id = os.getenv("VAL_CHANNEL_ID")
blackie_id = os.getenv("BLACKIE_CHANNEL_ID")
chuthulu_id = os.getenv("CHUTHULU_CHANNEL_ID")
nightmare_id = os.getenv("NIGHTMARE_CHANNEL_ID")
vnot_id = os.getenv("VAL_NOTI_CHANNEL")
cnot_id = os.getenv("COMMON_NOTI_CHANNEL")
rid = int(os.getenv("ROLE_ID"))  
guild_id = int(os.getenv("GUILD_ID"))  

channel_ids = [val_id, blackie_id, chuthulu_id, nightmare_id]

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

utube = build('youtube', 'v3', developerKey=utube_api)

latest_vid_id = {}


@client.event
async def on_ready():
    global guild
    guild = client.get_guild(guild_id)
    if guild is None:
        print("Guild with ID not found")
        return
    
    activity = discord.Activity(type=discord.ActivityType.watching, name="YouTube")
    print(f"Logged in as {client.user.name}")
    await client.change_presence(activity=activity)
    check_new_video.start()


@tasks.loop(minutes=1)
async def check_new_video():
    global latest_vid_id

    for channel_id in channel_ids:
        try:
            request = utube.channels().list(part='contentDetails', id=channel_id)
            response = request.execute()
            playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

            request = utube.playlistItems().list(part='snippet', playlistId=playlist_id, maxResults=1)
            response = request.execute()

            new_video_id = response['items'][0]['snippet']['resourceId']['videoId']
            video_title = response['items'][0]['snippet']['title']
            video_url = f'https://www.youtube.com/watch?v={new_video_id}'
            last_video_id = get_id(channel_id)

            if channel_id not in latest_vid_id or new_video_id != latest_vid_id[channel_id]:
                latest_vid_id[channel_id] = new_video_id
                role = discord.utils.get(guild.roles, id=rid)
                if role is None:
                    print(f"Role with ID {rid} not found in guild.")
                    continue
                if last_video_id is None:
                    add_id(channel_id, new_video_id)
                elif last_video_id != new_video_id:
                    add_id(channel_id, new_video_id)
                    if channel_id == val_id:
                        channel = client.get_channel(int(vnot_id))
                        if channel is None:
                            print(f"Notification channel with ID {vnot_id} not found.")
                            continue
                        try:
                            await channel.send(f"ValentineisHere just uploaded a new video **{video_title}** Go check it out!!\n{video_url}\n{role.mention}")
                        except Exception as error:
                            print(f"Failed to send message in {vnot_id}: {error}")

                    elif channel_id == blackie_id:
                        channel = client.get_channel(int(cnot_id))
                        if channel is None:
                            print(f"Notification channel with ID {cnot_id} not found")
                            continue
                        try:
                            await channel.send(f"Mean just uploaded a new video **{video_title}** Go check it out!!\n{video_url}\n{role.mention}")
                        except Exception as error:
                            print(f"Failed to send message in {cnot_id}: {error}")
                    elif channel_id == chuthulu_id:
                        channel = client.get_channel(int(cnot_id))
                        if channel is None:
                            print(f"Notification channel with ID {cnot_id} not found")
                            continue
                        try:
                            await channel.send(f"not so great cthulhu just uploaded a new video **{video_title}** Go check it out!!\n{video_url}\n{role.mention}")
                        except Exception as error:
                            print(f"Failed to send message in {cnot_id}: {error}")
                    elif channel_id == nightmare_id:
                        channel = client.get_channel(int(cnot_id))
                        if channel is None:
                            print(f"Notification channel with ID {cnot_id} not found")
                            continue
                        try:
                            await channel.send(f"gamerXamit just uploaded a new video **{video_title}** Go check it out!!\n{video_url}\n{role.mention}")
                        except Exception as error:
                            print(f"Failed to send message in {cnot_id}: {error}")
        except KeyError as e:
            print(f"Error: {e}")
        except Exception as error:
            print(f"Error: {error}")


def main():
    client.run(bot_token)


if __name__ == "__main__":
    main()
