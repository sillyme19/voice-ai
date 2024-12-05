import assemblyai as ai
from elevenlabs import generate,stream
from openai import OpenAI
class Ai_assistant:
    def __init__(self):
        ai.settings.api_key='API-KEY'
        self.openai_client=OpenAI(api_key = "API-KEY")
        self.elevenlabs_api_key='API-KEY'

        self.transcriber=None

        self.full_transcript=[
            {'role':'system',
             'content':'hey welcome this is your personal voice over ai'}
        ]


    def start_transcription(self):
        self.transcriber=ai.RealtimeTranscriber(
            sample_rate=16000,
            on_data=self.on_data,
            on_error=self.on_error,
            on_open=self.on_open,
            on_close=self.on_close,
            end_utterance_silence_threshold=1000
        )

        self.transcriber.connect()
        try:
            microphone_Stream=ai.extras.MicrophoneStream(sample_rate=16000)
            self.transcriber.stream(microphone_Stream)
        except:
            print("error here")
    def stop_transcription(self):
         if self.transcriber:
             self.transcriber.close()
             self.transcriber=None

    def on_open(self,session_opened:ai.RealtimeSessionOpened):
        print("session ID:",session_opened.session_id)
    
    def on_data(self,transcript:ai.RealtimeFinalTranscript):
        if not transcript.text:
            print("no text received")
            return
        if isinstance(transcript,ai.RealtimeFinalTranscript):
            print("received transcript text")
            print(transcript.text,end='\r\n')
            self.generate_ai_response(transcript)
        else:
            print(transcript.text,end='\r')
    
    def on_error(self,error:ai.RealtimeError):
        print("an error occured",error)
        return
    def on_close(self):
        print("closing session")
        return
     

    def generate_ai_response(self,transcript):
        self.stop_transcription()

        self.full_transcript.append({'role':'user','content':transcript.text})
        print(f"\nUser:{transcript.text}",end='\r\n')
        response=self.openai_client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=self.full_transcript
        )

        ai_response=response.choices[0].message.content
        self.generate_audio(ai_response)

        self.start_transcription()


    def generate_audio(self,text):
        self.full_transcript.append({'role':'assistant','content':text})
        print(f"\nAssistant :{text}")

        audio_stream=generate(
            api_key=self.elevenlabs_api_key,
            text=text,
            voice="Roger",
            stream=True
        )

        stream(audio_stream)

greeting='hey i am your personal assistant. how can i help you?'
assistant=Ai_assistant()
assistant.generate_audio(greeting)
assistant.start_transcription()