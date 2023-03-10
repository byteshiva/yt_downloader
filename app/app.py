from flask import Flask, jsonify, request, Response
from werkzeug.utils import secure_filename
from pytube import YouTube
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = './downloads'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

class Downloader:
    def __init__(self, url):
        self.url = url

    def download(self):
        pass

class VideoDownloader(Downloader):
    def download(self):
        yt = YouTube(self.url)
        video = yt.streams.first()
        title = yt.title.replace(' ', '_').lower() + '.mp4'
        video.download(DOWNLOAD_FOLDER, filename=title)
        return title

class AudioDownloader(Downloader):
    def __init__(self, url):
        super().__init__(url)
        self.video_title = None

    def _get_video_title(self):
        yt = YouTube(self.url)
        self.video_title = yt.title

    def download(self):
        self._get_video_title()
        yt = YouTube(self.url)
        stream = yt.streams.filter(only_audio=True).first()
        filename = f"{self.video_title}.mp3"
        stream.download(DOWNLOAD_FOLDER, filename=filename)
        return filename

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    if not url:
        return jsonify({'message': 'Url parameter is missing'}), 400

    downloader = VideoDownloader(url)
    title = downloader.download()
    return jsonify({'title': title}), 200

@app.route('/audio', methods=['POST'])
def download_audio():
    url = request.form.get('url')
    if not url:
        return jsonify({'message': 'Url parameter is missing'}), 400

    downloader = AudioDownloader(url)
    title = downloader.download()
    return jsonify({'title': title}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
