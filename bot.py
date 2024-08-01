import requests
from enum import Enum
from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount, SuggestedActions, CardAction, ActionTypes

class TranslationSettings(Enum):
    french_english = ("fr", "en")
    english_spanish = ("en", "es")
    english_hindi = ("en", "hi")
    english_french = ("en", "fr")

class MyBot(ActivityHandler):
    def __init__(self, subscription_key: str, region: str, endpoint: str):
        super().__init__()
        self.subscription_key = subscription_key
        self.region = region
        self.endpoint = endpoint
        self.user_language_preferences = {}  # Dictionary to store language preference for each user

    async def on_message_activity(self, turn_context: TurnContext):
        user_id = turn_context.activity.from_property.id
        user_text = turn_context.activity.text.lower()

        if user_text == "quit":
            if user_id in self.user_language_preferences:
                del self.user_language_preferences[user_id]
            await turn_context.send_activity("You have exited the translation mode.")
            await self._send_language_options(turn_context)
            return

        # Check if the message is a language selection
        if any(user_text == setting.name.split('_')[1].lower() for setting in TranslationSettings):
            selected_language = next(setting for setting in TranslationSettings if setting.name.split('_')[1].lower() == user_text)
            self.user_language_preferences[user_id] = selected_language
            await turn_context.send_activity(f"Language set to {selected_language.name.split('_')[1].capitalize()}")
            await turn_context.send_activity("Please type something to translate.")
            return

        # Prompt user to choose a language if 'hi' is typed
        if user_text == "hi":
            await turn_context.send_activity("Please choose a language:")
            await self._send_language_options(turn_context)
            return

        # Get user's preferred language, default to English to French
        user_language = self.user_language_preferences.get(user_id, TranslationSettings.english_french)

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
            'from': user_language.value[0],
            'to': [user_language.value[1]]
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
                await self._send_language_options(turn_context)

    async def _send_language_options(self, turn_context: TurnContext):
        reply = MessageFactory.text("Choose your language:")
        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="हिन्दी",
                    type=ActionTypes.post_back,
                    value=TranslationSettings.english_hindi.name.split('_')[1].lower(),
                ),
                CardAction(
                    title="English",
                    type=ActionTypes.post_back,
                    value=TranslationSettings.french_english.name.split('_')[1].lower(),
                ),
                CardAction(
                    title="French",
                    type=ActionTypes.post_back,
                    value=TranslationSettings.english_french.name.split('_')[1].lower(),
                ),
                CardAction(
                    title="Spanish",
                    type=ActionTypes.post_back,
                    value=TranslationSettings.english_spanish.name.split('_')[1].lower(),
                ),
            ]
        )
        await turn_context.send_activity(reply)
