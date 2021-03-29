import pip

def install(package_name):
        try:
            pip.main(['install', package_name])
        except:
            print("Unable to install " + package_name)
def run():
    imports = ['pillow','pyscreenshot', 'pyautogui']
    for i in imports:
        install(i)
