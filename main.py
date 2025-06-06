#jarvis my file
from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDictonaryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus)

from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import sys
import threading
import json
import os

env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
DefaultMessage = f'''{Username} : Hello {Assistantname}! How are you?
{Assistantname} : Hello {Username} I'm doing well, how can I help you today?
'''
subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

def ShowDefaultChatIfNoChats():
    File = open(r"Data\ChatLog.json", "r", encoding="utf-8")
    if len(File.read()) < 5:
        with open(TempDictonaryPath("Database.data"), "w", encoding="utf-8") as file:
            file.write("")

        with open(TempDictonaryPath("Responses.data"), "w", encoding="utf-8") as file:
            file.write(DefaultMessage)

def ReadChatLogJson():
    with open(r"Data\ChatLog.json", "r", encoding="utf-8") as file:
        chatlog_data = json.load(file)
    return chatlog_data

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""

    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"User: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content']}\n"

    formatted_chatlog = formatted_chatlog.replace("User", Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname + " ")

    with open(TempDictonaryPath("Database.data"), "w", encoding="utf-8") as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    File = open(TempDictonaryPath("Database.data"), "r", encoding="utf-8")
    Data = File.read()

    if len(str(Data)) > 0:
        lines = Data.split("\n")
        result = '\n'.join(lines)
        File.close()
        File = open(TempDictonaryPath("Responses.data"), "w", encoding="utf-8")
        File.write(result)
        File.close()

def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

InitialExecution()

# def MainExecution():
#     TaskExecution = False
#     ImageExecution = False
#     ImageGenerationQuery = ""

#     SetAssistantStatus("Listining...")
#     Query = SpeechRecognition()
#     ShowTextToScreen(f"{Username} : {Query}")
#     SetAssistantStatus("Thinking...")
#     Decision = FirstLayerDMM(Query)

#     print("")
#     print(f"Decision: {Decision}")
#     print("")

#     G = any([i for i in Decision if i.startswith("general")])
#     R = any([i for i in Decision if i.startswith("realtime")])

#     Merged_query = " and ".join(
#         [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
#     )

#     for queries in Decision:
#         if "generate " in queries:
#             ImageGenerationQuery = str(queries)
#             ImageExecution = True
        
#     for queries in Decision:
#         if TaskExecution == False:
#             if any(queries.startswith(func) for func in Functions):
#                 run(Automation(list(Decision)))
#                 TaskExecution = True

#     if ImageExecution == True:
#         with open(r"Frontend\Files\ImageGeneration.data", "w") as file:
#             file.write(f"{ImageGenerationQuery},True")

#         try:
#             subprocess.run(
#                 [sys.executable, r"Backend/ImageGeneration.py"],
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 text=True  # This will decode the output to a string
#             )
#         except Exception as e:
#             print(f"Error Generating Image: {e}")

#     if G and R or R:
#         SetAssistantStatus("Searching...")
#         Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
#         ShowTextToScreen(f"{Assistantname} : {Answer}")
#         SetAssistantStatus("Answering...")
#         TextToSpeech(Answer)
#         return True
    
#     else:
#         for Queries in Decision:
#             if "general " in Queries:
#                 SetAssistantStatus("Thinking...")
#                 QueryFinal = Queries.replace("general ", "")
#                 Answer = ChatBot(QueryModifier(QueryFinal))
#                 ShowTextToScreen(f"{Assistantname} : {Answer}")
#                 SetAssistantStatus("Answering...")
#                 print(Answer)
#                 TextToSpeech(Answer)
#                 return True
#             elif "realtime" in Queries:
#                 SetAssistantStatus("Thinking...")
#                 QueryFinal = Queries.replace("realtime ", "")
#                 Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
#                 ShowTextToScreen(f"{Assistantname} : {Answer}")
#                 SetAssistantStatus("Answering...")
#                 TextToSpeech(Answer)
#                 return True

#             elif "exit" in Queries:
#                 QueryFinal = "Okay, Bye!"
#                 Answer = ChatBot(QueryModifier(QueryFinal))
#                 ShowTextToScreen(f"{Assistantname} : {Answer}")
#                 SetAssistantStatus("Answering...")
#                 TextToSpeech(Answer)
#                 SetAssistantStatus("Answering...")
#                 os._exit(1)

def MainExecution():
    try:
        TaskExecution = False
        ImageExecution = False
        ImageGenerationQuery = ""

        SetAssistantStatus("Listening...")
        Query = SpeechRecognition()
        ShowTextToScreen(f"{Username} : {Query}")
        SetAssistantStatus("Thinking...")
        Decision = FirstLayerDMM(Query)

        print(f"\nDecision: {Decision}\n")

        G = any(i.startswith("general") for i in Decision)
        R = any(i.startswith("realtime") for i in Decision)

        Merged_query = " and ".join(
            [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
        )

        for queries in Decision:
            if "generate " in queries:
                ImageGenerationQuery = str(queries)
                ImageExecution = True

        for queries in Decision:
            if not TaskExecution and any(queries.startswith(func) for func in Functions):
                run(Automation(list(Decision)))
                TaskExecution = True

        if ImageExecution:
            with open(r"Frontend\Files\ImageGeneration.data", "w") as file:
                file.write(f"{ImageGenerationQuery},True")

            try:
                subprocess.run(
                    [sys.executable, r"Backend/ImageGeneration.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            except Exception as e:
                print(f"Error Generating Image: {e}")

        Answer = ""

        if G and R or R:
            SetAssistantStatus("Searching...")
            Answer = RealtimeSearchEngine(QueryModifier(Merged_query))

        else:
            for Queries in Decision:
                if "general " in Queries:
                    SetAssistantStatus("Thinking...")
                    QueryFinal = Queries.replace("general ", "")
                    Answer = ChatBot(QueryModifier(QueryFinal))
                    break

                elif "realtime " in Queries:
                    SetAssistantStatus("Thinking...")
                    QueryFinal = Queries.replace("realtime ", "")
                    Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                    break

                elif "exit" in Queries:
                    QueryFinal = "Okay, Bye!"
                    Answer = ChatBot(QueryModifier(QueryFinal))
                    ShowTextToScreen(f"{Assistantname} : {Answer}")
                    SetAssistantStatus("Answering...")
                    TextToSpeech(Answer)
                    os._exit(1)

        if Answer:
            ShowTextToScreen(f"{Assistantname} : {Answer}")
            SetAssistantStatus("Answering...")
            TextToSpeech(Answer)
            return True

    except Exception as e:
        print(f"[ERROR in MainExecution]: {e}")



def FirstThread(): 
    while True:
        CurrentStatus = GetMicrophoneStatus()

        if CurrentStatus == "True":
            MainExecution()

        else:
            AIStatus = GetAssistantStatus()

            if "Available..." in AIStatus:
                sleep(0.1)
            
            else:
                SetAssistantStatus("Available...")

def SecondThread():
    GraphicalUserInterface()

if __name__ == "__main__":
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()
