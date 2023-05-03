import json
import os
from natsort import natsorted
from tinydb import TinyDB, Query
from pyrogram import Client
from pyrogram.raw import functions
from random import randint
from colorama import Fore, Style
from .CoolText import getImage
from magic import Magic
from .VideoDetails import videoDetails
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv()
api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")

logoID = 1779834160


def progress(current, total):
    bar_length = 50
    filled_length = int(round(bar_length * current / float(total)))
    percents = round(100.0 * current / float(total), 1)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    tqdm.write(f'|{bar}| {percents}%\r', end='')


async def start(section_name, section_path, database, group_id):
    mime = Magic(mime=True)
    db = TinyDB(database)
    Section = Query()
    async with Client("my_account", api_id, api_hash) as app:
        files = natsorted(os.scandir(section_path), key=lambda x: x.name)
        print(Fore.BLUE + f"Section: {section_name} ->" + Style.RESET_ALL)

        # Check if Section Exists or not at DB, if exists then it exists in telegram also.
        try:
            if db.search(Section.name == section_name)[0]["path"] == section_path:
                section_exists = True
        except:
            section_exists = False

        # If Section Exists, get thread ID or else Create Section, get thread ID, all using DB.
        if section_exists:
            thread_id = db.search(Section.name == section_name)[0]["thread"]
            print(
                Fore.CYAN + f"  Section already exists at thread ID: {thread_id}." + Style.RESET_ALL)
        else:
            channel_id = await app.resolve_peer(group_id)
            rn_id = randint(10000, 20000000)
            create_topic_res = await app.invoke(functions.channels.CreateForumTopic(channel=channel_id,
                                                                                    title=section_name,
                                                                                    random_id=rn_id
                                                                                    ))

            create_topic_res = json.loads(str(create_topic_res))

            db.insert({'Type': 'Section',
                       'name': section_name,
                       'path': section_path,
                       'thread': create_topic_res['updates'][0]['id']
                       })
            thread_id = db.search(Section.name == section_name)[0]["thread"]
            print(
                Fore.GREEN + f"  Section Successfully created at thread ID: {thread_id}" + Style.RESET_ALL)

        # Send Topic heading image using Cool Text.
        if db.search(Section.HeadImage == section_name):
            find_head = db.search(Section.HeadImage == section_name)
            print(
                Fore.GREEN + f"  Heading Image Already Existed at message ID: {find_head[0]['chatID']}")
        else:
            image_result = getImage(fileName=section_name, logoID=logoID)
            logoID = image_result["newID"]

            heading_caption = f'''<b>{section_name}</b>'''

            heading_image_result = await app.send_photo(chat_id=group_id,
                                                        reply_to_message_id=thread_id,
                                                        photo=image_result['image'],
                                                        caption=heading_caption,
                                                        parse_mode=app.parse_mode.HTML
                                                        )

            heading_image_result = json.loads(str(heading_image_result))

            db.insert({'type': "HeadingImage", 'HeadImage': section_name,
                      'chatID': heading_image_result['id']})
            print(
                Fore.GREEN + f"  Successfully Uploaded Section heading image at message ID: {heading_image_result['id']}")

        # Send all Section Videos and Files.
        for file in files:
            if db.search(Section.filePath == file.path):
                search_result = db.search(Section.filePath == file.path)
                print(Fore.GREEN + f"    File -> {file.name}")
                print(
                    Fore.YELLOW + f"      Already Exists at chatID: {search_result[0]['chatId']}\n"+Style.RESET_ALL)
            else:
                filename = mime.from_file(file.path)
                file_type = file.name.split(".")[-1]

                if file.is_file() and filename.find('video') != -1:

                    print(Fore.GREEN + f"    File -> {file.name}")

                    video_details = videoDetails(file.path)
                    vid_thumbnail = video_details["thumb"]
                    vid_duration = video_details["duration"]
                    vid_width = video_details["width"]
                    vid_height = video_details["height"]
                    vid_caption = f"<b>{file.name}</b>"

                    video_upload_result = await app.send_video(chat_id=group_id,
                                                               reply_to_message_id=thread_id,
                                                               video=file.path,
                                                               caption=vid_caption,
                                                               parse_mode=app.parse_mode.HTML,
                                                               duration=vid_duration,
                                                               thumb=vid_thumbnail,
                                                               width=vid_width,
                                                               height=vid_height,
                                                               progress=progress
                                                               )
                    print('\n')

                    file_sent = json.loads(str(video_upload_result))

                    print(
                        Fore.BLUE + f"      Successfully uploaded at message ID: {file_sent['id']}" + Style.RESET_ALL)
                    db.insert(
                        {'type': 'video', 'filePath': file.path, 'chatId': file_sent["id"]})

                elif file_type == "vtt" or file_type == "srt":
                    print(Fore.GREEN + f"   File -> {file.name}")
                    print(Fore.LIGHTMAGENTA_EX +
                          f"        Uploading File..." + Style.RESET_ALL)
                    file_sent = await app.send_document(chat_id=group_id,
                                                        document=file.path,
                                                        reply_to_message_id=thread_id
                                                        )
                    file_sent = json.loads(str(file_sent))
                    db.insert(
                        {'type': 'video', 'filePath': file.path, 'chatId': file_sent["id"]})
                    print(
                        Fore.BLUE + f"      Successfully Uploaded at chatID : {file_sent['id']}\n"+Style.RESET_ALL)

                else:
                    print(Fore.GREEN + f"   File -> {file.name}")
                    print(Fore.LIGHTMAGENTA_EX + f"     Uploading File...")
                    file_sent = await app.send_document(chat_id=group_id,
                                                        document=file.path,
                                                        reply_to_message_id=thread_id
                                                        )
                    file_sent = json.loads(str(file_sent))
                    db.insert(
                        {'type': 'video', 'filePath': file.path, 'chatId': file_sent["id"]})
                    print(
                        Fore.BLUE + f"      Successfully Uploaded at chatID : {file_sent['id']}\n"+Style.RESET_ALL)
