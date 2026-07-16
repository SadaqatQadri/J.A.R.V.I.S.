import os
import json
from groq import Groq
from dotenv import load_dotenv
from weather import get_weather
from news import get_news
from spotify import play_song, play_playlist, pause, resume, skip, previous, volume, current_track

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city to get weather for"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_news",
            "description": "Get top news headlines, optionally filtered by country and topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "country": {"type": "string", "description": "Two-letter country code, e.g. us, gb, pk"},
                    "topic": {"type": "string", "description": "News category, e.g. technology, sports, business"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "play_song",
            "description": "Play a specific song on Spotify.",
            "parameters": {
                "type": "object",
                "properties": {"song_name": {"type": "string"}},
                "required": ["song_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "play_playlist",
            "description": "Play a specific playlist on Spotify.",
            "parameters": {
                "type": "object",
                "properties": {"playlist_name": {"type": "string"}},
                "required": ["playlist_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {"name": "pause", "description": "Pause Spotify playback.", "parameters": {"type": "object", "properties": {}}}
    },
    {
        "type": "function",
        "function": {"name": "resume", "description": "Resume Spotify playback.", "parameters": {"type": "object", "properties": {}}}
    },
    {
        "type": "function",
        "function": {"name": "skip", "description": "Skip to the next track on Spotify.", "parameters": {"type": "object", "properties": {}}}
    },
    {
        "type": "function",
        "function": {"name": "previous", "description": "Go back to the previous track on Spotify.", "parameters": {"type": "object", "properties": {}}}
    },
    {
        "type": "function",
        "function": {
            "name": "set_volume",
            "description": "Set Spotify playback volume, 0-100.",
            "parameters": {
                "type": "object",
                "properties": {"level": {"type": "integer"}},
                "required": ["level"]
            }
        }
    },
    {
        "type": "function",
        "function": {"name": "current_track", "description": "Get the currently playing track on Spotify.", "parameters": {"type": "object", "properties": {}}}
    }
]

def call_function(name, input_data):
    if name == "get_weather":
        return get_weather(input_data["city"])
    elif name == "get_news":
        return get_news(input_data.get("country", "us"), input_data.get("topic"))
    elif name == "play_song":
        return play_song(input_data["song_name"])
    elif name == "play_playlist":
        return play_playlist(input_data["playlist_name"])
    elif name == "pause":
        return pause()
    elif name == "resume":
        return resume()
    elif name == "skip":
        return skip()
    elif name == "previous":
        return previous()
    elif name == "set_volume":
        return volume(input_data["level"])
    elif name == "current_track":
        return current_track()
    else:
        return "Unknown function."

SYSTEM_PROMPT = (
    "You are JARVIS, a personal voice assistant speaking out loud to your user, Sadaqat. "
    "Keep responses short, natural, and conversational, like a calm and capable butler AI. "
    "Address him as 'sir'. Use the available tools whenever the request involves weather, "
    "news, or Spotify control. Only include tool arguments that are explicitly defined in "
    "the tool's schema, and only when the user's request actually specifies them. "
    "If no tool applies, just respond conversationally."
)


def think(user_text):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_text}
    ]

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=400
        )
    except Exception as e:
        return "Sorry sir, I had trouble understanding that. Could you try rephrasing?"

    response_message = response.choices[0].message

    while response_message.tool_calls:
        messages.append({
            "role": "assistant",
            "content": response_message.content,
            "tool_calls": [tc.model_dump() for tc in response_message.tool_calls]
        })

        for tool_call in response_message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            try:
                result = call_function(name, args)
            except Exception as e:
                result = "Sorry, sir, that service seems to be having trouble at the moment. Please try again in a bit"

                
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=400
            )
        except Exception as e:
            return "Sorry sir, something went wrong while processing that."

        response_message = response.choices[0].message

    return response_message.content