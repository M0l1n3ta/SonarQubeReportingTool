import requests
import sys

#sys.path.insert(0, '../src')
from sonarqubeAPI import SonarQubeBaseAPI
import sonarqubeAPI_83
import reportGen as report
import utilityGenerator as ugen

sqc = SonarQubeBaseAPI()
list = ['8.2','8.3']

sqc = SonarQubeBaseAPI()
version = sqc.get_SonarQubeVersion()

if version in list:
    sqc = sonarqubeAPI_83.SonarQubeAPI83()

project = 'avm9.vcx'
#sqc.get_hotspots('dwva')
print(f'Numero de errores: ',sqc.get_issues_number(project))

ncloc = sqc.get_loc(project)
languages = sqc.get_loc_lang_metrics(project, ncloc)

issues = sqc.get_issues(languages, project)

for issue in issues :
        row = []
        try:
            line = iss['line']
        except: 
            line = ""
        for iss in issue[1] :
            row = [issue[0], iss['message'], iss['type'], iss['component'].split(":")[1] + ":" + str(line)]
            fp_worksheet.write_row('A'+str(j), row)
            j += 1
#ugen.generate_excel_violated_rules_by_lang(sqc,'dwva')