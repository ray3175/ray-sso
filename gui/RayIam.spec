# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew


block_cipher = None


a = Analysis(['run.py'],
             pathex=['E:\\git\\ray-iam\\gui'],
             binaries=[],
             datas=[],
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
          [],
          exclude_binaries=True,
          name='RayIam',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='ray-iam.ico')
coll = COLLECT(exe, Tree('E:\\git\\ray-iam\\gui\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
			   *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='RayIam')