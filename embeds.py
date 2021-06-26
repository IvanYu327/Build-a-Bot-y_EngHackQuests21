import discord

#PLAN EMBED
def plan(member,data):
    
    id=str(member)

    embed=discord.Embed(title=str(member.display_name)+"'s Exercise Profile",color=0xfbff00 )
    embed.set_thumbnail(url = member.avatar_url)

    if str(member) in data["users"]:
        score =str(data[id]["completed"])+"/"+str(data[id]["completed"]+data[id]["missed"])
        embed.add_field(name="Info", value="⏲Remind time: "+str(data[id]["remind"]+"\n💯Score: "+score), inline=False)

        for dayTitle in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']:
            day=str.lower(dayTitle)

            if data[id]["Plan"][day]["completed"] == 'yes':
                dayTitle = "✅ "+dayTitle
            elif data[id]["Plan"][day]["subplans"]:
                dayTitle = "❌ "+dayTitle

            plans = ""

            if data[id]["Plan"][day]["subplans"]:
                for x in data[id]["Plan"][day]["subplans"]:
                    plans += x+"\n"
            else:
                dayTitle = "🛌 "+dayTitle
                plans="No plans. Rest day!"

            embed.add_field(name=dayTitle, value=plans, inline=True)
    else:
        print("elsed")
        embed.add_field(name="❌No profile found",value="This user did not create a profile yet!", inline=True)
    return embed


#WELCOME EMBED
def welcome():
    embed=discord.Embed(title="Build A Bot-y", description="Welcome to Build A Bot-y, a customizable weekly workout plan bot made to help BUILD YOUR BODY, keep you ACCOUNTABLE, track your progress, and see how your friends are doing!", color=0xfbff00)
    embed.set_thumbnail(url="https://i.pinimg.com/originals/fb/54/84/fb54840e84aef6e2dcda3609caa8478f.gif")
    embed.add_field(name="!create", value="Creates a new account if you don't have one!", inline=False)
    embed.add_field(name="!add [day][item]", value="Ex: !add monday legs (Adds legs to monday)", inline=False)
    embed.add_field(name="!add default", value="Replaces your weekly plan with a preset one", inline=False)
    embed.add_field(name="!clear [day]", value="Clears out the day specified", inline=False)
    embed.add_field(name="!remind [HH:MM]", value="Set a daily reminder in 24 hour time", inline=False)
    embed.add_field(name="!plan [@user-optional argument]", value="View your (or other people's) weekly plan, progress, all time scores", inline=False)
    embed.add_field(name="!motivate", value="Sends you some exercise motivation", inline=False)
    embed.add_field(name="!scores", value="Shows a scoreboard", inline=False)
    return embed

#LEADERBOARD
def lb(data):
    embed=discord.Embed(title="Scores", description="Scores based on percentage completion", color=0xfbff00)
    embed.set_thumbnail(url="https://i.pinimg.com/originals/fb/54/84/fb54840e84aef6e2dcda3609caa8478f.gif")
    userList=""
    userScores=""
    userPercents=""
    
    for user in data["users"]:
        userList += user+"\n"
        
        score =str(data[user]["completed"])+"/"+str(data[user]["completed"]+data[user]["missed"])
        userScores += score+"\n"

        top = int(data[user]["completed"])
        bottom = int(data[user]["completed"])+int(data[user]["missed"])
        print(top)
        print(bottom)
        if(top+bottom==0):
            percent="0"
        else:
            percent=int(top/bottom*100)
        userPercents += str(percent)+"%\n"
    
    print(userList)
    print(userScores)
    print(userPercents)

    embed.add_field(name="Users", value=userList, inline=True)
    embed.add_field(name="Percentage", value=userPercents, inline=True)
    embed.add_field(name="Score", value=userScores, inline=True)
    return embed