# Coding Thunder 

This is a Flask-based web application designed to help you manage your notes with AI summarization capabilities.

## Getting Started

Follow these steps to set up and run the application locally.

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone [https://github.com/AreebaShakeel12/Codingthunder.git](https://github.com/AreebaShakeel12/codingthunder.git)
cd Codingthunder


### Configuration

This application relies on a `config.json` file to store various application settings, including sensitive API keys and database connection details. For security reasons, this file is **NOT** included in the repository (it's listed in `.gitignore`) and should never be committed to version control.

**Steps to create and populate your `config.json` file:**

1.  **Create the `config.json` file:**
    * In the **root directory** of your project (the same folder where `app.py` and `requirements.txt` are located), create a new file named exactly `config.json`.

2.  **Add the basic structure:**
    * Copy the following JSON structure into your newly created `config.json` file. This defines the `params` object which holds all your configuration variables:

    ```json
    {
      "params": {
        "local_server": true,
        "local_uri": "mysql+pymysql://root:your_mysql_password@localhost/Codingthunder",
        "prod_uri": "mysql+pymysql://username:password@your_production_db_host/your_prod_db",
        "gmail_user": "your_gmail_username",
        "gmail_password": "your_gmail_app_password",
        "upload_location": "path/to/your/upload/folder",
        "fb_url": "https://facebook.com/codingthunder",
        "tw_url": "https://twitter.com/codingthunder",
        "gh_url": "https://github.com/codingthunder",
        "blog_name": "Coding Thunder",
        "tag_line": "Heaven for programmers",
        "no_of_posts": no of post you want to appear at once,
        "logo": "logo.svg",
        "admin_user": "your admin name (like ali)",
        "admin_password": "your admin password"
      }
    }
    ```

3.  **Populate with your specific details:**

    * **`"local_server": true/false`**:
        * Set to `true` if you are running the application on your local machine for development.
        * Set to `false` if you are deploying to a production server (though typically, this might be handled by environment variables in a production setup).

    * **`"local_uri": "mysql+pymysql://root:@localhost/smarthub"`**:
        * This is your **database connection string for local development**.
        * **`mysql+pymysql`**: Specifies the database type (MySQL) and the Python driver (`pymysql`).
        * **`root:@localhost`**: Your MySQL username (`root`) and an empty password (`:` before `@`). Replace `root` with your actual MySQL username if different. If you have a password for your MySQL user, it would be `username:password@localhost`.
        * **`/smarthub`**: The name of your database. Ensure you have a database named `smarthub` created in your MySQL server, or change this to your desired database name.

    * **`"prod_uri": "mysql+pymysql://root:@localhost/Codingthunder"`**:
        * This is intended for your **production database connection string**.
        * **Important:** In a real production deployment, this URI will be different (e.g., pointing to a cloud database service) and should ideally be managed via **environment variables** on your hosting platform, not hardcoded here. For a truly production setup, you would likely remove this from `config.json` and use `os.environ.get('DATABASE_URL_PROD')` in your Flask app.

    
    * **`"upload_location": "path/to/your/upload/folder"`**:
        * Specify the **absolute or relative path** to a directory where files (if your application handles uploads) will be stored.
        * Example (relative path, within your project): `"upload_location": "static/uploads"`
        * Example (absolute path for testing, Windows): `"upload_location": "C:\\Users\\YourUser\\Desktop\\flask\\taskmanager\\uploads"` (Note the double backslashes for Windows paths in JSON).
        * Ensure this folder exists and your application has write permissions to it.

