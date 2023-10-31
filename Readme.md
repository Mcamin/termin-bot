# Berlin Auslaenderbehorde Termin Bot

This python script uses Selenium library to automatically detect when an appointment is available at
the Ausländerbehörde Berlin for the selected visa service. Whenever an available day is found, it beeps.

To create instructions for setting up your Python project, including creating a virtual environment, installing requirements, running the script, and adjusting the `.env` file, you can include the following steps in your README file:

## Setup

Follow these steps to set up and run your Python project:

### 1. Prerequisites

Make sure you have the following prerequisites installed on your system:

- Python (version >= 3.10)
- pip (Python package manager)

### 2. Clone the Repository

First, clone the repository to your local machine using the following command:
p
```bash
git clone https://github.com/Mcamin/termin-bot
cd termin-bot
```

Replace `<repository_url>` with the URL of your Git repository and `<repository_directory>` with the desired folder name.

### 3. Create a Virtual Environment

It's a good practice to create a virtual environment to isolate your project's dependencies. To create a virtual environment, use the following commands:

```bash
# On Windows
python -m venv venv

# On macOS and Linux
python3 -m venv venv
```

This will create a virtual environment named `venv` in your project directory.

### 4. Activate the Virtual Environment

Activate the virtual environment using the appropriate command for your operating system:

- On Windows:
  ```bash
  .\venv\Scripts\activate
  ```

- On macOS and Linux:
  ```bash
  source venv/bin/activate
  ```

### 5. Install Project Dependencies

Once the virtual environment is activated, install the project dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 6. Rename `.env.default` to `.env`

You should have a `.env.default` file in your project directory. Make a copy of this file and rename it to `.env`. Adjust the configuration settings in the `.env` file according to your project's requirements. This file may contain sensitive information like API keys or database credentials, so be sure to keep it secure and never commit it to version control.

### 7. Run the Python Script

You can now run your Python script using the following command, assuming your main script is named `main.py`:

```bash
python main.py
```

Your Python project should now be set up and running. Make sure to consult your project's documentation for specific usage instructions and details about its functionality.

That's it! Your README should provide clear and concise instructions for setting up and running your Python project.


