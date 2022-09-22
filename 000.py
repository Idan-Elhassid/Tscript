import smtplib
from datetime import *
import time
import random
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# the randomizer and random section's are used to mimic a human player to avoid penalties and ban's.
time.sleep(random.randint(1, 30))
in_code_randomizer = random.randint(1, 7)


list_of_dates = []
for number in range(1, 45):
    date_x = datetime.today() - timedelta(days=number)
    date_x_date = str(date_x.strftime("%d.%m.%y"))
    list_of_dates.append(date_x_date)

animal_dic = {
            "Rat": 20,
            "Spider": 40,
            "Snake": 60,
            "Bat": 50,
            "Wild": 33,
            "Wolf": 70,
            "Bear": 200,
            "Crocodile": 240,
            "Elephant": 520,
            "Tiger": 250,
            "Rats": 20,
            "Spiders": 40,
            "Snakes": 60,
            "Bats": 50,
            "Wolves": 70,
            "Bears": 200,
            "Crocodiles": 240,
            "Tigers": 250,
            "Elephants": 520,
        }

login_page = "https://ts2.x1.international.travian.com/logout"

# insert username and password below:
username = "the username"
password = "the password"

# going to the main page - make a login
service = Service(r"C:\Users\yedidya\PycharmProjects\chromedriver_win32\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(login_page)

login_name = driver.find_element(By.XPATH, '//*[@id="loginForm"]/tbody/tr[1]/td[2]/input')
login_password = driver.find_element(By.XPATH, '//*[@id="loginForm"]/tbody/tr[2]/td[2]/input')

login_name.send_keys(f"{username}")
login_password.send_keys(f"{password}")
login_password.send_keys(Keys.ENTER)
time.sleep(2)

# navigate to the farmlists
go_to_village_000 = driver.find_element(By.XPATH, '//*[@id="sidebarBoxVillagelist"]/div[2]/div[2]/div[2]/div/a/span/span[2]')
go_to_village_000.click()

time.sleep(in_code_randomizer)

farm_list = driver.find_element(By.XPATH, '//*[@id="sidebarBoxLinklist"]/div[2]/ul/li[5]/a')
farm_list.click()

dropdown = driver.find_element(By.XPATH, '//*[@id="raidList4625"]/div[1]/div[4]')
try:
    dropdown.click()
    time.sleep(1)

except selenium.common.exceptions.ElementNotInteractableException:
    dropdown.click()
    time.sleep(1)

# this section will get us all the urls in our requested farmlist
parent = driver.find_element(By.XPATH, '//*[@id="raidList4625"]')
list_of_links = []
links = parent.find_elements(By.TAG_NAME, "a")
for link in links:
    list_of_links.append(link.get_attribute("href"))

new_list = []
for item in list_of_links:
    if item == None:
        list_of_links.remove(item)
    elif "x=" in item:
        new_list.append(item)

x = 0
report_list = []
for check in new_list:
    driver.get(new_list[x])
    troops_check = driver.find_element(By.ID, 'troop_info').text
    time.sleep(in_code_randomizer)
    # we want to avoid actions on oasis's that don't have troops, or containing Elephants
    if "none" in troops_check or "Elephants" in troops_check or "Elephant" in troops_check:
        print(f"no troops in {x} or Elephants in this oasis")
        x += 1
    # if a date from our list of dates above is found or one the words mentioned that means the oasis is occupied and we will want to remove it from our farmlist
    elif any(date in troops_check for date in list_of_dates) or "No" in troops_check or "today," in troops_check:
        print("this is occupied, i will remove it from the list")
        remove = driver.find_element(By.CLASS_NAME, 'farmListDetails')
        remove.click()
        time.sleep(1)
        delete_from_list = driver.find_element(By.XPATH, '//*[@id="edit_form"]/a/div')
        delete_from_list.click()
        press_delete = driver.find_element(By.XPATH, '//*[@id="dialogContent"]/div/div[2]/button[2]')
        press_delete.click()
        report_list.append(f"{troops_check} in {new_list[x]} was found occupied")
        x += 1
    else:
        # anything else is an oasis to fight with and by building the list below we can continue to the next section.
        oasis_troops_received_from_site = troops_check.split()
        oasis_troops_list = []

        # by the animals found in the oasis we will build a database of the oasis powers based on the animal dictionary we build earlier
        def animal_in_dic(dic, animal_list, animal_list2):
            for entry in animal_list:
                if entry in dic:
                    animal_list2.append(int(dic[entry]))
                elif entry == "simulate" or entry == "raid" or entry == "Boar" or entry == "Boars":
                    pass
                else:
                    animal_list2.append(int(entry))


        animal_in_dic(animal_dic, oasis_troops_received_from_site, oasis_troops_list)
        length_animal_list = len(oasis_troops_list)
        oasis_total_animal_power = 0

        # this section is needed to help calculate the oasis animal power
        if length_animal_list == 2:
            oasis_total_animal_power = (oasis_troops_list[0] * oasis_troops_list[1])
        elif length_animal_list == 4:
            oasis_total_animal_power = (oasis_troops_list[0] * oasis_troops_list[1]) + (oasis_troops_list[2] * oasis_troops_list[3])
        elif length_animal_list == 6:
            oasis_total_animal_power = (oasis_troops_list[0] * oasis_troops_list[1]) + (oasis_troops_list[2] * oasis_troops_list[3]) + (
                    oasis_troops_list[4] * oasis_troops_list[5])
        elif length_animal_list == 8:
            oasis_total_animal_power = (oasis_troops_list[0] * oasis_troops_list[1]) + (
                        oasis_troops_list[2] * oasis_troops_list[3]) + (
                                               oasis_troops_list[4] * oasis_troops_list[5]) + (oasis_troops_list[6] * oasis_troops_list[7])

# calculate and send a raid
        if oasis_total_animal_power < 200 or oasis_total_animal_power > 1000:
            horse_power_needed = oasis_total_animal_power * 25
        else:
            horse_power_needed = oasis_total_animal_power * 14

        add_random_to_horse_ratio = random.randint(40, 90)
        white_horses_to_attack = int((horse_power_needed / 120) + add_random_to_horse_ratio)
        brown_horses_to_attack = int((horse_power_needed / 115) + add_random_to_horse_ratio)

        begin_raid = driver.find_element(By.XPATH, '//*[@id="tileDetails"]/div[1]/div[1]/div[2]/a')
        begin_raid.click()

        time.sleep(in_code_randomizer)

        validate_village = driver.find_element(By.XPATH, '//*[@id="sidebarBoxVillagelist"]/div[2]/div[2]/div[2]/div/a/span/span[2]')
        validate_village.click()
        try:
            check_horses_available = driver.find_element(By.XPATH, '//*[@id="troops"]/tbody/tr[2]/td[2]/a')
            input_brown_horses = driver.find_element(By.XPATH, '//*[@id="troops"]/tbody/tr[2]/td[2]/input')
            input_brown_horses.send_keys(brown_horses_to_attack)
            time.sleep(2)
            input_different_horses = driver.find_element(By.XPATH, '//*[@id="troops"]/tbody/tr[1]/td[2]/input')
            reinforcement = (random.randint(40, 75)) + (int(brown_horses_to_attack / 4))
            input_different_horses.send_keys(reinforcement)

            send_raid = driver.find_element(By.XPATH, '//*[@id="ok"]')
            time.sleep(in_code_randomizer)
            send_raid.click()
            time.sleep(in_code_randomizer)

            confirm_raid = driver.find_element(By.XPATH, '//*[@id="checksum"]')
            time.sleep(in_code_randomizer)
            confirm_raid.click()
            time.sleep(2)
            new_line = f"this oasis has:{troops_check}, its power is {oasis_total_animal_power} i recommend {brown_horses_to_attack} horses to attack, its local is:{new_list[x]}"
            x += 1
            report_list.append(new_line)
            print(f"power is {oasis_total_animal_power} i recommend {brown_horses_to_attack} brown horses to attack + reinforcement: {reinforcement}, its local is:{x}")


# when the main type of horses is depleted this exception is raised and we change horse type
        except selenium.common.exceptions.NoSuchElementException:
            time_now = datetime.now()
            report_list.append(time_now)
            alert = "there were no more horses here - i tried to resolve the issue"
            report_list.append(alert)
            validate_village = driver.find_element(By.XPATH, '//*[@id="sidebarBoxVillagelist"]/div[2]/div[2]/div[2]/div/a/span/span[2]')
            validate_village.click()
            final_attack_reinforcement = random.randint(400, 500)
            input_different_horses = driver.find_element(By.XPATH, '//*[@id="troops"]/tbody/tr[1]/td[2]/input')
            input_different_horses.send_keys(white_horses_to_attack + final_attack_reinforcement)
            send_raid = driver.find_element(By.XPATH, '//*[@id="ok"]')
            send_raid.click()
            time.sleep(2)
            confirm_raid = driver.find_element(By.XPATH, '//*[@id="checksum"]')
            confirm_raid.click()
            new_line = f"there was an Error here! this oasis has:{troops_check}, its power is {oasis_total_animal_power} i recommend {white_horses_to_attack} horses to attack, its local is:{new_list[x]}"
            x += 1
            report_list.append(new_line)
            print(f"power is {oasis_total_animal_power} i recommend final attack: {white_horses_to_attack + final_attack_reinforcement}, its local is:{x}")

# at the very end we can see the report list of all the attacks (i sometimes change this section to send the report by email)
print(report_list)



