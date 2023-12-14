import discord
from discord.ext import commands
import pytesseract
import cv2
import numpy as np
from PIL import Image
import requests

def get_string(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite("removed_noise.png", img)
    cv2.imwrite(img_path, img)   

    result = pytesseract.image_to_string(Image.open(img_path), lang="pol")
    return result


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='.', description="This is an OCR_test bot")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


@client.event
async def on_message(message):
    if message.content.startswith('$ocr'):
        try:
            url = message.attachments[0].url
            r = requests.get(url)
            filename = "img.png"
            with open(filename, 'wb') as out_file:
                out_file.write(r.content)
                print(url)
                context = await bot.get_context(message)
                ocr = get_string("img.png")

            try:
                await context.send(ocr)
            except:
                await context.send("Nie znaleziono tesktu.")
        except:
            pass
        await client.process_commands(message)

client.run('MTE3NzMxMDU5MzM3MjQwNTg4MA.G1TYoB.B7EehZpdN9k0WoYRrrrWoWF9hyWGGtbiI2n_CM')
