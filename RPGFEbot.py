import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
import random

# Variables para el juego
player_stats = {"nivel": 1, "experiencia": 0, "vida": 100, "ataque": 10}
monstruos = [{"nombre": "Orco", "vida": 50, "ataque": 5},
             {"nombre": "Goblin", "vida": 30, "ataque": 3},
             {"nombre": "Troll", "vida": 80, "ataque": 8}]
             
# Funciones del juego
def atacar(update, context):
    monstruo = random.choice(monstruos)
    dano = player_stats["ataque"]
    monstruo["vida"] -= dano
    if monstruo["vida"] <= 0:
        update.message.reply_text(f'{monstruo["nombre"]} ha sido derrotado!')
        ganar_experiencia(update, context)
    else:
        player_stats["vida"] -= monstruo["ataque"]
        if player_stats["vida"] <= 0:
            update.message.reply_text(f'Has sido derrotado por {monstruo["nombre"]}!')
            player_stats["vida"] = 100
        else:
            update.message.reply_text(f'Atacas a {monstruo["nombre"]} y le quitas {dano} puntos de vida.\n\n'
                                      f'{monstruo["nombre"]} te ataca y te quita {monstruo["ataque"]} puntos de vida.\n\n'
                                      f'Tu vida: {player_stats["vida"]}\n'
                                      f'{monstruo["nombre"]}: {monstruo["vida"]}')
                                      
def ganar_experiencia(update, context):
    player_stats["experiencia"] += 10
    if player_stats["experiencia"] >= player_stats["nivel"] * 100:
        player_stats["nivel"] += 1
        player_stats["experiencia"] = 0
        player_stats["vida"] = 100
        player_stats["ataque"] += 5
        update.message.reply_text(f'¡Felicidades! Has subido de nivel. Tu nivel ahora es {player_stats["nivel"]}.')
    else:
        update.message.reply_text(f'Has ganado 10 puntos de experiencia.\n\n'
                                  f'Experiencia: {player_stats["experiencia"]}/{player_stats["nivel"] * 100}')

def estadisticas(update, context):
    update.message.reply_text(f'Tus estadísticas:\n\n'
                              f'Nivel: {player_stats["nivel"]}\n'
                              f'Experiencia: {player_stats["experiencia"]}/{player_stats["nivel"] * 100}\n'
                              f'Vida: {player_stats["vida"]}\n'
                              f'Ataque: {player_stats["ataque"]}')
                              
# Funciones para conectarse a la API de Telegram
def start(update, context):
    update.message.reply_text('¡Hola! Bienvenido a mi juego RPG.\n\n'
                              'Escribe /atacar para comenzar a jugar.\n'
                              'Escribe /estadisticas para ver tus estadísticas.')

def main():
    # Conexión con la API de Telegram
    updater = Updater('6023889253:AAFMeQbO8F9YYnDazpTPkaWJvGCdah3dCNo', use_context=True)
    dp = updater.dispatcher

    # Manejadores
    # Comandos
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('atacar', atacar))
    dp.add_handler(CommandHandler('estadisticas', estadisticas))

    # Mensajes
    dp.add_handler(MessageHandler(Filters.text, start))

    # Iniciar el bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
