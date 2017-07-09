import subprocess
import os
import shutil
from urllib.parse import urlparse
import feedparser
import requests
import newspaper
from ffmpy import FFmpeg

feed = feedparser.parse('http://feeds.feedburner.com/iolandachannel')
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
    inputs = {
        'article.mp3': None,
    }
    for image in images:
        inputs[image] = None
    ff = FFmpeg(inputs=inputs, outputs={'article.avi': '-y'})
    print(ff.cmd)
    ff.run()
    command = f'youtube-upload article.avi --title "{title}"'
    command += f' --description "{text}\n\n'
    command += f'LINK PARA A NOTÍCIA ORIGINAL: {news_link}"'
    subprocess.call(command, shell=True)
    print(f'Article parsed: {title}')
    import sys; sys.exit()

print('That\'s all folks!')
