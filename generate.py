import os
import csv

# Text Metadata
depends_file = 'depends.csv'
status_file = 'Status.csv'
owners_file = 'Owners.csv'
uuid_file = 'UUID.csv'

# Create Folders and Files
def create_dependency_directories():
    # Read UUID.csv
    uuid_mapping = {}
    with open(uuid_file, 'r') as uuid_csv:
        reader = csv.DictReader(uuid_csv)
        for row in reader:
            uuid_mapping[row['name']] = row['uuid']

    # Read Owners.csv
    owners = {}
    with open(owners_file, 'r') as owners_csv:
        reader = csv.DictReader(owners_csv)
        for row in reader:
            owners[row['component']] = row['name']

    # Read depends.csv
    dependencies = {}
    with open(depends_file, 'r') as depends_csv:
        reader = csv.DictReader(depends_csv)
        for row in reader:
            component = row['component']
            depends_on = row.get('depends_on', '')
            if depends_on:
                dependencies[component] = depends_on.split(',')
            else:
                dependencies[component] = []

    # Read Status.csv
    status_info = {}
    with open(status_file, 'r') as status_csv:
        reader = csv.DictReader(status_csv)
        for row in reader:
            component = row['component']
            status = row['status']
            notes = row['notes']
            status_info[component] = (status, notes)

    # Create Folders and Files for Components
    for component in dependencies.keys():
        # Get UUID
        uuid = uuid_mapping.get(component, '')

        # Create Folder
        component_folder = os.path.join(uuid)
        os.makedirs(component_folder, exist_ok=True)

        # Create Info.txt
        with open(os.path.join(component_folder, 'Info.txt'), 'w') as info_file:
            info_file.write(f"Name: {component}\n")
            info_file.write(f"UUID: {uuid}\n")
            owner = owners.get(component, '')
            info_file.write(f"Owner: {owner}\n")
            status, eta = status_info.get(component, ('', ''))
            info_file.write(f"Status: {status}\n")
            info_file.write(f"Notes: {notes}\n")

        # Create Dependencies.txt
        with open(os.path.join(component_folder, 'Dependencies.txt'), 'w') as dep_file:
            dependencies_list = dependencies.get(component, [])
            for dependency in dependencies_list:
                dep_file.write(dependency + '\n')

# Run
create_dependency_directories()
