# script.submerge
Kodi script to merge two subtitle SRT files of different languages into one file.

# Description of settings
The setting names are all pretty straight forward, but I've written descriptions off everything if anything happens to be confusing.

Note: The two subtitle files are referred to as "Master" and "Sub-Master". Master being the first file you choose, and Sub-Master being the second.
## Timing Options
- **Auto Shift**: Will align text lines from Master and Sub-Master which have equal beginnings and endings within an amount of time determined by the **time difference threshold** setting. This setting only shifts the timing of the Sub-Master file and uses the Master file as the base to compare. (*on/off*)
- **Time difference threshold**: Sets the threshold for how far apart lines need to be before not being aligned by **Auto Shift**. (*Whole positive number, 100 = 1 Second*)
- **Manually Shift Sub-Master**: Will shift the Sub-Master file by user determined amount of time. Applied before **Auto Shift** if both are enabled. (*on/off*) (*Whole number, 100 = 1 Second*)
- **Manually Shift Both**: Will shift the both the Master and Sub-Master files by user determined amount of time. (*on/off*) (*Whole number, 100 = 1 Second*)
## Text Options
Note: Colors are all in hexadecimal (RRGGBB)
#### Text Positioning and Styling
- **Font Size**: Subtitle text font size in pixels. (*Whole positive number*)
- **Master Location**: Location of the Master text. (*Top/Bottom*)
- **Sub-Master Location**: Location of the Sub-Master text. (*Top/Bottom*)
- **Outline Style**: What type of background the text will have. Note: Shadow, outline, and background can all be turned off by setting their width to 0. (*Outline and shadow/Solid box*)
#### Base Color Options
- **Master Color**: Inner/base color of Master text. (*Color*)
- **Sub-Master Color**: Inner/base color of Sub-Master text. (*Color*)
#### Outline/Background Options
- **Master Color**: Color of the outline/background for Master text. (*Color*)
- **Sub-Master Color**: Color of the outline/background for Sub-Master text. (*Color*)
- **Opacity**: Opacity percentage of the outline/background. (*Whole number, 0-100*)
- **Width**: How wide the outline/background will be. (*Whole number, 0-4*)
#### Shadow Options
- **Master Color**: Color of the shadow for Master text. (*Color*)
- **Sub-Master Color**: Color of the shadow for Sub-Master text. (*Color*)
- **Opacity**: Opacity percentage of the shadow. (*Whole number, 0-100*)
- **Width**: How wide the shadow will be. (*Whole number, 0-4*)
## File Options
- **Permanently Save Merged File**: Saves the merged file to a user determined location. Prompts for file name at the end of conversion. If disabled, files will be saved to Kodi's temp folder. (*on/off*) (*Folder Location*)
- **Automatically apply to current video**: Will automatically set the completed subtitle as the current subtitle, and then focus the player if a video is open. (*on/off*)
- **Warn File Overwrite**: Will warn the user if the program is about to overwrite an existing file. (*on/off*)
- **Preview files and edit settings before each merge**: Will open a text boxes with original Master and Sub-Master files and then open settings to allow for any changes. (*on/off*)
- **Open file search in temp folder**: Will open the select a file dialog in Kodi's temp folder. (This is where subtitle addons default to downloading subtitle files). If disabled, the dialog will open to a user specified location. (*on/off*) (*Folder Location*)
