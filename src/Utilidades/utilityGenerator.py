# -*- coding: utf-8 -*-
#
#################################################################
# Software created by: Josue Pradas Sacristan for Sogeti
# Contact: josue.pradas-sacristan@sogeti.com
#################################################################
#

import xlsxwriter
import resources
import os
from sys import platform

def get_platform():
    if platform == "cygwin" or platform == "linux" or platform == "linux2":
        system = "linux"
    else:
        system = "win"
    return system

def generate_HTML_violated_rules_by_lang(sqc, project):
    ncloc = sqc.get_loc(project)
    languages = sqc.get_loc_lang_metrics(project, ncloc)
    violations = []
    print("> Retrieving violated rules...")
    print("        -> BUGS")
    violations.append(sqc.get_violations(languages, "BUG", project))
    print("        -> VULNERABILITIES")
    violations.append(sqc.get_violations(languages, "VULNERABILITY,SECURITY_HOTSPOT", project))
    print("        -> CODE SMELL")
    violations.append(sqc.get_violations(languages, "CODE_SMELL", project))

    fout = open('html_rules_report_'+ project +'.html','w')

    fout.write("<!doctype html>")
    fout.write('<html lang="en">')
    fout.write("<head>")
    fout.write('<meta charset="utf-8">')
    fout.write('<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
    fout.write('<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">')
    fout.write("<title>Sonarqube violated rules - " + project + "</title>")
    fout.write("</head>")
    fout.write("<body>")
    fout.write('<h2>Sonarqube violated rules: <small class="text-muted">' + project + '</small></h2>')
    fout.write('<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>')
    fout.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>')
    fout.write('<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>')

    fout.write("</body>")
    fout.write("</html>")

    fout.close()

def generate_excel_violated_rules_by_lang(sqc, project):
    workbook = xlsxwriter.Workbook(project + '_violated_rules.xlsx')
    worksheet = workbook.add_worksheet(project + "_violated_rules")
    fp_worksheet = workbook.add_worksheet(project + "_falsePositives")
    bold = workbook.add_format({'bold': 1})
    gray_background = workbook.add_format()
    gray_background.set_bg_color('gray')
    gray_background.set_font_color('white')
    light_bg = workbook.add_format()
    light_bg.set_bg_color('#B5BEBF')
    light_bg.set_bold()

    ncloc = sqc.get_loc(project)
    languages = sqc.get_loc_lang_metrics(project, ncloc)
    violations = []
    print("> Retrieving violated rules...")
    print("        -> BUGS")
    violations.append(sqc.get_violations(languages, "BUG", project))
    if sqc.version == '7.9':
        print("        -> VULNERABILITIES,SECURITY_HOTSPOT")
        violations.append(sqc.get_violations(languages, "VULNERABILITY", project))
    else:
        print("        -> VULNERABILITIES")
        violations.append(sqc.get_violations(languages, "VULNERABILITY", project))
        print("        -> HOTSPOTS")
        violations.append(sqc.get_hotspots(project))
    print("        -> CODE SMELL")
    violations.append(sqc.get_violations(languages, "CODE_SMELL", project))
    issues = sqc.get_issues(languages, project)

    i = 1
    j = 1
    for type in violations:
        worksheet.write('A'+str(i), type[0], light_bg)
        worksheet.write('B'+str(i), "", light_bg)
        worksheet.write('C'+str(i), "", light_bg)
        i += 1

        worksheet.write('A'+str(i), "Lenguaje", gray_background)
        worksheet.write('B'+str(i), "Regla", gray_background)
        worksheet.write('C'+str(i), "Problemas", gray_background)
        i += 1

        row = []
        rowtwo = []

        for lang in type[2]:
            for rule in lang[1]:
                row = [lang[0], rule[0], rule[1]]
                worksheet.write_row('A'+str(i), row)
                i += 1
        row = ["TOTAL", "", type[1]]
        worksheet.write_row('A'+str(i),row)
        i += 2

    fp_worksheet.write('A'+str(j), "Lenguaje", gray_background)
    fp_worksheet.write('B'+str(j), "Regla", gray_background)
    fp_worksheet.write('C'+str(j), "Tipo", gray_background)
    fp_worksheet.write('D'+str(j), "Ruta fichero", gray_background)
    fp_worksheet.write('E'+str(j), "Falso positivo", gray_background)
    j += 1

    for issue in issues :
        row = []
        try:
            line = iss['line']
        except: 
            line = ""
        for iss in issue[1] :
            row = [issue[0], iss['message'], iss['type'], iss['component'].split(":")[1] + (":"+str(iss['line']) if 'line' in iss else "")]
            fp_worksheet.write_row('A'+str(j), row)
            j += 1

    workbook.close()
    print("")
    print("> " + project + "_violated_rules.xlsx saved!")
    input("Press enter to continue...")


def generate_excel_by_lang(language, sqc):
    workbook = xlsxwriter.Workbook(language + '_rules.xlsx')
    worksheet = workbook.add_worksheet("Sonarqube rules " + resources.languages[language])
    bold = workbook.add_format({'bold': 1})

    rules = sqc.get_rules_by_lang(language)
    if len(rules) == 0 :
        return 1

    header = ["name", "level", "url", "key", "repo", "createdAt", "htmlDesc", "mdDesc", "severity", "status", "isTemplate", "tags", "sysTags", \
    "lang", "langName", "params", "defaultDebtRemFnType", "defaultDebtRemFnCoeff", "effortToFixDescription", "debtOverloaded", "debtRemFnType", \
    "debtRemFnCoeff", "defaultRemFnType", "defaultRemFnGapMultiplier", "remFnType", "remFnGapMultiplier", "remFnOverloaded", "gapDescription", "scope", "type"]

    worksheet.write_row('A1', header)

    barra = 1
    for i in range(len(rules)):
        offset = i + 2
        params = ""
        for x in range(len(rules[i]["params"])):
            params = params + rules[i]["params"][x]["key"] + ","
        row = [rules[i]["name"], \
        #level
        "",\
        "http://srv-analiza/sonar/coding_rules?open="+rules[i]["key"]+"&q="+rules[i]["key"],\
        rules[i]["key"],\
        rules[i]["repo"],\
        rules[i]["createdAt"],\
        rules[i]["htmlDesc"],\
        rules[i]["mdDesc"], \
        rules[i]["severity"],\
        rules[i]["status"],\
        rules[i]["isTemplate"],\
        ",".join(rules[i]["tags"]), \
        ",".join(rules[i]["sysTags"]), \
        rules[i]["lang"],\
        rules[i]["langName"],\
        params, \
        get_rule(rules[i], "defaultDebtRemFnType"),\
        get_rule(rules[i],"defaultDebtRemFnCoeff"),\
        get_rule(rules[i],"effortToFixDescription"),\
        get_rule(rules[i],"debtOverloaded"),\
        get_rule(rules[i],"debtRemFnType"),\
        get_rule(rules[i],"debtRemFnCoeff"),\
        get_rule(rules[i],"defaultRemFnType"),\
        get_rule(rules[i],"defaultRemFnGapMultiplier"),\
        get_rule(rules[i],"remFnType"),\
        get_rule(rules[i],"remFnGapMultiplier"),\
        get_rule(rules[i],"remFnOverloaded"),\
        get_rule(rules[i],"gapDescription"),\
        rules[i]["scope"], \
        rules[i]["type"]]

        worksheet.write_row("A"+ str(offset), row)

        os.system('cls') if get_platform()=="win" else os.system('clear')
        print(" ")
        print("> Writing Excel file (" + str(round(float(i)/float(len(rules)), 3) * 100) + "%) " + barra_next(barra))
        if barra < 4:
            barra += 1
        else:
            barra = 1

    os.system('cls') if get_platform()=="win" else os.system('clear')
    workbook.close()
    return 0

def generate_html_by_lang(language, sqc):
    # TODO
    rules = sqc.get_rules_by_lang(language)
    if len(rules) == 0 :
        return 1

    fout = open('html_rules_report_'+ language +'.html','w')

    fout.write("<!doctype html>")
    fout.write('<html lang="en">')
    fout.write("<head>")
    fout.write('<meta charset="utf-8">')
    fout.write('<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
    fout.write('<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">')
    fout.write("<title>Sonarqube rules " + resources.languages[language] + "</title>")
    fout.write("</head>")
    fout.write("<body>")
    fout.write('<h2>Sonarqube rules: <small class="text-muted">' + resources.languages[language] + '</small></h2>')
    fout.write('<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>')
    fout.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>')
    fout.write('<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>')
    fout.write('<table class="table table-striped">')
    fout.write('<thead>')
    fout.write('<tr>')
    fout.write('<th scope="col">#</th>')
    fout.write('<th scope="col">name</th>')
    fout.write('<th scope="col">level</th>')
    fout.write('<th scope="col">key</th>')
    fout.write('<th scope="col">repo</th>')
    fout.write('<th scope="col">createdAt</th>')
    fout.write('<th scope="col">htmlDesc</th>')
    fout.write('<th scope="col">severity</th>')
    fout.write('<th scope="col">status</th>')
    fout.write('<th scope="col">isTemplate</th>')
    fout.write('<th scope="col">tags</th>')
    fout.write('<th scope="col">sysTags</th>')
    fout.write('<th scope="col">lang</th>')
    fout.write('<th scope="col">langName</th>')
    fout.write('<th scope="col">params</th>')
    fout.write('<th scope="col">defaultDebtRemFnType</th>')
    fout.write('<th scope="col">defaultDebtRemFnCoeff</th>')
    fout.write('<th scope="col">effortToFixDescription</th>')
    fout.write('<th scope="col">debtOverloaded</th>')
    fout.write('<th scope="col">debtRemFnType</th>')
    fout.write('<th scope="col">debtRemFnCoeff</th>')
    fout.write('<th scope="col">defaultRemFnType</th>')
    fout.write('<th scope="col">defaultRemFnGapMultiplier</th>')
    fout.write('<th scope="col">remFnType</th>')
    fout.write('<th scope="col">remFnGapMultiplier</th>')
    fout.write('<th scope="col">remFnOverloaded</th>')
    fout.write('<th scope="col">gapDescription</th>')
    fout.write('<th scope="col">scope</th>')
    fout.write('<th scope="col">type</th>')
    fout.write('</tr>')
    fout.write('</thead>')
    fout.write('<tbody>')

    for i in range(len(rules)) :
        params = ""
        for x in range(len(rules[i]["params"])):
            params = params + rules[i]["params"][x]["key"] + ","
        fout.write('<tr>')
        fout.write('<th scope="row">'+ str(i) +'</th>')
        fout.write('<td>'+ rules[i]["name"] +'</td>')
        fout.write('<td> </td>')
        fout.write('<td><a href=http://srv-analiza/sonar/coding_rules?open='+rules[i]["key"]+'&q='+rules[i]["key"] +'>'+rules[i]["key"]+'</a></td>')
        fout.write('<td>'+ rules[i]["repo"] +'</td>')
        fout.write('<td>'+ rules[i]["createdAt"] +'</td>')
        fout.write('<td>'+ rules[i]["htmlDesc"].encode('utf-8').strip() +'</td>')
        fout.write('<td>'+ rules[i]["severity"] +'</td>')
        fout.write('<td>'+ rules[i]["status"] +'</td>')
        fout.write('<td>'+ str(rules[i]["isTemplate"]) +'</td>')
        fout.write('<td>'+ ",".join(rules[i]["tags"]) +'</td>')
        fout.write('<td>'+ ",".join(rules[i]["sysTags"]) +'</td>')
        fout.write('<td>'+ rules[i]["lang"] +'</td>')
        fout.write('<td>'+ rules[i]["langName"] +'</td>')
        fout.write('<td>'+ params +'</td>')
        fout.write('<td>'+ str(get_rule(rules[i], "defaultDebtRemFnType")) +'</td>')
        fout.write('<td>'+ str(get_rule(rules[i], "defaultDebtRemFnCoeff")) +'</td>')
        fout.write('<td>'+ str(get_rule(rules[i], "effortToFixDescription")) +'</td>')
        fout.write('<td>'+ str(get_rule(rules[i], "debtOverloaded")) +'</td>')
        fout.write('<td>'+ str(get_rule(rules[i], "debtRemFnType")) +'</td>')
        fout.write('<td>'+ str(get_rule(rules[i], "debtRemFnCoeff")) +'</td>')
        fout.write('<td>'+ str(get_rule(rules[i], "defaultRemFnType")) +'</td>')
        fout.write('<td>'+ str(get_rule(rules[i], "defaultRemFnGapMultiplier")) +'</td>')
        fout.write('<td>'+ str(get_rule(rules[i], "remFnType")) +'</td>')
        fout.write('<td>'+ str(get_rule(rules[i], "remFnGapMultiplier")) +'</td>')
        fout.write('<td>'+ str(get_rule(rules[i], "remFnOverloaded")) +'</td>')
        fout.write('<td>'+ str(get_rule(rules[i], "gapDescription")) +'</td>')
        fout.write('<td>'+ rules[i]["scope"] +'</td>')
        fout.write('<td>'+ rules[i]["type"] +'</td>')
        fout.write('</tr>')

    fout.write("</body>")
    fout.write("</html>")

    # fout.write("<!DOCTYPE html>")
    # fout.write("<html>")
    # fout.write("<head>")
    # fout.write("")
    # fout.write("</head>")
    # fout.write("<body>")
    # fout.write("<h1>"+resources.languages[language]+"</h1>")
    # fout.write("<ul>")
    # for i in range(len(rules)):
    #     fout.write("<li><a href=http://srv-analiza/sonar/coding_rules?open="+rules[i]["key"]+"&q="+rules[i]["key"]+">"+rules[i]["name"]+"</a><li>")
    # fout.write("</ul>")
    # fout.write("</body>")
    # fout.write("</html>")

    fout.close()
    return 0

def barra_next(barra):
    if(barra == 1):
        return "|"
    elif(barra == 2):
        return "/"
    elif(barra == 3):
        return "--"
    elif(barra == 4):
        return "\\"

def get_rule(rules, key):
    try:
        return rules[key]
    except:
        return " "
