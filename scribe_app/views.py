import openai
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from .models import Patient, UploadedPDF
from .forms import UploadPDFForm
from .generate_hpi import open_patient_info, VoiceRecorder
from PyPDF2 import PdfReader
from django.conf import settings

class PatientView(ListView):
    template_name = 'patient_list.html'
    model = Patient

def extract_content_from_pdf(pdf_path):
    content = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            content += page.extract_text()
    return content

def upload_pdf(request):
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = UploadedPDF(file=request.FILES['file'])
            pdf.save()
            
            content = extract_content_from_pdf(pdf.file.path)
            hpi = generate_hpi_from_content(content)
            
            pdf.generated_hpi = hpi
            pdf.save()

            return redirect('show_hpi', pdf_id=pdf.id)
    else:
        form = UploadPDFForm()

    return render(request, 'upload.html', {'form': form})

def show_hpi(request, pdf_id):
    pdf = UploadedPDF.objects.get(id=pdf_id)
    return render(request, 'show_hpi.html', {'hpi': pdf.generated_hpi})

def generate_hpi_from_content(content):
    return generate_hpi_with_chatgpt(content)

def generate_hpi_with_chatgpt(content):
    openai.api_key = settings.OPENAI_API_KEY
    
    prompt = f"Generate a History of Present Illness based on the following content:\n{content}"

    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=1200
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Error generating HPI. Please try again."

def record_voice_view(request):
    recorder = VoiceRecorder()
    saved_audio_path = recorder.record()

    transcription = transcribe_patient(saved_audio_path)

    pdf = UploadedPDF(generated_hpi=transcription)
    pdf.save()

    return HttpResponseRedirect(reverse('show_hpi', args=(pdf.id,)))



# import openai
# from django.shortcuts import render, redirect
# from django.views.generic import ListView
# from .models import Patient
# from .forms import UploadPDFForm
# from .models import UploadedPDF
# from PyPDF2 import PdfReader
# from django.conf import settings


# class PatientView(ListView):
#     template_name = 'patient_list.html'
#     model = Patient


# def extract_content_from_pdf(pdf_path):
#     content = ""
#     with open(pdf_path, 'rb') as file:
#         reader = PdfReader(file)
#         for page in reader.pages:
#             content += page.extract_text()
#     return content


# def upload_pdf(request):
#     if request.method == 'POST':
#         form = UploadPDFForm(request.POST, request.FILES)
#         if form.is_valid():
#             pdf = UploadedPDF(file=request.FILES['file'])
#             pdf.save()
            
#             # Extract content from the uploaded PDF
#             content = extract_content_from_pdf(pdf.file.path)
            
#             # Generate the HPI using the content
#             hpi = generate_hpi_from_content(content)
            
#             pdf.generated_hpi = hpi
#             pdf.save()

#             # Redirect to a new page showing the generated HPI
#             return redirect('show_hpi', pdf_id=pdf.id)
#     else:
#         form = UploadPDFForm()

#     return render(request, 'upload.html', {'form': form})


# def show_hpi(request, pdf_id):
#     pdf = UploadedPDF.objects.get(id=pdf_id)
#     return render(request, 'show_hpi.html', {'hpi': pdf.generated_hpi})

# def generate_hpi_from_content(content):
#     return generate_hpi_with_chatgpt(content)


# def generate_hpi_with_chatgpt(content):
#     openai.api_key = settings.OPENAI_API_KEY
    
#     # Prepare the prompt
#     prompt = f"Generate a History of Present Illness based on the following content:\n{content}"

#     try:
#         response = openai.Completion.create(
#             engine="davinci",
#             prompt=prompt,
#             max_tokens=1200
#         )
#         return response.choices[0].text.strip()

#     except Exception as e:
#         print(f"Error: {e}")
#         return "Error generating HPI. Please try again."

