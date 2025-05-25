import io
import os
import uuid
import requests
import csv

BASE_URL = 'https://kc-eu.kobotoolbox.org'
TOKEN = '' # Enter your KoboToolbox account Token

folder_path = "Data"

SUMISSION_URL = f'{BASE_URL}/api/v1/submissions'
headers = {'Authorization': f'Token {TOKEN}'}

# Get formhub/uuid from api - need "View Submission" permission
def get_uuid_by_kpi_asset_uid(target_kpi_asset_uid):
    api_url = f"{BASE_URL}/api/v1/forms"

    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        for form in data:
            kpi_asset_uid = form.get('kpi_asset_uid')
            uuid = form.get('uuid')
            
            if kpi_asset_uid == target_kpi_asset_uid:
                return uuid
            
        return None  
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

# Format data in XML
def create_xml_submission(csv_row, _uuid, target_kpi_asset_uid, formhub_uuid):
    xml_content = f'''
    <payload id="{target_kpi_asset_uid}">
        <formhub>
            <uuid>{formhub_uuid}</uuid>
        </formhub>
        {csv_row}
        <meta>
            <instanceID>uuid:{_uuid}</instanceID>
        </meta>
    </payload>
    '''

    xml_content = xml_content.replace("\ufeff", "")

    return xml_content.encode('utf-8')

# Process data then submit it
def process_data(csv_row,target_kpi_asset_uid,formhub_uuid,index,image_file_names):
    _uuid = str(uuid.uuid4())
    xml_content = create_xml_submission(csv_row, _uuid, target_kpi_asset_uid, formhub_uuid)
    
    # Prepare XML file tuple
    xml_file_tuple = (_uuid, io.BytesIO(xml_content))
    
    # Prepare image file tuples
    image_tuples = []
    for image_file_name in image_file_names:
        image_tuples.append((f'{folder_path}/Assets/{image_file_name}', open(f'{folder_path}/Assets/{image_file_name}', 'rb')))
    
    # Combine XML and image file tuples into files dictionary
    files = {'xml_submission_file': xml_file_tuple}
    for image_tuple in image_tuples:
        files[image_tuple[0]] = image_tuple
    

    res = requests.Request(
        method='POST', url=SUMISSION_URL, files=files, headers=headers
    )
    session = requests.Session()

    res = session.send(res.prepare())

    if res.status_code == 201:
        print(f'Successfully submit data ({index})')
    else:
        print(f'Something went wrong 😢: {res.status_code}')
        print(files)
        print('---------------------------------------------------------------')


def extract_filename_from_url(url):
    return url.split("%2F")[-1]


def process_file(filename):
    print(f"Processing {filename}")
    # Open the input CSV file
    with open(filename, "r", encoding="utf-8") as csv_file:
        index = 1
        target_kpi_asset_uid = os.path.splitext(os.path.basename(filename))[0]
        formhub_uuid = get_uuid_by_kpi_asset_uid(target_kpi_asset_uid)
        if(formhub_uuid == None):
            print('formhub_uuid: None')
            print('Stopping Script ...')
            return
        
        csv_reader = csv.reader(csv_file)

        # Read the header row
        header_row = next(csv_reader)

        for row in csv_reader:
            data_dict = {}
            image_file_names = []  # Store image file names


            for header, value in zip(header_row, row):
            
                if '/' in header:
                    parts = header.split('/')
                    nested_dict = data_dict
                    for part in parts[:-1]:
                        nested_dict = nested_dict.setdefault(part, {})
                    nested_dict[parts[-1]] = value
                    # Extract file name from URLs ending with "_URL"
                    for key, value in nested_dict.items():
                        if key.endswith("_URL"):
                            filename = extract_filename_from_url(value)
                            if filename != '':
                                image_file_names.append(filename)  # Add image file name to the list
                else:
                    data_dict[header] = value

            # Extract file name from URLs ending with "_URL"
            for key, value in data_dict.items():
                if key.endswith("_URL"):
                    filename = extract_filename_from_url(value)
                    if filename != '':
                        image_file_names.append(filename)  # Add image file name to the list

            # Generate formatted XML-like output
            def generate_xml(data_dict, indent=""):
                xml_output = ""
                for key, value in data_dict.items():
                    if not(key.endswith("_URL")): # Ignore URL fields
                        if isinstance(value, dict):
                            xml_output += f"{indent}<{key}>\n"
                            xml_output += generate_xml(value, indent + "    ")
                            xml_output += f"{indent}</{key}>\n"
                        else:
                            xml_output += f"{indent}<{key}>{value}</{key}>\n"
                return xml_output


            formatted_xml = generate_xml(data_dict)

            process_data(formatted_xml,target_kpi_asset_uid,formhub_uuid, index, image_file_names)

            index = index + 1
    print(f"{filename} has been processed")


for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        filename = os.path.join(folder_path, filename)
        process_file(filename)
  