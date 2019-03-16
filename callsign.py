import os, sys, traceback, json
import discord, pymysql.cursors
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()
TOKEN = os.getenv('TOKEN')
NAME = os.getenv('NAME')
conn = pymysql.connect( host = os.getenv('HOST'),
                        user = os.getenv('USER'),
                        password = os.getenv('PASSWORD'),
                        db = os.getenv('DATABASE'),
                        charset = 'utf8mb4',
                        cursorclass = pymysql.cursors.DictCursor)

def check_if_bot_mentioned(mentions):
    if len(mentions) == 0:
        return False
    else:
        for member in mentions:
            if NAME in str(member): return True
    return False

def has_other_mention(mentions):
    if len(mentions) == 0:
        return False
    else:
        for member in mentions:
            if NAME not in str(member): return str(member)
    return False


def help_response():
    return """
    **CallSign Bot Help**
        __Simple Commands__
        - Help (you know this one already!): shows list
            ex: `@Callsign help`

        - Add {username_on_game_youre_adding} : {game_name}: Adds callsign to game.
          Note: This will update name also if game is already in list.
            ex: `@CallSign add [UN1T]Example : Squad`

        - Remove {game}: Removes Callsigns for game.
            ex: `@Callsign remove Ground Branch`


        __Lookup Callsigns for Games__
            ex: `@Callsign @USER_OF_INTEREST`
            - will return list of all callsigns (usernames) in games they have registered.
    """

def get_callsign(msg):
    return msg.split(' :', 1)[0]

def user_in_db(user):
    user_name = str(user)

    with conn.cursor() as cursor:
        sql = f"SELECT `id` FROM `callsigns` WHERE `user` = %s"
        cursor.execute(sql, (user_name,))
        users = cursor.fetchall()
        return any(users)

def create_user_in_db(user):
    user_name = str(user)

    with conn.cursor() as cursor:
        sql = f"INSERT INTO `callsigns` (`user`) VALUES (%s) "
        cursor.execute(sql, (user_name,))
        return conn.commit()

def get_user_callsigns(user):
    user_name = str(user)

    with conn.cursor() as cursor:
        sql = f"SELECT `data` FROM `callsigns` WHERE `user` = %s"
        cursor.execute(sql, (user_name,))
        results = cursor.fetchone()
        return results['data']

def update_callsigns_for_user(user, callsign_list):
    user_name = str(user)
    data = json.dumps(callsign_list)

    with conn.cursor() as cursor:
        sql = f"UPDATE `callsigns` SET `data` = %s WHERE `user` = %s"
        cursor.execute(sql, (data, user_name))
        return conn.commit()




# ====================================================================== #
@client.event
async def on_ready():
    print("Callsign is ready to go")
    await client.change_presence(game=discord.Game(name="Watching Comms"))

@client.event
async def on_message(message):
    try:
        # ignore messages from the Bot itself
        if message.author == client.user:
            return

        bot_was_mentioned = check_if_bot_mentioned(message.mentions)

        if bot_was_mentioned:
            message_content = message.content.lower().strip()
            print(message_content)

            if " help" in message_content:
                await client.send_message(message.channel, help_response())
                return


            elif " add" in message_content:
                user = message.author
                callsign = get_callsign( message.content.split(' add ', 1)[1].strip() )
                game = message.content.split(' : ', 1)[1].strip()

                if user_in_db(user) == False:
                    create_user_in_db(user)

                user_callsigns = get_user_callsigns(user)
                if user_callsigns == None:
                    # Setting a Fresh record for the User
                    updated_callsigns = {}
                    updated_callsigns[game] = callsign
                else:
                    # Update the Records for the User
                    updated_callsigns = json.loads(user_callsigns)
                    updated_callsigns[game] = callsign

                update_callsigns_for_user(user, updated_callsigns)
                await client.send_message(message.channel, f"Your Callsign for `{game}` is now `{callsign}`!")
                return

            elif " remove" in message_content:
                user = message.author
                game = message.content.split('remove ', 1)[1].strip()

                if user_in_db(user) == False:
                    await client.send_message(message.channel, "You cant remove any Callsigns - You havent even added any!")
                    return

                user_callsigns = get_user_callsigns(user)
                if user_callsigns == None:
                    await client.send_message(message.channel, "You cant remove any Callsigns - You havent even added any!")
                    return
                else:
                    # Update the Records for the User
                    updated_callsigns = json.loads(user_callsigns)
                    if game in updated_callsigns:
                        del updated_callsigns[game]
                    else:
                        await client.send_message(message.channel, f"You dont have a callsign for {game}!")
                        return


                update_callsigns_for_user(user, updated_callsigns)
                await client.send_message(message.channel, f"Your Callsign for `{game}` has been removed!")
                return

            elif has_other_mention(message.mentions) != False:
                # Lookup Users CallSigns
                user = has_other_mention(message.mentions)

                if user_in_db(user) == False:
                    await client.send_message(message.channel, f"{user} is not in CallSign System Yet.")
                    return

                user_callsigns = get_user_callsigns(user)

                if user_callsigns == None:
                    await client.send_message(message.channel, f"{user} has no CallSigns")
                    return
                else:
                    callsigns = json.loads(user_callsigns)
                    if not callsigns:
                        await client.send_message(message.channel, f"{user} has no CallSigns")
                        return
                    else:
                        response = f"Callsigns for **{user.split('#',1)[0]}**\n\n"
                        for key in callsigns:
                            response += f"**{key}** : _{callsigns[key]}_\n"

                        await client.send_message(message.channel, response)
                        return
                exit()

            else:
                await client.send_message(message.channel, "Uhh...what? Try @CallSign help.")
                return
    except Exception:
        print(traceback.format_exc())

        await client.send_message(message.channel, "Uhh...what? Try @CallSign help.")
        return

client.run(TOKEN)
