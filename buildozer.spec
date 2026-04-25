[app]
title = Origen 58 Burger
package.name = fastfoodapp
package.domain = org.jdproducciones
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# --- ESTO ES LO QUE FALTABA ---
p4a.branch = master
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25.2.9519653
android.accept_sdk_license = True
android.skip_update = False
