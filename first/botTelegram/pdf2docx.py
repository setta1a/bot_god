from typing import Tuple
from pdf2docx import parse


def convert_pdf2docx(input_file: str, output_file: str, pages: Tuple = None):
    """Преобразует PDF в DOCX"""
    if pages:
        pages = [int(i) for i in list(pages) if i.isnumeric()]
    result = parse(pdf_file=input_file, docx_with_path=output_file, pages=pages)
    summary = {
        "Исходный файл": input_file,
        "Страниц": str(pages),
        "Результат преобразования": output_file
    }
    # Печать сводки
    print("#### Отчет ########################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("###################################################################")
    return result


@bot.message_handler(commands=['pdf2docx'])
def pdf2docx_command(message):
    if not os.path.exists('files'):
        os.mkdir("files")
    send = bot.send_message(message.chat.id, 'Отправьте pdf файл')
    bot.register_next_step_handler(send, pdf2docx)


def pdf2docx(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    except:
        bot.send_message(message.chat.id, 'Вы отправили что-то не то')
        delete_all_tmp_files()
        return
    src = 'files/' + message.document.file_name
    tmpdocx = open("files/tmpdocx.docx", "w")
    tmpdocx.close()
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    try:
        convert_pdf2docx(src, "files/tmpdocx.docx")
    except:
        bot.send_message(message.chat.id, 'Не могу конвертировать файл')
        delete_all_tmp_files()
        return
    srcdocx = src[0:len(src) - 3] + 'docx'
    bot.send_document(message.chat.id, open(srcdocx, 'rb'))
    delete_all_tmp_files()
