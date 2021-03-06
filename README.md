# Easy Markov Chain Text Generation
***An implementation of the Markov Chain in python tuned for text generation with a simple CLI.***


## Getting Started
Download the release and place it in an empty folder. If you chose the .zip, extract it into the empty folder. Double-click the `Markov_Text_Generator_CLI.exe` or `Markov_Text_Generator_CLI.PythonPackaged.v0.3.exe` to start.
[***Downloads can be found here.***](https://github.com/PhlegethonAcheron/Easy_Markov_Chain_Text_Generation/releases/tag/v0.3-alpha)

## Using the CLI

The program needs the source text file to be in the same directory as the executable for the file to be found. *This will be fixed in a later version.* The entered filename __must__ be the filename only, not the path to the file. For example, `example_filename.txt` is valid, but `C:\Users\Username\example_filename.txt`will result in an error and crash the program. *This will also be fixed in a later version.*

## Entering Text at the Cursor
Option 3 will type the text generated by simulating the keypresses required to type those words, entering the text into whatever text input is currently focused.
Since the program simulates keypresses, caution is recommended to ensure that no unwanted action occurs. There is a 2-second delay before text starts being entered to allow the cursor to be placed in the intended text input area.

## Stopping the Program
To stop the program at any point while it is entering characters, simply move the mouse swiftly to the top left corner of the screen. Note that this only works if Option 3 has been selected to output text.
To stop the program at any point, enter <kbd>Ctrl</kbd> + <kbd>C</kbd>. This hotkey will work at any point in the program's operation.

## Currently-Known Bugs:
There are stability problems, and RAM usage graphs while the program is running look like a saw wave. RAM will likely be the limiting factor while the program is running.