import subprocess
import os
import shutil
from urllib.parse import urlparse
import feedparser
import requests
import newspaper

feed = feedparser.parse('http://feeds.feedburner.com/vice/AprM')
chapters = []

for entry in feed['entries']:
    title = entry['title']
    print(f'Parsing: {title}')
    news_link = entry['link']
    article = newspaper.Article(news_link)
    article.download()
    article.parse()
    media = article.top_img
    if not media:
        continue
    images = []
    response = requests.get(media, stream=True)
    filename = os.path.basename(urlparse(media).path)
    filename = f'images/{filename}'
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    images.append(filename)

    from gtts import gTTS
    text = article.text
    tts = gTTS(text=text, lang='pt', slow=False)
    tts.save("article.mp3")
    command = 'ffmpeg -y -loop 1 -r 1'
    for image in images:
        command += f' -i {image}'
    command += '  -i article.mp3 -acodec copy -shortest -qscale 5 article.avi'
    print(command)
    subprocess.call(command, shell=True)
    command = f'youtube-upload article.avi --title "{title}"'
    command += f' --description "{text}"'
    subprocess.call(command, shell=True)
    print(f'Article parsed: {title}')

print('That\'s all folks!')
