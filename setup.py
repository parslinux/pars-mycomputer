#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

from setuptools import setup, find_packages


def create_mo_files():
    podir = "po"
    mo = []
    for po in os.listdir(podir):
        if po.endswith(".po"):
            lang = po[:-3]
            local_dir = os.path.join(podir, lang, "LC_MESSAGES")
            os.makedirs(local_dir, exist_ok=True)
            mo_file = os.path.join(local_dir, "pars-mycomputer.mo")

            subprocess.call(["msgfmt", os.path.join(podir, po), "-o", mo_file])
            mo.append((f"/usr/share/locale/{lang}/LC_MESSAGES", [mo_file]))
    return mo


changelog = "debian/changelog"
if os.path.exists(changelog):
    head = open(changelog).readline()
    try:
        version = head.split("(")[1].split(")")[0]
    except:
        print("debian/changelog format is wrong for get version")
        version = ""
    f = open("src/__version__", "w")
    f.write(version)
    f.close()

data_files = [
                 ("/usr/share/applications/",
                  ["tr.org.pars.mycomputer.desktop"]),
                 ("/usr/share/pars/pars-mycomputer/",
                  ["pars-mycomputer.svg"]),
                 ("/usr/share/pars/pars-mycomputer/src", [
                     "src/Main.py",
                     "src/MainWindow.py",
                     "src/DiskManager.py",
                     "src/FstabWriter.py",
                     "src/Unmount.py",
                     "src/UserSettings.py",
                     "src/__version__"
                 ]),
                 ("/usr/share/pars/pars-mycomputer/ui",
                  ["ui/MainWindow.glade"]),
                 ("/usr/share/pars/pars-mycomputer/autostart/",
                  ["autostart/pars-mycomputer-add-to-desktop"]),
                 ("/usr/share/pars/pars-mycomputer/css/",
                  ["css/style.css"]),
                 ("/etc/xdg/autostart",
                  ["autostart/pars-mycomputer-add-to-desktop.desktop"]),
                 ("/usr/bin/",
                  ["pars-mycomputer"]),
                 ("/usr/share/icons/hicolor/scalable/apps/", [
                     "pars-mycomputer.svg",
                     "pars-mycomputer-emblem-pars-symbolic.svg"
                 ]),
                 ("/usr/share/polkit-1/actions",
                  ["tr.org.pars.pkexec.pars-mycomputer.policy"])
             ] + create_mo_files()

setup(
    name="pars-mycomputer",
    version="0.1.0",
    packages=find_packages(),
    scripts=["pars-mycomputer"],
    install_requires=["PyGObject"],
    data_files=data_files,
    author="Pars Altyapı",
    author_email="dev@pars.org.tr",
    description="My Computer, UI for information and management of disks on your computer.",
    license="GPLv3",
    keywords="",
    url="https://www.pars.org.tr",
)
