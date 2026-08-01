# HandRacer Project Notes

## venv kya hai?
Ek alag, isolated "box" project ke liye jisme sirf isi project ki Python libraries install hongi — main system Python se alag. Faida: agar iss project mein specific versions ki libraries chahiye, wo doosre projects ko affect nahi karengi.

## "Activate" karna kya matlab hai?
Matlab: ab jo bhi commands chalaunga (jaise `pip install`), wo isi box (venv) ke andar jayengi, bahar wali main Python mein nahi.

Jab terminal mein `(venv)` likha dikhe shuru mein, matlab hum us box ke andar hain — jo bhi install karenge, sirf isi HandRacer project ke liye hoga.

## Ab tak kya kiya
1. Python install kiya (system pe)
2. Isolated environment (venv) banaya is project ke liye
3. Usko activate kiya

## Agla step
3 libraries install karni hain box ke andar (OpenCV, MediaPipe, pyautogui) — hand-tracking aur keyboard-control ke liye.

Command:
```
pip install opencv-python mediapipe pyautogui
```


## 3 libraries kis kaam ke liye install ki

1. **opencv-python (cv2)** — webcam se live video capture karne ke liye, aur har frame ko dikhane/process karne ke liye. Ye "aankhein" hain — camera ka feed lene aur screen pe dikhane ka kaam isi ka hai.

2. **mediapipe** — Google ki library, jo actual hand-detection karti hai. Har frame mein haath dhoondhti hai aur uski landmarks (fingers, palm, knuckles ke exact points) nikaal ke deti hai. Ye "dimaag" hai jo samajhta hai ke haath kahan hai aur kaisa hai.

3. **pyautogui** — detected haath ki position ko actual keyboard key press mein convert karke bhejti hai (jaise Left arrow, Right arrow). Ye "haath" hai jo system ko batata hai ke keyboard pe kya press hua.

**Simple flow:** opencv webcam se video le → mediapipe usme haath dhoondhe → pyautogui us haath ki position ke hisab se keyboard key press simulate kare → game usko receive kare.


## hand_landmarker.task file kya thi aur kyun download ki

Naya mediapipe (1.0.0) purane simple tarike (`mp.solutions.hands`) ki jagah "Tasks API" use karta hai. Is naye tarike mein hand-detection ka actual AI model khud library ke andar built-in nahi hota — alag se ek trained model file download karni padti hai jisme haath detect karne ka pura ML model hota hai (Google ne train kiya hua, hazaron hand images pe).

Ye file browser se download ki: `hand_landmarker.task`

Ye file project folder mein (venv ke bahar) rakhi gayi, aur code mein `model_asset_path="hand_landmarker.task"` line se usko point kiya — taake code ko pata ho ke actual "hath pehchanne wala dimaag" kahan rakha hai.

Bina is file ke, MediaPipe ko pata hi nahi chalta ke haath kaisa dikhta hai — ye file hi wo cheez hai jo real detection karti hai, baaki code sirf webcam se frame lekar isko deta hai aur result draw karta hai.