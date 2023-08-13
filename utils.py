# utils.py
import openai
import requests
import json

encryption_key = 5474

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


modelOutput = {"overall_outfit": "Overall description of the outfit","individual_apparels": {"apparel_1": {"name": "ex.Kurta,Shirt,Saaree","description": ""},"apparel_2": {"name": "","description": ""}}}
output_string = json.dumps(modelOutput)

modelInformation = f"As a Fashion Outfit Generator, Generate a outfit according to the user message. Specify all the clothing item seperatly in detail. Specify color and other properties. Consider and remember the userInfo, userPastOrders, socialMediaTrendInfo."

#Dummy Data
userInfo = "Age:21, Sex:Female, BodyType:Fit, City:Moradabad"
userPastOrders = "Purchase History: Aug 5, 2023 - ₹8,700.00: Floral Print Dress (Biba) - ₹5,000.00, White Sneakers (U.S. Polo ASSN) - ₹3,700.00; Jul 20, 2023 - ₹5,546.40: Striped T-shirt (Allen Solly) - ₹1,960.00, Denim Shorts (Indigo Nation) - ₹3,586.40; Jun 10, 2023 - ₹6,162.50: Summer Hat (Global desi) - ₹1,500.00, Sunglasses (Vero Moda) - ₹2,362.50, Beach Towel (Levi’s) - ₹2,300.00; May 2, 2023 - ₹9,104.70: Blue Jeans (Louis Philippe) - ₹4,000.00, Graphic Print T-shirt (Only) - ₹1,625.90, Sneakers (Lombard) - ₹3,478.80; Apr 15, 2023 - ₹13,230.00: Evening Gown (Label Ritu Kumar) - ₹11,000.00, Clutch Bag (AccessorizeMe) - ₹2,230.00."
socialMediaTrendInfo = ""


def generate_combined_outfit_text(input):
    messages = [
        {"role": "system",
         "content": f"{modelInformation},userInfo:{userInfo},userPastOrders:{userPastOrders},socialMediaTrendInfo:{socialMediaTrendInfo}"},
    ]

    messages.append({"role": "user", "content": f"{input} "})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    combined_outfit_text = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": f"{combined_outfit_text}"})

    image_prompts_json_string = generate_image_prompts(combined_outfit_text)
    image_prompts_json = convert_json_string(image_prompts_json_string)
    print(image_prompts_json)
    return combined_outfit_text


def generate_image_prompts(outfit_text):
    messages = [
        {"role": "user","content": f"({outfit_text}) Generate ecommerce search prompts for each of the individual items in the outfit.Give Json object with 'clothingItem' Array contatining 'name' and 'searchPrompt'"},

        #{"role": "user", "content": f"({outfit_text}) Generate short image generation prompts for each of the individual items in the outfit.Give Json object with 'clothingItem' Array contatining 'name' and 'imagePrompt'"},
    ]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    image_prompts_json = completion.choices[0].message.content
    return image_prompts_json

def convert_json_string(json_string):
    # Convert the cleaned string to a JSON object
    json_object = json.loads(json_string)
    return json_object

def getFlipkartSearch(input):
    base_url = "https://flipkart-scraper-api.dvishal485.workers.dev/search/"
    url = base_url + input

    response = requests.get(url)

    if response.status_code == 200:
        products = response.json() #["result"][:5]  # Extract the top 5 results
        return topFiveResults(products)
    else:
        return None

def topFiveResults(input_json):
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

    return {"top_results": filtered_results}

# def generate_image(prompt):
#     response = openai.Image.create(
#         prompt=prompt,
#         n=1,
#         size="256x256"
#     )
#     image_url = response['data'][0]['url']
#     return image_url
#


# def detect_image_web(uri):
#     """Detects web annotations in the file located in Google Cloud Storage."""
#     from google.cloud import vision
#
#     client = vision.ImageAnnotatorClient()
#     image = vision.Image()
#     image.source.image_uri = uri
#
#     response = client.web_detection(image=image)
#     annotations = response.web_detection
#
#     if annotations.best_guess_labels:
#         for label in annotations.best_guess_labels:
#             print(f"\nBest guess label: {label.label}")
#
#     if annotations.pages_with_matching_images:
#         print(
#             "\n{} Pages with matching images found:".format(
#                 len(annotations.pages_with_matching_images)
#             )
#         )
#
#         for page in annotations.pages_with_matching_images:
#             print(f"\n\tPage url   : {page.url}")
#
#             if page.full_matching_images:
#                 print(
#                     "\t{} Full Matches found: ".format(len(page.full_matching_images))
#                 )
#
#                 for image in page.full_matching_images:
#                     print(f"\t\tImage url  : {image.url}")
#
#             if page.partial_matching_images:
#                 print(
#                     "\t{} Partial Matches found: ".format(
#                         len(page.partial_matching_images)
#                     )
#                 )
#
#                 for image in page.partial_matching_images:
#                     print(f"\t\tImage url  : {image.url}")
#
#     if annotations.web_entities:
#         print("\n{} Web entities found: ".format(len(annotations.web_entities)))
#
#         for entity in annotations.web_entities:
#             print(f"\n\tScore      : {entity.score}")
#             print(f"\tDescription: {entity.description}")
#
#     if annotations.visually_similar_images:
#         print(
#             "\n{} visually similar images found:\n".format(
#                 len(annotations.visually_similar_images)
#             )
#         )
#
#         for image in annotations.visually_similar_images:
#             print(f"\tImage url    : {image.url}")
#
#     if response.error.message:
#         raise Exception(
#             "{}\nFor more info on error messages, check: "
#             "https://cloud.google.com/apis/design/errors".format(response.error.message)
#         )
#
#

