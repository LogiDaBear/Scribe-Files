import openai
from dotenv import load_dotenv
import os
import PyPDF2
import io
# from .models import PatientVisitInfo  # Assuming there's a model to store patient info
import gradio as gr
import whisper
import pyaudio
import wave
import time
import threading
import tkinter as tk

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def transcribe_patient(audio_file):
    model = whisper.load_model('base')
    result = model.transcribe(audio_file)
    return result['text']

class VoiceRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.button = tk.Button(text="&#127908",
                                 command=self.click_handler)
        self.button.pack()
        self.label = tk.Label(text="00:00:00")
        self.recording = False
        self.root.mainloop()

    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(fg='black')
        else:
            self.recording = True
            self.button.config(fg='red')
            threading.Thread(target=self.record).start()

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1,
                            rate=44100, input=True, frames_per_buffer=1024)
        frames = []
        start = time.time()

        while self.recording:
            data = stream.read(1024)
            frames.append(data)

            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.label.config(text=f'{int(hours):02d}:{int(mins):02d}:{int(secs):02d}')

        stream.stop_stream()
        stream.close()
        audio.terminate()

        exists = True
        i = 1
        while exists:
            if os.path.exists(f'recording{i}.wav'):
                i += 1
            else:
                exists = False

        sound_file = wave.open(f'recording{i}.wav', 'wb')
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()

        return f'recording{i}.wav'

def open_patient_info(pdf_path_or_bytes):
    if isinstance(pdf_path_or_bytes, bytes):
        pdf_stream = io.BytesIO(pdf_path_or_bytes)
    else:
        pdf_stream = open(pdf_path_or_bytes, 'rb')
    
    reader = PyPDF2.PdfReader(pdf_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    return text

def generate_hpi(visit_date, age, gender, occupation, last_seen, smoking_status, medical_history, 
                 present_symptoms, vitals, pft_results, additional_info=""):
    prompt = (
        f"Generate a History of Present Illness based on the following details:\n"
        f"Visit Date: {visit_date}\n"
        f"Age: {age}\n"
        f"Gender: {gender}\n"
        f"Occupation: {occupation}\n"
        f"Last Seen: {last_seen}\n"
        f"Smoking Status: {smoking_status}\n"
        f"Medical History: {medical_history}\n"
        f"Present Symptoms: {present_symptoms}\n"
        f"Vitals: {vitals}\n"
        f"PFT Results: {pft_results}\n"
        f"Additional Info: {additional_info}\n"
    )

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1200,
        temperature=0.7,
        top_p=0.9,
    )
    return response.choices[0].text.strip()

# import openai
# from dotenv import load_dotenv
# import os
# import PyPDF2
# import io
# from .models import PatientVisitInfo  # Assuming there's a model to store patient info
# import gradio as gr
# import whisper

# def transcribe_patient(audio_file):
#     model = whisper.load_model('base')
#     result = model.transcribe(audio_file)
#     return result['text']

# def main():
#     audio_input = gr.inputs.Audio(source='upload', type='filepath')
#     output_text = gr.outputs.Textbox()

#     iface = gr.Interface(fn=transcribe_patient, inputs=audio_input, outputs=output_text, title= 'Audio Transcription', description='Upload audio file and hit the Submit button')

#     iface.launch()

# load_dotenv()
# openai.api_key = os.getenv('OPENAI_API_KEY')

# def open_patient_info(pdf_path_or_bytes):
#     # Check if the input is a path or bytes object
#     if isinstance(pdf_path_or_bytes, bytes):
#         # Convert bytes to a file-like object
#         pdf_stream = io.BytesIO(pdf_path_or_bytes)
#     else:
#         pdf_stream = open(pdf_path_or_bytes, 'rb')
    
#     reader = PyPDF2.PdfReader(pdf_stream)
#     text = ""
#     for page in reader.pages:
#         text += page.extract_text()
    
#     return text

# def upload_patient_info(request):
#     if request.method == 'POST' and request.FILES.get('pdf_file'):
#         pdf_contents = request.FILES.get('pdf_file').read()

#         # Extract text from the PDF
#         visit_info_text = open_patient_info(pdf_contents)
#         stored_info = PatientVisitInfo(description=visit_info_text)
#         stored_info.save()
#     return JsonResponse({'status': 200})

# def generate_hpi(visit_date, age, gender, occupation, last_seen, smoking_status, medical_history, 
#                  present_symptoms, vitals, pft_results, additional_info=""):
#     prompt = (
#         f"Generate a History of Present Illness based on the following details:\n"
#         f"Visit Date: {visit_date}\n"
#         f"Age: {age}\n"
#         f"Gender: {gender}\n"
#         f"Occupation: {occupation}\n"
#         f"Last Seen: {last_seen}\n"
#         f"Smoking Status: {smoking_status}\n"
#         f"Medical History: {medical_history}\n"
#         f"Present Symptoms: {present_symptoms}\n"
#         f"Vitals: {vitals}\n"
#         f"PFT Results: {pft_results}\n"
#         f"Additional Info: {additional_info}\n"
#     )

#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=1200,
#         temperature=0.7,
#         top_p=0.9,
#     )
#     return response.choices[0].text.strip()


# if __name__ == "__main__":
#     main()