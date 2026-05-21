NeonFlux: App Disassembler/Hex Viewer
Created By JackTheGothGuy








**Summary**
This  Program Allows Users To Disassemble Any Coded Binary, Compiled Code And View The Hex And Data Layout Of The Program
Mainly Used By Reverse Engineers And Binary Analysts 















**1.	Libraries**
Tkinter: Visual Interface For The App Used To Make Interaction Easier


Capstone: Disassembly Framework/Disasm Engine For Binary Analysis


PEfile: .exe/Windows Reader, Inspector, Parser and Editor. Used In Malware Analysis


Threading: A Module Used To Run Multiple Operations Within A 	Process












2.	Themes
DORFic: Orange/White Classy Theme For a Bright Warm Look

Glossy Aqua: Nostalgic Water Theme Based On Windows 7 Aesthetic

Dark Frutiger: Cozy Version Of Glossy Aqua Featuring A Mix Of Gray, Blue And Pastel/Neon Green

Galaxy: The Galaxy Palette, Dark And Cozy

Y2K Girly: For The Pink Lovers Out There












How To Use Tutorial
1-Download Package From Github
https://github.com/JackTheGothGuy/NeonFlux-WindowsApp-Disassembler/tree/main
 

2-Go to dist/ and Open NeonFlux.exe
 

3-Click Open And Load Any Windows/Linux(MacOS Not Supported Yet) Executable File
 

4-Although Editing Is Possible, The Text Layout Is Still Not Perfectly Done, And Messing Up The Slightest Byte Can Break Your File, Make Sure To Create A Backup Copy Before Editing





5-Press Patch To Apply Changes To Your Binary
 


6-Save Your New File




Extra Info
 












Program Overview
Quick Action Buttons: Faster Navigation/Actions
 

File Details
 

Memory Sections
 




Strings(WIP): All Decoded Strings From The Binary That Resemble Any Human Readable String Will Be Extracted Here, However As For The Current State This Functionality Does Not Work As Intended
 








Disassembly Tab:
Format: [Address Offset] [Hex Binary] [Decoded Assembly]
Simply The Program Converts Hex From the .text (the place in memory where the code is written) And Converts it Into “Human Readable” Disassembly
 





HxD Style Hex Editor: With Rom Space To Avoid Overflows, Still Not Recommended To Edit, 
 

Conclusion
Although This Tool Is Very Experimental, In Its Early State And Very Unstable, It Works As A Good Base For More Features In The Future And Serves As A Good Basic Tool For Lightweight Reverse Engineering
