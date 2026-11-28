[app]
title = Pixel Runner
package.name = pixelrunner
package.domain = com.jraymond.games
source.dir = .
source.include_exts = py,png,ttf,wav,ogg
version = 1.0
requirements = python3==3.10.12,hostpython3==3.10.12,pygame
p4a.branch = develop
p4a.bootstrap = sdl2
orientation = landscape
fullscreen = 1
android.archs = arm64-v8a
android.api = 33
android.ndk = 25b
android.ndk_api = 24
android.accept_sdk_license = True
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/loading_screen.png

[buildozer]
log_level = 2
warn_on_root = 1
