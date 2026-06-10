from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
import requests
from django.conf import settings
from openai import OpenAI

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from django.http import JsonResponse
import json

from .serializers import GroupSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

def home(request):
    return render(request, 'home.html')

def avvia_oroscopo(request):
    return redirect('oroscopo')

def pagina_oroscopo(request):
    oroscopo = request.session.pop('oroscopo_testo', None)
    segno = request.session.pop('segno_scelto', None)
    
    mostra_box = True if oroscopo else False


    provider = request.session.get('provider_scelto', None)

    return render(request, 'oroscopo.html', {
        'oroscopo': oroscopo,
        'segno': segno,
        'mostra_box': mostra_box,
        'provider': provider
    })

def recupera_oroscopo_corriere(segno_scelto):
    oroscopo_testo = None
    if segno_scelto:
        try:
            url = f"https://www.corriere.it/oroscopo/oggi/{segno_scelto}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            risposta = requests.get(url, headers=headers)
            if risposta.status_code == 200:
                soup = BeautifulSoup(risposta.text, 'html.parser')
                elemento_oroscopo = soup.findAll('div', class_='content')
                elemento_oroscopo = elemento_oroscopo[1]
                if elemento_oroscopo:
                    frammenti_testo = list(elemento_oroscopo.stripped_strings)
                    if frammenti_testo:
                        oroscopo_testo = frammenti_testo[-1]
                    else:
                        oroscopo_testo = "Impossibile trovare il testo dell'oroscopo."
                else:
                    oroscopo_testo = "Impossibile trovare il testo dell'oroscopo."
            else:
                oroscopo_testo = f"Errore di connessione (Codice: {risposta.status_code})."
        except Exception as e:
                oroscopo_testo = f"Errore di rete: {str(e)}"
    return oroscopo_testo

def recupera_oroscopo_sky(segno_scelto):
    oroscopo_testo = None
    if segno_scelto:
        try:
            url = f"https://tg24.sky.it/lifestyle/oroscopo/{segno_scelto}/oggi"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x60)'}
            risposta = requests.get(url, headers=headers)
            if risposta.status_code == 200:
                soup = BeautifulSoup(risposta.text, 'html.parser')
                elemento_oroscopo = soup.findAll('div', class_='c-article-section j-article-section c-article-section--secondary l-spacing-m')
                elemento_oroscopo = elemento_oroscopo[0]
                if elemento_oroscopo:
                    oroscopo_testo = elemento_oroscopo.get_text(strip=True)
                else:
                    oroscopo_testo = "Impossibile trovare il testo dell'oroscopo."
            else:
                oroscopo_testo = f"Errore di connessione (Codice: {risposta.status_code})."
        except Exception as e:
                oroscopo_testo = f"Errore di rete: {str(e)}"
    return oroscopo_testo

def recupera_oroscopo_oggi(segno_scelto):
    oroscopo_testo = None
    if segno_scelto:
        try:
            url = f"https://www.oggi.it/oroscopo/oroscopo-di-oggi/{segno_scelto}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x60)'}
            risposta = requests.get(url, headers=headers)
            if risposta.status_code == 200:
                soup = BeautifulSoup(risposta.text, 'html.parser')
                elemento_oroscopo = soup.findAll('p', class_='oroscopoSign__txt')

                elemento_oroscopo = elemento_oroscopo[0]
                if elemento_oroscopo:
                    frammenti_testo = list(elemento_oroscopo.stripped_strings)
                    if frammenti_testo:
                        oroscopo_testo = f"{frammenti_testo[0]} {frammenti_testo[1]} {frammenti_testo[2]}"

                    else:
                        oroscopo_testo = "Impossibile trovare il testo dell'oroscopo."

            else:
                oroscopo_testo = f"Errore di connessione (Codice: {risposta.status_code})."
        except Exception as e:
                oroscopo_testo = f"Errore di rete: {str(e)}"
    return oroscopo_testo

def recupera_oroscopo_internazionale(segno_scelto):
    oroscopo_testo = None
    if segno_scelto:
        url = f"https://www.internazionale.it/oroscopo"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x60)'}
        risposta = requests.get(url, headers=headers)
        if risposta.status_code == 200:
            soup = BeautifulSoup(risposta.text, 'html.parser')
            elementi_segni = soup.findAll('div', class_='item_text')
            url_segno = None
            for el in elementi_segni:
                a = el.find("a", href = True)
                if a and segno_scelto.lower() in a["href"]:
                    url_segno = a["href"]

        try:
            url = f"https://www.internazionale.it{url_segno}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x60)'}
            risposta = requests.get(url, headers=headers)
            if risposta.status_code == 200:
                soup = BeautifulSoup(risposta.text, 'html.parser')
                elemento_oroscopo = soup.find('div', class_='item_text')
                if elemento_oroscopo:
                    oroscopo_testo = elemento_oroscopo.get_text(strip=True)
                else:
                    oroscopo_testo = "Impossibile trovare il testo dell'oroscopo."
            else:
                oroscopo_testo = f"Errore di connessione (Codice: {risposta.status_code})."
        except Exception as e:
                oroscopo_testo = f"Errore di rete: {str(e)}"
    return oroscopo_testo

def recupera_oroscopo_ai(segno_scelto):
    oroscopo_testo = None
    if segno_scelto:
        try:
            oroscopo_internazionale = recupera_oroscopo_internazionale(segno_scelto)
            oroscopo_corriere = recupera_oroscopo_corriere(segno_scelto)
            oroscopo_oggi = recupera_oroscopo_oggi(segno_scelto)
            oroscopo_sky = recupera_oroscopo_sky(segno_scelto)
            
            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=settings.NVIDIA_API_KEY
            )

            response = client.chat.completions.create(
                model="meta/llama-3.3-70b-instruct",
                messages=[
                    {"role": "system", "content": "Fai una sintesi ironica degli oroscopi che ti vengono forniti, dammi solo la sintesi e non dirmi Ecco una sintesi ironica degli oroscopi."},
                    {"role": "user", "content": f"Ecco i testi degli oroscopo di oggi da sintetizzare:\n\nInternazionale: {oroscopo_internazionale} \n\nCorriere: {oroscopo_corriere} \n\nOggi: {oroscopo_oggi} \n\nSky: {oroscopo_sky}"}
                ],
                temperature=0.7,
                max_tokens=1024
            )

            oroscopo_testo = response.choices[0].message.content
            print("NVIDIA AI RESPONSE: ", oroscopo_testo)

        except Exception as e:
                oroscopo_testo = f"Errore di elaborazione AI: {str(e)}"
    return oroscopo_testo


@csrf_exempt
def recupera_oroscopo(request):
    if request.method == "POST":
        data = json.loads(request.body)
        provider_scelto = data.get('provider', '').lower()
        segno_scelto = data.get('segno', '').lower()
        oroscopo_testo=None
        if provider_scelto == "internazionale":
            oroscopo_testo = recupera_oroscopo_internazionale(segno_scelto)
        elif provider_scelto == "sky":
            oroscopo_testo = recupera_oroscopo_sky(segno_scelto)
        elif provider_scelto == "oggi":
            oroscopo_testo = recupera_oroscopo_oggi(segno_scelto)
        elif provider_scelto == "corriere":
            oroscopo_testo = recupera_oroscopo_corriere(segno_scelto)
        elif provider_scelto == "ai":
            oroscopo_testo = recupera_oroscopo_ai(segno_scelto)
        
        return JsonResponse({'oroscopo': oroscopo_testo, 'segno': segno_scelto, 'provider': provider_scelto})
        
    return redirect('oroscopo')