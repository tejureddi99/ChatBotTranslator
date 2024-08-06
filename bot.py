import json
import os
import requests
from enum import Enum
from botbuilder.core import ActivityHandler, TurnContext, MessageFactory, CardFactory
from botbuilder.schema import ChannelAccount, SuggestedActions, CardAction, ActionTypes, Attachment
from enum import Enum

class TranslationSettings(Enum):
    english_spanish = ("en", "es", "Spanish")
    english_hindi = ("en", "hi", "Hindi")
    english_french = ("en", "fr", "French")

language_full_names = {
    "en": "English",
    "es": "Spanish",
    "hi": "Hindi",
    "fr": "French"
}

class MyBot(ActivityHandler):
    def __init__(self, subscription_key: str, region: str, endpoint: str):
        super().__init__()
        self.subscription_key = subscription_key
        self.region = region
        self.endpoint = endpoint
        self.user_language_preferences = {}  # Dictionary to store language preference for each user

    async def on_message_activity(self, turn_context: TurnContext):
        user_id = turn_context.activity.from_property.id
        user_text = turn_context.activity.text.lower() if turn_context.activity.text else ""

        # Check if the language was selected from the adaptive card
        if turn_context.activity.value and "language" in turn_context.activity.value:
            selected_language = turn_context.activity.value["language"]
            if selected_language in TranslationSettings.__members__:
                self.user_language_preferences[user_id] = TranslationSettings[selected_language]
                await turn_context.send_activity(f"Language set to {TranslationSettings[selected_language].value[2]}. Please type something to translate.")
                return

        if user_text == "quit":
            if user_id in self.user_language_preferences:
                del self.user_language_preferences[user_id]
            await turn_context.send_activity("You have exited the translation mode.")
            await self._send_language_options(turn_context)
            return

        if any(user_text == setting.name.split('_')[1].lower() for setting in TranslationSettings):
            selected_language = next(setting for setting in TranslationSettings if setting.name.split('_')[1].lower() == user_text)
            self.user_language_preferences[user_id] = selected_language
            await turn_context.send_activity(f"Language set to {selected_language.value[2]}. Please type something to translate.")
            return

        if user_text == "hi":
            await turn_context.send_activity("Please choose a language:")
            await self._send_language_options(turn_context)
            return

        # Check if the user text is valid before making the translation request
        if not user_text.strip():
            await turn_context.send_activity("Please enter a valid text to translate.")
            return

        user_language = self.user_language_preferences.get(user_id, TranslationSettings.english_french)
        detected_language = await self.detect_language(user_text)

        # Determine the target language based on detected language
        if detected_language == user_language.value[0]:
            target_language = user_language.value[1]
        else:
            target_language = user_language.value[0]

        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-Type': 'application/json',
        }

        body = [{'text': turn_context.activity.text}]
        params = {
            'api-version': '3.0',
            'from': detected_language,
            'to': [target_language]
        }

        constructed_url = f"{self.endpoint}/translate"
        response = requests.post(constructed_url, headers=headers, params=params, json=body)
        response_json = response.json()

        if response.status_code == 200:
            translations = response_json[0]['translations']
            translation_texts = [f"{language_full_names[trans['to']]}: {trans['text']}" for trans in translations]
            await turn_context.send_activity("\n".join(translation_texts))
        else:
            await turn_context.send_activity(f"Error: {response.status_code} - {response.text}")

    async def detect_language(self, text: str) -> str:
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-Type': 'application/json',
        }

        body = [{'text': text}]
        params = {
            'api-version': '3.0',
        }

        constructed_url = f"{self.endpoint}/detect"
        response = requests.post(constructed_url, headers=headers, params=params, json=body)
        response_json = response.json()

        if response.status_code == 200:
            return response_json[0]['language']
        else:
            raise Exception(f"Error detecting language: {response.status_code} - {response.text}")

    async def on_members_added_activity(self, members_added: [ChannelAccount], turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                welcome_card = self._create_adaptive_card_attachment()
                await turn_context.send_activity(MessageFactory.attachment(welcome_card))

    async def _send_language_options(self, turn_context: TurnContext):
        reply = MessageFactory.text("Choose your language:")
        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="हिन्दी (Hindi)",
                    type=ActionTypes.post_back,
                    value=TranslationSettings.english_hindi.name.split('_')[1].lower(),
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

    def _create_adaptive_card_attachment(self) -> Attachment:
        card_path = os.path.join(os.getcwd(), "cards", "welcomeCard.json")
        with open(card_path, "rt", encoding="utf-8") as in_file:
            card_data = json.load(in_file)
        return CardFactory.adaptive_card(card_data)
