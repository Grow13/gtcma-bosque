import requests

def alma_32(autor):
    nombre_busqueda = autor.replace('.', '').replace(' ', '+')
    url = f"https://openlibrary.org/search/authors.json?q={nombre_busqueda}"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if not data.get('docs'):
            return f"{autor} (no encontrado)"
        a = data['docs'][0]
        nombre = a.get('name', autor)
        nacimiento = a.get('birth_date', '')
        if nacimiento:
            return f"{nombre} ({nacimiento})"
        return nombre
    except Exception as e:
        return autor
