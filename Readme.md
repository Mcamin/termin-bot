# Berlin Auslaenderbehorde Termin Bot

This python script uses Selenium library to automatically detect when an appointment is available at
the Ausländerbehörde Berlin for the selected visa service. Whenever an available day is found, it beeps.


## Setup

Follow these steps to set up and run your Python project:

### 1. Prerequisites

Make sure you have the following prerequisites installed on your system:

- Python (version >= 3.10)
- pip (Python package manager)

### 2. Clone the Repository

First, clone the repository to your local machine using the following command:
```bash
git clone https://github.com/Mcamin/termin-bot
cd termin-bot
```

### 3. Create a Virtual Environment

To create a virtual environment, use the following commands:

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

You should have a `.env.default` file in your project directory. Make a copy of this file and rename it to `.env`. Adjust the configuration settings in the `.env` file accordingly.

### 7. Run the Python Script

You can now run your Python script using the following command:

```bash
python main.py
```




