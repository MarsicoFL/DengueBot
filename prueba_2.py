#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 14:17:05 2021

@author: agf
"""

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
        update.message.reply_text('Esta aplicación está pensada para apoyar el trabajo territorial de agentes sanitarios en la prevención de criaderos de mosquitos Aedes aegypti, transmisores del dengue.')

                
        context.user_data['agente_id'] = update.message.from_user['id']
        context.user_data['nombre'] = update.message.from_user['first_name']
        context.user_data['apellido'] = update.message.from_user['last_name']
        
        update.message.reply_text("¿En dónde te encontrás? Compartinos tu ubicación (Location) haciendo click en el “ganchito” ubicado debajo a la izquierda.")       
        
        return AGENTE_UBICACION
    else:
        update.message.reply_text('Hola {}!'.format(agente[0][0]))
        if agente[0][1]==1:
            update.message.reply_text('Tenemos guardado {} reporte tuyo!'.format(agente[0][1]))
        else:
            update.message.reply_text('Tenemos guardado {} reportes tuyos!'.format(agente[0][1]))
        
        
        update.message.reply_text("¿En dónde te encontrás? Compartinos tu ubicación (Location) haciendo click en el “ganchito” ubicado debajo a la izquierda.")
        
        
        return AGENTE_UBICACION



def ubicacion(update, context):
    user = update.message.from_user
    context.user_data['latitud'] = update.message.location.latitude
    context.user_data['longitud'] = update.message.location.longitude
    
    user_location = update.message.location
    logger.info("Ubicación de %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    
def ubicacionAgente(update, context):
    ubicacion(update, context)
    update.message.reply_text('!Gracias por enviarnos tu ubicación!')
    nuevoAgente(update, context)
    bienvenide(update, context)
    return ConversationHandler.END

def ubicacionAgente_texto(update, context):
    estado = ubicacion_texto(update, context, END, AGENTE_UBICACION)
    if estado == END:
        update.message.reply_text('!Gracias por enviarnos tu ubicación!')
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
        
        update.message.reply_text('Si querés salir envía la palabra: cancelar')
        return anterior
       
def bienvenide(update, context):
    
    update.message.reply_text('Bienvenidxs!')
    update.message.reply_text('Esta aplicación está pensada para apoyar el trabajo territorial de agentes sanitarios en la prevención de criaderos de mosquitos Aedes aegypti, transmisores del dengue.')
        

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
    
    
    