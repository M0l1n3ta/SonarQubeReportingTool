#=================================================================
#======== Clase que controla el acceso al API Sonarqube ==========
#=================================================================
#
#################################################################
# Contact: emilio-jose.roldan-navarro@sogeti.com
#################################################################
#

import requests
import sys
from sonarqubeAPI import SonarQubeBaseAPI
import resources
from requests.exceptions import HTTPError

class hotspotItem:  
    def __init__(self, name, message,count):  
        self.securityCategory = name  
        self.message = message
        self.count = count

    def add_count(lista, securityCategory):
        for item in lista:
            if item.securityCategory== securityCategory:
                item.count += 1
                return True
        return False

    def __str__(self):
        return self.securityCategory 

    def __eq__(self, other):
        return other == self.securityCategory

class SonarQubeAPI83(SonarQubeBaseAPI) :

    def __init__(self,version):
        SonarQubeBaseAPI.__init__(self)
        self.version = version

    def get_issues_number(self, project) :
        response = requests.get(self.url + "api/issues/search", headers=self.headers, auth=(self.user, self.psw), params={"projects": project, "statuses": "OPEN,REOPENED,CONFIRMED", "types": "BUG,VULNERABILITY,CODE_SMELL"})
        num_issues = int(response.json()["total"])
        
        return num_issues + self.get_hot_spot_number(project)

    def get_hot_spot_number(self,project) :
        response = requests.get(self.url + "api/hotspots/search", headers=self.headers, auth=(self.user, self.psw), params={"projectKey": project})
        num_hotspots = int(response.json()['paging']['total'])
        return num_hotspots

    def get_violations(self, lang, type, project) : 
        try :
            r = list()
            sum = 0
            for language in lang :
                reglas = list()
                response = requests.get(self.url + "api/issues/search", headers=self.headers, auth=(self.user, self.psw), params={"projectKeys": project, "facets": "rules", "types": type, "languages": language[3], "statuses": "OPEN,CONFIRMED,REOPENED"})
                sum += int(response.json()["total"])
                rules = response.json()["facets"][0]["values"]

                if len(rules) > 0 :
                    for i in range(len(rules)):
                        wget = requests.get(self.url + "api/rules/show", headers=self.headers, auth=(self.user, self.psw), params={"key": rules[i]["val"]})
                        rule_name = wget.json()["rule"]["name"].replace('<','').replace('>','')
                        reglas.append((rule_name, resources.span_number_format(int(rules[i]["count"]))))
                        print(round(float(i)/float(len(rules)), 3)*100, "%", language[0], "   \r")
                    
                    r.append((language[0], reglas))
            total = (type, resources.span_number_format(int(sum)), r)
            return total
        except Exception as e:
            print(e)
            return list()

    def get_hotspots(self,project):
        try :
            r = list()
            sum = 0
            p =1 
            reglas = list()
            while True:
                response = requests.get(self.url + "api/hotspots/search", headers=self.headers, auth=(self.user, self.psw), params={"projectKey": project,"p":p,"ps":100})
                sum = int(response.json()["paging"]["total"])   
                hotspot_list = response.json()["hotspots"]
                
                for item in hotspot_list:
                    if not item["securityCategory"] in reglas:
                        reglas.append(hotspotItem(item["securityCategory"],item["message"], 1))
                    else:
                        hotspotItem.add_count(reglas,item["securityCategory"]) 

                if len(hotspot_list) < 100:
                    break
                else:
                    p +=1
            for item in reglas:
                r.append((item.securityCategory,[(item.message,item.count)]))
            total = ("HOTSPOT", resources.span_number_format(int(sum)), r)
            return total
        except Exception as e:
            print(e)
            return list()


    def get_issues(self, lang, project) :
            issues = list()
            i = 1
            for language in lang :
                print(round(float(i / len(language)), 3) * 100, "%", language[0],"     \r")
                response = requests.get(self.url + "api/issues/search", headers=self.headers, auth=(self.user, self.psw), params={"projects": project, "statuses": "OPEN,REOPENED", "languages":language[3],"ps":500})
                total = int(response.json()["total"])
                limit = len(response.json()["issues"])
                if total >= 500:
                    p=2
                    issues.append((language[0], response.json()["issues"]))
                    length = len(response.json()["issues"])
                    while length >= 500 and limit < 10000: #Limite global de sonar para recuperar valores
                        limit+= length
                        response = requests.get(self.url + "api/issues/search", headers=self.headers, auth=(self.user, self.psw), params={"projects": project, "statuses": "OPEN,REOPENED", "languages":language[3],"ps":500, "p": p})
                        length = len(response.json()["issues"])
                        issues.append((language[0], response.json()["issues"]))
                        p += 1
                else:
                    issues.append((language[0], response.json()["issues"]))
            return issues


    def get_issues_on_type(self, type, project) :
        response = requests.get(self.url + "api/issues/search", headers=self.headers, auth=(self.user, self.psw), params={"projects": project, "statuses": "OPEN,REOPENED", "types": type})
        return response.json()["total"]
    

    def get_issues_on_type_and_language(self, type, project, lang):
        response = requests.get(self.url + "api/issues/search", headers=self.headers, auth=(self.user, self.psw), params={"projects": project, "statuses": "OPEN,REOPENED", "types": type, "languages": lang})
        return response.json()["total"]

    def get_num_violations_by_lang(self, project, lang):
        sum = 0
        for type in ("VULNERABILITY", "BUG", "CODE_SMELL"):
            response = requests.get(self.url + "api/issues/search", headers=self.headers, auth=(self.user, self.psw), params={"projectKeys": project, "facets": "rules", "types": type, "languages": lang, "statuses": "OPEN,REOPENED"})
            sum += len(response.json()["facets"][0]["values"])
        return sum