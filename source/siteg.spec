# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['siteg.py'],
             pathex=['/home/amrit44/Desktop/final/static page generator'],
             binaries=[],
             datas=[('SitegCore/baseHTML','SitegCore/baseHTML'), ('SitegCore/site_files','SitegCore/site_files'), ('SitegCore/static','SitegCore/static'), ('SitegCore/templates','SitegCore/templates'), ('SitegCore/tree.set','SitegCore')],
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
          name='siteg',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='siteg')
