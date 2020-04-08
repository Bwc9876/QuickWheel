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
An item requires a name and the name of the image file (stored in the Images folder)
An item also takes a command, <b>the arguments of command are seperated by "\~" to allow for paths with spaces</b>  
  -<b>launch~{Absolute/Path/To/Exe}</b>: This will launch an exe file without any arguments  
  -<b>open~{Absolute/path/to/file}</b>: Opens an image, text document, video, etc. in the default editor  
  -<b>run~{Absolute/path/to/file}</b>: Runs a file based off its extension (supports python, autohotkey) [[EDIT]]  
### Folders
You can also create folders to store items for orginization, a folder needs a name and an image, but also takes a string of the names of the items in it seperated by a ~  
A folder also takes a string like that, but for folders  
Finally, the parent directory, this is the directory that the folder will go to when it is backed out of  
### Additional Info  
An item or folder can be shown no matter what folder you're in by appending "~~" to teh front of the name  
If for whatever reasoon you want to make a seperate button for exiting or adding, use "~~Add~~" and "~~Exit~~" as the commands

  
