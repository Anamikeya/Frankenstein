# Frankenstein Asset Manager

Frankenstein aims to be the best free open source Asset manager with feature support for 3D models, Audio, Video,
Images. It is used to browse your large assets library of 3d models, large textures, video footage and sound fx etc fast and dragdrop them into your application of choice.

### Why?
#### The initial issue that started this project
The problem I had initially was finding the right texture or 3d model quickly on my network storage. Even though performance to the drives where not terrible, windows explorer were really slow (same with finder). That's when I started to look around for an assets manager like connector or Adobe Bridge, but both of them cant handle 3d models very well or at all and are lacking in some way. They're both hard or impossible to customize as well.

This is why I started this project so my goal is to have a opensource 3dviewer, audio finder (for sound fx or foley), texture viewer and manager with drag and drop to whatever program you're using (Maya, 3Ds Max, Houdini, Blender etc). Making it opensource people can add the implementation for the software that they're using if necessary.

### How?
Frankenstein indexes files in selected folders to a locally stored index. The folders can be locally or on a network drive. The index process is fast and afterwards you can browse the files quickly instead of using windows explorer and wait for a folder to load only to realize that it's the wrong folder. 

Scanning a big assets folder on the NAS took around 120s in windows explorer when in the SQLite db it took 1s or less after indexed (don't even remember, it was ridiculous).

[Video showing basic functionality](https://www.youtube.com/watch?v=IhL5Lrm5JWU)

### GUI

TO edit the gui download the QT Designer (Link in bottom of readme) and just open the ui.ui file.

### Code

Crossplatform - Code is written with crossplatform in mind (only windows tested so far).

GUI: Pyside6

Database: SQLite (sqlite-utils to read/write)

### Teams
The program (as of now) is not built with teams in mind even though switching to a postgres db and version control would solve most of it. 


# TODO

## Features

* Drag & Drop functionallity
* Make thumbnails of files and store locally
* Combine Diffuse, Spec, Normalmap, Displacement Map etc files as one texture. 
* Add support for Audio files
* Add support for 3d files
* Add support for EXR files
* Version Control of files and assets
* DB sees if you moved or changed a folder. Maybe only when trying to access that file?
* Add tests in code
* Handling of proxy files
* Renaming and moving files (in thread please)
* Blender Addon
* Maya Addon
* Houdini Addon
* Postgres implementation for teams
* 

## Optimize

* Do scanning using QtThread or just thread, whats better?
* Only scan those files that have changed
* Comments and code-cleanup for easier code

# Documentation

[Pyside6 Documentation](https://doc.qt.io/qtforpython/contents.html)

[Sqlite-utils Documentation](https://sqlite-utils.datasette.io/en/stable/python-api.html)

[QT Designer Download](https://build-system.fman.io/qt-designer-download)
