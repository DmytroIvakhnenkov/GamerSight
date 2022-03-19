import urllib.request, urllib.parse, urllib.error
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import json


'''=======================================================Functions================================================================'''

#Uses YouTube API, searhes YouTube for a name of the game, prints five first results
def searchByKeyword(keyword):
    youtube = build('youtube', 'v3', developerKey=You_Tube_key)
    request = youtube.search().list(q = keyword+" game", part = 'snippet', maxResults=5, type="video")
    response = request.execute()
    for items in response["items"]:
        print(items["snippet"]["title"], end=" - ")
        print("https://www.youtube.com/watch?v="+items["id"]["videoId"])
    if len(response["items"])==0:
        print("Sorry, no videos were found")

#Extracts and prints a piece of infromation from the JSON file received from GiantBomb        
def standart_extract(extract_parameter, results):
    c=0
    if results.get(extract_parameter,'None')!='None' and results.get(extract_parameter,'None')!=None:
        print(extract_parameter.capitalize(), end=": ")
        for elem in results[extract_parameter]:
            if c==0:
                c=c+1
            else:
                print(", ",end="")
            print(elem["name"], end="")
        print('\n')

#Requests search results using API key, number of a page(one page = 10 results) of search results, and the name of the game
#shows results to a user, returns  number of a search result page, number of search results total
def show_list(key,p,keyword):
    global k
    url  = "http://www.giantbomb.com/api/search/?api_key="+key+'&format=json'+'&page='+str(p)+'&query="'+keyword+'"&resources=game'
    source = urllib.request.urlopen(url)
    data = source.read().decode().strip()
    json_file = json.loads(data)
    
    if(json_file["number_of_page_results"]==0):
        print("Sorry, nothing was found")
    
    else:
        p_continue = 'yes'
        #printing a list of games (max results=10)
        for elem in json_file["results"]:
            print(k+1,":",elem["name"])
            k = k+1
        print()
        
        #If max amount of results was shown
        if (k%10==0):
            
            #getting yes or no answer from the user in order to know if it is needed to prolong the search results list
            
            not_correct = True  #not_correct is a variable used for detecting incorrect input
            
            #This while loop prevents the user from entering something besides yes or no
            while not_correct:
                
                p_continue = input("Do you want more results? Type 'yes', if yes; type 'no', if no: ").lower()
                print()
                
               #Exit of the loop
                if p_continue =='yes' or p_continue =='no':
                    not_correct=False
                    
                else:
                    print("Are you sure that you entered a 'yes' or 'no'?", end="\n")
                
                #yes -> another 10 search results    
                if p_continue == 'yes':
                    p=p+1
                    show_list(key,p,keyword)  
                    
    return p

#Requests data from IGN top 100 games page, searches for the keyword(the name of a game) 
#if succeeds in finding -> notifies the user
def scrapeIGN(keyword):
    url  = "https://www.ign.com/lists/top-100-games/"
    source = urllib.request.urlopen(url)
    data = source.read().decode().strip()
    if data.find(keyword)!=-1:
        print("Great! Your game is on IGN's top 100 games list!\n")
    

'''=======================================================Main body================================================================'''

You_Tube_key = 'AIzaSyBgl1fwqe42dRVp6s7db8MoSsCspAyS4R8'
key = 'e31d3fa24fce36fe993df6f1aa46000ca1074e8d'
keyword = input("Input a keyword to search with it for a game: ").replace(" ","%20")

p=1 #p is a number of a search result page (Note: each page is 10 results max)
k=0 #k is a number of search results total
p=show_list(key,p,keyword)

#checking if there are any results
if k>0:
    not_correct = True  #not_correct is a variable used for detecting incorrect input
    
    while not_correct:
        
        #try catches the error when the user enters something besides an integer
        try:
            
            Userpick = int(input("Choose the number of a game you wish to know more about: "))
            
            #checks whether the user inputted the number from the ones he/she has been shown
            if (Userpick > k) or (Userpick < 1):
                
                print("Are you sure that you entered a number from the ones you have been shown?")
                
            else:
                
                not_correct = False 
                
        except ValueError: #ValueError occurs when a program connot use int(), hence incorrect input was entered by the User
            
            print("Are you sure that you entered a number?")
            
        print() #indent
        
    #Requesting search data from GiantBomb, extracting ID of the game user picked
        
    url  = "http://www.giantbomb.com/api/search/?api_key="+key+'&format=json'+'&page='+str(p)+'&query="'+keyword+'"&resources=game'
    source = urllib.request.urlopen(url)
    data = source.read().decode().strip()
    json_file = json.loads(data)
    guid = json_file["results"][(Userpick%10)-1]["guid"] #ID of the game
    
#Requesting game information from GiantBomb, showing it to user
    
    url = 'http://www.giantbomb.com/api/game/'+guid+'/?api_key='+key+'&format=json'
    source = urllib.request.urlopen(url)
    data = source.read().decode().strip()
    json_file = json.loads(data)
    results = json_file["results"]  

    print("\t\t", results["name"]+'\n') #Name of the game
    scrapeIGN(results["name"].strip()) #IGN top-100 games appearance
    standart_extract("genres", results) #Genres         
    
    #Release date
    if results.get("expected_release_year",'None')!='None' and results.get("expected_release_year",'None')!=None:
        print("Release date", end="")
        release_day = str(results["expected_release_day"])
        release_month = str(results["expected_release_month"])
        release_year = str(results["expected_release_year"])
        print("(dd/mm/yyyy): "+release_day+"/"+release_month+"/"+release_year)
    print() #indent
    
    standart_extract("platforms", results) #Platforms
    standart_extract("developers", results) #Developers
    standart_extract("themes", results) #Themes
    standart_extract("original_game_rating", results) #Age rating
    
    
    if results.get("description",'None')!='None' and results.get("description",'None')!=None: #Checking if there is any data in description section
        
        #Overview
        
        print("Overview:")
        soup = BeautifulSoup(results["description"], 'html.parser')
        overview = soup.find("p")
        for string in overview.strings:
            print(string, end = "")
        print("\n") 
        
        #Hardware requirements
        
        hardware = soup.find_all("h3")
        if len(hardware)==2:
            even = 1
            print("Minimum hardware requirements:")
            for string in hardware[0].next_sibling.strings:
                print(string, end = "")
                if even%2==0:
                    print()
                even = even+1
            print() 

            even = 1
            print("Recommended hardware requirements:")
            for string in hardware[1].next_sibling.strings:
                print(string, end = "")
                if even%2==0:
                    print()
                even = even+1
            print() 
    
    #YoutubeVideos
    
    print("List of videos you might want to watch:")
    searchByKeyword(results["name"])
    print() 
    
    #ReferenceSite

    print("Reference site: " + results["site_detail_url"])




