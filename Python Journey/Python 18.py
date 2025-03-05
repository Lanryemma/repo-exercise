#How to connect to an API 
#in this example we are gonna connect to the pokemon API
import requests
#since request doesn't come with the installed python package we would have to install it
#first we activate .venv by running ".venv\Scripts\activate" in the terminal

#Now we will use the URL from from the website that provide the API

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(name):
    #from the site the full url is the base_urk/pokemon/pokemon-name
    Full_url = f"{base_url}/pokemon/{name}"
    #and now we will request data from the site using request method
    response = requests.get(Full_url)
    print (response)
    #now we use a conditional statement to check if the request was successful
    if response.status_code == 200:
    #now we collect the data in json form and convert it to a dictionary
        pokemon_data = response.json()
        #print(pokemon_data)
        return pokemon_data
    else:
        print(f"Failed to retrieve data {response.status_code}")
    

pokemon_name ="milotic" #"typhlosion"#"pikachu"
#there are many other pokemon names to chose from and get their data
#e.g typhlosion,bulbasaur,charmander,charmeleon,wartortle, onix, steelix, milotic,guzzlord
pokemon_info = get_pokemon_info(pokemon_name)
#this give us "Response [200]>" which mans successful response

if pokemon_info:#This is to verify if the pokemon info was successfully collected  
    print(f"Name: {pokemon_info["name"]}")
    print(f"Id: {pokemon_info["id"]}") #requesting the "id" date from the api
    print(f"Height: {pokemon_info["height"]}")
    print(f"Weight: {pokemon_info["weight"]}")#requesting the "" date from the api