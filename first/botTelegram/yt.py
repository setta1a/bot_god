

from pytube import YouTube
from pytube import Playlist
import datetime
import re




def writes_logs(_ex):
    """Записывает логи в файл 'logs.log', в котором будет время и ошибка"""
    with open('logs.log', 'a') as file_log:
        file_log.write('\n' + str(datetime.datetime.now()) + ': ' + str(_ex))


def create_audio(url):
    """Скачивает и открывает файл на бинарное чтение"""
    try:
        yt = YouTube(url).streams.get_highest_resolution()
        path = yt.download("music")
        audio = open(path, 'rb')
        return audio
    except Exception as _ex:
        writes_logs(_ex)


def delete_all_music_in_directory():
    """Удаляет все скаченные аудио из папки 'music'"""
    if not os.path.exists('music'):
        os.mkdir('music')
    for file in os.listdir('music'):
        try:
            if re.search('mp4', file):
                mp4_path = os.path.join('music', file)
                os.remove(mp4_path)
        except Exception as _ex:
            writes_logs(_ex)

