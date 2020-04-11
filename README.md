<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
    <h1>
        How to use:
    </h1>
    <h2> Controls </h2>
    <ul>
        <li>Left/Right/A/D: Rotates the wheel</li>
        <li>Up/Enter/W: Opens a folder or activates an item</li>
        <li>Down/S: Goes out of a folder</li>
        <li>E: Edit the selected item</li>
        <li>Q: Delete an item</li>
    </ul>
    <h2>Items</h2>
    <p>Items are the things that you actually launch, they can open programs, open files, or open web-pages</p>
    <h3>Creating an item</h3>
    <p>To create an item go into the system folder, then choose "Add" from here there are many options</p>
    <ol>
        <li>Name: What the name of the item will be</li>
        <li>Image: What image the item will be in the menu (this needs to be an ~100x100px png image)</li>
        <li>Command: Tells the system what to run when the item is activated the commands are:
            <ul>
                <li>launch: will launch the executable specified</li>
                <li>open: will open a file in the default editor</li>
                <li>openwith: opens a file in the given program, assuming the program takes what file to open as the first argument</li>
                <li>run:Runs a command (like in command prompt)</li>
                <li>web: Opens the given url in the default web browser</li>
            </ul>
        </li>
        <li>Arguments: the arguments that the command will take, the command will not run if the arguments aren't correctly made
            <ul>
                <li>Launch takes an absolute path to an exe file</li>
                <li>Open takes an absolute path to any file</li>
                <li>OpenWith takes an absolute path to a file, then a "~", and then an absolute path to an exe file (notes.txt~notepad.exe)</li>
                <li>Run: takes an number of args and will run it like a command in command prompt</li>
                <li>Web: takes a single url</li>
            </ul>
        </li>
        <li>Folder: What folder to put the item in (Base is the top level)</li>
    </ol>
    <p> If an image isn't specified, the system will use the default icon image specified in the settings</p>
    <h2>Folders</h2>
    <p>A folder stores items to allow for organization, items can be in multiple folders and folders can be in folders</p>
    <h3> Creating a folder </h3>
    <p>In order to create a folder, navigate into system and then go into add, then, navigate to the "Folder" tab where the following fields are available</p>
    <ol>
        <li>Name: What name to display</li>
        <li>Image: The image that will show up in the wheel</li>
        <li>Items: the items in the folder</li>
        <li>Folders: What folders to show in the folder</li>
        <li>Parent Folder: What folder to put this one in, and what folder to go to when you go back (Base is the top level)</li>
    </ol>
    <p> If an image isn't specified, the system will use the default folder icon image specified in the settings</p>
    <h3>Editing the base folder</h3>
    <p>The base folder is where the system folder is contained, in order to edit it go to System and then go into Edit Base Folder, you will have two options</p>
    <ol>
        <li>Items: The items in the base folder</li>
        <li>Folders: The folders in the base folder (System folder cannot be removed)</li>
    </ol>

    <h2>Appearance Settings</h2>
    <h3>Editing the settings</h3>
    <p>In order to edit the appearance settings, go to system and then enter appearance where you can edit the following fields:</p>
    <ol>
        <li>Cursor Position: Where to display the cursor</li>
        <li>Transparency: How solid or transparent the wheel should be</li>
        <li>Default Icon image: What to display if an item doesn't have an image or the one specified isn't found</li>
        <li>Default Folder Image: What to display if a folder doesn't have an image or the one specified isn't found</li>
        <li>Wheel Color: The color of the wheel itself</li>
        <li>Inner Wheel Color: The color of the center of the wheel</li>
        <li>Name Color: The color of the name of items and folders</li>
        <li>Cursor Color: The color of the cursor that shows the currently selected item or folder</li>
    </ol>
    <h3>Resetting appearance settings</h3>
    <p>If you mess something up in the appearance settings, you can reset them by navigating to System, and then reset appearance settings</p>
    <h1>
        The following icons were used from other sources:
    </h1>
    <ul>
        <li>
            <a target="_blank" href="https://icons8.com/icons/set/back">Back icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        </li>
        <li>
            <a target="_blank" href="https://icons8.com/icons/set/settings">Settings icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        </li>
        <li>
            <a target="_blank" href="https://icons8.com/icons/set/paint-brush">Paint Brush icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        </li>
        <li>
            <a target="_blank" href="https://icons8.com/icons/set/cancel">Cancel icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        </li>
        <li>
            <a target="_blank" href="https://icons8.com/icons/set/folder-invoices">Folder icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        </li>
        <li>
            <a target="_blank" href="https://icons8.com/icons/set/plus">Plus icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        </li>
        <li>
            <a target="_blank" href="https://icons8.com/icons/set/question-mark">Question Mark icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        </li>
        <li>
            <a target="_blank" href="https://icons8.com/icons/set/sync-settings">Sync Settings icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        </li>
        <li>
            <a target="_blank" href="https://icons8.com/icons/set/data-backup">Data Backup icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        </li>
        <li>
            <a target="_blank" href="https://icons8.com/icons/set/settings-backup-restore">Restore icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        </li>
        <li>
            <a target="_blank" href="https://icons8.com/icons/set/edit-folder">Edit Folder icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        </li>
    </ul>
</body>
</html>
