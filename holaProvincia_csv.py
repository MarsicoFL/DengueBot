#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import requests
import pandas as pd
import os
#import sys

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)#, InlineKeyboardMarkup) #InlineKeyboardButton
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler)


import  psycopg2


os.chdir('/home/agus/dengue/DengueBot-main')

token = '5009804862:AAHUaqVBiXjHDO4t4eesy73ssgZrNjhPKFI' 

#con = psycopg2.connect(database='dengue', user='dengue_bot', host='127.0.0.1', password='d3ngu3_80t')
#c = con.cursor()
    
diccionario = {}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

SELECCION, RECIBIR, ENVIAR, GENDER, PHOTO, LOCATION, BIO, AGENTE_UBICACION = range(8)
END = -1 


if os.path.isfile('dengue.csv'):
    data_frame = pd.read_csv('dengue.csv')
else:
    data_frame = pd.DataFrame(columns = ['nombre', 'apellido', 'agente_id', 'latitud', 'longitud', 'fecha', 'tipo', 'espacio', 'inicio', 'final'])
print(data_frame)

def prueba(update, context):
    #canal_id = -1001431836706
    update.message.reply_text("Hola!, Esto es una prueba.")

def start(update, context):    

    diccionario['fecha'] = update.message.date
    id = update.message.from_user['id']
    filtro = data_frame[data_frame['agente_id'] == id]
    print('prueba')
    print(len(filtro))
    if len(filtro) == 0:

        update.message.reply_text("¡Bienvenidx!")
        update.message.reply_text('Esta aplicación está pensada para apoyar el trabajo territorial de agentes sanitarios en la prevención de criaderos de mosquitos <b><i>Aedes aegypti</i></b>, transmisores del dengue.', parse_mode='html')


        diccionario['agente_id'] = update.message.from_user['id']
        
        try:
            diccionario['nombre'] = update.message.from_user['first_name']
        except:
            diccionario['nombre'] = 'Agente sin nombre'
        
        try:    
            diccionario['apellido'] = update.message.from_user['last_name']
        except:
            diccionario['apellido'] = 'Agente sin apellido'
            
        diccionario['inicio'] = update.message.date
        
        update.message.reply_text("¿En dónde te encontrás? Compartinos tu ubicación (Location) haciendo click en el “ganchito” ubicado debajo a la derecha.")       
        
        return AGENTE_UBICACION
    
    else:
         

        update.message.reply_text('¡Hola {}!'.format(filtro['nombre'].iloc[0]))
        
        if len(filtro)==1:
            
            update.message.reply_text('¡Tenemos guardado {} reporte tuyo!'.format(len(filtro)))
        
        else:
            
            update.message.reply_text('¡Tenemos guardado {} reportes tuyos!'.format(len(filtro)))
        
        
        update.message.reply_text("¿En dónde te encontrás? Compartinos tu ubicación (Location) haciendo click en el “ganchito” ubicado debajo a la derecha.")
        
        
        
        try:
            diccionario['nombre'] = update.message.from_user['first_name']
        except:
            diccionario['nombre'] = 'Agente sin nombre'
        
        try:    
            diccionario['apellido'] = update.message.from_user['last_name']
        except:
            diccionario['apellido'] = 'Agente sin apellido'
            
        diccionario['inicio'] = update.message.date
        diccionario['agente_id'] = update.message.from_user['id']
        
        return LOCATION



def ubicacion(update, context):
    user = update.message.from_user
    
    diccionario['latitud'] = update.message.location.latitude
    diccionario['longitud'] = update.message.location.longitude
    
    user_location = update.message.location
    #logger.info("Ubicación de %s: %f / %f", user.first_name, user_location.latitude,
     #           user_location.longitude)
    
def ubicacionAgente(update, context):
    ubicacion(update, context)
    update.message.reply_text('!Gracias por enviarnos tu ubicación!')
    #nuevoAgente(update, context)
    #bienvenide(update, context)
# =============================================================================
#     reply_keyboard = [['Recibir', 'Enviar']]
#         
#     update.message.reply_text(
#         'Qué querés hacer hoy?',
#         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
#     )
# =============================================================================
    reply_keyboard = [['Basural a cielo abierto'],
                      ['Acumulación de basura en la calle'],
                      ['Neumáticos en desuso'], 
                      ['Chatarra, chapas u otros objetos voluminosos al descubierto'],
                      ['Recipiente'],
                      ['Terreno sin desmalezar'], 
                      ['Vivienda con objetos que acumulan agua']]
    
    

    
    update.message.reply_text(
        '¿Allí visualizás algún posible criadero de mosquitos? Ingresá la opción que corresponda:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, )
    )    
    
    return GENDER

def ubicacionAgente_texto(update, context):
    estado = ubicacion_texto(update, context, END, AGENTE_UBICACION)
    if estado == END:
        update.message.reply_text('!Gracias por enviarnos tu ubicación!')
        #nuevoAgente(update, context)
        #bienvenide(update, context)
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
        diccionario['latitud'] = lat
        diccionario['longitud'] = lon    
        link = "https://www.google.com/maps/@{},{},15z".format(lat,lon)
        update.message.reply_text('enviaste la siguiente coordenada')
        update.message.reply_text(link) 
        return siguiente
    if len(texto.split(","))==2:
        lat = float(texto.split(",")[0])
        lon = float(texto.split(",")[1])
        link = "https://www.google.com/maps/@{},{},15z".format(lat,lon)
        diccionario['latitud'] = lat
        diccionario['longitud'] = lon
        update.message.reply_text('enviaste la siguiente coordenada')
        update.message.reply_text(link) 
        return siguiente
    else:
        update.message.reply_text('Lo que nos enviaste no lo podemos identificar como una ubicación '
                                  ' Si estás en el lugar del hecho, compartinos la ubicación desde tu celular. '
                                  ' Sino compartinos una ubicación de google maps, '
                                  'o directamente envianos las coordenadas ')
        
        update.message.reply_text('Si querés salir envía la palabra: cancelar')
        return anterior
# =============================================================================
#        
# def bienvenide(update, context):
#     
#     update.message.reply_text('Bienvenidxs!')
#     update.message.reply_text('Esta aplicación está pensada para apoyar el trabajo territorial de agentes sanitarios en la prevención de criaderos de mosquitos Aedes aegypti, transmisores del dengue.')
# =============================================================================
        

#def nuevoAgente(update, context):
    

    
  #  insert = """
   # insert into agente 
    #(agente_id, nombre, apellido, latitud, longitud, fecha, reportes )
    #values (%s,%s,%s,%s,%s,%s,%s)"""
    
    #c.execute(insert,(
     #       context.user_data['agente_id'],
      #      context.user_data['nombre'],
         #   context.user_data['apellido'],
        #    context.user_data['latitud'],
       #     context.user_data['longitud'],
      #      update.message.date,
     #       0))
    
    #con.commit()

# =============================================================================
# def seleccion(update, context):
#     if update.message.text == "Recibir":
#         recibir(update, context)
#         cancel(update, context)
#         return ConversationHandler.END
#     if update.message.text == "Enviar":
#         query = """
#         select reportes
#         from agente
#         where agente_id={}
#         """.format(update.message.from_user['id'])
#         
#         c.execute(query)#con.rollback()
#         context.user_data['numero'] = c.fetchall()[0][0] + 1
#         
#         context.user_data['agente_id'] = update.message.from_user['id']
#         context.user_data['nombre'] = update.message.from_user['first_name']
#         context.user_data['apellido'] = update.message.from_user['last_name'] #Acá hay que poner un if por si no tienen Z
#         context.user_data['inicio'] = update.message.date
#         enviar(update, context)
#         return GENDER
# 
# =============================================================================
# =============================================================================
# def recibir(update, context):
#     update.message.reply_text('Mirá este video')
#     update.message.reply_text('https://www.youtube.com/watch?v=cV7fsxosrDc')
#     update.message.reply_text('Compartilo!')
#     
# 
# 
# 
# =============================================================================
# =============================================================================
# def enviar(update, context):
#     reply_keyboard = [KeyboardButton('Basural a cielo abierto'),
#                       KeyboardButton('Acumulación de basura en la calle'), 
#                       KeyboardButton('Neumáticos en desuso'), 
#                       KeyboardButton('Chatarra, chapas u otros objetos voluminosos al descubierto'), 
#                       KeyboardButton('Recipientes'), 
#                       KeyboardButton('Terreno sin desmalezar'), 
#                       KeyboardButton('Vivienda con objetos que acumulan agua')]
#     
#     
# 
#     
#     update.message.reply_text(
#         '¿Allí visualizás algún posible criadero de mosquitos? Ingresá la opción que corresponda:',
#         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
#     )    
# 
# =============================================================================
    

 
def gender(update, context):
    
    
    user = update.message.from_user
  
    diccionario['tipo'] = update.message.text
  
    if update.message.text == 'Basural a cielo abierto':
        update.message.bot.send_photo(chat_id=update.message.chat['id'], photo=open('imagenes/basural.jpg', 'rb'))
  
    if update.message.text == 'Acumulación de basura en la calle':
        update.message.bot.send_photo(chat_id=update.message.chat['id'], photo=open('imagenes/basura_calle.jpg', 'rb'))
  
    if update.message.text == 'Neumáticos en desuso':
        update.message.bot.send_photo(chat_id=update.message.chat['id'], photo=open('imagenes/neumaticos.jpg', 'rb'))
  
    if update.message.text == 'Chatarra, chapas u otros objetos voluminosos al descubierto':
        update.message.bot.send_photo(chat_id=update.message.chat['id'], photo=open('imagenes/chatarra.jpg', 'rb'))

    if update.message.text == 'Recipiente':
        update.message.bot.send_photo(chat_id=update.message.chat['id'], photo=open('imagenes/balde.jpg', 'rb'))
  
    if update.message.text == 'Terreno sin desmalezar':
        update.message.bot.send_photo(chat_id=update.message.chat['id'], photo=open('imagenes/terreno.jpg', 'rb'))
  
    if update.message.text == 'Vivienda con objetos que acumulan agua':
        update.message.bot.send_photo(chat_id=update.message.chat['id'], photo=open('imagenes/casa.jpg', 'rb'))
      
  
    #logger.info("El usuario {} denuncia presencia de {}".format(user.first_name, update.message.text) )
    reply_keyboard = [['¡Sí pude eliminarlo!'],
                      ['Predio deshabilitado o sin acceso'],
                      ['No se encuentra lx residente presente'],
                      ['El gran volumen requiere asistencia'],
                      ['Lx residente no accedió a realizar la acción']]
    
    update.message.reply_text(
        'Si no se pudieron eliminar los criaderos identificados, ¿cuál fue el motivo?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    
    return PHOTO
 

def photo(update, context):
    print('pp')
    print(update.message.text)
    diccionario['espacio'] = update.message.text
    

    
    update.message.reply_text('Tu respuesta fue {}'.format(update.message.text))
    update.message.reply_text('¡Gracias por tu reporte! Para señalar otros potenciales criaderos, volvé a escribirme.')
    diccionario['final'] = update.message.date
    
    nuevoReporte(update, context)
    return ConversationHandler.END


def skip_photo(update, context):
    
    texto = 'Necestiamos saber la cantidad. \n Si querés cancelar el reporte enviá cancelar'
                      
    
    update.message.reply_text(texto)

    return ConversationHandler.END




# =============================================================================
  
def location(update, context):
    
  ubicacion(update, context)
  update.message.reply_text('Gracias por enviarnos la ubicación de tu reporte!')
  reply_keyboard = [['Basural a cielo abierto'],
                      ['Acumulación de basura en la calle'],
                      ['Neumáticos en desuso'], 
                      ['Chatarra, chapas u otros objetos voluminosos al descubierto'],
                      ['Recipiente'],
                      ['Terreno sin desmalezar'], 
                      ['Vivienda con objetos que acumulan agua']]
    
    

    
  update.message.reply_text(
        '¿Allí visualizás algún posible criadero de mosquitos? Ingresá la opción que corresponda:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )    
    
  return GENDER
  
# =============================================================================
# 
# def publico_privado(update, context):
#     reply_keyboard = [['Predio deshabilitado o sin acceso', 'No se encuentra lx residente presente', 'Lx residente no accedió a realizar la acción', 'El gran volumen requiere asistencia(personal, camión, etc)']]
#     
#     update.message.reply_text(
#         'Si no se pudieron eliminar los criaderos identificcados, ¿cuál fue el motivo?',
#         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
#     )
# 
# 
# 
# def skip_location(update, context):
#     estado = ubicacion_texto(update, context, BIO, LOCATION)
#     if estado == BIO:
#         publico_privado(update, context)
#     return estado
# 
# =============================================================================
def nuevoReporte(update, context):
    
    data = pd.DataFrame([diccionario])
    if os.path.isfile('dengue.csv'):
        data_frame = pd.read_csv('dengue.csv')
    else:
        data_frame = pd.DataFrame(columns = ['nombre', 'apellido', 'agente_id', 'latitud', 'longitud', 'fecha', 'tipo', 'espacio', 'inicio', 'final'])

    data_frame = data_frame.append(data, ignore_index = True)

    data_frame.to_csv('dengue.csv',index=False)

    
    return data_frame
    
# =============================================================================
# def bio(update, context):
#     user = update.message.from_user
#     
#     context.user_data['espacio'] = update.message.text
#     
#     logger.info("El reporte de %s se encuentra en un espacio %s", user.first_name, update.message.text)
#     update.message.reply_text(
#             '¡Gracias por tu reporte! '
#             )
#     
#     context.user_data['final'] = update.message.date
#     
#     nuevoReporte(update, context)
#     
#     update.message.reply_text('Para señalar otros potenciales criaderos, volvé a escribirme')
#     return ConversationHandler.END
# 
# =============================================================================

def button(update, context):
    query = update.callback_query
    query.edit_message_text(text="Opción seleccionada fue: {}".format(query.data))
    
def cancel(update, context):
    texto = 'Nos vemos! \n Recordá que sin agua estancada no hay dengue! \n'\
            'Para evitar los mosquitos, eliminen todo los objetos que tengan agua estancada' \
            'Avisanos por acá cuando ustedes ya no lo puedan resolver!'
    
    user = update.message.from_user
    #logger.info("El usuario %s canceló el reporte.", user.first_name)
    update.message.reply_text(texto,
                              reply_markup=ReplyKeyboardRemove())
    update.message.reply_text('Chau!')

    return ConversationHandler.END


def error(update, context):
 #   """Log Errors caused by Updates."""
    #con.rollback()
    update.message.reply_text('Perdón!, tuvimos un problema.')
    logger.warning('Update "%s" caused error "%s"', update, context.error)


#def agentes(update, context):
 #   texto = update.message.text
    
  #  if texto.split(' ')[1]=='d3ngu3_80t':
        
   #     query = """
    #    select *
     #   from agente
      #  """
       # c.execute(query)#con.rollback()
        #agente = c.fetchall()
        #update.message.reply_text("{}".format(agente))
    #else:
     #   update.message.reply_text("Opción invalida")


# Create the Updater and pass it your bot's token.
# Make sure to set use_context=True to use the new context based callbacks
# Post version 12 this will no longer be necessary
updater = Updater(token, use_context=True)

# Get the dispatcher to register handlers
dp = updater.dispatcher

#dp.add_handler(CommandHandler('recibir', recibir))
dp.add_handler(CommandHandler('prueba', prueba))
#dp.add_handler(CommandHandler('agentes', agentes))
dp.add_handler(CommandHandler('canelar', cancel))



# Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, start)],

    states={
        AGENTE_UBICACION:[MessageHandler(Filters.location, ubicacionAgente),
                          MessageHandler(Filters.text, ubicacionAgente_texto)],
                          
        LOCATION: [MessageHandler(Filters.location, location)],
        #SELECCION : [MessageHandler(Filters.regex('^(Recibir|Enviar)$'), seleccion)],
        GENDER: [MessageHandler(Filters.regex('^(Basural a cielo abierto|Acumulación de basura en la calle|Neumáticos en desuso|Chatarra, chapas u otros objetos voluminosos al descubierto|Recipiente|Terreno sin desmalezar|Vivienda con objetos que acumulan agua)$'), gender)],

        PHOTO: [MessageHandler(Filters.regex('^(¡Sí pude eliminarlo!|Predio deshabilitado o sin acceso|No se encuentra lx residente presente|El gran volumen requiere asistencia|Lx residente no accedió a realizar la acción)$'), photo)],

# =============================================================================
#         LOCATION: [MessageHandler(Filters.location, location),
#                    MessageHandler(Filters.text, skip_location)],
# 
#         BIO: [MessageHandler(Filters.regex('^(Predio deshabilitado o sin acceso.|No se encuentra lx residente presente.|Lx residente no accedió a realizar la acción.|El gran volumen requiere asistencia(personal, camión, etc))$'), bio)]
# =============================================================================
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


