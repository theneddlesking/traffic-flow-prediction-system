#Requires AutoHotkey v2.0

#Persistent
SetTitleMatchMode, 2  ; Makes it easier to match browser window titles
SetWorkingDir, %A_ScriptDir%  ; Ensures script works from its own directory
CoordMode, Mouse, Screen  ; Ensure coordinates are relative to screen

#Persistent
SetTitleMatchMode("Contains")  ; Makes it easier to match browser window titles
SetWorkingDir(A_ScriptDir)  ; Ensures script works from its own directory
CoordMode("Mouse", "Screen")  ; Ensure coordinates are relative to screen

; Load CSV file with Start and End coordinates
csvFile := "input_file.csv"
csvData := FileRead(csvFile)

Loop Parse, csvData, "`n", "`r"  ; Parse the CSV row by row
{
    ; Skip header row
    if A_Index = 1
        continue

    ; Parse the row
    fields := StrSplit(A_LoopField, ",")
    
    ; Read the coordinates from CSV
    start_lat := fields[1]
    start_long := fields[2]
    end_lat := fields[3]
    end_long := fields[4]

    ; Open Google Maps in browser
    Run("https://www.google.com/maps")
    WinWait("Google Maps")
    Sleep(2000)

    ; Input start and end coordinates into Google Maps search box
    Send(start_lat "," start_long "{Tab}" end_lat "," end_long "{Enter}")
    Sleep(3000)  ; Wait for Google Maps to load results

    ; Copy travel time from Google Maps (inspect the element beforehand to ensure accuracy)
    ; This part can be tricky as the exact coordinates or method for selecting text may vary
    MouseClick("Left", 450, 350)  ; Click on travel time (adjust coordinates)
    Sleep(500)
    Send("^c")  ; Copy travel time to clipboard

    ; Store the travel time from clipboard
    travel_time := Clipboard
    FileAppend(start_lat "," start_long "," end_lat "," end_long "," travel_time "`n", "output_file.csv")
    Clipboard := ""  ; Clear clipboard for next use

    ; Close Google Maps tab
    Send("^w")
    Sleep(1000)
}
ExitApp()
