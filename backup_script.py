import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from datetime import date
import os
import subprocess
import argparse
import shutil


SCOPES = ["https://www.googleapis.com/auth/drive"]

def update_backup_on_drive(service, backup):
  response = service.files().list(
    q = "name='backup' and mimeType='application/vnd.google-apps.folder'",
    spaces = "drive"
  ).execute()

  if not response['files']:
    file = service.files().create(
      body = {
          "name": "backup",
          "mimeType": "application/vnd.google-apps.folder"
        },
      fields = "id"
    ).execute()

    folder_id = file.get("id")
  else:
    folder_id = response['files'][0]["id"]


  upload_file = service.files().create(
    body={
      "name": date.today().strftime("%y-%m-%d"),
      "parents": [folder_id]
    },
    media_body = MediaFileUpload(backup)
  ).execute()

  print("File has been successfully uploaded")


#"credentials.json"
def connect_and_upload_to_drive(backup, credential):
  if not credential:
    return
  
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          credential, SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    update_backup_on_drive(
      build("drive", "v3", credentials=creds),
      backup
    )
    
  except HttpError as error:
    print(f"An error occurred: {error}")


def perform_backup(source, backup_type = "full") -> str:
    date_str = date.today().strftime('%Y-%m-%d')
    backup_name = f"./backup-{date_str}.tar.gz"

    os.system(f"tar -czvf {backup_name} {source}")

    return backup_name


def move_file(src_path, dest_path):
    try:
        shutil.move(src_path, dest_path)
        print(f"File moved from {src_path} to {dest_path} successfully.")
    except Exception as e:
        print(f"Error moving file: {e}")

def remove_file(file_path):
    try:
        os.remove(file_path)
        print(f"File {file_path} removed successfully.")
    except Exception as e:
        print(f"Error removing file: {e}")

def main(args):
   if not args.source:
      return
   
   backup_name = perform_backup(args.source)

   if credentials := args.credentials:
      connect_and_upload_to_drive(backup_name, credentials)
      
   if destination := args.destination:
      move_file(backup_name, destination)
   else:
      remove_file(backup_name)
  

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Penguin's Rescue Backup Tool")
  parser.add_argument('--source', required=True, help="Source path to back up")
  parser.add_argument('--destination', required=False, help="Backup destination path")
  parser.add_argument('--credentials', required=False, help="Path to the Google Drive API credentials JSON file")
  args = parser.parse_args()
  
  main(args)
  