import discord
from discord.commands import Option

bot = discord.Bot()

# If you use commands.Bot, @bot.slash_command should be used for
# slash commands. You can use @bot.slash_command with discord.Bot as well


# Example of a slash command using Option type-hints.

@bot.slash_command(guild_ids=[...])
async def hello(
    ctx,
    name: Option(str, "Enter your name"),
    gender: Option(str, "Choose your gender", choices=["Male", "Female", "Other"]),
    age: Option(int, "Enter your age", required=False, default=18),
):
    await ctx.respond(f"Hello {name}, you are {age} years old and you gender is {gender}!")

    
# Example of a slash command using Option decorators.

@bot.slash_command(guild_ids=[...])
@discord.option("name", "Enter your name")
@discord.option("gender", "Choose your gender", choices=["Male", "Female", "Other"])
@discord.option("age", "Enter your age", required=False, default=18)
async def hello(ctx, name: str, gender: str, age: int):
    await ctx.respond(f"Hello {name}, you are {age} years old and you gender is {gender}!")
    

bot.run("TOKEN")
