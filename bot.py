import requests
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount

class MyBot(ActivityHandler):
    def __init__(self, subscription_key: str, region: str, endpoint: str):
        super().__init__()
        self.subscription_key = subscription_key
        self.region = region
        self.endpoint = endpoint

    async def on_message_activity(self, turn_context: TurnContext):
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-Type': 'application/json',
        }

        body = [{
            'text': turn_context.activity.text
        }]

        params = {
            'api-version': '3.0',
            'from': 'en',
            'to': ['fr', 'es', 'hi']
        }

        constructed_url = f"{self.endpoint}/translate"
        response = requests.post(constructed_url, headers=headers, params=params, json=body)
        response_json = response.json()

        if response.status_code == 200:
            translations = response_json[0]['translations']
            translation_texts = [f"{trans['to']}: {trans['text']}" for trans in translations]
            await turn_context.send_activity("\n".join(translation_texts))
        else:
            await turn_context.send_activity(f"Error: {response.status_code} - {response.text}")

    async def on_members_added_activity(self, members_added: [ChannelAccount], turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
