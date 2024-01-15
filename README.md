## Phonebook App

This is a simple Phonebook application developed using Python and the Tkinter library. It allows users to create, edit, delete, search, and sort contacts stored in a CSV file.

### Features

- Add a contact: Users can add a new contact by providing the first name, last name, and phone number. The input is validated to ensure that the contact does not already exist and that the names contain only letters and the phone number contains only digits.
- Display contact details: Users can select a contact from the list and view their details, including the full name and phone number.
- Edit contact: Users can edit the details of an existing contact, including the first name, last name, and phone number. The changes are saved and reflected in the contact list.
- Delete contact: Users can delete a contact from the list, and the contact will be removed from the CSV file.
- Search contacts: Users can search for contacts by entering a name or phone number. The application will display the matching contacts in the list.
- Sort contacts: Users can sort the contacts by different criteria such as date added, first name, last name, or phone number. The sorting order can be set as ascending or descending.

### Dependencies

- Python 3.x
- tkinter library

### Usage

1. Clone the repository: `git clone [repository_url]`
2. Go to the project directory: `cd [project_directory]`
3. Install the dependencies (if necessary): `pip install -r requirements.txt`
4. Run the application: `python phonebook_app.py`

