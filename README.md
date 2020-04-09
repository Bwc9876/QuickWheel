# QuickWheel

Access the programs and files you need faster

# How to use

## Controls
Upon launch you can use the arrow keys, or WASD to navigate
left and right arrow keys will rotate the wheel (this can be inversed in the settings)
the up arrow key launches or opens a file or enters a folder
the down arrow exits a directory
the escape key exits the program

## Basics
The Add item allows you to add items or folders to your wheel
### Items
An item requires a name and an image file (a ~100x100 png), if no image is provided, it will use the default from the settings
An item also takes a command, <b>the arguments of command are seperated by "\~" to allow for paths with spaces</b>  
+ <b>launch~{Absolute/Path/To/Exe}</b>: This will launch an exe file without any arguments  
+ <b>open~{Absolute/path/to/file}</b>: Opens an image, text document, video, etc. in the default editor 
+ <b>openwith~{Absolute/path/to/file}~{Absolute/path/to/program}</b>: Opens a file in a given editor (assuming the first argument is the file to open)
+ <b>run~{Absolute/path/to/file}</b>: Runs a file based off its extension (supports python, autohotkey) [[EDIT]]  
### Folders
You can also create folders to store items for orginization, a folder needs a name and an image, but also takes a string of the names of the items in it seperated by a ~  
A folder also takes a string like that, but for folders  
Finally, the parent directory, this is the directory that the folder will go to when it is backed out of  
### Additional Info  
An item or folder can be shown no matter what folder you're in by appending "\~\~" to the front of the name  
If for whatever reasoon you want to make a seperate button for exiting or adding, use "\~\~Add\~\~" and "\~\~Exit\~\~" as the commands  
#### Meta Commands
In addition to the regulaur commands, there are certain commands that perform tasks, most of these are used internally by system items, however they can be used if you really want to. A meta command is wraped in two \~'s so it would be "\~\~{MetaCommand}\~\~". Meta commands dont accept arguments.  
+ <b>Add</b>: Opens the window to add an item or folder
+ <b>Exit</b>: Exits the wheel
+ <b>Set</b>: Opens the settings window
+ <b>Back</b>: Goes up a directory (don't use in base directory)
+ <b>Dummy</b>: If able to, will print "Dummy command triggered" to console

  
