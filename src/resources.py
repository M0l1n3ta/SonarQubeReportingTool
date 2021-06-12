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

def span_number_format(number):
    return "{:,}".format(number).replace(",", "@").replace(".", ",").replace("@", ".")
