#-*- coding: utf-8 -*-

import urllib.request
import pyrebase
import json
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, Filters, MessageHandler


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

config = {
    "apiKey": "API firebase",
    "authDomain": "lanparty-b7120.firebaseapp.com",
    "databaseURL": "https://lanparty-b7120.firebaseio.com",
    "storageBucket": "lanparty-b7120.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
data = db.child("ParticipantesIV").get().val()

global_id = ""
ultimo_participante = ""
ultimo_usuario = ""

print("se ha cargado la base de datos correctamente")

def start(update, context):
    id=update.message.chat_id

    if id<0:
        update.message.reply_text("Buenas, soy IAN. Soy el encargado de comunicar las cosas de la V Fortuna LanParty.")
    else:
        update.message.reply_text("Bienvenido, soy IAN. Introduce el codigo de organizador.\n Ejemplo: /code \"codigo\"")

def code(update, context):
    id=update.message.chat_id
    data = db.child("ParticipantesIV").get().val()
    if id<0:
        update.message.reply_text("Este chat no es privado.")
    else:
        code_user = "".join(context.args)
        if data["Organizadores"]["codigo"] == code_user:
            if str(id) in data["Organizadores"]:
                update.message.reply_text("Ya has sido autorizado anteriormente.")
            else:
                db.child("ParticipantesIV").child("Organizadores").child(id).set(update.message.from_user.first_name)
                update.message.reply_text("Usuario autorizado.")
        else:
            update.message.reply_text("Codigo incorrecto")

def usuario(dni, usuario):
    usuario_participante = "<b>Nombre:</b> " + str(usuario["nombre"]) + "\n"
    usuario_participante = usuario_participante + "<b>Fecha nacimiento:</b> " + str(usuario["fecha_nacimiento"]) + "\n"
    usuario_participante = usuario_participante + "<b>Telefono:</b> " + str(usuario["telefono"]) + "\n"
    usuario_participante = usuario_participante + "<b>Email:</b> " + str(usuario["email"]) + "\n"
    usuario_participante = usuario_participante + "<b>Dirección:</b> " + str(usuario["dir"]) + "\n"
    usuario_participante = usuario_participante + "<b>Localidad:</b> " + str(usuario["localidad"]) + "\n"
    usuario_participante = usuario_participante + "<b>Nick:</b> " + str(usuario["nick"]) + "\n"
    usuario_participante = usuario_participante + "<b>Clan:</b> " + str(usuario["clan"]) + "\n"
    usuario_participante = usuario_participante + "<b>Nombre camiseta:</b> " + str(usuario["nombre_camiseta"]) + "\n"
    usuario_participante = usuario_participante + "<b>Talla camiseta:</b> " + str(usuario["talla_camiseta"]) + "\n"
    usuario_participante = usuario_participante + "<b>Torneos:</b> " + str(usuario["torneos"]) + "\n"
    usuario_participante = usuario_participante + "<b>Pagado:</b> " + str(usuario["pagado"]) + "\n"
    usuario_participante = usuario_participante + "<b>Sugerencias:</b> " + str(usuario["sugerencias"]) + "\n"
    usuario_participante = usuario_participante + "<b>Número de inscripción:</b> " + str(usuario["numero_de_inscripcion"])
    return usuario_participante

def participante(update, context):
    id=update.message.chat_id
    global global_id
    global ultimo_participante
    global ultimo_usuario
    global_id = id
    data = db.child("ParticipantesIV").get().val()
    if str(id) in data["Organizadores"]:
        dni = "".join(context.args).upper()
        if dni in data:
            ultimo_participante = dni
            ultimo_usuario = usuario(dni, data[dni])
            keyboard = [[InlineKeyboardButton("Pagar", callback_data='pagar'), InlineKeyboardButton("Modificar", callback_data='modificar')],
                        [InlineKeyboardButton("Nada", callback_data='nada')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(ultimo_usuario, parse_mode="html", reply_markup=reply_markup)

        else:
            update.message.reply_text("Usuario no encontrado.")
    else:
        update.message.reply_text("No estas autorizado.")

def button(update, context):
    query = update.callback_query
    global ultimo_usuario
    global global_id
    data = db.child("ParticipantesIV").get().val()
    if query.data == 'pagar':
        db.child("ParticipantesIV").child(ultimo_participante).child("pagado").set("Sí")
        query.edit_message_text("El usuario con dni " + str(ultimo_participante) + "ha pagado correctamente")
    if query.data == 'modificar':
        ultimo_usuario = usuario(ultimo_participante, data[ultimo_participante]) + "\n \n <b> Modificar datos reemplazara los datos antiguos </b>"
        keyboard = [[InlineKeyboardButton("Nombre", callback_data='nombre'), InlineKeyboardButton("Fecha", callback_data='fecha'), InlineKeyboardButton("Teléfono", callback_data='telefono')],
                    [InlineKeyboardButton("Email", callback_data='email'), InlineKeyboardButton("Direccion", callback_data='direccion'), InlineKeyboardButton("Localidad", callback_data='localidad')],
                    [InlineKeyboardButton("Nick", callback_data='nick'), InlineKeyboardButton("Clan", callback_data='clan'), InlineKeyboardButton("Nombre camiseta", callback_data='nombre_camiseta')],
                    [InlineKeyboardButton("Talla camiseta", callback_data='talla_camiseta'), InlineKeyboardButton("Torneos", callback_data='torneos'), InlineKeyboardButton("Sugerencias", callback_data='sugerencias')],
                    [InlineKeyboardButton("No modificar nada", callback_data='no_modificado')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(ultimo_usuario, parse_mode="html", reply_markup=reply_markup)

    if query.data == 'no_modificado':
        ultimo_usuario = usuario(ultimo_participante, data[ultimo_participante])
        keyboard = [[InlineKeyboardButton("Pagar", callback_data='pagar'), InlineKeyboardButton("Modificar", callback_data='modificar')],
                    [InlineKeyboardButton("Nada", callback_data='nada')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(ultimo_usuario, parse_mode="html", reply_markup=reply_markup)

    if query.data == 'nada':
        query.edit_message_text(ultimo_usuario, parse_mode="html")

    if query.data == 'dato_modificado':
        ultimo_usuario = usuario(ultimo_participante, data[ultimo_participante]) + "\n \n <b> Modificar datos reemplazara los datos antiguos </b> \n \n"
        keyboard = [[InlineKeyboardButton("Nombre", callback_data='nombre'), InlineKeyboardButton("Fecha", callback_data='fecha'), InlineKeyboardButton("Teléfono", callback_data='telefono')],
                    [InlineKeyboardButton("Email", callback_data='email'), InlineKeyboardButton("Direccion", callback_data='direccion'), InlineKeyboardButton("Localidad", callback_data='localidad')],
                    [InlineKeyboardButton("Nick", callback_data='nick'), InlineKeyboardButton("Clan", callback_data='clan'), InlineKeyboardButton("Nombre camiseta", callback_data='nombre_camiseta')],
                    [InlineKeyboardButton("Talla camiseta", callback_data='talla_camiseta'), InlineKeyboardButton("Torneos", callback_data='torneos'), InlineKeyboardButton("Sugerencias", callback_data='sugerencias')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(ultimo_usuario, parse_mode="html", reply_markup=reply_markup)

    if query.data == 'nombre':
        context.bot.send_message(chat_id=global_id , text="Introduce el nuevo nombre: /name nombre_nuevo")

    if query.data == 'fecha':
        context.bot.send_message(chat_id=global_id, text="Introduce la nueva fecha de nacimiento: /date fecha_nueva")

    if query.data == 'telefono':
        context.bot.send_message(chat_id=global_id, text="Introduce el nuevo teléfono: /tlf telefono_nuevo")

    if query.data == 'email':
        context.bot.send_message(chat_id=global_id, text="Introduce el nuevo email: /email email_nuevo")

    if query.data == 'direccion':
        context.bot.send_message(chat_id=global_id, text="Introduce la nueva dirección: /dir direccion_nueva")

    if query.data == 'localidad':
        context.bot.send_message(chat_id=global_id, text="Introduce la nueva localidad: /loc localidad_nueva")

    if query.data == 'nick':
        context.bot.send_message(chat_id=global_id, text="Introduce el nuevo nick: /nick nick_nuevo")

    if query.data == 'clan':
        context.bot.send_message(chat_id=global_id, text="Introduce el nuevo clan: /clan clan_nuevo")

    if query.data == 'nombre_camiseta':
        context.bot.send_message(chat_id=global_id, text="Introduce el nuevo nombre de camista: /name_shirt nombre_camiseta_nuevo")

    if query.data == 'talla_camiseta':
        context.bot.send_message(chat_id=global_id, text="Introduce la nueva talla de camiseta: /size talla_camiseta_nueva")

    if query.data == 'torneos':
        context.bot.send_message(chat_id=global_id, text="Selecciona los torneos que participa: /tournaments LOL TFT Rocket_League CSGO Fortnite FIFA19 DbD Tekken Prop_hunt APEX")

    if query.data == 'sugerencias':
        context.bot.send_message(chat_id=global_id, text="Introduce las nuevas sugerencias: /suggestions nuevas sugerencias")

def name(update, context):
    id=update.message.chat_id
    query = update.callback_query
    global global_id
    global ultimo_participante
    global ultimo_usuario
    global_id = id
    data = db.child("ParticipantesIV").get().val()
    if str(id) in data["Organizadores"]:
        dato = "".join(context.args)
        db.child("ParticipantesIV").child(ultimo_participante).child("nombre").set(dato)
        context.bot.send_message(chat_id=global_id, text="Nombre modificado", callback_data='dato_modificado')
    else:
        update.message.reply_text("No estas autorizado.")

def date(update, context):
    id=update.message.chat_id
    query = update.callback_query
    global global_id
    global ultimo_participante
    global ultimo_usuario
    global_id = id
    data = db.child("ParticipantesIV").get().val()
    if str(id) in data["Organizadores"]:
        dato = "".join(context.args)
        db.child("ParticipantesIV").child(ultimo_participante).child("Fecha_nacimiento").set(dato)
        context.bot.send_message(chat_id=global_id, text="Fecha modificada", callback_data='dato_modificado')
    else:
        update.message.reply_text("No estas autorizado.")

def tlf(update, context):
    id=update.message.chat_id
    query = update.callback_query
    global global_id
    global ultimo_participante
    global ultimo_usuario
    global_id = id
    data = db.child("ParticipantesIV").get().val()
    if str(id) in data["Organizadores"]:
        dato = "".join(context.args)
        db.child("ParticipantesIV").child(ultimo_participante).child("telefono").set(dato)
        context.bot.send_message(chat_id=global_id, text="Teléfono modificado", callback_data='dato_modificado')
    else:
        update.message.reply_text("No estas autorizado.")


def email(update, context):
    id=update.message.chat_id
    query = update.callback_query
    global global_id
    global ultimo_participante
    global ultimo_usuario
    global_id = id
    data = db.child("ParticipantesIV").get().val()
    if str(id) in data["Organizadores"]:
        dato = "".join(context.args)
        db.child("ParticipantesIV").child(ultimo_participante).child("email").set(dato)
        context.bot.send_message(chat_id=global_id, text="Email modificado", callback_data='dato_modificado')
    else:
        update.message.reply_text("No estas autorizado.")


def dir(update, context):
    id=update.message.chat_id
    query = update.callback_query
    global global_id
    global ultimo_participante
    global ultimo_usuario
    global_id = id
    data = db.child("ParticipantesIV").get().val()
    if str(id) in data["Organizadores"]:
        dato = "".join(context.args)
        db.child("ParticipantesIV").child(ultimo_participante).child("dir").set(dato)
        context.bot.send_message(chat_id=global_id, text="Dirección modificada", callback_data='dato_modificado')
    else:
        update.message.reply_text("No estas autorizado.")


def loc(update, context):
    id=update.message.chat_id
    query = update.callback_query
    global global_id
    global ultimo_participante
    global ultimo_usuario
    global_id = id
    data = db.child("ParticipantesIV").get().val()
    if str(id) in data["Organizadores"]:
        dato = "".join(context.args)
        db.child("ParticipantesIV").child(ultimo_participante).child("localidad").set(dato)
        context.bot.send_message(chat_id=global_id, text="Localidad modificada", callback_data='dato_modificado')
    else:
        update.message.reply_text("No estas autorizado.")


def nick(update, context):
    id=update.message.chat_id
    query = update.callback_query
    global global_id
    global ultimo_participante
    global ultimo_usuario
    global_id = id
    data = db.child("ParticipantesIV").get().val()
    if str(id) in data["Organizadores"]:
        dato = "".join(context.args)
        db.child("ParticipantesIV").child(ultimo_participante).child("nick").set(dato)
        context.bot.send_message(chat_id=global_id, text="Nick modificado", callback_data='dato_modificado')
    else:
        update.message.reply_text("No estas autorizado.")


def clan(update, context):
    id=update.message.chat_id
    query = update.callback_query
    global global_id
    global ultimo_participante
    global ultimo_usuario
    global_id = id
    data = db.child("ParticipantesIV").get().val()
    if str(id) in data["Organizadores"]:
        dato = "".join(context.args)
        db.child("ParticipantesIV").child(ultimo_participante).child("clan").set(dato)
        context.bot.send_message(chat_id=global_id, text="Clan modificado", callback_data='dato_modificado')
    else:
        update.message.reply_text("No estas autorizado.")


def name_shirt(update, context):
    id=update.message.chat_id
    query = update.callback_query
    global global_id
    global ultimo_participante
    global ultimo_usuario
    global_id = id
    data = db.child("ParticipantesIV").get().val()
    if str(id) in data["Organizadores"]:
        dato = "".join(context.args)
        db.child("ParticipantesIV").child(ultimo_participante).child("nombre_camiseta").set(dato)
        context.bot.send_message(chat_id=global_id, text="Nombre de camiseta modificado", callback_data='dato_modificado')
    else:
        update.message.reply_text("No estas autorizado.")


def size(update, context):
    id=update.message.chat_id
    query = update.callback_query
    global global_id
    global ultimo_participante
    global ultimo_usuario
    global_id = id
    data = db.child("ParticipantesIV").get().val()
    if str(id) in data["Organizadores"]:
        dato = "".join(context.args)
        db.child("ParticipantesIV").child(ultimo_participante).child("talla_camiseta").set(dato)
        context.bot.send_message(chat_id=global_id, text="Talla camiseta modificada", callback_data='dato_modificado')
    else:
        update.message.reply_text("No estas autorizado.")


def tournaments(update, context):
    id=update.message.chat_id
    query = update.callback_query
    global global_id
    global ultimo_participante
    global ultimo_usuario
    global_id = id
    data = db.child("ParticipantesIV").get().val()
    if str(id) in data["Organizadores"]:
        dato = "".join(context.args)
        db.child("ParticipantesIV").child(ultimo_participante).child("torneos").set(dato)
        context.bot.send_message(chat_id=global_id, text="Torneos modificados", callback_data='dato_modificado')
    else:
        update.message.reply_text("No estas autorizado.")


def suggestions(update, context):
    id=update.message.chat_id
    query = update.callback_query
    global global_id
    global ultimo_participante
    global ultimo_usuario
    global_id = id
    data = db.child("ParticipantesIV").get().val()
    if str(id) in data["Organizadores"]:
        dato = "".join(context.args)
        db.child("ParticipantesIV").child(ultimo_participante).child("sugerencias").set(dato)
        context.bot.send_message(chat_id=global_id, text="Sugerencias modificadas", callback_data='dato_modificado')
    else:
        update.message.reply_text("No estas autorizado.")



def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    updater = Updater("TELEGRAM", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('code', code))
    updater.dispatcher.add_handler(CommandHandler('participante', participante))
    updater.dispatcher.add_handler(CommandHandler('name', name))
    updater.dispatcher.add_handler(CommandHandler('date', date))
    updater.dispatcher.add_handler(CommandHandler('tlf', tlf))
    updater.dispatcher.add_handler(CommandHandler('email', email))
    updater.dispatcher.add_handler(CommandHandler('dir', dir))
    updater.dispatcher.add_handler(CommandHandler('loc', loc))
    updater.dispatcher.add_handler(CommandHandler('nick', nick))
    updater.dispatcher.add_handler(CommandHandler('clan', clan))
    updater.dispatcher.add_handler(CommandHandler('name_shirt', name_shirt))
    updater.dispatcher.add_handler(CommandHandler('size', size))
    updater.dispatcher.add_handler(CommandHandler('tournaments', tournaments))
    updater.dispatcher.add_handler(CommandHandler('suggestions', suggestions))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
