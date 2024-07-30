## About

This is a small cli application that integrates with Google Drive. The application is able to perform the following tasks:

1. Authenticate the user using OAuth 2.0.
2. List files in the user’s Google Drive.
3. Upload a file to the user’s Google Drive.
4. Download a file from the user’s Google Drive.
5. Delete a file from the user’s Google Drive

Here's why:
* Allows the user to quickly manage their google drive from the terminal
* Improves efficiency by preventing the user from having to switch away from their terminal

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

Install dependencies using the following methods.
* Git
* Python 3.10.7 or greater
* The pip package management tool
* A Google Cloud project.
* A Google account with Google Drive enabled.

### Installation

1. Clone the repo
   ```sh
   git clone git@github.com:Jorgensonnj/google-ftp.git
   ```
2. Install python packages
   ```sh
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```
   or
   ```sh
   sudo pacman -S python-google-api-python-client python-google-auth-httplib2 python-google-auth-oauthlib
   ```
3. Create [Google Account](https://developers.google.com/workspace/guides/create-project) with Google Drive API enabled
4. Create [Google Cloud Project](https://developers.google.com/drive/api/quickstart/python)
5. Save the downloaded JSON file as `creds.json`, and move the file to your google-ftp project directory

## Usage

Here are some examples of the cli in use

* Listing all files
  ```sh
  ./main.py ls
  ```
* Uploading a file
  ```sh
  ./main.py ucp ~/test.docx
  ```
* Downloading a file
  ```sh
  ./main.py dcp "test.docx" ~/test.docx
  ```
* Removing a file
  ```sh
  ./main.py rm "test.docx"
  ```
