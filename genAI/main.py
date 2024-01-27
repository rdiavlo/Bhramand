from openai import OpenAI
from configparser import ConfigParser


# Get the configparser object
config_object = ConfigParser()
# Read the contents of the `config.ini.ini` file:
config_object.read('config.ini')

p_api_key = config_object.get('OpenAI', 'api_key')
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=p_api_key,
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)