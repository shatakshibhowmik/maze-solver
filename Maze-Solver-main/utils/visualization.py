#final with detecting start and end point in all four direction
import numpy as np
import imageio

def visualize_maze_animated(maze, traversal, path, start, end, final_path=False):
    img = np.zeros((maze.shape[0], maze.shape[1], 3), dtype=np.uint8)
    img[maze == 0] = [0, 0, 0]
    img[maze == 1] = [255, 255, 255]

    for node in traversal:
        img[node] = [100, 100, 255]

    if final_path:
        for node in path:
            img[node] = [0, 255, 255]
    else:
        for node in path:
            img[node] = [0, 0, 255]

    img[start] = [0, 255, 0]
    img[end] = [255, 0, 0]
    return img

import imageio
import cv2

def create_animation(frames, output_path="static/maze_a_star_with_traversal.gif", scale=2.2):
    """
    Creates an animated GIF from the given frames, resizing them slightly to make them bigger.

    Args:
        frames (list): A list of image frames (numpy arrays).
        output_path (str): Path to save the GIF.
        scale (float): Scaling factor to resize the frames.

    Returns:
        None
    """
    print("Creating animation...")

    # Resize frames to make the animation bigger
    resized_frames = []
    for frame in frames:
        height, width = frame.shape[:2]
        new_size = (int(width * scale), int(height * scale))  # Scale up the frame dimensions
        resized_frame = cv2.resize(frame, new_size, interpolation=cv2.INTER_LINEAR)
        resized_frames.append(resized_frame)
    
    # Save the resized frames as an animated GIF
    imageio.mimsave(output_path, resized_frames, duration=0.1)
    print(f"Animation saved as {output_path}")
