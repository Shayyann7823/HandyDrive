Hand-gesture controlled keyboard input for browser racing games (e.g. Turbo Moto Racer), using MediaPipe HandLandmarker + `pydirectinput`.

## Controls

| Gesture | Action | Key |
|---|---|---|
| Koi bhi haath dikhe (khula, fingers seedhe) | Accelerate | `up` (held) |
| Muthi (fist) | Brake / Reverse | `down` (held) |
| Koi haath na ho (screen se gayab) | Brake / Reverse (default) | `down` (held) |
| **Right hand**, sirf 1 ungli khuli (index) | Right turn | `right` (held) |
| **Right hand**, 2 ungliyan khuli (index + middle) | Left turn | `left` (held) |
| Left hand, ya koi aur finger count | Koi turn nahi | — |

## Important Notes

- **Sirf right hand** turn control karta hai. Accelerate/brake **kisi bhi haath** se kaam karta hai.
- Turn detection sirf 4 fingers count karta hai (index, middle, ring, pinky) — thumb exclude hai kyunke uska up/down detect karna unreliable hota hai.
- Camera flip (`cv2.flip`) ki wajah se MediaPipe handedness label reverse ho jata hai — code mein `hand_label == "Left"` check actually tumhara **real right hand** hai.
- Accelerate/brake aur turn dono `keyDown`/`keyUp` (real key hold) use karte hain — `pyautogui.press()` (tap-tap) ya `keyDown/keyUp` from plain `pyautogui` **kaam nahi karta tha** is game ke saath; `pydirectinput` ke real hold se hi reliably kaam kiya.

## Running the Script

1. Project folder mein jao aur venv activate karo:
  
   ```
2. Script chalao:
   ```powershell
   python main.py
   ```
3. Chhoti camera preview window top-left corner mein khulegi — **isko click mat karo**.
4. Game/Chrome window pe **click karo** taake wahi active/focused rahe.
5. Gesture start karo.

Agar keys game tak nahi pahunch rahin, terminal ko **Run as Administrator** se try karo.

## Files

- `main.py` — main control script
- `hand_landmarker.task` — MediaPipe hand landmark model file (required, same folder mein hona chahiye)