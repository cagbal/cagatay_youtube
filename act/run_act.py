import time
import numpy as np
import torch
import mss
import cv2
from pynput.mouse import Controller as MouseController, Button
from pynput import keyboard, mouse 

from lerobot.policies.act.modeling_act import ACTPolicy
from pathlib import Path

import time
import numpy as np
import torch
import mss
import cv2
from pynput.mouse import Controller as MouseController, Listener as MouseListener, Button
from pynput import keyboard
import threading 
from pathlib import Path

PRETRAINED_POLICY_PATH = Path("best_model_loss_0.037")

ONE_HOT_VECTORS = {
    "task_A": [1.0, 0.0],
    "task_B": [0.0, 1.0]
}

current_task = "task_A"
ONE_HOT_VECTOR = ONE_HOT_VECTORS[current_task]

IMG_SIZE = (448, 448)

FPS = 10 

running = True

mouse_state = {
    'left': 0.0,
    'right': 0.0,
    'lock': threading.Lock()
}

# --- Callback for the mouse listener ---
def on_click(x, y, button, pressed):
    """Updates the global mouse_state dictionary on click events."""
    with mouse_state['lock']:
        if button == Button.left:
            mouse_state['left'] = 1.0 if pressed else 0.0
        elif button == Button.right:
            mouse_state['right'] = 1.0 if pressed else 0.0

def on_press(key):
    """Listens for ESC to stop and SHIFT to toggle the one-hot vector."""
    global running, ONE_HOT_VECTOR, current_task

    if key == keyboard.Key.esc:
        print("Stopping script...")
        running = False
        return False # Stop the listener thread

    if key in [keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r]:
        # Toggle the task
        if current_task == "task_A":
            current_task = "task_B"
        else:
            current_task = "task_A"

        ONE_HOT_VECTOR = ONE_HOT_VECTORS[current_task]
        print(f"\n--- Task toggled to '{current_task}' ---")
        print(f"New one-hot vector: {ONE_HOT_VECTOR}\n")


def main():
    global running
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # --- Load the pre-trained ACT policy ---
    if not PRETRAINED_POLICY_PATH.exists():
        print(f"Error: Model file not found at '{PRETRAINED_POLICY_PATH}'")
        print("Please update the PRETRAINED_POLICY_PATH variable in the script.")
        return
    
    policy = ACTPolicy.from_pretrained(PRETRAINED_POLICY_PATH)
    policy.n_action_steps = 20
    policy.eval()
    policy.to(device)
    policy.reset()


    # --- Initialize controllers and listeners ---
    mouse_controller = MouseController()
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()
    # Mouse listener is started later to avoid capturing setup clicks if any
    mouse_listener = mouse.Listener(on_press=on_press)
    mouse_listener.start()

    print("\n--- Inference Script Started ---")
    print(f"Initial task: '{current_task}' with one-hot vector: {ONE_HOT_VECTOR}")
    print("The model is now controlling the mouse.")
    print("\n>>> Press SHIFT to toggle the task <<<")
    print(">>> Press ESC to stop the script <<<")


    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screen_width = monitor["width"]
        screen_height = monitor["height"]

        while running:
            start_time = time.time()

             # --- 1. Capture and Preprocess Observation ---
            img = sct.grab(monitor)
            frame = np.array(img)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
            frame_resized = cv2.resize(frame_rgb, IMG_SIZE)
            frame_tensor = torch.from_numpy(frame_resized).to(torch.float32) / 255.0
            frame_tensor = frame_tensor.permute(2, 0, 1)

            # --- Get current mouse position ---
            current_x_abs, current_y_abs = mouse_controller.position
            current_x_norm = current_x_abs / screen_width
            current_y_norm = current_y_abs / screen_height

            # --- Get current click states from the listener ---
            with mouse_state['lock']:
                left_click_state = mouse_state['left']
                right_click_state = mouse_state['right']

            state_components = [
                current_x_norm,
                current_y_norm,
                left_click_state,
                right_click_state
            ] + ONE_HOT_VECTOR

            state_tensor = torch.tensor(state_components, dtype=torch.float32)

                      # --- 2. Prepare Tensors for the Model ---
            frame_tensor = frame_tensor.to(device, non_blocking=True).unsqueeze(0)
            state_tensor = state_tensor.to(device, non_blocking=True).unsqueeze(0)

            observation_input = {
                "observation.image.screen": frame_tensor,
                "observation.state": state_tensor,
            }

             # --- 3. Run Inference ---
            with torch.no_grad():
                action = policy.select_action(observation_input)

            action_numpy = action.squeeze(0).to("cpu").numpy()

             # --- 4. Execute the Action ---
            target_x_norm, target_y_norm, pred_left_click, pred_right_click = action_numpy
            
            target_x = int(target_x_norm * screen_width)
            target_y = int(target_y_norm * screen_height)
            
            target_x = max(0, min(screen_width - 1, target_x))
            target_y = max(0, min(screen_height - 1, target_y))

            mouse_controller.position = (target_x, target_y)

            if pred_left_click > 0.5:
                mouse_controller.press(Button.left)
            else:
                mouse_controller.release(Button.left)

            if pred_right_click > 0.5:
                mouse_controller.press(Button.right)
            else:
                mouse_controller.release(Button.right)

             # --- Maintain FPS ---
            elapsed_time = time.time() - start_time
            sleep_time = max(0, (1 / FPS) - elapsed_time)
            time.sleep(sleep_time)

    # Stop all listeners before exiting
    mouse_listener.stop()
    keyboard_listener.stop()
    print("--- Script Finished ---")


if __name__ == "__main__":
    main()

