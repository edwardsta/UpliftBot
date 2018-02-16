
# Here we create a web application using Flask which will
# define an endpoint where a user's request is handled, and
# a response can be returned from our bot.

import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAADhJZAuDaxkBAJzUcCKwEMoih6gxyWxN2Tkbv9MXf1MtVo6PxCTaQ5rxKMA04HbjEZBh4ZArSbvP2WB8jJ0lqMgg9ZAyZAXmScRhHQQtTJArYmbp1GYmM9s7hnzhHEAZBMdnzAvoRZCCLfOVmBCKy9JIZC1MWvJJZCLZBylZC4kCRvQAZDZD'
VERIFY_TOKEN = 'Liftmeup'
bot = Bot(ACCESS_TOKEN)

# This endpoint is where messages from Facebook are recieved by our bot
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        # Facebook requires a verify token to confirm all
        # requests that our bot recieves came from Facebook
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # If the request was not GET, it must be POST
    else:
        # Get message sent to bot by user
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # Facebook Messenger ID for user so we know where to send response
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    # If user sends us photo, vid, GIF, or other non-text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def verify_fb_token(token_sent):
    # Compare token sent by Facebook to verify token we sent
    # If they match, all request, otherwise return error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def get_message():
    sample_responses = ["You're the best!", "You are SO pretty", "I'm proud of you :D", "Keep being you"]
    #chatterbot_response = chatbot.get_response(message)
    return random.choice(sample_responses)
    
def send_message(recipient_id, response):
    # Send user the text message provided by input response  argument
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()



