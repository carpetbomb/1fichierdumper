import sys
import requests
from bs4 import BeautifulSoup
import os
import json
import webbrowser
import PySimpleGUI as sg
import re
import math

os.system("color")

class c:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

check_file = os.path.isdir('./dumps')
if check_file == False:
	os.mkdir("./dumps", 0o777)

def menu(q):
	valid = {"1": True, "2": True, "3": True, "4": True}
    
	prompt = "\n=============================\n[1] - Dump directory to json \n[2] - View dumped directory in GUI\n[3] - List dumped files\n[4] - exit \n"
	mt = "Input Selection"
	while True:
		sys.stdout.write("=============================\n" + mt + prompt)
		sys.stdout.write(f"{c.CYAN}--> {c.ENDC}")
		choice = input().lower()
		if choice in valid:
			return valid[choice], choice
		else:
			sys.stdout.write("Invalid Input" "\n")

def dumpdir():
	while True:
		sys.stdout.write(f"{c.YELLOW}[Enter 1File Link to dump] {c.ENDC} \n")
		sys.stdout.write(f"{c.CYAN} --> {c.ENDC}")
		choice = input()
		url = choice

		append = ""

		if url.find("dir") == -1:
			sys.stdout.write(f"{c.RED} --> Invalid directory link, returning to selecton {c.ENDC}" "\n")
			return
		if url.find("https://1fichier.com/dir/") == -1:
			sys.stdout.write(f"{c.RED} --> Invalid directory link, returning to selecton {c.ENDC}" "\n")
			return

		sys.stdout.write("--> Dumping directory ["+url+"]" "\n")

		page = requests.get(url)
		if str(page).find("200") != 1:# and not str(page).find("Flood"):
			print(f"{c.GREEN} --> Got Response [200] {c.ENDC}")
		else:
			addition = ""
			print(page)
			if str(page).find("Flood") != -1:
				addition = "Use a VPN, IP flagged for flood"
			sys.stdout.write(f"{c.RED} --> Request Failed "+addition); sys.stdout.write(f"{c.ENDC} \n")
			return
	

		sys.stdout.write(f"{c.CYAN} --> Scraping Page {c.ENDC}" "\n")

		soup = BeautifulSoup(page.content, "html.parser")

		posts = soup.find_all("tr")

		#print(len(results))
		data = {}
		maindata = {}
		numero = 1

		
		for post_element in posts:
			gameName = "N/A"
			link_url = "N/A"
			gameSize = "N/A"
			gameName2 = "N/A"
			
			for post_element2 in post_element.find_all("td"):

				postClass = post_element2['class']
				postClassLength = 0
				for i in postClass:
					postClassLength = postClassLength + 1

				if postClassLength == 3 and postClass[1] == "alg":
					link_url = post_element2.find_all("a")[0]["href"]
					gameName = str(post_element2.find('a').contents[0])
					if gameName.find("'") != -1:
						gameName = gameName.replace("'","")



				if postClass[0] == "normal" and postClassLength == 1:
					size = str(post_element2.contents[0])
					if size.find("GB") != -1 or size.find("MB") != -1:
						gameSize = size
			#.encode('utf-8')
			if gameName != "N/A":
				data[gameName.encode('utf-8')] = {
					"link" : link_url.encode('utf-8'),
					"size" : gameSize.encode('utf-8')
				}

				maindata.update(data)
				numero = numero + 1


		sys.stdout.write(" --> Enter a file name to dump as (will dump to .json)\n")
		sys.stdout.write(f"{c.CYAN} --> {c.ENDC}")
		choice = input()

		with open("./dumps/"+str(choice)+".json", "w") as write_file:
			json.dump(str(maindata), write_file)

		print(f"{c.GREEN} --> Successfully dumped directory to file. {c.ENDC}" "\n")
		return

def download(lnk:str):
	with open("apikey.txt", "r", encoding='utf-8-sig') as f: # grab text
		key = f.read()

	URL = 'http://api.alldebrid.com/v4/user?agent=myAppName&apikey='+key
	headers = {'User-Agent': 'Mozilla/5.0'}
	page = requests.get(URL, headers=headers).text
	soup = BeautifulSoup(page, features='html.parser')

	jsonResponse = json.loads(page)
	print("--> API Authorisation "+jsonResponse['status'], flush=True)

	if jsonResponse['status'] == 'success':
		URL = 'https://api.alldebrid.com/v4/link/unlock?agent=myAppName&apikey='+key+'&link='+lnk
		headers = {'User-Agent': 'Mozilla/5.0', 'link': ''}
		page = requests.get(URL, headers=headers).text
		soup = BeautifulSoup(page, features='html.parser')
		jsonResponse = json.loads(page)
		if jsonResponse['status'] == 'success':
			webbrowser.open(jsonResponse['data']['link'])
		else:
			if jsonResponse['status'] == 'error':
				sys.stdout.write(f"{c.RED} --> Got Response ["+jsonResponse['error']['code'] + ' | ' +jsonResponse['error']['message']+"]"); sys.stdout.write(f"{c.ENDC} \n")

	else:
		sys.stdout.write(f"{c.RED} --> Invalid API Key!! {c.ENDC}", True)

def loadList(fname):
	with open(fname, 'r') as data: #Cleaning up import impurities
			loaded = data.read()
			s = loaded.strip('\"')

	with open(fname, 'w') as data: #Cleaning up import impurities
			data.write(s)

	with open(fname, "r", encoding='utf-8-sig') as f: # Counting game amount
		string = f.read()
		#listOfGames = f.read()
		listOfGames = eval(string)
		txt = "Got "+str(len(listOfGames))+" Games"

	return listOfGames, txt

class Item(): # Defining item for metatable
    def __init__(self, gameName, link, size):
        self.gameName = gameName
        self.link = link
        self.gameCUSA = size


    def __str__(self):
        return self.gameName


while True:
	valid, mchoice = menu("")
	if str(mchoice) == "1":
		dumpdir()
	elif str(mchoice) == "3":
		dfiles = os.listdir("./dumps")
		sys.stdout.write(f"{c.YELLOW}=====Dumps===== {c.ENDC} \n")
		for i in dfiles:
			filesize = os.path.getsize("./dumps/"+i)
			print(i, math.floor(filesize/1024), "KB")
		sys.stdout.write(f"{c.YELLOW}=============== {c.ENDC} \n")

	elif str(mchoice) == "4":
		print(f"{c.GREEN}--> Exiting. {c.ENDC}" "\n")
		break
	elif str(mchoice) == "2":
		sys.stdout.write(f"{c.CYAN} --> Enter file name to open (no extension) {c.ENDC} \n")
		sys.stdout.write(f"{c.CYAN} --> {c.ENDC}")
		choice = input()

		check_file = os.path.isfile('./apikey.txt')
		if check_file == False:
			print(f"{c.RED} -->   API Key file not found! Making one now... {c.ENDC}")
			with open("apikey.txt", "w") as write_file:
				write_file.write("")

		sg.theme('dark gray 13')

		my_item_list = []

		gamesListRaw, gameAmount = loadList("./dumps/"+choice+".json")

		for game in gamesListRaw: # Adding to item list
			#print(game, a[game])
			gameInfo = gamesListRaw[game]
			gameName = game.decode()
			#print(gameInfo['link'])
			obj = Item(gameName, gameInfo['link'], gameInfo['size'])

			my_item_list.append(obj)

		layout = [  
			[sg.Titlebar("1File directory List")],

			[sg.MenubarCustom([['&Options', ['File Download API']]], key = 'menu', bar_text_color = 'White', background_color = 'White')],
			[sg.Text(gameAmount, justification='center' )],
			[sg.Input(size=(40, 1), enable_events=True, default_text="Input Search...", key='-INPUT-'), sg.Button('Clear Search')],
			[sg.Listbox(my_item_list, key='-LB-', s=(51,10), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED)],
			[sg.Column([[sg.Frame('Actions:',[[sg.Column([[sg.Button('Open Page'), sg.Button('Download'), sg.Button('Exit')]],size=(375,45), pad=(0,0))]])]], pad=(0,0))],
			[sg.StatusBar('Coded by zbombr115', key='-STAT-')],
		]

		window1 = sg.Window('Coded by zbombr115', layout, keep_on_top=True, finalize=True)

		while True:

			window, event, values = sg.read_all_windows()
			if window == window1 and event == sg.WIN_CLOSED:
				window1.close()
				if 'window4' in globals():
					window4.close()
				break
			if 'window4' in globals() and window == window4 and event == sg.WIN_CLOSED:
				window4.close()
			if 'window4' in globals() and event == 'Exit':
				window4.close()
			if event == 'Exit':
				window.close()
				if window == window1:
					break
			elif event == 'Open Page':
				for item in values['-LB-']:
					webbrowser.open(item.link.decode("ASCII"))
			if event == 'Download':
				for item in values['-LB-']:
					download(item.link.decode("ASCII"))
			if event == 'File Download API':
				inp = ""
				with open("apikey.txt", "r", encoding='utf-8-sig') as f: # grab text
					inp = f.read()
				layout3 = [
					[sg.Titlebar("API Key Input (alldebrid.com)")],
					[sg.Column([[sg.Frame('API Key:',[[sg.Column([[sg.Input(inp, key='-API-')]],pad=(0,0))]])]], pad=(0,0))],
				]

				window4 = sg.Window('API', layout3, keep_on_top=True, finalize=True)
			if 'window4' in globals() and window == window4:
				if '-API-' in values and values['-API-'] != "":
					with open("apikey.txt", "w") as write_file:
						write_file.write(values['-API-'])