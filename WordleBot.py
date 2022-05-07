from discord.ext import tasks, commands
import discord
import datetime
import re
import os.path
from table2ascii import table2ascii as t2a, PresetStyle
import sys

TOKEN = ""

intents = discord.Intents().all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    wordleMessage.start()




@tasks.loop(seconds=10)
async def wordleMessage():

    channel = await client.fetch_channel(944480120041771049)

    await updateScores()


    formattedData = formatOutput()

    # In your command:
    output = t2a(
        header=["User", "Points"],
        body=formattedData,
        first_col_heading=True
    )

    await channel.send(
        "------------------------\nThere's a new wordle!\n "

        "\n------------------------\n"+

        f"\n**Leaderboard**```\n{output}\n```"

                        )


    sys.exit("Complete")

def formatOutput():

    f = open("leaderboard.txt", "r")

    listofScores = []

    for i in f:
        listofScores.append(i.strip().split(" "))

    for i in listofScores:
        i[1] = int(i[1])

    f.close()

    print(listofScores)

    listofScores.sort(key=lambda x: x[1], reverse=True)



    print(listofScores)

    return listofScores



async def loopDays():

    """
    Gets all wordle score messages from past day
    :return: A list of all messages following format of Wordle Score
    """

    # Get yesterdays date.
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)

    # Set Channel
    channel = client.get_channel(944480120041771049)

    messageList = []

    todaysMessages = await channel.history(limit=None, after=yesterday).flatten()


    for i in todaysMessages:
        #if the message content follows regex pattern:
        if re.match("^Wordle\s[0-9]+\s[0-9]/[0-9]*", i.content):
            #append message object to list
            messageList.append(i)

    return messageList






async def buildBoard():

    """
    Gets all scores from text file formats into a list.
    Creates text file if it does not exist.
    Adds new players if not already in list.

    :return: return: All players and their current scores formatted as 2D array [[Player1, 64], [Player2, 33], ...]
    """


    #list of all messages which are wordle scores from past day
    messageList = await loopDays()

    #list of players and their score
    formatData = []

    #Create file if it does not exist
    if not os.path.isfile("leaderboard.txt"):

        f = open("leaderboard.txt", 'w+')

        f.close()


    f = open("leaderboard.txt", 'r')

    #format the text file data into 2D array
    for i in f:
        (formatData.append(i.strip("\n").split(" ")))

    #change string score to integer
    for i in range(len(formatData)):
        formatData[i][1] = int(formatData[i][1])



    flag = False
    tempArr = []

    #now check for new players who participated in past day
    for message in messageList:
        for currentPlayers in formatData:

            #if the player already exists in the list, set flag to true
            if currentPlayers[0] == message.author.name:
                flag = True

        #if flag comes back false, add to a temp list with score of 0
        if flag == False:
            tempArr.append([message.author.name, 0])

    #add all new players to list
    for i in tempArr:
        formatData.append(i)

    f.close()

    return formatData




async def getNewScores(messageList):

    """
    Extracts the score from wordle score message
    :param messageList: List of messages from past day (loopDay() return)
    :return: array formatted as [[Player, P1's score today], [Player2, P2's score today]]
    """

    """
    Scores are as follows:
    1: 12
    2: 7
    3: 4
    4: 3
    5: 2
    6: 1
    X: -6
    """


    todaysScore = []

    for i in messageList:

        content = i.content

        score = content.split(" ")
        score = score[2].split()
        score = score[0][0]


        if score == "1":

            todaysScore.append([i.author.name, 12])

        elif score == "2":
            todaysScore.append([i.author.name, 7])

        elif score == "3":
            todaysScore.append([i.author.name, 4])

        elif score == "4":
            todaysScore.append([i.author.name, 3])

        elif score == "5":

            todaysScore.append([i.author.name, 2])

        elif score == "6":

            todaysScore.append([i.author.name, 1])

        elif score == "X":
            todaysScore.append([i.author.name, -5])

    return todaysScore




async def updateScores():

    """
    Updates players array with new scores
    :return: players array with new scores
    """


    messageList = await loopDays()

    #Go through content for each person and extract their new score

    newScores = await getNewScores(messageList)

    oldScores = await buildBoard()


    playerScore = []

    for i in newScores:
        for j in oldScores:

            if j[0] == i[0]:
                playerScore.append([i[0], i[1]+int(j[1])]) #Why isnt this an int already lmao




    updateFile(playerScore)



    return playerScore


#write to file

def updateFile(updatedArray):

    writeString = ""

    for i in updatedArray:
        for j in i:

            writeString += str(j)
            writeString += " "

        writeString += "\n"


    f = open("temp.txt", "w+")

    f.write(writeString)

    f.close()

    os.remove("leaderboard.txt")
    os.rename("temp.txt", "leaderboard.txt")


#format the output

#sort the scores




def main():
    print("Up and Running")
    client.run(TOKEN)



main()