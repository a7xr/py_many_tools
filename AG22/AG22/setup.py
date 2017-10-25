# -*- coding: cp1252 -*-
from distutils.core import setup
import py2exe
import os
import sys
import subprocess
import shutil


#data_files = ["CONTROLES_data_FORMATAGE.sql","CONTROLES_shema_FORMATAGE.sql","CONTROLESTACQ_DATA_FORMATAGE.sql","CONTROLESTACQ_SHEMAFORMATAGE.sql","EXPORT_SCHEMA_FORMATAGE.sql"]
#setup(zipfile = None,windows=[dict(script = 'menusGJP001.py', icon_resources = [(0, ico_file)])])
setup(options = {"py2exe": {"compressed": 0, "optimize": 0, "bundle_files": 1, 'dll_excludes': ['w9xpopen.exe'] } },
    zipfile = None,name="Saisie Coupons ",
      version="1.0",
      description="Outils formatage [Author: Harifetra_IAM]",
      author="Harifetra",
        windows=[{
            "script": "SGC_AG22_ASSEMBLAGE.py", "icon_resources": [(0x0004,"icone.ico")]
        }],)
