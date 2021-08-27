import random
import requests
from PIL import *
import os
from multiprocessing.dummy import Pool as ThreadPool
import PySimpleGUI as sg
from PIL import Image
import csv
from functools import partial

sg.theme('DarkTeal6') #SimplePyGUI theme
global locale
locale = "hu_HU" #alap locale, language_region formattal
squareurl = "https://cdn.communitydragon.org/latest/champion/champion_name/square" #Champképek urlje communitydragonról
abilityurl = "https://cdn.communitydragon.org/latest/champion/champion_name/ability-icon/" #Abilityképek urlje communitydragonról
workingdir = os.getenv('APPDATA')+"\\Spellfinder\\" #képek helye
abilityletters = ["p","q","w","e","r"] #elfogadható ability keyek (kisbetű, passzívval együtt)
pool = ThreadPool(os.cpu_count()) #thread
title = "Spellfinder" #GUI title
global pontok
pontok = 0
champability = ""
champ = random.randbytes(5)
randomspell = ""
latest = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
global ver
ver = latest.json()[0]
global champlist
champlist = list()
languagelist = ["en_US","hu_HU"]

def beautify(ugly): #Formázza a champneveket ahol különleges (és Wukongnál)
    return { 
        "Aurelion Sol":"aurelionsol",
        "Cho'Gath":"chogath",
        "Dr. Mundo":"drmundo",
        "Jarvan IV":"jarvaniv",
        "Kai'Sa":"kaisa",
        "Kha'Zix":"khazix",
        "Kog'Maw":"kogmaw",
        "Lee Sin":"leesin",
        "Master Yi":"masteryi",
        "Miss Fortune":"missfortune",
        "Nunu & Willump":"nunu",
        "Rek'Sai":"reksai",
        "Tahm Kench":"tahmkench",
        "Twisted Fate":"twistedfate",
        "Vel'Koz":"velkoz",
        "Wukong":"monkeyking",
        "Xin Zhao":"xinzhao"
        }.get(ugly, ugly)

def directorycheck(championname): #Használt champnevek és rövidítések
    return {
        "Alistar":"ali",
        "Amumu":"mumu",
        "Aurelion Sol":"asol",
        "Blitzcrank":"blitz",
        "Caitlyn":"cait",
        "Cassiopeia":"cassio",
        "Cho'Gath":"cho",
        "Dr. Mundo":"mundo",
        "Evelynn":"eve",
        "Ezreal":"ez",
        "Fiddlesticks":"fiddle",
        "Gangplank":"gp",
        "Hecarim":"heca",
        "Heimerdinger":"heimer",
        "Jarvan IV":"jarvan4",
        "Jarvan IV":"j4",
        "Jarvan IV":"jarvan",
        "Kassadin":"kassa",
        "Katarina":"kat",
        "Katarina":"kata",
        "Kha'Zix":"kha",
        "Kog'Maw":"kog",
        "LeBlanc":"lb",
        "Lee Sin":"lee",
        "Lissandra":"liss",
        "Lucian":"luc",
        "Malphite":"malph",
        "Malzahar":"malz",
        "Master Yi":"yi",
        "Miss Fortune":"mf",
        "Mordekaiser":"morde",
        "Morgana":"morg",
        "Nasus":"susaN",
        "Nautilus":"naut",
        "Nidalee":"nida",
        "Nocturne":"noc",
        "Nunu & Willump":"Nunu és Willump",
        "Nunu & Willump":"Nunu and Willump",
        "Orianna":"ori",
        "Pantheon":"panth",
        "Renekton":"renek",
        "Rengar":"rengo",
        "Sejuani":"seju",
        "Seraphine":"sera",
        "Shyvana":"shyv",
        "Tahm Kench":"tahm",
        "Tristana":"trist",
        "Tryndamere":"trynda",
        "Tryndamere":"trynd",
        "Twisted Fate":"tf",
        "Vladimir":"vlad",
        "Volibear":"voli",
        "Warwick":"ww",
        "Wukong":"wu",
        "Xin Zhao":"xin",
        "Yasuo":"yas",
        "Zilean":"zil"
    }.get(championname,championname)

def createifdoesntexist():
    if not os.path.exists(workingdir):
        os.makedirs(workingdir)
        os.makedirs(workingdir+"pics")
    for lang in languagelist:
        if not os.path.isfile(workingdir+"champions_"+lang+".csv"):
            with open(workingdir+"champions_"+lang+".csv","w",newline='') as file:
                headerList = ['name','p','q','w','e','r']
                writer= csv.writer(file)
                writer.writerow(headerList)
    if not os.path.isfile(workingdir+"pics\\"+"default.png"):
        img = Image.new('RGBA', (64,64),(0,0,0,0))
        img.save(workingdir+"pics\\"+'default.png','PNG')
    if not os.path.isfile(workingdir+"pics\\"+"hardmode.png"):
        img = Image.new('RGBA', (1,1),(0,0,0,0))
        img.save(workingdir+"pics\\"+'hardmode.png','PNG')

def getpassiveandspells(champ,lang):
    with open(workingdir+"champions_"+lang+".csv",'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if champ == row[0]:
                return row

def abilitydl(champion): #Letölti az adott champnek az abilityképeit
    for ability in abilityletters:
        try:
            open(workingdir+"pics\\"+beautify(champion)+"_{}.png".format(ability))
        except FileNotFoundError:
            champurl = abilityurl.replace("champion_name",beautify(champion))+"{}".format(ability)
            img_data = requests.get(champurl).content
            with open(workingdir+"pics\\"+beautify(champion)+"_{}.png".format(ability), 'wb') as handler:
                handler.write(img_data)
                handler.close()

def champpicdl(champion): #unused
    try:
        open(workingdir+"pics\\"+beautify(champion)+".png")
    except FileNotFoundError:
        champurl = squareurl.replace("champion_name",beautify(champion))
        img_data = requests.get(champurl).content
        with open (workingdir+"pics\\"+beautify(champion)+".png", 'wb') as handler:
            handler.write(img_data)
            handler.close()

def d156(): #eldob egy 156 oldalú dobókockát, visszaad egy oldalt (béna vagy mátétea)
    champlistcreate()
    choice = random.choice(champlist)
    return choice

def reroll(): #main logic
    global champ
    champ = d156()
    champability = getpassiveandspells(champ,lang=lang)
    global randomspellnumber
    randomspellnumber = random.randint(0,4)
    randomspell = champability[randomspellnumber+1]
    if randomspellnumber == 0:
        window['ability'].update(workingdir+"pics\\"+beautify(champ)+"_p.png")
    elif randomspellnumber == 1:
        window['ability'].update(workingdir+"pics\\"+beautify(champ)+"_q.png")
    elif randomspellnumber == 2:
        window['ability'].update(workingdir+"pics\\"+beautify(champ)+"_w.png")
    elif randomspellnumber == 3:
        window['ability'].update(workingdir+"pics\\"+beautify(champ)+"_e.png")
    elif randomspellnumber == 4:
        window['ability'].update(workingdir+"pics\\"+beautify(champ)+"_r.png")
    window['champnev'].update(randomspell)
    if values['hardmode'] == True:
        window['ability'].update(workingdir+"pics\\"+"hardmode.png")
    if pontok == 5:
        window['os'].update(disabled=False)
    if values['os'] == True:
        window['txtinput'].update(background_color="red")
    else:
        window['txtinput'].update(background_color="white")

def pontupdate(): #pontupdate (nice)
    if pontok == 69:
        window['pontoktext'].update("Pontjaid: nice cock")
    else:
        window['pontoktext'].update("Pontjaid: {}".format(str(pontok)))

def compare(comp1,comp2): #összehasonlítás
    if str(comp1).lower() == str(beautify(comp2)).lower():
        return True
    elif str(comp1).lower() == str(comp2).lower():
        return True
    elif str(comp1).lower() == str(directorycheck(comp2)).lower():
        if values['dir'] == True:
            return True
        else:
            return False
    else:
        return False

def logic(txtinput,champ,num): #összehasonlításos és pontkezelős logika
    if compare(txtinput,champ) is True:
        if randomspellnumber == num:
            incpontok()
            reroll()         
        else:
            decpontok()
            if values['os'] == True:
                reroll()
    else:
        decpontok()
        if values['os'] == True:
            reroll()

def incpontok(): #+1 pont
    global pontok
    pontok = pontok + 1

def decpontok(): #-1 pont ha pontok > 0
    global pontok
    if pontok > 0:
        pontok = pontok - 1

def dbcreate(champion,lang):
    if type(champion) is list:
        pool.map(partial(dblogic, ver=ver, lang=lang), champion)
    else:
        dblogic(champion,ver,lang)

def dblogic(champ,ver,lang):
    url = "https://ddragon.leagueoflegends.com/cdn/{0}/data/{1}/champion/{2}.json".format(ver,lang,champ)
    raw = requests.get(url).json()
    jsonchampname = raw["data"][champ]
    namepassiveandspells = list()
    namepassiveandspells.append(champ)
    namepassiveandspells.append(jsonchampname["passive"]["name"])
    for i in range(4):
        namepassiveandspells.append(jsonchampname["spells"][i]["name"])
    with open(workingdir+"champions_"+lang+".csv","a",newline='') as db:
        writer = csv.writer(db)
        writer.writerow(namepassiveandspells)

def champlistcreate():
    url = "https://ddragon.leagueoflegends.com/cdn/{0}/data/en_US/champion.json".format(ver)
    raw = requests.get(url).json()
    champdict = dict(raw["data"])
    champamount = len(raw["data"])
    global champlist
    champlist = list(champdict.keys())[:champamount]

def firstsetup():
    if not os.path.exists(workingdir):
        sg.Popup("Első indítás!","Szükséges adatok letöltése, ez eltarthat egy ideig!",title=title)
        createifdoesntexist()
        champlistcreate()
        for language in languagelist:
            dbcreate(champlist,lang=language)
        pool.map(abilitydl,champlist)
        pool.close()
    else:
        pass

firstsetup()

tab1_layout = [ #Játék tab
        [sg.Text(text="Kattints a Reroll gombra!",enable_events=True,key='champnev',size=(25,1)),
        sg.Text(text="Pontjaid: {}".format(str(pontok)),enable_events=True,key='pontoktext',justification="Right",size=(9,1))],
        [sg.Image(workingdir+"pics\\"+"default.png",key='ability')],
        [sg.Input(key='txtinput',do_not_clear=False,focus=True,size=(40,1))],
        [sg.Button(' P '), sg.Button(' Q '), sg.Button(' W '), sg.Button(' E '), sg.Button(' R ')],
        [sg.Button('Reroll'),sg.Button('Bezárás')],
        ]

tab2_layout = [ #Beállítások tab
        [sg.Text("Nyelv / Language:"),sg.Combo(languagelist,key='nyelv',readonly=True,default_value="hu_HU")],
        [sg.Checkbox('Hardmode',key='hardmode'),sg.Button(" ? ",key="hardmodedoc")],
        [sg.Checkbox('Advanced directory',key='dir',default=True),sg.Button(" ? ",key="advdirectorydoc")],
        [sg.Checkbox('Oneshot',key='os',disabled=True),sg.Button(" ? ",key="oneshotdoc")]
        ]

layout = [ #Main layout (két tab)
        [sg.TabGroup([[sg.Tab('Játék', tab1_layout), sg.Tab('Beállítások', tab2_layout)]],)],
        ]

window = sg.Window(title=title,layout=layout) #Define window

while True: #Logic when GUI
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Bezárás'):
        break
    if event == 'Reroll':
        lang = values['nyelv']
        decpontok()
        pontupdate()
        reroll()
    if event == ' P ':
        txtinput = values['txtinput']
        logic(txtinput,champ,0)
        pontupdate()
    if event == ' Q ':
        txtinput = values['txtinput']
        logic(txtinput,champ,1)
        pontupdate()
    if event == ' W ':
        txtinput = values['txtinput']
        logic(txtinput,champ,2)
        pontupdate()
    if event == ' E ':
        txtinput = values['txtinput']
        logic(txtinput,champ,3)
        pontupdate()
    if event == ' R ':
        txtinput = values['txtinput']
        logic(txtinput,champ,4)
        pontupdate()
    if event == 'hardmodedoc':
        sg.popup("A hardmode bekapcsolásával","elrejted a megjelenő képeket!",title=title)
    if event == 'advdirectorydoc':
        sg.popup("Az advanced directory kikapcsolásával","kikapcsolod a rövidítések használatát,","így teljes névvel ki kell írnod a karaktereket!","Például: yi helyett Master Yi",title=title)
    if event == 'oneshotdoc':
        sg.popup("A oneshot mód bekapcsolásakor csak","egy lehetőséged lesz próbálkozni!","Figyelj a champnévre!","A oneshot mód 5 elért pont után válik elérhetővé.",title=title)

window.close()