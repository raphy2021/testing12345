from discord_webhook import DiscordWebhook, DiscordEmbed
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import time
import tweepy
from datetime import datetime
import re

def scrape_hashtags(tweet):
    tags = []
    for hashtags in tweet.entities["hashtags"]:
        tags.append(hashtags["text"])
    the_boys =""
    for tag in tags:
        the_boys+="%23"+str(tag)+"%20"
    return the_boys

def create_embed(tweet, the_boys):
    embed = DiscordEmbed(title="@" + tweet.user.screen_name, description="[Click Here To Tweet And Enter!](https://twitter.com/intent/tweet?text="+the_boys+")", color=0xf1c40f)
    embed.set_author(name='NEW FOOJI FROM:', icon_url='https://pbs.twimg.com/profile_images/1112870837093322756/0Q_XSAQk_400x400.png')
    embed.set_footer(text='Monitor made by gray#8532')
    return embed

def create_webhook(embed, webhook_urls):
    webhook = DiscordWebhook(url=webhook_urls)
    webhook.add_embed(embed)
    return webhook

def trigger(tweet):
    if tweet.user.verified == True:
        reg = re.findall("[0-9][0-9] [0-9][0-9]:", str(tweet.created_at))
        twitday = int(reg[0][0:2])
        twithour = int(reg[0][3:5])
        if tweet.id not in found and twitday == day and abs(twithour - hour) <= 1:
            return True
    return False

def original_tweet_send(tweet, webhook_urls):
    webhook = DiscordWebhook(url=webhook_urls, content="https://twitter.com/"+tweet.user.screen_name+"/status/"+str(tweet.id))
    response = webhook.execute()

def user_entry_send(tweet, the_boys, webhook_urls):
    embed = create_embed(tweet, the_boys)
    webhook = create_webhook(embed, webhook_urls)
    response = webhook.execute()

webhook_urls = ['https://discord.com/api/webhooks/903757117645815808/LljOoQE0Ha118AoVFEbZfR25ajiJLBJGMvaYMKxCmXVSzvFCPDOKh2RN-BWnYMcx-Dni']

webhook = DiscordWebhook(url=webhook_urls, content='Fooji Detector is On! This is a test webhook')

response = webhook.execute()

found = set()
found_content = set()

api_consumer_key = 'DObMXoR9venvwrSPZJo1PjYGA'
api_consumer_secret_key = 'X4mGxkVJFLAWUopUPAqSLIu3MTT4SOrERGZsYIMgqwmPoG2X4k'
access_token_key = '761890871864356864-4wa6hUiQ17HVT8znL0zwG0TjwiGHArC'
access_token_secret_key = 'GrqFS7hoD1mKX1zPWAGcfJ08XVKppVcmbqsm4nfZmdBKd'


auth = tweepy.OAuthHandler(api_consumer_key, api_consumer_secret_key)
auth.set_access_token(access_token_key, access_token_secret_key)

api = tweepy.API(auth)

phrases = ["fooji.info/", "NoPurNec.18+VoidWhereProhib."]

while True:
    for phrase in phrases:
        hour = int(datetime.now().hour)
        day = int(datetime.now().day)
        thing = api.search_tweets(phrase, result_type = "recent", count = 3, tweet_mode='extended')
        for tweet in thing:
            if trigger(tweet):
                the_boys = scrape_hashtags(tweet)
                    
                original_tweet_send(tweet, webhook_urls)

                user_entry_send(tweet, the_boys, webhook_urls)
                    
                found.add(tweet.id)
    

                    
    thing = api.search_tweets("l.fooji.com/l/", result_type = "recent", count = 2)
    for tweet in thing:
        if tweet.user.verified == True:

            reg = re.findall("[0-9][0-9] [0-9][0-9]:", str(tweet.created_at))

            twitday = int(reg[0][0:2])
            twithour = int(reg[0][3:5])

            try:
                if tweet.user.screen_name not in found_content and (twitday == day or (abs(twitday - day) <= 1 and (twithour == 0 or twithour == 23)) or abs(twitday - day > 27)) and abs(twithour - hour) <= 1:
                    reply = api.get_status(tweet.in_reply_to_status_id)

                    the_boys = scrape_hashtags(reply)

                    original_tweet_send(tweet, webhook_urls)

                    user_entry_send(tweet, the_boys, webhook_urls)
                    
                    found_content.add(tweet.user.screen_name)
            except:
                print("Original Tweet is Gone")
    
 
    time.sleep(20) 

