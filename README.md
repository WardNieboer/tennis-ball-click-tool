# tennis-ball-click-tool
This repository contains a tool for extracting frames from video files and manually annotating tennis ball and court coordinates using mouse clicks. The tool processes frames from tennis match videos, allowing users to click specific locations in the frame and export the coordinates for further analysis.

Features

   - Extract frames from a video at a specified interval.
   - Click to annotate four key points (ball, top of the net, left baseline, right baseline) for each frame.
   - Save the annotated coordinates and export them as Excel files for later analysis.

Requirements

This project requires Python and the following libraries:

   - opencv-python
   - pandas

Usage

To run the tool, modify the script to specify the participant and trial number in the extract_frames_with_ball_click function. Here's an example:

git clone https://github.com/WardNieboer/tennis-ball-click-tool.git
cd tennis-ball-click-tool

python

# Select participant and trial here
participant = 'P1'
trial_nr = '1'

# Example usage
video_path = f"D:/Tennis project/{participant}/trial{trial_nr}.avi"
output_path = f"D:/Tennis project/{participant}/frames_t{trial_nr}"
frame_interval = 1  # Extract every frame

df_ball_coordinates, df_baseline_L, df_baseline_R, df_top_net = extract_frames_with_ball_click(video_path, output_path, frame_interval)

# Save results to Excel
df_ball_coordinates.to_excel(os.path.join(output_path, 'ball_coordinates.xlsx'))
df_baseline_L.to_excel(os.path.join(output_path, 'baseline_L_coordinates.xlsx'))
df_baseline_R.to_excel(os.path.join(output_path, 'baseline_R_coordinates.xlsx'))
df_top_net.to_excel(os.path.join(output_path, 'top_net_coordinates.xlsx'))

Once you have modified the script for your video files, run the Python script:

Parameters

   - video_path: Path to the input video file.
   - output_path: Directory where the extracted frames and output files will be saved.
   - frame_interval: Interval for extracting frames (e.g., 1 for every frame, 2 for every other frame).

Coordinate Clicking

   - The video frames will appear one by one.
   - Click four points in each frame:
        -First click: Ball position
        -Second click: Top of the net
        -Third click: Left baseline position
        -Fourth click: Right baseline position
   - After clicking all four points, the next frame will appear, or you can press 'q' to quit.

Output

The tool generates the following Excel files:

   - ball_coordinates.xlsx: Coordinates of the tennis ball.
   - baseline_L_coordinates.xlsx: Coordinates of the left baseline.
   - baseline_R_coordinates.xlsx: Coordinates of the right baseline.
   - top_net_coordinates.xlsx: Coordinates of the top of the net.
