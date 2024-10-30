# Django Gdrive Backup Tool

Django Gdrive Backup Tool is a Python utility for automating backups of Django applications. It creates a database dump and packages it with the media folder in a zip file, then uploads it to Google Drive. The tool supports multiple Django apps and includes a command-line interface for managing backups.

## Features

- **Database Backup**: Uses Django’s `dumpdata` to export the database.
- **Media Folder Backup**: Archives the media folder with the database dump.
- **Google Drive Upload**: Uploads the zip file to a designated Google Drive folder using the Drive API.
- **Multi-App Support**: Allows managing and backing up multiple Django apps.

## Setup

### Prerequisites

1. **Python**: Make sure Python is installed on your system.
2. **Google API Client Secret**:
   - Go to the [Google Developer Console](https://console.developers.google.com/).
   - Enable the Google Drive API.
   - Download the `client_secret.json` file and place it in your project directory (Note: The secret file needs to be exactly `client_secret.json`.).

### Installation

1. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Authorize the App**: Run the `initiate` command to authorize the app with your Google Drive account.
   ```bash
   python main.py initiate
   ```
   This command will:
   - Prompt for Google authorization and create `token.pickle` for future use.
   - Create a root backup folder on Google Drive.
   - Generate a `config.json` file locally to store the root folder ID and Django app configurations.

### Adding Django Apps

To configure multiple Django apps for backup, use the `add-app` command:

```bash
python main.py add-app <app_path> <python_path> <media_path>
```

Replace the placeholders:
- `<app_path>`: Path to your Django project.
- `<python_path>`: Path to the Python interpreter that the django app uses.
- `<media_path>`: Path to the media folder in your Django app.

### Performing a Backup

To back up a specific Django app, use the `backup-app` command:

```bash
python main.py backup-app <app name>
```

This command will:
- Generate a database backup using Django's `dumpdata`.
- Create a zip file containing the database JSON and media folder contents.
- Upload the zip file to Google Drive in the configured root folder.

## Automating Daily Backups

To automate daily backups, you can set up a cron job that runs in the virtual environment. 

1. Locate the Python path in your virtual environment:
   ```bash
   which python  # Use `where python` on Windows
   ```

2. Add a cron job to run the backup command daily. For example:
   ```bash
   crontab -e
   ```
   Add the following line, replacing `<venv_python_path>` and `<app name>` as needed:
   ```bash
   0 2 * * * /path/to/venv/bin/python /path/to/main.py backup-app <app name>
   ```

This cron job will run the `backup-app` command at 2 AM daily.

## Commands Overview

| Command                          | Description                                                |
|----------------------------------|------------------------------------------------------------|
| `main.py initiate`               | Initializes the app, authorizing Google Drive access.      |
| `main.py add-app <...>`          | Adds a Django app configuration for backup.                |
| `main.py backup-app <app name>`  | Backs up the specified app and uploads it to Google Drive. |

## Example Usage

```bash
source venv/bin/activate
python main.py initiate
python main.py add-app "/path/to/django/project" "/path/to/python" "/path/to/media"
python main.py backup-app my_app
```

## License

This project is licensed under the MIT License.