TARGET = imagesorter
HEADERS = imageviewer.h \
    directoryfeeder.h \
    organize.h
SOURCES = imageviewer.cpp \
    main.cpp \
    directoryfeeder.cpp \
    organize.cpp

# install
target.path = /usr/local/bin
INSTALLS += target
