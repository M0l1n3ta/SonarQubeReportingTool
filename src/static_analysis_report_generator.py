#################################################################
# Contact: EmilioJRoldan@gmail.com
#################################################################
#
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
from sys import platform, path
from pathlib import Path
import requests
path_root = Path(__file__).parent
path.append(str(path_root))
from sonarqubeAPI import SonarQubeBaseAPI
import sonarqubeAPI_83
import reportGen as report
import Utilidades.utilityGenerator as ugen
from art import text2art

list = ['8.2','8.3']
sqc = SonarQubeBaseAPI()
version = sqc.get_SonarQubeVersion()

if version in list:
    sqc = sonarqubeAPI_83.SonarQubeAPI83(version)


def print_heading(text):
    os.system('cls') if get_platform()=="win" else os.system('clear')
    print(text)
    print("===================================================================== ")
    print("")

def get_platform():
    if platform == "cygwin" or platform == "linux" or platform == "linux2":
        system = "linux"
    else:
        system = "win"
    return system

def print_welcome():
    os.system('cls') if get_platform()=="win" else os.system('clear')
    print("  ")
    print(text2art("ESIIAB","colossal"))
    print(text2art('''SonarQube  
    Reporting Tool''', font="small")) 
    print("  ")
    #input("  Press enter to continue...")

def print_actions(project, issues):
    os.system('cls') if get_platform()=="win" else os.system('clear')
    print(" ")
    print(" " + project)
    print("===================================================================== ")
    print(" ")
    print(" Issues:", str(issues))
    print(" ")
    print(" 1.- Generate list of defects (.xlsx).")
    print(" 2.- Generate detailed report (.docx, template required).")
    print(" 3.- Generate executive report (.docx, template required).")
    print(" 4.- Retrieve madurity of application.")
    print(" 5.- Back")
    print(" ")

def print_projects(projects,heading):
    #print len(projects)
    if len(projects) < 1 :
        print("> User with insufficient privileges. Use an Admin account. Exiting.")
        time.sleep(2)
        return True
    print_heading(heading)
    for i in range(len(projects)):
        print(" " + str(i + 1) + ".- " + projects[i][0])
    print(" " + (str(len(projects) + 1)) + ".- Exit")
    print(" ")
    return False

def print_orgs(orgs, heading):
    if len(orgs) < 1 :
        print("> User incorrect. Exiting")
        time.sleep(2)
        return True
    print_heading(heading)
    #print len(projects)
    for i in range(len(orgs)):
        print(" " + str(i + 1) + ".- " + orgs[i][0])
    print(" " + (str(len(orgs) + 1)) + ".- Exit")
    print(" ")
    return False


def print_utility_menu():
    print(" 1.- Language Rules (HTML)")
    print(" 2.- Language Rules (Excel)")
    print(" 3.- Violated rules (HMTL) - still not implemented")
    print(" 4.- Violated rules (Excel)")
    print(" 5.- Back")
    print(" ")

def exit():
    os.system('cls') if get_platform()=="win" else os.system('clear')
    print(" ")
    print("> Exiting Sonarqube reporting tool...")
    heading = ""
    time.sleep(1)
    os.system('cls') if get_platform()=="win" else os.system('clear')

def print_main_menu():
    #os.system('cls') if get_platform()=="win" else os.system('clear')
    print(" 1.- Reporting tool")
    print(" 2.- Utility tool")
    print(" 3.- Exit")
    print("")

def print_languages(languages):
    # print(" "
    for i in range(len(languages)):
        print(" " + str(i + 1) + ".- " + languages[i]["name"])
    print(" " + (str(len(languages) + 1)) + ".- Exit")
    print(" ")

def main():
    print(path)
    print_welcome()
    heading = ""
    while True:
        print_main_menu()
        select_option = input("> Please select an option: ")
        if select_option.isdigit():
            orgs = sqc.get_organizations()
            if int(select_option) == 1 :
                heading = "Reporting tool"
                #if print_orgs(orgs,heading):
                #    break
                #select_org = input("> Please select an organization: ")
                select_org = "1"
                if select_org.isdigit():
                    if(int(select_org) >= 1) & (int(select_org) <= len(orgs)):
                        org = orgs[int(select_org) - 1][1]
                        projects = sqc.get_projects(org)
                        print_projects(projects,heading)
                        select_project = input("> Please select a project: ")
                        if select_project.isdigit():
                            if (int(select_project) >= 1) & (int(select_project) <= len(projects) ):
                                print("> Calculating number of issues...")
                                project = projects[int(select_project) - 1][1]["key"]
                                issues_num = sqc.get_issues_number(project)

                                while True:
                                    print_actions(project, issues_num)
                                    select_report = input("> Please select the report you want: ")
                                    print(" ")

                                    if select_report.isdigit():
                                        if(int(select_report) >= 1) & (int(select_report) <= 5):
                                            filename = orgs[int(select_org)-1][1] + "_" + projects[int(select_project)-1][0] + "_" \
                                            + projects[int(select_project)-1][1]["lastAnalysisDate"][:10] + "_".strip()
                                            if int(select_report) == 1:
                                                project = projects[int(select_project) - 1][1]["key"]
                                                ugen.generate_excel_violated_rules_by_lang(sqc, project)

                                            if int(select_report) == 2 :
                                                filename += "detail"
                                                report.generate_detailed_report(projects[int(select_project)-1], filename, sqc)
                                                print(" ")
                                                print(">", filename + ".docx saved.")
                                                print(" ")
                                                print("> Press enter to continue...")
                                                input()
                                            if int(select_report) == 3 :
                                                filename += "executive"
                                                report.generate_executive_report(projects[int(select_project)-1], filename, sqc)
                                                print("")
                                                print(">", filename + ".docx saved.")
                                                print("") 
                                                print("> Press enter to continue...")
                                                input()
                                            if int(select_report) == 4 :
                                                report.calculate_madurity(projects[int(select_project)-1], sqc)
                                                print("> Press enter to continue...")
                                                input()
                                            if int(select_report) == 5 :
                                                break

                            else :
                                exit()
                                break
                    else :
                        exit()
                        break
            elif int(select_option) == 2 :
                heading = "Utility tool"
                while True:
                    print_heading(heading)
                    print_utility_menu()
                    select_format = input("> Select option: ")
                    if select_format.isdigit() :
                        if int(select_format) == 1:
                            heading += " > Languaje rules (HTML)"
                            lenguajes = sqc.get_languages()
                            print_heading(heading)
                            print_languages(lenguajes)
                            select_language = input("> Select language: ")
                            if select_language.isdigit():
                                if(int(select_language) >= 1) & (int(select_language) <= len(lenguajes)):
                                    lang_key = lenguajes[int(select_language) - 1]["key"]
                                    ret = ugen.generate_html_by_lang(lang_key, sqc)
                                    if ret == 0:
                                        print("HTML made!")
                                        input("Press enter to continue...")
                                else:
                                    heading = "Utility tool"

                        elif int(select_format) == 2:
                            heading += " > Languaje rules (Excel)"
                            lenguajes = sqc.get_languages()
                            print_heading(heading)
                            print_languages(lenguajes)
                            select_language = input("> Select language: ")
                            if select_language.isdigit():
                                if(int(select_language) >= 1) & (int(select_language) <= len(lenguajes)):
                                    lang_key = lenguajes[int(select_language) - 1]["key"]
                                    ret = ugen.generate_excel_by_lang(lang_key, sqc)
                                    if int(ret) == 1:
                                        print("Something went wrong...")
                                        time.sleep(1)
                                        break
                                    print("> Excel saved!")
                                    input("Press enter to continue...")
                                else:
                                    heading = "Utility tool"

                        elif int(select_format) == 3:
                            heading += " > Violated rules (Excel)"
                            print_heading(heading)
                            print_orgs()
                            select_org = input("> Please select an organization: ")
                            if select_org.isdigit():
                                if(int(select_org) >= 1) & (int(select_org) <= len(orgs)):
                                    org = orgs[int(select_org) - 1][1]
                                    projects = sqc.get_projects(org)
                                    if len(projects) < 1 :
                                        print("> User with insufficient privileges. Use an Admin account. Exiting.")
                                        time.sleep(2)
                                        break

                                    print_heading(heading)
                                    print_projects(projects)
                                    select_project = input("> Please select a project: ")
                                    if select_project.isdigit():
                                        if (int(select_project) >= 1) & (int(select_project) <= len(projects)):
                                            project = projects[int(select_project) - 1][1]["key"]

                                            heading = "Utility tool"
                                        else:
                                            exit()
                                            break
                                else:
                                    heading = "Utility tool"
                        elif int(select_format) == 5:
                            break

            elif int(select_option) == 3 :
                exit()
                break
main()
