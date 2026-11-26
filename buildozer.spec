[app]
title = Pixel Runner
package.name = pixelrunner
package.domain = com.jraymond.games
source.dir = .
source.include_exts = py,png,ttf,wav,ogg
version = 1.0
requirements = python3==3.11.6,hostpython3==3.11.6,pygame,pyjnius==1.5.0
orientation = landscape
fullscreen = 1
android.archs = arm64-v8a
android.ndk = 25b
android.accept_sdk_license = True
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/loading_screen.png

[buildozer]
log_level = 2
warn_on_root = 1
