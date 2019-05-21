# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\ajun\\WorkSpace\\15alert'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['./hooks'],
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
          [],
          exclude_binaries=True,
          name='15Alert',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='hiyoko.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='15Alert')
