
#  Job Changes Linkedin
ProxyCurl Data Scraper is a powerful yet easy-to-use tool for scraping LinkedIn profile data and analyzing employee job changes. The program is written in Python and leverages asynchronous HTTP requests to efficiently process large sets of profiles. It utilizes the ProxyCurl API to fetch LinkedIn profile data, providing valuable insights into job changes directly from LinkedIn profiles. Its high performance and user-friendly interface, combined with the accuracy provided by the ProxyCurl API, make it an essential tool for recruiters and HR professionals looking to keep track of job market trends.

![a](https://github.com/maciekstrach01/ProxyCurl_Data_Scraper/assets/146733279/1ac6e063-e07f-4360-9b29-27ace0d3a1e4)

![b](https://github.com/maciekstrach01/ProxyCurl_Data_Scraper/assets/146733279/0cd5d8b5-c6da-4d6e-91f1-e5d9755c988b)


## Features of the program

High Performance:

    Achieves a productivity rate of approximately 60 seconds for 100 profiles thanks to asynchronous HTTP requests.

User-Friendly:

    The user only needs to execute the provided EXE file, input the URLs of LinkedIn profiles, and specify the date from which to search for job changes.
    After clicking the "Fetch Profiles" button, a JSON file containing scraped LinkedIn profile data will be created in the same directory as the executable file.
    By clicking the "Analyze and Export" button, an Excel file will be generated in the same directory, listing employees who have changed jobs since the specified date.

Data Accuracy and Update:

    The tool provides reliable and updated information about job changes, ensuring users get the most current data.

Utilizes ProxyCurl API:

    The program uses the ProxyCurl API to fetch LinkedIn profile data, ensuring accurate and comprehensive information.
## Files and Structure

performance_test.exe: Executable file for users to run the data scraping and analysis.

performance_test.py: Python script that performs the main functionality of the program.

performance_test.spec: Configuration file for building the executable using PyInstaller.

profiles_data.json: JSON file where the scraped LinkedIn profile data is stored.

eligible_profiles.xlsx: Excel file generated after analyzing and exporting profiles of employees who have changed jobs.

build/ and dist/: Directories created by PyInstaller during the build process.
## 🛠 Skills
Python: The main programming language used to create applications.

Asynchronous Programming: Using asynchronous HTTP requests to process large data sets.

API Integration: Integration with the ProxyCurl API to retrieve data from LinkedIn.

Data Scraping: Collecting data from LinkedIn profiles.

Data Analysis: Analyzing data on user job changes.

JSON: Storing data in JSON format.

Excel: Exporting data to Excel files.

PyInstaller: Using PyInstaller to create an executable file from Python code.

Mingw64 (Git Bash): Using Git Bash to manage a Git repository in a Windows environment.

Git: A version control system used to manage code.

GitHub: A platform for hosting code and managing a project.


## Running Tests



1. Clone the repository from Github:

```
git clone https://github.com/maciekstrach01/ProxyCurl_Data_Scraper
```

2. Setup:

    Ensure you have the required dependencies installed. If using the Python script directly, you may need to set up a virtual environment and install necessary packages.

3. Running the Program:

    Remember to enter your own API key from the ProxyCurl profile in the performance_test.py file in the line API_KEY = ''  # API key defined in class individual for each profile in ProxyCurl
    Without this the program will not retrieve any data!
    Execute the performance_test.exe file.
    Input the URLs of LinkedIn profiles you wish to scrape.
    Specify the date from which to search for job changes.
    Click "Fetch Profiles" to start the scraping process. The JSON file will be created in the same directory as the executable.
    Click "Analyze and Export" to generate an Excel file containing profiles of employees who have changed jobs since the specified date.
