from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import messagebox

import os
from download_audio import download_audio
import time
import subprocess


# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--window-size=1920x1080")  # Set window size
chrome_options.add_argument("--no-sandbox")  # Run Chrome without sandboxing
chrome_options.add_argument("--disable-dev-shm-usage")  # Reduce resource usage

# Initialize WebDriver with headless mode enabled
driver = webdriver.Chrome(options=chrome_options)
cookies = driver.get_cookies()

# Open YouTube
driver.get('https://www.youtube.com')

# Wait for the page to load
time.sleep(2)


def checking_if_file_exists(location):
    if os.path.exists(location):
        print(f"File exists: {location}")
        return True
    else:
        return False

# def search_video():
#     query = search_box.get()
#     searching(query)
#     titles, hrefs = get_video_elements()
#     # Here, you'd call your search function
#     print(f"Searching for: {query}")
#     return titles, hrefs
def genrating_file_path(name):
    return f"/home/sarvesh/Documents/personal/audio_box/box_/audio/{name}.mp3"


def getting_url(index):
    return video_href[index]


def playing_audio(location):
    # vlc_command = ["vlc", "--intf", "dummy", "--play-and-exit", location]
    vlc_command = ["vlc", "--intf", "dummy", "--extraintf", "rc", "--volume", "256", "--play-and-exit", location]

    print("Playing now....")
    # process = subprocess.Popen(vlc_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process = subprocess.Popen(vlc_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print("Press 'p' to pause/play, 'q' to quit")
    while True:
        user_input = input("Enter a command (p to pause/play, q to quit): ")

        if user_input == 'p':
            # Send 'pause' command to VLC (it toggles between play and pause)
            process.stdin.write(b"pause\n")
            process.stdin.flush()
            print("Toggled pause/play.")

        elif user_input == 'q':
            # Stop VLC and exit
            process.stdin.write(b"stop\n")
            process.stdin.flush()
            process.terminate()
            print("Exiting.")
            break

    stdout, stderr = process.communicate()
    # print("VLC Output:", stdout.decode())
    # print("VLC Errors:", stderr.decode())


def searching(query):
    # # Find the search box using its name attribute
    # search_box = driver.find_element(By.NAME, 'search_query')
    # search_box.clear()  # Clear any previous text
    #
    # # Type the query and submit
    # search_box.send_keys(query)
    # search_box.send_keys(Keys.RETURN)
    # search_box.clear()  # Clear any previous text
    # # Wait for the search results to load
    # try:
    #     WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, '//a[@id="video-title"]'))
    #     )
    # except Exception as e:
    #     print(f"Error: {e}")
    #     driver.quit()
    #     exit()
    while True:
        try:
            search_box = driver.find_element(By.NAME, 'search_query')
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            search_box.clear()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[@id="video-title"]'))
            )
            return  # Exit the function if search is successful
        except Exception as e:
            print(f"Error during search: {e}")
            print("Search failed. Please check your connection or the search query.")
            user_input = input("Would you like to try again? (y/n): ")
            if user_input.lower() != 'y':
                print("Exiting search.")
                driver.quit()
                exit()  # Exit the program if user chooses not to retry
            else:
                print("Retrying search...")
                time.sleep(2)  # Optional: Wait before retrying
                continue


def get_video_elements():
    # Find all video elements on the page
    video_elements = driver.find_elements(By.XPATH, '//a[@id="video-title"]')
    # Extract and print the titles of all videos
    temp_video_titles = [video.get_attribute('title') for video in video_elements]
    temp_video_href = [video.get_attribute('href') for video in video_elements]
    return temp_video_titles, temp_video_href


while True:
    # Get search query from user input
    print("\n\n")
    print("type 'exit' for ofcourse exit ;)")
    search_query = input("Search: ")

    if search_query.lower() == 'exit':
        break

    searching(search_query)
    time.sleep(2)

    video_titles, video_href = get_video_elements()
    base_url = 'https://www.youtube.com'

    if not video_titles:
        print("No videos found. Please check your search query.")
    else:
        for i, title in enumerate(video_titles):
            print(i + 1, title)
        print("\n\n")

        try:

            index_input = input(
                "Enter a index number to play the title or press 0 to search again and you already know about exit : ")

            if index_input.lower() == "exit":
                break

            try:
                index = int(index_input)
                if index == 0:
                    continue

                elif 1 <= index <= len(video_titles):
                    title_name = video_titles[index - 1]
                    url = getting_url(index - 1)
                    path = genrating_file_path(title_name)

                    if checking_if_file_exists(path):
                        playing_audio(path)

                    else:
                        download_audio(url, title_name)
                        playing_audio(path)
                else:

                    print("Invalid index number. Please try again.")

            except ValueError:

                print("Please enter a valid number.")

        except Exception as e:
            print(e)

# def about_app():
#     messagebox.showinfo("About", "Audio Player\nDeveloped by Sarvesh © 2024")
#
# # Create the main application window
# app = tk.Tk()
# app.title("MelodyNectar")
#
# about_button = tk.Button(app, text="About", command=about_app)
# about_button.pack(side=tk.BOTTOM)
# # Create and place the search box
# search_box = tk.Entry(app, width=50)
# search_box.pack(pady=10)
#
# search_button = tk.Button(app, text="Search", command=search_video)
# search_button.pack()
#
# # Play and Pause buttons
# play_button = tk.Button(app, text="Play", command=play_audio)
# play_button.pack(side=tk.LEFT, padx=10)
#
# pause_button = tk.Button(app, text="Pause", command=pause_audio)
# pause_button.pack(side=tk.LEFT, padx=10)
#
# # Create a Listbox to display search results
# result_list = tk.Listbox(app, width=80, height=20)
# result_list.pack(pady=10)
#
# # Start the Tkinter event loop
# app.mainloop()
# Close the browser
driver.quit()
