from dotenv import load_dotenv
import os

env_path = ".env/ibm-credentials.env"

load_dotenv(dotenv_path=env_path, verbose=True)

SPEECH_API_KEY = os.getenv("SPEECH_TO_TEXT_APIKEY")
SPEECH_URL = os.getenv("SPEECH_TO_TEXT_URL")
SPEECH_IAM_APIKEY = os.getenv("SPEECH_TO_TEXT_IAM_APIKEY")
SPEECH_AUTH_TYPE = os.getenv("SPEECH_TO_TEXT_AUTH_TYPE")


LT_API_KEY = os.getenv("LANGUAGE_TRANSLATOR_APIKEY")
LT_IAM_APIKEY = os.getenv("LANGUAGE_TRANSLATOR_IAM_APIKEY")
LT_URL = os.getenv("LANGUAGE_TRANSLATOR_URL")
LT_AUTH_TYPE = os.getenv("LANGUAGE_TRANSLATOR_AUTH_TYPE")
