
from lerobot.datasets.lerobot_dataset import LeRobotDataset
from pynput import mouse, keyboard 
import numpy as np
import mss
import threading
import time
import cv2

# --- Configuration ---
repo_id = "cagatayodabasi/drag_rectangle"
repo_root = "drag_rectangle"
fps = 10

TASKS = [
    "Drag the red square to the blue area",
    "Drag the red square to the yellow area"
]
TASK_ONE_HOT = [
    np.array([1.0, 0.0], dtype=np.float64),
    np.array([0.0, 1.0], dtype=np.float64)
]

# --- LeRobot Dataset Features Definition ---
features_obs = {
    "observation.image.screen": {
        "dtype": "video",
        "shape": [3, 1440, 2560],
        "names": ["channel", "height", "width"],
        "video_info": {
            "video.fps": fps,
            "video.is_depth_map": False
        }
    },
    "observation.state": {
        "dtype": "float64",
        "shape": (6,),
        "names": {
            "coord": ["x", "y"],
            "click": ["left", "right"],
            "task_id": ["task_0", "task_1"]
        }
    },
    "action": {
        "dtype": "float64",
        "shape": (4,),
        "names": {
            "coord": ["x", "y"],
            "click": ["left", "right"]
        }
    }
}

# --- Thread-Safe Input State Management ---
input_state = {
    'mouse_x': 0,
    'mouse_y': 0,
    'left_click': 0.0,
    'right_click': 0.0,
    'running': True,
    'task_to_start': None,
    'save_episode': False,
    'discard_episode': False,
    'lock': threading.Lock()
}

# --- Pynput Event Handlers ---
def on_move(x, y):
    with input_state['lock']:
        input_state['mouse_x'] = x
        input_state['mouse_y'] = y

def on_click(x, y, button, pressed):
    with input_state['lock']:
        if button == mouse.Button.left:
            input_state['left_click'] = 1.0 if pressed else 0.0
        elif button == mouse.Button.right:
            input_state['right_click'] = 1.0 if pressed else 0.0

def on_press(key):
    with input_state['lock']:
        try:
            if key.char == 'q':
                input_state['running'] = False
        except AttributeError:
            if key == keyboard.Key.space:
                input_state['task_to_start'] = 0
            elif key == keyboard.Key.shift or key == keyboard.Key.shift_r:
                input_state['task_to_start'] = 1
            elif key == keyboard.Key.enter:
                input_state['save_episode'] = True
            elif key == keyboard.Key.esc:
                input_state['discard_episode'] = True
                input_state['running'] = False


def main():
    dataset = LeRobotDataset.create(
        repo_id=repo_id,
        fps=fps,
        root=repo_root,
        features=features_obs,
        use_videos=True,
    )
    
    # ADDED: Create a mouse controller instance
    mouse_controller = mouse.Controller()

    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener.start()
    keyboard_listener.start()

    recording_state = 'WAITING'
    episode_count = 0
    current_task_id = None

    print("--- Data Recorder Initialized ---")
    print(f"  - SPACE: Start recording task 0: '{TASKS[0]}'")
    print(f"  - SHIFT: Start recording task 1: '{TASKS[1]}'")
    print("  - ENTER: Save the current episode.")
    print("  - ESC:   Discard current episode and exit.")
    print("  - 'q':   Quit.")
    print("\nStatus: WAITING")

    last_obs = None

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screen_width = monitor["width"]
        screen_height = monitor["height"]
        print(f"\nRecording on monitor of size: {screen_width}x{screen_height}")

        start_pos_x, start_pos_y = screen_width // 2, screen_height // 2

        is_running = True
        while is_running:
            start_time = time.time()
            
            img = sct.grab(monitor)
            frame = np.array(img)
            frame_transposed = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB).transpose(2, 0, 1)

            with input_state['lock']:
                current_x = input_state['mouse_x']
                current_y = input_state['mouse_y']
                left_click = input_state['left_click']
                right_click = input_state['right_click']

                if input_state['task_to_start'] is not None:
                    if recording_state == 'WAITING':
                        current_task_id = input_state['task_to_start']
                        print(f"Status: RECORDING Task {current_task_id}: '{TASKS[current_task_id]}'")
                        
                        mouse_controller.position = (start_pos_x, start_pos_y)

                        recording_state = 'RECORDING'
                        last_obs = None
                    input_state['task_to_start'] = None

                if input_state['save_episode']:
                    if recording_state == 'RECORDING':
                        print(f"Saving episode {episode_count}...")
                        dataset.save_episode()
                        print('\a', flush=True)
                        episode_count += 1
                        print("Episode saved! | Status: WAITING")
                        recording_state = 'WAITING'
                        current_task_id = None
                    input_state['save_episode'] = False

                if input_state['discard_episode']:
                     if recording_state == 'RECORDING':
                        print("Episode discarded. Exiting.")
                     else:
                        print("Exiting.")

                is_running = input_state['running']

                if recording_state == 'RECORDING':
                    normalized_x = current_x / screen_width
                    normalized_y = current_y / screen_height

                    base_state_and_action = np.array(
                        [normalized_x, normalized_y, left_click, right_click], 
                        dtype=np.float64
                        )
                    
                    task_one_hot_vector = TASK_ONE_HOT[current_task_id]
                    
                    full_state = np.concatenate([base_state_and_action, task_one_hot_vector])
                    
                    current_obs = {
                        'observation.image.screen': frame_transposed,
                        'observation.state': full_state
                    }
                    
                    if last_obs is not None:
                        task_description = TASKS[current_task_id]
                        last_obs['action'] = base_state_and_action
                        dataset.add_frame(last_obs, task=task_description)

                    last_obs = current_obs

                elapsed_time = time.time() - start_time
                sleep_time = max(0, (1/fps) - elapsed_time)
                time.sleep(sleep_time)


if __name__ == '__main__':
    main()