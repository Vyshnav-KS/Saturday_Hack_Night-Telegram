import requests
from datetime import datetime

base_cowin_url ="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
telegram_api = "https://api.telegram.org/bot2025671698:AAHiFy1Zo_-7sawCHVyzZHtFS9ES9R2VOd0/sendMessage?chat_id=@__group_id__&text="
group_id= "vac_bot_test"

district_ids_kerala = [295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308]

def apiFromCowin(district_id):
    query_params = "?district_id={}&date={}".format(district_id,today_date)
    final_url = base_cowin_url + query_params
    response = requests.get(final_url)
    availableData(response)
    # print(response.text)
    
def apiFromState(district_ids):
    for district_id in district_ids:
        apiFromCowin(district_id)
        
def availableData(response):
    json_response = response.json()
    for center in json_response["centers"]:
        for session in center["sessions"]:
            if session["available_capacity_dose1"] > 0 and session["min_age_limit"]==18:
                message= "Pincode : {} \nName : {} \nSlots for dose 1 : {} \nSlots for dose 2 : {} \nMinimum Age : {} \nVaccine : {}".format(
                center["pincode"], 
                center["name"], 
                session["available_capacity_dose1"], 
                session["available_capacity_dose2"],
                session["min_age_limit"],
                session["vaccine"])
                telegram_message(message)
                # print(message)

def telegram_message(message):
    final_telegram_url = telegram_api.replace("__group_id__", group_id)
    final_telegram_url = final_telegram_url + message
    response = requests.get(final_telegram_url)
    print(response)
    


if __name__ == "__main__":
    apiFromState(district_ids_kerala)