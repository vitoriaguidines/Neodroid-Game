# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/home/rodrigobarroso/Neodroid'],
             binaries=[],
             datas=[("audio", "audio"), ("img", "img"), ("PPlay", "PPlay"), ("level1_data.csv", "."),
                    ("level2_data.csv", "."), ("level3_data.csv", "."), ("level4_data.csv", "."),
                    ("level5_data.csv", "."), ("futura.ttf", ".")],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Neodroid',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )