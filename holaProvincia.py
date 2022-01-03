#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################
# alerta_dengue_bot
# token = "931371541:AAHWAtaJf8t5dWYGPSeN-RRpgWUG46d2Ncc"
# alerta_dengue_bot
##################

##################
# desarrollo_alerta_dengue_bot
token = '5009804862:AAHUaqVBiXjHDO4t4eesy73ssgZrNjhPKFI' 
# desarrollo_alerta_dengue_bot
##############


import logging
import requests
#import sys

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)#, InlineKeyboardMarkup) #InlineKeyboardButton
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler)

import  psycopg2

con = psycopg2.connect(database='dengue', user='dengue_bot', host='127.0.0.1', password='d3ngu3_80t')
c = con.cursor()
    


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

SELECCION, RECIBIR, ENVIAR, GENDER, PHOTO, LOCATION, BIO, AGENTE_UBICACION = range(8)
END = -1 

def prueba(update, context):
    #canal_id = -1001431836706
    update.message.reply_text("Hola!, Esto es una prueba.")

def start(update, context):
    
    query = """
    select nombre, reportes
    from agente
    where agente_id={}
    """.format(update.message.from_user['id'])
    c.execute(query)#con.rollback()
    agente = c.fetchall()
    if len(agente)==0:
        update.message.reply_text("Bienvenidx!")
        update.message.reply_text("TODO: Verificar que le agente participe del canal de telegram para promotores de salud") 
        
        context.user_data['agente_id'] = update.message.from_user['id']
        context.user_data['nombre'] = update.message.from_user['first_name']
        context.user_data['apellido'] = update.message.from_user['last_name']
        
        update.message.reply_text("Envianos tu ubicación, la tuya, de donde sos vos")       
        
        return AGENTE_UBICACION
    else:
        update.message.reply_text('Hola {}!'.format(agente[0][0]))
        if agente[0][1]==1:
            update.message.reply_text('Tenemos guardado {} reporte tuyo!'.format(agente[0][1]))
        else:
            update.message.reply_text('Tenemos guardado {} reportes tuyos!'.format(agente[0][1]))
        reply_keyboard = [['Recibir', 'Enviar']]
        
        update.message.reply_text(
            'Qué querés hacer hoy?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        
        return SELECCION



def ubicacion(update, context):
    user = update.message.from_user
    context.user_data['latitud'] = update.message.location.latitude
    context.user_data['longitud'] = update.message.location.longitude
    
    user_location = update.message.location
    logger.info("Ubicación de %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    
def ubicacionAgente(update, context):
    ubicacion(update, context)
    update.message.reply_text('Gracias por enviarnos tu ubicación!')
    nuevoAgente(update, context)
    bienvenide(update, context)
    return ConversationHandler.END

def ubicacionAgente_texto(update, context):
    estado = ubicacion_texto(update, context, END, AGENTE_UBICACION)
    if estado == END:
        update.message.reply_text('Gracias por enviarnos tu ubicación!')
        nuevoAgente(update, context)
        bienvenide(update, context)
        return ConversationHandler.END
    return estado

def ubicacion_texto(update, context, siguiente, anterior):
    #user = update.message.from_user
   
    texto = update.message.text
    
    if "goo.le/maps/" in texto or "google.com/maps" in texto:
        #url = 'https://goo.gl/maps/B1csvRNvmKmjjBY88'
        #url = 'https://www.google.com/maps/@4.116412,-72.958531,6z'
        page = requests.get(texto) 
        lat = float(page.text.split("center=")[1].split("%")[0])
        lon = -float(page.text.split("center=")[1].split("%")[1].split("-")[1].split("&")[0])
        context.user_data['latitud'] = lat
        context.user_data['longitud'] = lon    
        link = "https://www.google.com/maps/@{},{},15z".format(lat,lon)
        update.message.reply_text('enviaste la siguiente coordenada')
        update.message.reply_text(link) 
        return siguiente
    if len(texto.split(","))==2:
        lat = float(texto.split(",")[0])
        lon = float(texto.split(",")[1])
        link = "https://www.google.com/maps/@{},{},15z".format(lat,lon)
        context.user_data['latitud'] = lat
        context.user_data['longitud'] = lon
        update.message.reply_text('enviaste la siguiente coordenada')
        update.message.reply_text(link) 
        return siguiente
    else:
        update.message.reply_text('Lo que nos enviaste no lo podemos identificar como una ubicación '
                                  ' Si estás en el lugar del hecho, compartinos la ubicación desde tu celular. '
                                  ' Sino compartinos una ubicación de google maps, '
                                  'o directamente envianos las coordenadas ')
        
        update.message.reply_text('Si querés salir evía la palabra: cancelar')
        return anterior
       
def bienvenide(update, context):
    
    update.message.reply_text('Bienvenide!')
    update.message.reply_text('Eliminado los objetos que juntan agua evitamos los mosquitos!')
    update.message.reply_text('Contactame cuando veas criaderos y mosquitos')
    update.message.reply_text('Pero lo más importante es lo que puedan hacer ustedes en el momento!')
    update.message.reply_text('A los mosquitos y el dengue lo evitamos entre tod*s')
    update.message.reply_text('Nos vemos!')
        

def nuevoAgente(update, context):
    

    
    insert = """
    insert into agente 
    (agente_id, nombre, apellido, latitud, longitud, fecha, reportes )
    values (%s,%s,%s,%s,%s,%s,%s)"""
    
    c.execute(insert,(
            context.user_data['agente_id'],
            context.user_data['nombre'],
            context.user_data['apellido'],
            context.user_data['latitud'],
            context.user_data['longitud'],
            update.message.date,
            0))
    
    con.commit()

def seleccion(update, context):
    if update.message.text == "Recibir":
        recibir(update, context)
        cancel(update, context)
        return ConversationHandler.END
    if update.message.text == "Enviar":
        enviar(update, context)
        return GENDER

def recibir(update, context):
    update.message.reply_text('Mirá este video')
    update.message.reply_text('https://www.youtube.com/watch?v=cV7fsxosrDc')
    update.message.reply_text('Compartilo!')

def enviar(update, context):
    reply_keyboard = [['Criaderos', 'Larvas', 'Mosquitos']]
    
    
    query = """
    select reportes
    from agente
    where agente_id={}
    """.format(update.message.from_user['id'])
    
    update.message.reply_text('Sin agua estancada no hay ni mosquitos ni dengue!')
    
    c.execute(query)#con.rollback()
    context.user_data['numero'] = c.fetchall()[0][0] + 1

    
    update.message.reply_text(
        'Qué querés reportar hoy?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )    

    context.user_data['agente_id'] = update.message.from_user['id']
    context.user_data['nombre'] = update.message.from_user['first_name']
    context.user_data['apellido'] = update.message.from_user['last_name'] #Acá hay que poner un if por si no tienen Z
    context.user_data['inicio'] = update.message.date
    

def gender(update, context):
    user = update.message.from_user
    
    context.user_data['tipo'] = update.message.text
    
    if update.message.text == 'Criaderos':
        update.message.bot.send_photo(chat_id=update.message.chat['id'], photo=open('imagenes/criaderos.jpg', 'rb'))
    
    if update.message.text == 'Larvas':
        update.message.bot.send_photo(chat_id=update.message.chat['id'], photo=open('imagenes/larvas-medio.jpg', 'rb'))
    
    if update.message.text == 'Mosquitos':
        update.message.bot.send_photo(chat_id=update.message.chat['id'], photo=open('imagenes/mosquitos-muchos.jpg', 'rb'))
        
    
    logger.info("El usuario {} denuncia presencia de {}".format(user.first_name, update.message.text) )
    reply_keyboard = [['Poca', 'Bastante', 'Mucha']]
    
    update.message.reply_text(
        'La cantidad de {} es:'.format(update.message.text),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

    return PHOTO


def photo(update, context):
    
    context.user_data['magnitud'] = update.message.text
    
    update.message.reply_text('Tu respuesta fue {}'.format(update.message.text))
    update.message.reply_text('Ahora envianos la ubicación donde se observó el hecho')
    return LOCATION


def skip_photo(update, context):
    
    texto = 'Necestiamos saber la cantidad. \n Si querés cancelar el reporte enviá cancelar'
                      
    
    update.message.reply_text(texto)

    return LOCATION


def location(update, context):
    ubicacion(update, context)
    update.message.reply_text('Gracias por enviarnos la ubicación de la denuncia!')
    publico_privado(update, context)
    return BIO

def publico_privado(update, context):
    reply_keyboard = [['Público', 'Privado']]
    
    update.message.reply_text(
        'Decinos si es un espacio de acceso público o privado',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )



def skip_location(update, context):
    estado = ubicacion_texto(update, context, BIO, LOCATION)
    if estado == BIO:
        publico_privado(update, context)
    return estado

def nuevoReporte(update, context):
    
    insert = """
    insert into reporte 
    (agente_id, numero, tipo, magnitud, espacio, latitud, longitud, inicio, final)
    values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    res = ( context.user_data['agente_id'],
            context.user_data['numero'],
            context.user_data['tipo'],
            context.user_data['magnitud'],
            context.user_data['espacio'],
            context.user_data['latitud'],
            context.user_data['longitud'],
            context.user_data['inicio'],
            context.user_data['final']
    )
    c.execute(insert,res)
    
    update = """
    UPDATE agente
    SET reportes = {}
    WHERE agente_id = {}
    """.format(context.user_data['numero'],context.user_data['agente_id'])
    c.execute(update)
    
    con.commit()
    return res
    
def bio(update, context):
    user = update.message.from_user
    
    context.user_data['espacio'] = update.message.text
    
    logger.info("El reporte de %s se encuentra en un espacio %s", user.first_name, update.message.text)
    update.message.reply_text(
            'Muchas gracias!'
            'Tu reporte lo estamos usando para decidir dónde enviar una ayuda especial'
            'Lo que puedan hacer ustedes en el momento es mucho más importante'
            'Eliminado los objetos que juntan agua evitamos los mosquitos!'
            )
    
    context.user_data['final'] = update.message.date
    
    nuevoReporte(update, context)
    
    update.message.reply_text('Chau!')
    return ConversationHandler.END


def button(update, context):
    query = update.callback_query
    query.edit_message_text(text="Opción seleccionada fue: {}".format(query.data))
    
def cancel(update, context):
    texto = 'Nos vemos! \n Recordá que sin agua estancada no hay dengue! \n'\
            'Para evitar los mosquitos, eliminen todo los objetos que tengan agua estancada' \
            'Avisanos por acá cuando ustedes ya no lo puedan resolver!'
    
    user = update.message.from_user
    logger.info("El usuario %s canceló el reporte.", user.first_name)
    update.message.reply_text(texto,
                              reply_markup=ReplyKeyboardRemove())
    update.message.reply_text('Chau!')

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    con.rollback()
    update.message.reply_text('Perdón!, tuvimos un problema.')
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def agentes(update, context):
    texto = update.message.text
    
    if texto.split(' ')[1]=='d3ngu3_80t':
        
        query = """
        select *
        from agente
        """
        c.execute(query)#con.rollback()
        agente = c.fetchall()
        update.message.reply_text("{}".format(agente))
    else:
        update.message.reply_text("Opción invalida")


# Create the Updater and pass it your bot's token.
# Make sure to set use_context=True to use the new context based callbacks
# Post version 12 this will no longer be necessary
updater = Updater(token, use_context=True)

# Get the dispatcher to register handlers
dp = updater.dispatcher

dp.add_handler(CommandHandler('recibir', recibir))
dp.add_handler(CommandHandler('prueba', prueba))
dp.add_handler(CommandHandler('agentes', agentes))


# Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, start)],

    states={
        AGENTE_UBICACION:[MessageHandler(Filters.location, ubicacionAgente),
                          MessageHandler(Filters.text, ubicacionAgente_texto)],
        SELECCION : [MessageHandler(Filters.regex('^(Recibir|Enviar)$'), seleccion)],
        GENDER: [MessageHandler(Filters.regex('^(Criaderos|Larvas|Mosquitos)$'), gender)],

        PHOTO: [MessageHandler(Filters.regex('^(Poca|Bastante|Mucha)$'), photo),
                MessageHandler(Filters.text, skip_photo)],

        LOCATION: [MessageHandler(Filters.location, location),
                   MessageHandler(Filters.text, skip_location)],

        BIO: [MessageHandler(Filters.regex('^(Público|Privado)$'), bio)]
    },

    fallbacks=[MessageHandler(Filters.regex('^(cancelar|Cancelar|salir|stop|quit|exit)$'), cancel), CallbackQueryHandler(cancel, pattern='^' + str(END) + '$')]
)

dp.add_handler(conv_handler)

# log all errors
dp.add_error_handler(error)

# Start the Bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()



