from selenium import webdriver

import urllib.request as req
import platform
import zipfile
import os

from pathlib import Path

WINDOWS = 'Windows'
LINUX = 'Linux'
MAC = 'Darwin'

root = str(Path(os.getcwd()).parent.parent)

ZIP_DOWNLOAD_PATH = f'{root}{os.sep}downloads{os.sep}driver.zip'
WINDOWS_DRIVER_PATH = f'{root}{os.sep}downloads{os.sep}chromedriver.exe'
LINUX_DRIVER_PATH = f'{root}{os.sep}downloads{os.sep}chromedriver'
MAC_DRIVER_PATH = f'{root}{os.sep}downloads{os.sep}chromedriver'

WINDOWS_DRIVER_LINK = 'https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_win32.zip'
LINUX_DRIVER_LINK = 'https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip'
MAC_DRIVER_LINK = 'https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_mac64.zip'


def get_driver():
    system = platform.system()

    if system == WINDOWS:
        if not os.path.exists(WINDOWS_DRIVER_PATH):
            download(WINDOWS_DRIVER_LINK)
        return _get_windows_driver()

    if system == LINUX:
        if not os.path.exists(LINUX_DRIVER_PATH):
            download(LINUX_DRIVER_LINK)

        return _get_linux_driver()

    if system == MAC:
        if not os.path.exists(MAC_DRIVER_PATH):
            download(MAC_DRIVER_LINK)
        return _get_mac_driver()

    raise Exception("Can't detect the OS name")


def _get_windows_driver():
    return webdriver.Chrome(WINDOWS_DRIVER_PATH)


def _get_mac_driver():
    return webdriver.Chrome(MAC_DRIVER_PATH)


def _get_linux_driver():
    os.chmod(f'{root}{os.sep}downloads{os.sep}chromedriver', 0o755)
    return webdriver.Chrome(LINUX_DRIVER_PATH)


def download(link):
    if not os.path.exists(root + os.sep + 'downloads'):
        os.makedirs(root + os.sep + 'downloads')
    with req.urlopen(link) as zip_file:
        with open(ZIP_DOWNLOAD_PATH, 'wb') as out_file:
            out_file.write(zip_file.read())
    zip_file = zipfile.ZipFile(ZIP_DOWNLOAD_PATH)
    zip_file.extractall(f'{root}{os.sep}downloads')
    zip_file.close()
    os.remove(ZIP_DOWNLOAD_PATH)
