import telebot
import cv2
import os
import time
import shutil
from threading import Thread
from ultralytics import YOLO

# Telegram bot information
TOKEN = '7438316929:AAEnEsHdgwDbzEPngtxqDquGfqXf7R7CG_4'
bot = telebot.TeleBot(TOKEN)

# Global variables and settings for YOLO and video
image_folder = 'images'  
captured_objects = set()  
last_capture_time = 0  
video_running = False  
last_sent_image = ""  
model = YOLO('yolov8n.pt')

# Video path
video_path = 'D:\\alarm bot\\video.mp4'

# Delete the 'images' folder if it exists and create a new empty folder
if os.path.exists(image_folder):
    shutil.rmtree(image_folder)  
os.makedirs(image_folder)  

# Function to detect and save images when a person is detected
def process_video():
    global last_capture_time, video_running, last_sent_image
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    video_running = True
    while cap.isOpened() and video_running:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        results = model(frame)

        # Check if there are any detections
        if results[0].boxes:
            for box in results[0].boxes:
                conf = box.conf[0]  
                cls = int(box.cls[0])  
                x1, y1, x2, y2 = map(int, box.xyxy[0])  

                # Check if the object is a person and confidence >= 70%
                if cls == 0 and conf >= 0.7:
                    # Draw bounding box and label
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)  # Red box
                    cv2.putText(frame, f'Warning', (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 3)  # Red text

                    # Create a unique ID for the bounding box
                    box_id = (x1, y1, x2, y2)

                    # Current time
                    current_time = time.time()

                    # Check if the object has been captured and 30 seconds have passed
                    if box_id not in captured_objects and (current_time - last_capture_time) >= 30:
                        last_sent_image = os.path.join(image_folder, f'captured_{int(current_time)}.png')
                        cv2.imwrite(last_sent_image, frame)  
                        print(f"Image saved: {last_sent_image}")
                        captured_objects.add(box_id)  
                        last_capture_time = current_time  

                        # Send notification to the Telegram bot
                        bot.send_message(chat_id, "Burglar detected!")
                        with open(last_sent_image, 'rb') as photo:
                            bot.send_photo(chat_id, photo)  

                    break  

        # Display the frame
        cv2.imshow('Burglar is detecting', frame)

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    video_running = False

# /start command to begin the object detection process
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global video_running, chat_id
    chat_id = message.chat.id  
    if not video_running:
        bot.reply_to(message, "Camera is running.")
        video_thread = Thread(target=process_video)
        video_thread.start()
    else:
        bot.reply_to(message, "Video detection is already running.")

# Start the bot
bot.polling()

