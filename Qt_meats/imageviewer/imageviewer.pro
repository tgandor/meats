TARGET = imagesorter
HEADERS = imageviewer.h \
    directoryfeeder.h
SOURCES = imageviewer.cpp \
    main.cpp \
    directoryfeeder.cpp

# install
target.path = /usr/local/bin
INSTALLS += target
