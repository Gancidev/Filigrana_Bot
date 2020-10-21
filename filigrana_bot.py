#!/usr/bin/python
# -*- coding: latin-1 -*-
import time
import os
import telepot
from telepot.loop import MessageLoop
from pprint import pprint
from pdfrw import PdfReader, PdfWriter, PageMerge
import unicodedata


def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError):
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def remove_letter(text):
    text = strip_accents(text)
#    text = re.sub('[ ]+', "", text)
#    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    return text

def convert_this(dest, ext):
    #convertapi.convert('pdf',
    #        {'File': '{}'.format(dest)},
    #        from_format=ext[1:]).save_files('/home/pi/test_bot/mtp')
    comando="unoconv "+dest
    os.system(comando)

def sizepage(page):
    result = PageMerge()
    result.add(page)
    return result[0].w, result[0].h

def fixpage(page, width,height):
    result = PageMerge()
    result.add(page)
    if width > height:
        if width > 842:
            result[0].w = height * 1.6
            result[0].x = 50
        else:
            result[0].x = 0
            result[0].w = height * 1.4
    else:
        if height > 842:
            result[0].y = 125
        result[0].w = width
        result[0].x = 0
    return result.render()

def filigrana(input_file,output_file,chat_id):
    reader_input = PdfReader(input_file)
    writer_output = PdfWriter()

    page=reader_input.pages[0]
    w,h = sizepage(page)
    try:
        logo=open("/home/pino/ftp/converter_bot/"+str(chat_id)+"_logo_settings.txt","r")
        setting=logo.read()
        logo.close()
    except IOError:
        logo=open("/home/pino/ftp/converter_bot/"+str(chat_id)+"_logo_settings.txt","w")
        logo.write("on")
        setting="on"

    try:
        opacity=open("/home/pino/ftp/converter_bot/"+str(chat_id)+"_opacity_settings.txt","r")
        value_opacity=opacity.read()
        opacity.close()
    except IOError:
        opacity=open("/home/pino/ftp/converter_bot/"+str(chat_id)+"_opacity_settings.txt","w")
        opacity.write("25")
        opacity.close()
        value_opacity=25

    if setting=="on":
        if int(w) > int(h):
            watermark_input=PdfReader("/home/pino/ftp/filigrane/fil_"+str(value_opacity)+"_logo_or.pdf")
            watermark = fixpage(watermark_input.pages[0],int(w),int(h))
        else:
            watermark_input=PdfReader("/home/pino/ftp/filigrane/fil_"+str(value_opacity)+"_logo_ver.pdf")
            watermark = fixpage(watermark_input.pages[0],int(w),int(h))
    else:
        if int(w) > int(h):
            watermark_input=PdfReader("/home/pino/ftp/filigrane/fil_"+str(value_opacity)+"_or.pdf")
            watermark = fixpage(watermark_input.pages[0],int(w),int(h))
        else:
            watermark_input=PdfReader("/home/pino/ftp/filigrane/fil_"+str(value_opacity)+"_ver.pdf")
            watermark = fixpage(watermark_input.pages[0],int(w),int(h))

    for current_page in range(len(reader_input.pages)):
        merger = PageMerge(reader_input.pages[current_page])
        merger.add(watermark).render()
    writer_output.write(output_file, reader_input)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print "\n"
    pprint(msg)
    with open("/home/pino/ftp/log.txt",'a') as log:
        log.write("\n")
        log.write(str(msg))
        log.write("\n")
    username = msg['from']['username']
    user_id = msg['from']['id']
    if content_type == 'text':
	text=msg['text']
        if text == "/start" or text == "ciao":
            bot.sendMessage(chat_id, "Ciao " + username + ", mandami il file che vuoi convertire, oppure lancia il comando /help per scoprire il mio funzionamento.")
        elif text=="/help":
            bot.sendMessage(chat_id, "Il bot si occupa di convertire i file a lui inviati mediante il tool di sistema unoconv e in seguito appone una filigrana ad ogni pagina mediante la libreria pdfrw e i moduli di essa PdfWriter/Reader/ e PageMerge \n\nI comandi che supporta sono:\n 1) /filigrana - abilita o disabilita la filigrana;\n 2) /logo - che abilita o disabilita l'utilizzo del logo come filigrana;\n  3) /opacity {value} - che imposta il livello di opacita', value deve essere compreso tra 5 e 30 ed essere multiplo di 5 ( EX: /opacity 20 );\n  4) /help - stampa questo messaggio di aiuto.\n\n I file che vengono inviati al bot sono eliminati una volta terminato il processo di conversione e filigrana.")
        elif text=="/logo":
            try:
                logo=open("/home/pino/ftp/converter_bot/"+str(chat_id)+"_logo_settings.txt","r")
                setting=logo.read()
                logo.close()
                logo=open("/home/pino/ftp/converter_bot/"+str(chat_id)+"_logo_settings.txt","w")
                if setting=="on":
                    logo.write("off")
                    bot.sendMessage(chat_id,"Impostazione aggiornata ad OFF (filigrana i file con scritta)")
                else:
                    logo.write("on")
                    bot.sendMessage(chat_id,"Impostazione aggiornata ad ON (filigrana i file con logo)")
            except IOError:
                logo=open("/home/pino/ftp/converter_bot/"+str(chat_id)+"_logo_settings.txt","w")
                logo.write("on") 
                bot.sendMessage(chat_id,"Impostazione aggiornata ad ON (filigrana i file con logo)")
        elif text=="/opacity":
                bot.sendMessage(chat_id,"Sintassi del comando non rispettata: /opacity {value}")
        elif text[:8]=="/opacity" and text[9:]:
            new_opacity=int(text[9:])
            if new_opacity>=5 and new_opacity<=30 and new_opacity%5==0:
                opacity=open("/home/pino/ftp/converter_bot/"+str(chat_id)+"_opacity_settings.txt","w")
                opacity.write(str(new_opacity))
                bot.sendMessage(chat_id,"Impostazione aggiornata a "+str(new_opacity))
            else:
                bot.sendMessage(chat_id,"Valore di opacity: "+str(new_opacity)+" non valido, inserirne uno compreso tra 5 e 30 e multiplo di 5")
        elif text=="/filigrana":
            try:
                fil=open("/home/pino/ftp/converter_bot/"+str(chat_id)+"_filigrana_settings.txt","r")
                setting=fil.read()
                fil.close()
                fil=open("/home/pino/ftp/converter_bot/"+str(chat_id)+"_filigrana_settings.txt","w")
                if setting=="on":
                    fil.write("off")
                    bot.sendMessage(chat_id,"Impostazione aggiornata ad OFF (non filigrana)")
                else:
                    fil.write("on")
                    bot.sendMessage(chat_id,"Impostazione aggiornata ad ON (filigrana)")
            except IOError:
                fil=open("/home/pino/ftp/converter_bot/"+str(chat_id)+"_filigrana_settings.txt","w")
                fil.write("on")
                bot.sendMessage(chat_id,"Impostazione aggiornata ad ON (filigrana)")
        else:
            bot.sendMessage(chat_id,"Non posso interpretare messaggi di testo o comandi non supportati solo file.")

    if content_type == 'document':
        file_id = msg['document']['file_id']
        file_name = msg['document']['file_name']
        file_name_2 = file_name.replace(" ","_")
        dest="/home/pino/ftp/converter_bot/"+file_name_2
        dest=dest.encode("utf-8")
        dest=remove_letter(dest)
        bot.download_file(file_id, dest)
        name,ext=os.path.splitext(dest)
        convert_this(dest,ext)
        try:
            fil=open("/home/pino/ftp/converter_bot/"+str(chat_id)+"_filigrana_settings.txt","r")
            setting=fil.read()
            fil.close()
        except IOError:
            fil=open("/home/pino/ftp/converter_bot/"+str(chat_id)+"_filigrana_settings.txt","w")
            fil.write("on")
            setting="on"
        if setting=="on":
            filigrana(name+".pdf" , name+"_f.pdf",chat_id)
            f=open(name+"_f.pdf",'rb')
        else:
            f=open(name+".pdf",'rb')
        bot.sendDocument(chat_id,f)
        os.remove(dest)
        os.remove(name+'.pdf')
        os.remove(name+'_f.pdf')



TOKEN = '1282503366:AAF48z14JFuujbTMNzheTMPiwozVcuNfkqA'

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
