This is a discord bot you can deploy if you want to send Paypal payments via discord commands. 
Please keep in mind that you need to use your own discord bot token, paypal client id, and paypal client secret.

Setup:

1. Create your own .env file that includes your discord bot token, paypal client id, and paypal client secret.
    If you don't have a discord bot created already, you can follow the guide here https://discordpy.readthedocs.io/en/stable/discord.html
    to create the bot. You will need to authorize the intents of the discord bot like the screenshot below:
   <img width="1115" alt="image" src="https://github.com/user-attachments/assets/6b269fbc-124f-421a-9818-3b919d7c05c4" />

   (If you would like to run this bot in paypal production, please update payment_url and access_token_url in jshelpers.py to paypal production urls)
2. Install requirements
   ```pip install -r requirements.txt```
3. Start the bot
   ```python3 main.py```
