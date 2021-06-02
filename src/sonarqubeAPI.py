#=================================================================
#======== Clase que controla el acceso al API Sonarqube ==========
#=================================================================
#
#################################################################
# Software created by: Sogeti
# Contact: emilio-jose.roldan-navarro@sogeti.com
#################################################################
#

import requests
import sys
import resources
from requests.exceptions import HTTPError
import re

class SonarQubeBaseAPI(object) :

    def __init__(self) :
        self.user = resources.user
        self.psw = resources.pswd
        self.url = resources.url_base
        self.headers = resources.headers
        self.test_connection()
        self.version = '7.9'

    def get_SonarQubeVersion(self):
        try :
            response = requests.get(self.url + "api/server/version", auth=(self.user, self.psw))
            text =response.text
            p = re.compile('(\d\.\d).*')
            return p.match(text).group(1)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')

    def test_connection(self) :
        try :
            response = requests.get(self.url + "api/authentication/validate", headers=self.headers, auth=(self.user, self.psw))
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}') 
            sys.exit() 
        except Exception as e :
            print("Server unreacheable. Check provided URL: " + self.url)
            sys.exit()

    def get_organizations(self) :
        response = requests.get(self.url + "api/organizations/search", headers=self.headers, auth=(self.user, self.psw))
        o = list()
        try :
            organizations = response.json()
            for org in organizations['organizations']:
                o.append((org["name"], org["key"]))
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  
        except Exception as ex :
            print(ex)
        finally:
            return o

    def get_projects(self, org) :
        response = requests.get(self.url + "api/projects/search", headers=self.headers, auth=(self.user, self.psw), params={"organization": org})
        p = list()
        try :
            projects = response.json()
            for project in projects["components"]:
                p.append((project["name"], project))
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}') 
        except Exception as ex :
            print(ex)
        finally:
            return p

    def get_loc(self, project) :
        response = requests.get(self.url + "api/measures/component", headers=self.headers, auth=(self.user, self.psw), params={"component": project, "metricKeys": "ncloc"})
        return response.json()["component"]["measures"][0]["value"]

    def get_loc_lang_metrics(self, project, ncloc) :
        response = requests.get(self.url + "api/measures/component", headers=self.headers, auth=(self.user, self.psw), params={"component": project, "metricKeys": "ncloc_language_distribution"})
        languages = response.json()["component"]["measures"][0]["value"].split(";")
        m = list()
        for language in languages :
            s = language.split("=")
            dividendo = float(s[1])
            divisor = float(ncloc)
            percent = round(float(dividendo/divisor)*100, 2)
            if s[0] in resources.Valor_languages.keys():
                m.append((resources.Valor_languages[s[0]], resources.span_number_format(float(percent)), (s[0] if s[0] not in resources.clave_lenguajes else resources.clave_lenguajes[s[0]]) , resources.span_number_format(int(s[1]))))
        return m

    def get_issues(self, lang, project) :
        issues = list()
        i = 1
        for language in lang :
            print(round(float(i / len(language)), 3) * 100, "%", language[0],"     \r")
            response = requests.get(self.url + "api/issues/search", headers=self.headers, auth=(self.user, self.psw), params={"projects": project, "statuses": "OPEN,REOPENED,TO_REVIEW", "languages":language[3], "ps":500})
            total= int(response.json()["total"])
            limit = len(response.json()["issues"])
            if total >= 500:
                p=2
                issues.append((language[0], response.json()["issues"]))
                length = len(response.json()["issues"])
                while length >= 500 and limit < 10000: #Limite global de sonar para recuperar valores
                    limit+= length
                    response = requests.get(self.url + "api/issues/search", headers=self.headers, auth=(self.user, self.psw), params={"projects": project, "statuses": "OPEN,REOPENED,TO_REVIEW", "languages":language[3],"ps":500, "p": p})
                    length = len(response.json()["issues"])
                    issues.append((language[0], response.json()["issues"]))
                    p += 1
            else:
                issues.append((language[0], response.json()["issues"]))
        return issues

    def get_issues_number(self, project) :
        response = requests.get(self.url + "api/issues/search", headers=self.headers, auth=(self.user, self.psw), params={"projects": project, "statuses": "OPEN,REOPENED,TO_REVIEW"})
        return response.json()["total"]

    def get_issues_on_type(self, type, project) :
        response = requests.get(self.url + "api/issues/search", headers=self.headers, auth=(self.user, self.psw), params={"projects": project, "statuses": "OPEN,REOPENED,TO_REVIEW", "types": type})
        return response.json()["total"]

    def get_issues_on_type_and_language(self, type, project, lang):
        response = requests.get(self.url + "api/issues/search", headers=self.headers, auth=(self.user, self.psw), params={"projects": project, "statuses": "OPEN,REOPENED,TO_REVIEW", "types": type, "languages": lang})
        return response.json()["total"]

    def get_issues_on_severity(self, project, severity):
        list = {}
        for type in ["VULNERABILITY,SECURITY_HOTSPOT", "BUG", "CODE_SMELL"]:
            response = requests.get(self.url+ "api/issues/search", headers=self.headers, auth=(self.user, self.psw), params={"componentKeys": project, "resolved": "false", "severities": severity, "types": type})
            list[type] = response.json()["total"]
        return list

    def get_qprofiles_on_project(self, project):
        response = requests.get(self.url + "api/navigation/component", headers=self.headers, auth=(self.user, self.psw), params={"component": project})
        return response.json()["qualityProfiles"]

    def get_duplicated_blocks(self, project) :
        response = requests.get(self.url + "api/measures/component", headers=self.headers, auth=(self.user, self.psw), params={"component": project, "metricKeys": "duplicated_blocks"})
        return response.json()["component"]["measures"][0]["value"]

    def get_duplicated_density(self, project) :
        response = requests.get(self.url + "api/measures/component", headers=self.headers, auth=(self.user, self.psw), params={"component": project, "metricKeys": "duplicated_lines_density"})
        return response.json()["component"]["measures"][0]["value"]

    def get_violations(self, lang, type, project) : #podriamos devolver un codigo de error en caso de que hubiese problemas en vez de un array vacio
        try :
            r = list()
            sum = 0
            for language in lang :
                reglas = list()
                response = requests.get(self.url + "api/issues/search", headers=self.headers, auth=(self.user, self.psw), params={"projectKeys": project, "facets": "rules", "types": type, "languages": language[2], "statuses": "OPEN,TO_REVIEW,REOPENED"})
                rules = response.json()["facets"][0]["values"]
                if len(rules) > 0 :
                    for i in range(len(rules)):
                        wget = requests.get(self.url + "api/rules/show", headers=self.headers, auth=(self.user, self.psw), params={"key": rules[i]["val"]})
                        rule_name = wget.json()["rule"]["name"].replace('<','').replace('>','')
                        reglas.append((rule_name, resources.span_number_format(int(rules[i]["count"]))))
                        print(round(float(i)/float(len(rules)), 3)*100, "%", language[0], "   \r")
                    sum += int(response.json()["total"])
                    r.append((language[0], reglas))
            total = (type, resources.span_number_format(int(sum)), r)
            return total
        except :
            return list()
            
    def get_hotspots(self,project):
            return list()

    def get_rules_violated_on_bug_severity(self, project, severity, language):
        response = requests.get(self.url + "api/issues/search", headers=self.headers, auth=(self.user, self.psw), params={"componentKeys": project, "resolved": "false","types": "BUG", "severities": severity, "languages": language, "facets": "rules", "additionalFields": "_all"})
        return response.json()["rules"]

    def get_num_violations_by_lang(self, project, lang):
        sum = 0
        for type in ("VULNERABILITY,SECURITY_HOTSPOT", "BUG", "CODE_SMELL"):
            response = requests.get(self.url + "api/issues/search", headers=self.headers, auth=(self.user, self.psw), params={"projectKeys": project, "facets": "rules", "types": type, "languages": lang, "statuses": "OPEN,TO_REVIEW,REOPENED"})
            sum += len(response.json()["facets"][0]["values"])
        return sum

    def get_num_rules_by_qprofile(self, qprofile):
        response = requests.get(self.url + "api/rules/search", headers=self.headers, auth=(self.user, self.psw), params={"activation": "true", "qprofile": qprofile})
        return response.json()["total"]

    def get_qprofile_key_by_lang(self, project, lang):
        response = requests.get(self.url + "api/qualityprofiles/search", headers=self.headers, auth=(self.user, self.psw), params={"project": project, "language": lang})
        try :
            qprofile_key = response.json()["profiles"][0]["key"]
            return qprofile_key
        except :
            return None

    def get_languages(self):
        response = requests.get(self.url + "api/languages/list", headers=self.headers, auth=(self.user, self.psw))
        try:
            return response.json()["languages"]
        except:
            return list()

    def get_rules_by_lang(self, lang) :
        response = requests.get(self.url + "api/rules/search", headers=self.headers, auth=(self.user, self.psw), params={"languages": lang, "ps": "500"})
        try:
            return response.json()["rules"]
        except:
            return list()

    def get_project_analyses_issues(self, project) :
        response = requests.get(self.url + "api/measures/search_history", headers=self.headers, auth=(self.user, self.psw), params={"component": project, "metrics": "vulnerabilities,code_smells,bugs", "ps": "1000"})
        try:
            return response.json()["measures"]
        except:
            return list()

    def get_project_analyses_duplicity(self, project):
        response = requests.get(self.url + "api/measures/search_history", headers=self.headers, auth=(self.user, self.psw), params={"component": project, "metrics": "duplicated_blocks,duplicated_lines_density", "ps": "1000"})
        try:
            return response.json()["measures"]
        except:
            return list()
