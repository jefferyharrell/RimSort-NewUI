rm -f ./resources/.DS_Store

python -m nuitka \
    --standalone \
    --enable-plugin=pyside6 \
    --macos-create-app-bundle \
    --macos-app-icon=./resources/AppIcon_a.png \
    --output-dir=./build \
    --include-data-dir=./resources=resources \
    --disable-console \
    NewUI.py
