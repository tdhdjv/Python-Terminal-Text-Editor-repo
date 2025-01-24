# Terminal Text Editor

## Dependencies
- curse
  installation
  ```pip install windows-curses```

## Features
### 1. Edit Files
   - [x] add text
   - [x] delete text
   - [ ] select text
   - [ ] copy, paste text
### 2. Differing Modes
  - Default Mode:\
    can change to other modes
  - Insert Mode:\
    edit the text files
  - Command Mode:\
    can enter commands for saving, loading, and making new files
### 3. Save and Load Files
  - command for load: \
    `l + filepath` \
    `load + filepath` \
    `r + filepath` \
    `read + filepath` 
  - command for save: \
    `s`\
    `save`\
    `w`\
    `write`
  - command for new files: \
    `n`\
    `new`
### 4. HotKeys implementation
  - ```Ctrl```+```BackSpace```: Delete the whole word
  - ```Ctrl```+```←```: Move to the left by a whole word 
  - ```Ctrl```+```→```: Move to the right by a whole word
### 5. Resizing
  The Text Editor will automatically resize it's widgets to fit the screen
  ![Text editor Resize](https://github.com/user-attachments/assets/75ed511c-32d1-46f9-89e4-8a42b04ee53f)

