# ======================================================================
# ===== archivo que guarda los recursos necesarios para el programa ====
# ======================================================================

url_base = "http://localhost:9000/"
user = 'admin'
pswd = 'admin'
headers = {"Accept": "application/json"}

Valor_languages = {
    "py": "Python",
    "js": "JavaScript",
    "xml": "XML",
    "cs": "C#",
    "css": "CSS",
    "flex": "Flex",
    "go": "Go",
    "java": "Java",
    "kotlin": "Kotlin",
    "php": "PHP",
    "ts": "TypeScript",
    "web": "HTML",
    "plsqlopen": "PLSQL",
    "vbnet": "Visual Basic .NET",
    "jsp":"JSP",
    "plsqlopen":"PL/SQL",
    "ruby":"Ruby"
}

clave_lenguajes={
    'jsp':'web'
}

meses = {
    "1": "ene",
    "2": "feb",
    "3": "mar",
    "4": "abr",
    "5": "may",
    "6": "jun",
    "7": "jul",
    "8": "ago",
    "9": "sep",
    "10": "oct",
    "11": "nov",
    "12": "dic",
    "1c": "enero",
    "2c": "febrero",
    "3c": "marzo",
    "4c": "abril",
    "5c": "mayo",
    "6c": "junio",
    "7c": "julio",
    "8c": "agosto",
    "9c": "septiembre",
    "10c": "octubre",
    "11c": "noviembre",
    "12c": "diciembre",

}

def span_number_format(number):
    return "{:,}".format(number).replace(",", "@").replace(".", ",").replace("@", ".")
