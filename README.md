# ChatBotTranslator

## Translator Bot:
This bot has been created using [Bot Framework](https://dev.botframework.com). It is designed for two-way translation, allowing users to input text in one language and receive translations in the language of their choice.

## Purpose:
The Translator Bot allows users to select a language for translation. Once a language is selected, users can input text in any language, and the bot will detect the input language and translate it to the chosen language. The bot supports the following language pairs:
English to Hindi
English to French
English to Spanish

## Prerequisites
This sample requires prerequisites in order to run.

- Install Python 3.6 or greater.  
- Clone the repository and navigate to the project directory.
- Run `pip install -r requirements.txt` to install all dependencies.
- To consume the Microsoft Translator Text API, first obtain a key following the instructions in the [Microsoft Translator Text API documentation](https://learn.microsoft.com/en-us/azure/ai-services/translator/create-translator-resource). Paste the key in the `SUBSCRIPTION_KEY` and region in the `SUBSCRIPTION_REGION` settings in the `config.py` file.
- Run `python app.py` to start the bot.

## Testing the bot using Bot Framework Emulator

[Bot Framework Emulator](https://github.com/microsoft/botframework-emulator) is a desktop application that allows bot developers to test and debug their bots on localhost or running remotely through a tunnel.

- Install the Bot Framework Emulator version 4.3.0 or greater from [here](https://github.com/Microsoft/BotFramework-Emulator/releases)

### Connect to the bot using Bot Framework Emulator

- Launch Bot Framework Emulator
- File --> Open Bot
- Enter a Bot URL of `http://localhost:3978/api/messages`

## Further Reading

- [Bot Framework Documentation](https://docs.botframework.com)
- [Bot Basics](https://docs.microsoft.com/azure/bot-service/bot-builder-basics?view=azure-bot-service-4.0)
- [Dialogs](https://docs.microsoft.com/azure/bot-service/bot-builder-concept-dialog?view=azure-bot-service-4.0)
- [Gathering Input Using Prompts](https://docs.microsoft.com/azure/bot-service/bot-builder-prompts?view=azure-bot-service-4.0&tabs=csharp)
- [Activity processing](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-concept-activity-processing?view=azure-bot-service-4.0)
- [Azure Bot Service Introduction](https://docs.microsoft.com/azure/bot-service/bot-service-overview-introduction?view=azure-bot-service-4.0)
- [Azure Bot Service Documentation](https://docs.microsoft.com/azure/bot-service/?view=azure-bot-service-4.0)
- [Azure CLI](https://docs.microsoft.com/cli/azure/?view=azure-cli-latest)
- [Azure Portal](https://portal.azure.com)
- [Language Understanding using LUIS](https://docs.microsoft.com/azure/cognitive-services/luis/)
- [Channels and Bot Connector Service](https://docs.microsoft.com/azure/bot-service/bot-concepts?view=azure-bot-service-4.0)




