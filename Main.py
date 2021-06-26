import discord
from discord.ext import commands, tasks
import json
import os
import calendar
import datetime
import random
from discord.ext.commands import MemberConverter, context

import sys
from discord.ext.commands.bot import Bot

from discord.ext.commands.core import check
sys.path.append(".")

import EngHack.embeds as em

#STUFF ===================================================================================
TOKEN = 123 #Add token here
client = commands.Bot(command_prefix = '-')
os.chdir(r'C:\Users\yuiva\Documents\Ivans Documents\Code\EngHack')
file = "EngHackData.json"

@client.event
async def on_ready():
    print("ready")   
    checkTime.start()

#CREATE ===================================================
@client.command()
async def create(ctx):
    data = await get_data() 
    id=str(ctx.author)
    idNum = str(ctx.author.id)
    if id in str(data):
        await ctx.send("You already have an account!")
    else:
        data["users"].append(id)
        data[id]={}
        data[id]["id#"]=idNum
        data[id]["completed"]=0
        data[id]["missed"]=0
        data[id]["remind"]=""
        data[id]["Plan"]={}
        for x in range(0,7):
            day = str.lower(calendar.day_name[x])
            data[id]["Plan"][day]={}
            data[id]["Plan"][day]["completed"]="no"
            data[id]["Plan"][day]["subplans"]=[]
        await ctx.send(embed=em.welcome())

        with open(file,"w") as f:
            json.dump(data,f,indent=4)

    


#ADD PLAN ==========================================================================
@client.command()
async def add(ctx,day,plan=""):
    day = str.lower(day)    
    plan = str.lower(plan)
    id=str(ctx.author)
    print(plan)
    data = await get_data() 

    if day=="default":
        for dayTitle in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
            data[id]["Plan"][dayTitle]["subplans"]=[]
        data[id]["Plan"]["tuesday"]["subplans"].append("legs")
        data[id]["Plan"]["thursday"]["subplans"].append("arms")
        data[id]["Plan"]["saturday"]["subplans"].append("booty")
        data[id]["Plan"]["sunday"]["subplans"].append("chest")
        await ctx.send("✅  The default weekly plan has been added to your plan.")
   
    
    elif day in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
        if not plan in data[id]["Plan"][day]["subplans"]:
            data[id]["Plan"][day]["subplans"].append(plan)

            await ctx.send("✅  "+plan.capitalize()+" has been added to "+day.capitalize()+"!")

        else:     
            await ctx.send ("❗  "+plan.capitalize()+" is already added to "+day.capitalize()+"!")
    else:
        await ctx.send("❓  Please enter a day of the week.")
    with open(file,"w") as f:
            json.dump(data,f,indent=4)

#CLEAR PLAN ===================================================================
@client.command()
async def clear(ctx,day):
    print("clear")
    day = str.lower(day)    
    id=str(ctx.author)
    if day in ['monday','tuesday','wednesday','thurday','friday','saturday','sunday']:
        data = await get_data()     
        
        data[id]["Plan"][day]["subplans"]=[]
        
        await ctx.send("✅  "+day.capitalize()+"'s plan is now empty!")
        
        with open(file,"w") as f:
            json.dump(data,f,indent=4)
    else:
        await ctx.send("❓  Please enter a day of the week.")

#REMIND ==================================
@client.command()
async def remind(ctx,time:str):
    id=str(ctx.author)
    data = await get_data() 
    
    try:
        hour = int(time[:2])
        minute = int(time[3:])
        if hour<=24 and hour>=0 and minute<=59 and minute>=0:
            data[id]["remind"]=time
            await ctx.send("✅  You set your daily reminder for: "+time)
        else:
            await ctx.send("❌ Please enter a valid 24 hour time")
    except:
        await ctx.send("❌ Please enter a valid 24 hour time")

    with open(file,"w") as f:
        json.dump(data,f,indent=4)

@tasks.loop(seconds=60)
async def checkTime():
    data = await get_data()     
    fullTime=datetime.datetime.now()
    time=str(fullTime.strftime("%X"))
    time = time[:5]
    today = str.lower(calendar.day_name[datetime.datetime.today().weekday()])    
    print(time+"--"+today)
    
    for user in data["users"]:
        remind=data[user]["remind"]
        print(user+"--"+remind)
        
        if time == remind and data[user]["Plan"][today]["subplans"] and data[user]["Plan"][today]["completed"]=="no":
            idNum=data[user]["id#"]            
            username=await client.fetch_user(idNum)
            channel = await username.create_dm()
            await channel.send("🏋️‍♀️ This is your daily reminder to complete your exercise plan for today, "+today.capitalize()+"!")


#COMPLETE ========================================================================
@client.command()
async def complete(ctx):
    today = str.lower(calendar.day_name[datetime.datetime.today().weekday()])
    id=str(ctx.author)
    data = await get_data()     
    
    if data[id]["Plan"][today]["completed"]=="no":
        data[id]["Plan"][today]["completed"]="yes"
        await ctx.send("✅  Way to go for completing your "+today.capitalize()+" plan!")
        data[id]["completed"] += 1
    else:
        await ctx.send("❗  You have already completed today's goals! Take a break!")

    with open(file,"w") as f:
        json.dump(data,f,indent=4)

#SHOW PLAN==================================================
@client.command()
async def plan(ctx,member: discord.Member=None):
    if member == None:
        member=ctx.author
    data = await get_data()
    await ctx.send(embed = em.plan(member,data))

#SCORES==================================================
@client.command()
async def scores(ctx):
    data = await get_data()
    await ctx.send(embed = em.lb(data))

#MOTIVATE ===============================
@client.command()
async def motivate(ctx):
    motivate=[
        "https://giphy.com/gifs/jasonclarke-dog-animated-gif-vF25I06jdODgA",
        "https://giphy.com/gifs/EgkNhBeY289z2",
        "https://giphy.com/gifs/exercise-funny-weird-vuIVvW0NsWBzy",
        "https://giphy.com/gifs/dinosaur-t-rex-tyrannosaurus-NSodIu91KDWCs",
        "https://giphy.com/gifs/Openfit-o2UlYeHYbJrBKPaRzt",
        "https://giphy.com/gifs/workout-egg-pun-l2JhB4Sp6hz37lU1W",
        "https://giphy.com/gifs/pug-puglie-FP6uMQiUNRWnmSWkFt",
        "https://giphy.com/gifs/justviralnet-funny-gym-kid-XDpjeIC1f7wTcQj39H",
        "https://giphy.com/gifs/dogs-exercise-workout-5EJHDSPpFhbG0",
        "https://giphy.com/gifs/VFDeGtRSHswfe"
    ]
    await ctx.send(random.choice(motivate))

#HELP PAGE ================================================================================================================
client.remove_command("help")
@client.command(invoke_without_command = True)
async def help(ctx):
    await ctx.send(embed = em.welcome())

#ERROR ================================================================================================================
@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("❓  Missing argument(s).") 
    elif isinstance(error,commands.BadArgument):
        await ctx.send("❓  Invalid argument entered.")


#GET DATA ================================================================================================================
async def get_data():
    with open(file,"r") as f:
        stuff  = json.load(f)
    return stuff

client.run(TOKEN)
