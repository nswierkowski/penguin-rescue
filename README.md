# Penguin Rescue: Your Linux Backup Buddy


Penguin Rescue is a Python script designed to streamline and secure your Linux system backups. It offers two flexible saving options:

1. Google Drive Integration: Store your backups securely in the cloud by providing Google Drive API credentials.
2. Local Storage: Back up to a specified directory on your local machine for easy access.

Easy as One, Two, Rescue!

## Installation:

Ensure you have Python and pip (the package installer) installed. Open a terminal and run:

```
pip install -r requirements.txt
```


## Running the Script:

Use the following command in your terminal, replacing placeholders with your actual details:

```
python backup_script.py --source <source_directory> [--destination <destination_path>] [--credentials <credentials_file>] [--type <backup_type>]
```

## Flags Explained:

--source <source_directory> (Required): The path to the directory you want to archive.

--destination <destination_path> (Optional): The desired location to save the archive. If omitted, the script prompts for confirmation.

--credentials <credentials_file> (Optional): The path to your Google Drive API credentials JSON file (required for cloud backup).

## Important Notes:

If neither --destination nor --credentials is provided, the script won't save your backup.

Consult the script's documentation for detailed instructions on obtaining Google Drive API credentials.

## Start Backing Up with Confidence!
