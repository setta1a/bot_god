
    elif message.text[:38] == 'https://www.youtube.com/playlist?list=':
    # Для плейлиста
        playlist = Playlist(message.text)
        for url in playlist:
            try:
                audio = create_audio(url)
                bot.send_audio(message.chat.id, audio)
                bot.register_next_step_handler(delete_all_music_in_directory())
            except Exception as _ex:
                writes_logs(_ex)
        else:
            bot.send_message(message.chat.id, "Плейлист закрыт")

    elif message.text[:32] == 'https://www.youtube.com/watch?v=' or message.text[:17] == 'https://youtu.be/':
    # Для видео
        try:
            url = message.text
            audio = create_audio(url)
            bot.send_video(message.chat.id, audio)
            bot.register_next_step_handler(delete_all_music_in_directory())
        except Exception as _ex:
            writes_logs(_ex)
