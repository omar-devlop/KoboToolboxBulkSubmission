# KoboToolbox Bulk Submission with Media

This Python script allows you to perform bulk submissions with media files to forms on KoboToolbox using the KoboToolbox API. It is a convenient tool for automating data submissions when working with KoboToolbox forms.

## Prerequisites

Before you can use this script, make sure you have the following:

- Python 3 installed on your system.
- Required Python libraries (requests, csv) installed. You can install them using pip:

  ```shell
  pip install requests
  ```

- A KoboToolbox account and an API token. You can obtain an API token by following the instructions on the [KoboToolbox website](https://support.kobotoolbox.org/api.html#getting-your-api-token).

## Setup

1. Clone this repository to your local machine or download the script file.

2. Open the script in a text editor or integrated development environment (IDE).

3. Configure the script by filling in the necessary information:

- `BASE_URL`: The base URL for your KoboToolbox instance.
- `TOKEN`: Your KoboToolbox API token.


## Usage

To use the script, follow these steps:

- You could run `reset.bat` file to delete all data files and create the required folders.

1. Ensure that your CSV files are correctly formatted. Each CSV file should contain data for a specific form, and the column headers should correspond to the form fields, and name it with target form `uid`, and place them within `Data` folder.

  - You could download the data from old form as XLS file with `XML values and headers` and with those options:
    - Include groups in headers
    - Group separator `/`
    - Include media URLs
    then save file as CSV from Excel.


2. Place your media files (images, videos, etc.) in the `Assets` subfolder within `Data` folder.

3. Open a terminal or command prompt and navigate to the directory containing the script.

4. Run the script

5. The script will process each CSV file found in the specified folder, creating XML-like submissions and uploading associated media files to KoboToolbox.

6. You will receive status messages indicating whether each submission was successful or encountered an issue.

## Notes

- The script utilizes the KoboToolbox API to create submissions. Make sure you have the necessary permissions `View Submissions` to submit data to the forms you target.

- The script extracts media file names from URLs ending with "\_URL" in your CSV data and attempts to upload the corresponding media files.
  - If you want prepare data manually make sure to add column with header ending with "\_URL" contains media file name with "\/" as prefix.

- Ensure that your media files are located in the `Assets` subfolder with the same file names as specified in the CSV data.

## Troubleshooting

If you encounter issues or errors while using the script, refer to the error messages for guidance. Common issues may include problems with API token authentication, incorrect file paths, or missing media files.

## License

This script is provided under the [MIT License](LICENSE).
