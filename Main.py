import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
from Models.Persion import Person as pr

class PhonebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phonebook App")
        self.contacts = []
        self.show_contacts = []
        self.csv_file = "Datas\Contacts.csv"
        self.create_widgets()

    def create_widgets(self):
        
        self.contact_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.contact_listbox.bind('<<ListboxSelect>>', self.display_contact_details)
        self.load_contacts_from_csv(self.contact_listbox)
        
        button_add = tk.Button(self.root, text="Add Contact", command=self.show_add_contact_popup)
        button_save = tk.Button(self.root, text="Save Contacts", command=self.save_contacts)
        button_search = tk.Button(self.root, text="Search", command=self.search_contact)
        button_sort = tk.Button(self.root, text="Sort", command=self.show_sort_popup)
        
        button_add.grid(row=2, column=0, columnspan=2, pady=10)
        self.contact_listbox.grid(row=3, column=0, columnspan=2, pady=10)
        button_save.grid(row=5, column=0, columnspan=2, pady=10)
        button_search.grid(row=6, column=0, columnspan=2, pady=10)
        button_sort.grid(row=7, column=0, columnspan=2, pady=10)

    def show_add_contact_popup(self):
        add_popup = tk.Toplevel(self.root)
        add_popup.title("Add Contact")
        
        label_fname = tk.Label(add_popup, text="First Name:")
        label_lname = tk.Label(add_popup, text="Last Name:")
        label_phone = tk.Label(add_popup, text="Phone:")

        entry_fname = tk.Entry(add_popup)
        entry_lname = tk.Entry(add_popup)
        entry_phone = tk.Entry(add_popup)

        save_button = tk.Button(add_popup, text="Save", command=lambda: self.add_contact_from_popup(entry_fname.get(),entry_lname.get(), entry_phone.get(), add_popup))

        label_fname.grid(row=0, column=0, sticky=tk.E)
        entry_fname.grid(row=0, column=1)
        label_lname.grid(row=1, column=0, sticky=tk.E)
        entry_lname.grid(row=1, column=1)
        label_phone.grid(row=2, column=0, sticky=tk.E)
        entry_phone.grid(row=2, column=1)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

    def add_contact_from_popup(self, fname , lname , phone, add_popup):
        if self.input_error(fname,lname,phone):
                contact = pr(fname,lname,phone)
                self.contacts.append(contact)
                self.contact_listbox.insert(tk.END, f"{fname} {lname}")
                add_popup.destroy()
                self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "Name should contain only letters, and Phone should contain only digits.")
    
    def display_contact_details(self, event):
        selected_index = self.contact_listbox.curselection()
        if selected_index:
            selected_contact = self.contacts[selected_index[0]]

            # Create a popup window for contact info, edit, and delete options
            contact_info_popup = tk.Toplevel(self.root)
            contact_info_popup.title("Contact Information")

            # Labels
            label_name = tk.Label(contact_info_popup, text=f"{selected_contact.first_name}  {selected_contact.last_name}")
            label_phone = tk.Label(contact_info_popup, text=f"Phone: {selected_contact.phone_number}")

            # Buttons in contact info popup
            edit_button = tk.Button(contact_info_popup, text="Edit", command=lambda: self.edit_contact(selected_index[0], contact_info_popup))
            delete_button = tk.Button(contact_info_popup, text="Delete", command=lambda: self.delete_contact(selected_index[0], contact_info_popup))

            # Grid layout for contact info popup
            label_name.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
            label_phone.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
            edit_button.grid(row=2, column=0, pady=5)
            delete_button.grid(row=3, column=0, pady=5)

    def delete_contact(self,index, contact_info_popup):
        self.contacts.pop(index)
        self.contact_listbox.delete(index)
        contact_info_popup.destroy()
        self.clear_entries()
        
    def edit_contact(self,index,contact_info_popup):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Contact")
        
        selected_contact = self.contacts[index]
        
        label_fname = tk.Label(edit_window, text="First Name:")
        label_lname = tk.Label(edit_window, text="Last Name:")
        label_phone = tk.Label(edit_window, text="Phone:")

        entry_fname = tk.Entry(edit_window,textvariable=tk.StringVar(value=selected_contact.first_name))
        entry_lname = tk.Entry(edit_window,textvariable=tk.StringVar(value=selected_contact.last_name))
        entry_phone = tk.Entry(edit_window,textvariable=tk.StringVar(value=selected_contact.phone_number))
        
        save_button = tk.Button(edit_window, text="Save Changes", command=lambda: self.save_changes(index, entry_fname.get(),entry_lname.get(), entry_phone.get(), edit_window, contact_info_popup))
        
        label_fname.grid(row=0, column=0, sticky=tk.E)
        entry_fname.grid(row=0, column=1)
        label_lname.grid(row=1, column=0, sticky=tk.E)
        entry_lname.grid(row=1, column=1)
        label_phone.grid(row=2, column=0, sticky=tk.E)
        entry_phone.grid(row=2, column=1)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

    def save_changes(self, index, fname , lname , phone , edit_window, contact_info_popup):
        if self.input_error(fname,lname,phone):
            self.contacts[index].update(fname,lname,phone)
            messagebox.showinfo("Success", "Contact updated successfully.")
            edit_window.destroy()
            contact_info_popup.destroy()
            self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "Name should contain only letters, and Phone should contain only digits.")
    
    def save_contacts(self):
        with open(self.csv_file, mode="w", newline='') as file:
            fieldnames = ["First Name","Last Name", "Phone","Craete Date"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for contact in self.contacts:
                writer.writerow(contact.__str__())

    def search_contact(self):
        search_name = simpledialog.askstring("Search", "Enter name Or Number to search:") 
        if search_name == '*':
            self.show_contacts=self.contacts
        elif search_name.isalpha():
            self.show_contacts = [contact for contact in self.contacts if (search_name.lower() in contact.first_name.lower()) or (search_name.lower() in contact.last_name.lower())]
        elif search_name.isdigit():
            self.show_contacts = [contact for contact in self.contacts if search_name in contact.phone_number]
        else:
            messagebox.showinfo("Search Results", "Enter Valid Format")
        if not self.show_contacts.__len__:
            messagebox.showinfo("Search Results", "No matching contacts found.")
        self.update_contact_listbox()
            
    def clear_entries(self):
        self.entry_fname.delete(0, tk.END)
        self.entry_lname.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        
    def load_contacts_from_csv(self,contact_listbox):
        try:
            with open(self.csv_file, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    contact = pr(row["First Name"], row["Last Name"], row["Phone"],row["Craete Date"])
                    self.contacts.append(contact)
                    self.contact_listbox.insert(tk.END, f"{contact.first_name} {contact.last_name}")
                self.show_contacts=self.contacts
        except FileNotFoundError:
            open(self.csv_file, 'w').close()
    
    def input_error(self,fname,lname,phone):
        if fname.isalpha() and lname.isalpha() and phone.isdigit():
            if any(contact.phone_number == phone for contact in self.contacts):
                messagebox.showwarning("Duplicate Phone Number", "Contact with the same phone number already exists.")
                
            elif any(contact.first_name == fname and contact.last_name == lname for contact in self.contacts):
                messagebox.showwarning("Duplicate Phone Number", "Contact with the same phone number already exists.")
            else:
                return True
        return False
    
    def show_sort_popup(self):
            sort_popup = tk.Toplevel(self.root)
            sort_popup.title("Sort Contacts")

            sort_criteria = tk.StringVar(value="First Name")
            sort_order = tk.StringVar(value="Ascending")
            
            sort_label = tk.Label(sort_popup, text="Sort by:")
            radio_date_added = tk.Radiobutton(sort_popup, text="Date Added", variable=sort_criteria, value="Date Added")
            radio_fname = tk.Radiobutton(sort_popup, text="First Name", variable=sort_criteria, value="First Name")
            radio_lname = tk.Radiobutton(sort_popup, text="Last Name", variable=sort_criteria, value="Last Name")
            radio_phone = tk.Radiobutton(sort_popup, text="Phone Number", variable=sort_criteria, value="Phone Number")

            sort_order_label = tk.Label(sort_popup, text="Sort order:")
            radio_ascending = tk.Radiobutton(sort_popup, text="Ascending", variable=sort_order, value="Ascending")
            radio_descending = tk.Radiobutton(sort_popup, text="Descending", variable=sort_order, value="Descending")

            sort_button = tk.Button(sort_popup, text="Sort", command=lambda: self.sort_contacts(sort_criteria.get(),sort_order.get(), sort_popup))

            sort_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
            radio_date_added.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
            radio_fname.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
            radio_lname.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
            radio_phone.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)

            sort_order_label.grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
            radio_ascending.grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)
            radio_descending.grid(row=7, column=0, sticky=tk.W, padx=10, pady=5)

            sort_button.grid(row=8, column=0, columnspan=2, pady=10)

    def sort_contacts(self, sort_criteria , sort_order, sort_popup):
        if sort_criteria == "Date Added":
            self.show_contacts.sort(key=lambda x: x.create_date)
        elif sort_criteria == "First Name":
            self.show_contacts.sort(key=lambda x: x.first_name)
        elif sort_criteria == "Last Name":
            self.show_contacts.sort(key=lambda x: x.last_name)
        elif sort_criteria == "Phone Number":
            self.show_contacts.sort(key=lambda x: x.phone_number)

        if sort_order == "Descending":
            self.show_contacts.reverse()

        self.update_contact_listbox()
        sort_popup.destroy()

    def update_contact_listbox(self):
        self.contact_listbox.delete(0, tk.END)

        for contact in self.show_contacts:
            self.contact_listbox.insert(tk.END, f"{contact.first_name} {contact.last_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PhonebookApp(root)
    root.mainloop()
