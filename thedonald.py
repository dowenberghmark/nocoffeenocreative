import os
import time
from slackclient import SlackClient
from donald_generator import DonaldGen

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

class TheDonald():
    # starterbot's ID as an environment variable
    def __init__(self):
        self.BOT_ID = os.environ.get("BOT_ID")
        self.donald = DonaldGen()
    
        
    # constants
        self.AT_BOT = "<@" + self.BOT_ID + ">"
    #COMMANDS = ["do", "gif", "help"]


        self.COMMANDS = {"do" : "Sure...write some more code then I can do that!", "gif" : ":donald:"  }
    # instantiate Slack & Twilio clients

    def get_echo(self, sentence):
        response = sentence
        return response

    def get_response(self, sentence):
        response = self.donald.reply(sentence)    
        return response

    def help_commands(self):
        helper_string = ""
        for command in self.COMMANDS.keys():
            helper_string = helper_string+ " " + command 
            
        return ("Some commands" + helper_string)


    def handle_command(self, command, channel):
        """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
        """
        sentence = command.split(" ", 1)
        command = sentence[0]
        if command == "thoughts":
            response = self.get_response(sentence[1])
        elif command == "echo":
            response = self.get_echo(sentence[1])
        elif command in self.COMMANDS.keys():
            response = self.COMMANDS[command]
        elif command == "help":
            response = self.help_commands()
        else:
            response = "You are fired!!!"
        slack_client.api_call("chat.postMessage", channel=channel,
                              text=response, as_user=True)

    def parse_slack_output(self, slack_rtm_output):
        """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
        """
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and self.AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                    return output['text'].split(self.AT_BOT)[1].strip().lower(), \
                    output['channel']
        return None, None


    
if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    thisBot = TheDonald()
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        
        while True:
            command, channel = thisBot.parse_slack_output(slack_client.rtm_read())
            if command and channel:
                thisBot.handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")


