# Intrusion Detection System Using YOLOv8

## Introduction

This project is an intrusion detection system using the YOLOv8 model. When a person is detected in the video, a Telegram bot sends a notification to the user along with a saved image.

## Installation

1. Install Anaconda and create a virtual environment:
   ```bash
   conda create -n yolo_bot python=3.9
   conda activate yolo_bot
   ```

2. Install the required libraries:
   ```bash
   pip install telebot opencv-python ultralytics
   ```

3. Download the YOLOv8 model:
   - You can download the model from [Ultralytics](https://github.com/ultralytics/yolov5/releases) and save it in the project directory.

## Usage

1. Edit the source code to change the `TOKEN` variable with your Telegram bot's token.
2. Update the video path in the source code.
3. Run the bot:
   ```bash
   python your_script.py
   ```
4. Send the `/start` command to the bot to initiate detection.

## Limitations

1. **Accuracy**: The YOLO model may not detect all objects or may produce false detections.
2. **Response Time**: There may be delays in sending notifications due to video processing and network speed.
3. **Video Dependency**: The quality of the video affects detection capability. Low-quality videos may lead to false detections.
4. **Object Limitation**: Currently, it only detects humans; expanding the model to include other object types is needed.
5. **Network Issues**: Notifications may not be sent if there is a network connection problem.

## Future Development

1. **Accuracy Improvement**: Upgrade the model with custom training data.
2. **Response Time Optimization**: Improve processing performance and response time.
3. **Feature Addition**: Support multiple users, video analysis, and keep a history of intrusions.
4. **User Interface**: Develop a GUI for easier bot configuration.
5. **Multilingual Support**: Provide notifications in multiple languages.
6. **IoT Integration**: Connect with IoT devices to create a comprehensive security system.
7. **Statistics Dashboard**: Provide reports on detection frequency and related information.
