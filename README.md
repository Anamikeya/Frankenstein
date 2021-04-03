# Frankenstein
Asset manager with feature support for 3D models, Audio, Video, Images

###System Requirements
I've only tested on windows, but written "everything" to work crossplatform with pathlib etc.

#Goals
* Database (indexer) of files and folder
* DB sees if you moved or changed a folder. Maybe only when trying to access that file? 
* Refresh function
* Add folders to "watchlist"
* Add tests


#Database

Sqlite3 using sqlite-utils to read write data. 

The database.db file (sqlite) contains tables of each folder that's indexed. 
