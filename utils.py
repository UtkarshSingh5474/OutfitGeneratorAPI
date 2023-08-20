# utils.py
import openai
import requests
import json

encryption_key = 5474
seperator = "-SEPERATOR-"
def decrypt_api_key(encrypted_api_key):
    decrypted_chars = []
    for char in encrypted_api_key:
        decrypted_char = chr((ord(char) - encryption_key) % 256)
        decrypted_chars.append(decrypted_char)
    decrypted_api_key = ''.join(decrypted_chars)
    return decrypted_api_key

# Set your OpenAI API key
decrypted_key = decrypt_api_key("ÕÍ¤°¬®º©´¶µ·¯©¬Ò¼È¶¤ÎÄÍ¨¬¬¨Ô¹Ì¤ÙÅ¥ÐÜÅ©ªÅÕ®")
openai.api_key = decrypted_key


def generate_overview_text(input):

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=json.loads(input)
    )
    outfitOverview = completion.choices[0].message.content
    return outfitOverview


def generate_clothingItemsFlipkartSearchResults(outfit_text):
    return getMultipleFlipkartSearch(generate_search_prompts(outfit_text))

def generate_search_prompts(outfit_text,userInfo=""):
    # Split the text to separate userInfo and outfitOverview
    if "userInfo:" in outfit_text:
        parts = outfit_text.split("userInfo:")
        userInfo = parts[1].split(",")[0].strip() if len(parts) > 1 else None
        outfitOverview = parts[0].strip()
    else:
        userInfo = None
        outfitOverview = outfit_text.strip()

    messages = [
        {"role": "user","content": f"({outfitOverview}) Generate ecommerce search prompts for each of the individual items in the outfit.Give Json object with 'clothingItems' Array contatining 'name' and 'searchPrompt'.Add user info(sex,size,etc) in searchPrompts: {userInfo}"},

        #{"role": "user", "content": f"({outfit_text}) Generate short image generation prompts for each of the individual items in the outfit.Give Json object with 'clothingItem' Array contatining 'name' and 'imagePrompt'"},
    ]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    image_prompts_json = completion.choices[0].message.content
    return image_prompts_json



def getMultipleFlipkartSearch(searchPrompts):
    print(searchPrompts)
    searchPrompts = json.loads(searchPrompts)
    print("-----")
    print(searchPrompts)
    if 'user' in searchPrompts:
        del searchPrompts['user']
    if 'userInfo' in searchPrompts:
        del searchPrompts['userInfo']
    searchPrompts = json.loads(json.dumps(searchPrompts))
    print("-----")
    print(searchPrompts)
    allClothingItemsResults = {}
    for item in searchPrompts['clothingItems']:
        name = item['name']
        search_prompt = item['searchPrompt']
        allClothingItemsResults.update(getFlipkartSearchByName(name, search_prompt))

    return allClothingItemsResults



def getFlipkartSearchByName(name, searchPrompt):
    base_url = "https://flipkart-scraper-api.dvishal485.workers.dev/search/"
    url = base_url + searchPrompt

    response = requests.get(url)

    if response.status_code == 200:
        products = response.json() #["result"][:5]  # Extract the top 5 results
        return topFiveResults(name, products)
    else:
        return None
def getFlipkartSearch(input):
    base_url = "https://flipkart-scraper-api.dvishal485.workers.dev/search/"
    url = base_url + input

    response = requests.get(url)

    if response.status_code == 200:
        products = response.json() #["result"][:5]  # Extract the top 5 results
        return topFiveResults(input,products)
    else:
        return None

def topFiveResults(name,input_json):
    filtered_results = []

    if "result" in input_json:
        result_list = input_json["result"]
        for i in range(min(5, len(result_list))):
            item = result_list[i]
            filtered_item = {
                "name": item["name"],
                "current_price": item["current_price"],
                "link": item["link"],
                "thumbnail": item["thumbnail"]
            }
            filtered_results.append(filtered_item)
    fetch_from =input_json.get("fetch_from", "")

    return {f'{name}':{'searchLink':f'{fetch_from}','topResults':filtered_results}}

import json

def create_outfit_json(overviewtext, clothingItems):
    #clothingItems = clothingItems.get("clothingItems", [])

    outfit_data = {
        "outfitOverview": overviewtext,
        "clothingItems": clothingItems
    }
    #return json.loads(outfit_data, indent=2)
    return outfit_data
