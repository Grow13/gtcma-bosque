import requests
import traceback

def alma_31(autor):
    url = f"https://openlibrary.org/search/authors.json?q={autor.replace(' ', '%20')}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return f"{autor}: HTTP {r.status_code}"
        data = r.json()
        if not data.get('docs'):
            return f"{autor}: No encontrado"
        a = data['docs'][0]
        nombre = a.get('name', autor)
        nacimiento = a.get('birth_date', 'Desconocida')
        obras = a.get('work_count', 0)
        promedio = a.get('ratings_average', 0)
        top = a.get('top_work', 'Desconocida')
        return f"{nombre} ({nacimiento}) - {obras} obras, ⭐{promedio:.2f}. Obra destacada: {top}"
    except Exception as e:
        # Devolver el error real para depurar
        return f"{autor}: Error - {str(e)}"
