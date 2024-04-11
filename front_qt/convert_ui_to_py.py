import subprocess

# UI 파일과 변환될 Python 파일의 경로를 쌍으로 묶어 리스트로 정의
ui_files = [
    ("./static/main_app.ui", "./view/main_window.py"),
    ("./static/home.ui", "./view/home_view.py"),
]

# 각 UI 파일에 대해 pyuic5 명령어 실행
for ui_file, py_file in ui_files:
    command = f"pyuic5 -x {ui_file} -o {py_file}"
    subprocess.run(command, shell=True)

print("UI to Python conversion complete.")