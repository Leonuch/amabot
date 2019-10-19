''' GbeBot '''

from flask import Flask, render_template, request 
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import levenshtein_distance
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
APP = Flask(__name__)

EN_BOT = ChatBot("Chatterbot",
                      storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
                      database_uri='mongodb+srv://leobot:QQCtCUB8MmTdJnL@chatb-09nlj.gcp.mongodb.net/test?retryWrites=true&w=majority',# pylint: disable=line-too-long
                      statement_comparison_function=levenshtein_distance,
                      filters=[
                          'chatterbot.filters.RepetitiveResponseFilter'],
                      logic_adapters=[
                          {
                              'import_path': 'chatterbot.logic.BestMatch',
                              'threshold': 0.85,
                              'default_response': 'I am sorry, but I do not understand.'
                              }
                          ]
                      )

TRAINER = ChatterBotCorpusTrainer(EN_BOT)


# For training the corpus data
# TRAINER.train('chatterbot.corpus.english')
# TRAINER.train("./data/macorpus/")


@APP.route("/")
def home():
    ''' Home '''
    return render_template("index.html")

@APP.route("/get")
def get_bot_response():
    ''' Get reply from Bot '''
    user_text = request.args.get('msg')
    return str(EN_BOT.get_response(user_text))


if __name__ == "__main__":
    APP.run()