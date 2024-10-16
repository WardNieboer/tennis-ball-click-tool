# -*- coding: utf-8 -*-
"""
Frame extraction and ball coordinate clicking script
"""

import cv2
import pandas as pd
import os

def click_ball_coordinates(frame_path, frame_count):
    def draw_red_x(frame):
        # Draw a red 'x' at the top-left corner of the frame in case the ball is not in the frame
        color = (0, 0, 255)  # Red
        cv2.line(frame, (0, 0), (10, 10), color, 2)
        cv2.line(frame, (0, 10), (10, 0), color, 2)

    def mouse_click(event, x, y, flags, param):
        nonlocal click_counter, ball_coordinates, frame
        if event == cv2.EVENT_LBUTTONDOWN:
            ball_coordinates[click_counter].append((x, y, frame_count))
            print(f"Clicked coordinates {click_counter + 1}: ({x}, {y})")
            
            # Draw a circle on the frame at the clicked coordinates
            colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0)]  # Red, Green, Blue, Yellow
            cv2.circle(frame, (x, y), 5, colors[click_counter], -1)  # Draw a filled circle

            click_counter += 1

    frame = cv2.imread(frame_path)
    draw_red_x(frame)  # Draw red 'x' before clicking
    cv2.namedWindow("Frame")
    cv2.imshow("Frame", frame)

    click_counter = 0
    ball_coordinates = [[] for _ in range(4)]
    cv2.setMouseCallback("Frame", mouse_click)

    while True:
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or click_counter == 4:
            break

    cv2.destroyAllWindows()

    return ball_coordinates

def extract_frames_with_ball_click(video_path, output_path, frame_interval):
    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Check if the video is successfully opened
    if not video.isOpened():
        print("Error opening video file!")
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Initialize variables
    frame_count = 0
    success = True
    all_ball_coordinates = []
    baseline_coordinates_L = []
    baseline_coordinates_R = []  
    top_net = []
    
    # Iterate over frames
    while success:
        # Read the next frame
        success, frame = video.read()

        # Check if the frame is valid
        if success and frame_count % frame_interval == 0:
            frame_path = os.path.join(output_path, f"frame_{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)
            print(f"Frame {frame_count} saved.")

            # Perform manual ball clicking for the current frame
            ball_coordinates = click_ball_coordinates(frame_path, frame_count)
            
            # Append the coordinates
            all_ball_coordinates.extend(ball_coordinates[0])
            top_net.extend(ball_coordinates[1])
            baseline_coordinates_L.extend(ball_coordinates[2])
            baseline_coordinates_R.extend(ball_coordinates[3])

        frame_count += 1

    # Release the video capture object
    video.release()

    # Create DataFrames from the coordinates
    df_ball_coordinates = pd.DataFrame(all_ball_coordinates, columns=['x', 'y', 'frame_counter'])
    df_baseline_L = pd.DataFrame(baseline_coordinates_L, columns=['x', 'y', 'frame_counter'])
    df_baseline_R = pd.DataFrame(baseline_coordinates_R, columns=['x', 'y', 'frame_counter'])
    df_top_net = pd.DataFrame(top_net, columns=['x', 'y', 'frame_counter'])

    return df_ball_coordinates, df_baseline_L, df_baseline_R, df_top_net

# Select participant and trial here
participant = 'P1'
trial_nr = '1'

# Example usage
video_path = f"E:/Tennis project/{participant}/trial{trial_nr}.avi"
output_path = f"E:/Tennis project/{participant}/frames_t{trial_nr}"

frame_interval = 1  # Extract every frame

df_ball_coordinates, df_baseline_L, df_baseline_R, df_top_net = extract_frames_with_ball_click(video_path, output_path, frame_interval)

# Save results to Excel
df_ball_coordinates.to_excel(os.path.join(output_path, 'ball_coordinates.xlsx'))
df_baseline_L.to_excel(os.path.join(output_path, 'baseline_L_coordinates.xlsx'))
df_baseline_R.to_excel(os.path.join(output_path, 'baseline_R_coordinates.xlsx'))
df_top_net.to_excel(os.path.join(output_path, 'top_net_coordinates.xlsx'))

print("Frame extraction and ball clicking completed.")
