#!/usr/bin/env python

import os.path
import sys
import io
import shutil

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

class GoogleFTP:
    SCOPES = ['https://www.googleapis.com/auth/drive']

    PROJECT_DIRECTORY = os.path.dirname(__file__)
    # path to google api credentials and jwt token
    CRED_PATH = os.path.normpath(os.path.join(PROJECT_DIRECTORY, '../creds.json'))
    AUTH_PATH = os.path.normpath(os.path.join(PROJECT_DIRECTORY, '../token.json'))

    # available google api mimetypes
    MIMETYPES = {
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'odt': 'application/vnd.oasis.opendocument.text',
        'rtf': 'application/rtf',
        'pdf': 'application/pdf',
        'txt': 'text/plain',
        'zip': 'application/zip',
        'epub': 'application/epub+zip',
        'md': 'text/markdown',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'ods': 'application/x-vnd.oasis.opendocument.spreadsheet',
        'pdf': 'application/pdf',
        'zip': 'application/zip',
        'csv': 'text/csv',
        'tsv': 'text/tab-separated-values',
        'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'odp': 'application/vnd.oasis.opendocument.presentation',
        'pdf': 'application/pdf',
        'txt': 'text/plain',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'svg': 'image/svg+xml',
        'pdf': 'application/pdf',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'svg': 'image/svg+xml',
        'json': 'application/vnd.google-apps.script+json'
    }

    def __init__(self):
        self.creds = None
        # the file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        if os.path.exists(self.AUTH_PATH):
            self.creds = Credentials.from_authorized_user_file(self.AUTH_PATH, self.SCOPES)

        # if there are no valid credentials available attempt to login
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CRED_PATH, self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)

        # save the credentials for the next run
        with open(self.AUTH_PATH, "w") as token:
            token.write(self.creds.to_json())

        try:
            self.service = build("drive", "v3", credentials=self.creds)
        except HttpError as error:
            print(f"An error occurred: {error}")

    # list the files
    def FileList(self):
        try:
            results = (
                self.service.files()
                .list(
                    pageSize=10, fields="nextPageToken, files(name, mimeType, modifiedTime)"
                )
                .execute()
            )

            items = results.get("files", [])

            # if there are no files make sure the user knows this
            if not items:
                print("No files found.")
                return False

            # Print the file details
            print("Files:")
            if not items:
            for item in items:
                print(f"{item['name']} ({item['mimeType']}, {item['modifiedTime']})")

            return True

        except HttpError as error:
            # print the error message if something goes wrong
            print(f"An error occurred: {error}")
            return False

    # download files
    def FileDownload(self, download_file_name, save_name):
        try:
            # first lookup the file at see if it exists using the user given file name
            results = (
                self.service.files()
                .list(
                    q="name='" + download_file_name + "'",
                    pageSize=10,
                    fields="nextPageToken, files(name, id, mimeType)")
                .execute()
            )

            items = results.get("files", [])

            # if there are no files make sure the user knows this
            if not items:
                print("No files found.")
                return False

            item = items[0]

            # using the users destination file name determine
            # which mimetype google can convert the file to
            name = save_name.split('/')[-1]
            mimetype = self.MIMETYPES.get(name.split('.')[-1])

            # setup the download request
            request = self.service.files().export_media(
                fileId=item.get("id"), mimeType=mimetype
            )
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)

            # download the file
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}")

            file.seek(0)

            # write the received data to the file
            with open(save_name, 'wb') as f:
                shutil.copyfileobj(file, f)

            print(f"File Downloaded")

            return True

        except HttpError as error:
            # print the error message if something goes wrong
            print(f"An error occurred: {error}")
            return False

    def FileUpload(self, upload_file_name):
        try:
            # extract the file name out of the file path
            name = upload_file_name.split('/')[-1]
            mimetype = self.MIMETYPES.get(name.split('.')[-1])

            # create file metadata
            file_metadata = {'name': name}

            # create the request
            media = MediaFileUpload(upload_file_name, mimetype=mimetype)

            # upload the file
            file = self.service.files().create(
                body=file_metadata, media_body=media, fields='id'
            ).execute()

            return True

        except HttpError as error:
            # print the error message if something goes wrong
            print(f"An error occurred: {error}")
            return False

    def FileRemove(self, remove_file_name):
        print(remove_file_name)
        try:
            # determine if the user given file name exists
            results = (
                self.service.files()
                .list(
                    q="name='" + remove_file_name + "'",
                    pageSize=10,
                    fields="nextPageToken, files(name, id)")
                .execute()
            )

            items = results.get("files", [])

            if not items:
                print("No files found.")
                return False

            item = items[0]

            # if the file does exist remove it using the file id
            request = self.service.files().delete(
                fileId=item.get("id")
            ).execute()

            return True

        except HttpError as error:
            # print the error message if something goes wrong
            print(f"An error occurred: {error}")
            return False

# help the user use with this program
def help(option):
    match option:
        case "ls":
            print("Invalid use. Example ./main.py ls")
            print("(e.g. ./main.py ls")
        case "dcp":
            print("Invalid use. Example ./main.py dcp <file-name> <destination>")
            print("(e.g. ./main.py dcp 'hello world' ../download.txt")
        case "ucp":
            print("Invalid use. Example ./main.py ucp <source>")
            print("(e.g. ./main.py dcp ../download.txt")
        case "rm":
            print("Invalid use. Example ./main.py rm <file-name>")
            print("(e.g. ./main.py dcp 'hello world'")
        case _:
            print("Invalid use. Example ./main.py <option>")
            print("Possible options:")
            print(" - ls: list files")
            print(" - dcp: download a file")
            print(" - ucp: upload a file")
            print(" - rm: upload a file")

def main():
    # get command line arguments
    args = sys.argv

    # teach the user how to use the command
    if len(args) < 2:
        help("")
        quit()

    api = GoogleFTP()

    # determine how the user would like to use the program
    match args[1]:
        case "ls":
            if len(args) != 2:
                help("ls")
                quit()
            else:
                api.FileList()
        case "dcp":
            if len(args) != 4:
                help("dcp")
                quit()
            else:
                api.FileDownload(args[2], args[3])
        case "ucp":
            if len(args) != 3:
                help("ucp")
                quit()
            else:
                api.FileUpload(args[2])
        case "rm":
            if len(args) != 3:
                help("rm")
                quit()
            else:
                api.FileRemove(args[2])
        case _:
            help("")
            quit()

if __name__ == "__main__":
    main()
