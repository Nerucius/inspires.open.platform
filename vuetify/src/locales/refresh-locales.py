import requests
import codecs

distribution_hash = 'ba4e62c50bcec6bd1f09e98rgre'

locales = [
    (f"https://distributions.crowdin.net/{distribution_hash}/content/ar/strings.json", "ar.json"),
    (f"https://distributions.crowdin.net/{distribution_hash}/content/ca/strings.json", "ca.json"),
    (f"https://distributions.crowdin.net/{distribution_hash}/content/es-ES/strings.json", "es.json"),
    (f"https://distributions.crowdin.net/{distribution_hash}/content/fr/strings.json", "fr.json"),
    (f"https://distributions.crowdin.net/{distribution_hash}/content/hu/strings.json", "hu.json"),
    (f"https://distributions.crowdin.net/{distribution_hash}/content/it/strings.json", "it.json"),
    (f"https://distributions.crowdin.net/{distribution_hash}/content/nl/strings.json", "nl.json"),
    (f"https://distributions.crowdin.net/{distribution_hash}/content/pt-PT/strings.json", "pt.json"),
]

for url, filename in locales:
    tl_strings = requests.get(url).content.decode('utf-8')
    codecs.open(filename, 'w', 'utf-8').write(tl_strings)
