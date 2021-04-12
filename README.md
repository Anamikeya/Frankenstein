# Frankenstein Asset Manager

Frankenstein aims to be the best free open source Asset manager with feature support for 3D models, Audio, Video,
Images.

Frankenstein indexes files in selected folders that can be locally or on a network drive to speed up browsing.

Code is written with crossplatform in mind (only windows tested so far). 

### Code

Crossplatform
GUI: Pyside6
Database: SQLite (sqlite-utils to read/write)

### Database

The database.db file (sqlite) contains tables of each folder that's indexed.

# TODO

## Features

* Make thumbnails of files and store locally
* Add support for Audio files
* Add support for 3d files
* Add support for EXR files
* DB sees if you moved or changed a folder. Maybe only when trying to access that file?
* Add tests in code

## Optimize

* Only scan those files that have changed
* Comments and code-cleanup for easier code


# Docs

[Pyside6 Documentation](https://doc.qt.io/qtforpython/contents.html)
[Sqlite-utils Documentation](https://sqlite-utils.datasette.io/en/stable/python-api.html)
