import customtkinter as ctk
from tkinter import messagebox
import Backend

#https://www.geeksforgeeks.org/python/create-a-modern-login-ui-using-customtkinter-module-in-python/
#https://customtkinter.tomschimansky.com/documentation/widgets/tabview/

global logged_in_role

def login_window():
    def login():
        #FIXME Convert to grid from pack to align with other functions
        valid_login, logged_in_role = Backend.login(user_name.get(), user_pass.get())
        if valid_login:
            messagebox.showinfo("Valid Login", f"Good Login. User logged in as: {logged_in_role}")
            window.destroy()
            if logged_in_role == "Admin":
                admin_window()
            else:
                main_window()
        if not valid_login:
            messagebox.showwarning("Invalid Login", "Incorrect Username or Password. Please try again.")
        return
    
    window = ctk.CTk()
    window.geometry("400x400")
    window.title("Monash University Secured Electronic Health Record")
    
    frame = ctk.CTkFrame(window)
    frame.pack(pady=40, padx=40, fill="both", expand=True)

    title = ctk.CTkLabel(frame, text="User Login", font=("Arial", 20))
    title.pack(pady=12)

    user_name = ctk.CTkEntry(frame, placeholder_text="Username")
    user_name.pack(pady=10)

    user_pass = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
    user_pass.pack(pady=10)

    login_button = ctk.CTkButton(frame, text="Login", command=login)
    login_button.pack(pady=20)

    window.mainloop()

def admin_window():
    def add_new_staff():
        def add_staff_to_database():
            successful_add = Backend.new_user(staff_user_name.get(), staff_f_name.get(), staff_l_name.get(), staff_role.get())
            if successful_add:
                messagebox.showinfo("Successful User Add", "New user added to database.")
            elif not successful_add:
                messagebox.showwarning("Unsuccessful User Add", "User already exists in database. No changes made.")
            return

        tabview.add("Add New Staff")
        add_staff = tabview.tab("Add New Staff")
        staff_f_name_label = ctk.CTkLabel(add_staff, text="First Name:")
        staff_f_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        staff_f_name = ctk.CTkEntry(add_staff, placeholder_text="Enter First Name")
        staff_f_name.grid(row=0, column=1, pady=10, sticky="ew")
        
        staff_l_name_label = ctk.CTkLabel(add_staff, text="Last Name:")
        staff_l_name_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        staff_l_name = ctk.CTkEntry(add_staff, placeholder_text="Enter Last Name")
        staff_l_name.grid(row=0, column=3, pady=10, sticky="ew")

        staff_role_label = ctk.CTkLabel(add_staff, text="Role:")
        staff_role_label.grid(row=0, column=4, padx=10, pady=10, sticky="w")

        staff_role = ctk.CTkEntry(add_staff, placeholder_text="Enter Role")
        staff_role.grid(row=0, column=5, pady=10, sticky="ew")

        # This will be removed once I know how to create a unique username
        staff_user_name_label = ctk.CTkLabel(add_staff, text="Username:")
        staff_user_name_label.grid(row=5, column=2, padx=10, pady=10, sticky="w")

        staff_user_name = ctk.CTkEntry(add_staff, placeholder_text="Enter Username")
        staff_user_name.grid(row=5, column=3, pady=10, sticky="ew")
        
        add_button = ctk.CTkButton(add_staff, text="Add Staff", command=add_staff_to_database)
        add_button.grid(row=1, column=1, pady=20)
      
    
    def delete_existing_staff():
        def delete_staff_from_database():
            successful_delete = Backend.delete_user(staff_user_name.get())
            if successful_delete:
                messagebox.showinfo("Successful User Delete", "User removed from database.")
            elif not successful_delete:
                messagebox.showwarning("Unsuccessful User Delete", "User not found. No changes made.")
            return
        
        tabview.add("Delete Existing Staff")
        delete_staff = tabview.tab("Delete Existing Staff")
        # This will be removed once I know how to create a unique username
        staff_user_name_label = ctk.CTkLabel(delete_staff, text="Username:")
        staff_user_name_label.grid(row=5, column=2, padx=10, pady=10, sticky="w")

        staff_user_name = ctk.CTkEntry(delete_staff, placeholder_text="Enter Username")
        staff_user_name.grid(row=5, column=3, pady=10, sticky="ew")

        add_button = ctk.CTkButton(delete_staff, text="Remove Staff", command=delete_staff_from_database)
        add_button.grid(row=1, column=1, pady=20)
    
    def change_staff_role():
        def modify_role():
            role_change = Backend.change_role(staff_user_name.get(),staff_role.get())
            if role_change:
                messagebox.showinfo("Successful Role Change", "User role modified.")
            elif not role_change:
                messagebox.showwarning("Unsuccessful Role Change", "User not found. No changes made.")
            return
        
        tabview.add("Change Staff Role")
        staff_role = tabview.tab("Change Staff Role")

        staff_role_label = ctk.CTkLabel(staff_role, text="Role:")
        staff_role_label.grid(row=0, column=4, padx=10, pady=10, sticky="w")

        staff_role = ctk.CTkEntry(staff_role, placeholder_text="Enter Role")
        staff_role.grid(row=0, column=5, pady=10, sticky="ew")
        
        staff_user_name_label = ctk.CTkLabel(staff_role, text="Username:")
        staff_user_name_label.grid(row=5, column=2, padx=10, pady=10, sticky="w")

        staff_user_name = ctk.CTkEntry(staff_role, placeholder_text="Enter Username")
        staff_user_name.grid(row=5, column=3, pady=10, sticky="ew")

        add_button = ctk.CTkButton(staff_role, text="Add New Staff", command=modify_role)
        add_button.grid(row=1, column=1, pady=20)

# Patient Records will require searching by First and Last name, then allow the individual to pick the unique patient. 
# For visit removals, a second search record with all visits associated with the individual selected should appear. 
    def delete_patient_record():
        tabview.add("Delete Patient Record")

    def delete_patient_visit():
        tabview.add("Delete Patient Visit")

    window = ctk.CTk()
    window.geometry("900x600")
    window.title("Monash University Secured Electronic Health Record")

    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)
    
    frame = ctk.CTkFrame(window)
    frame.grid(row=0, column=0, sticky="nsew")
    
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    tabview = ctk.CTkTabview(master=frame)
    tabview.grid(row=0, column=0, sticky="nsew")

    add_new_staff()
    delete_existing_staff()
    change_staff_role()
    delete_patient_record()
    delete_patient_visit()

    window.mainloop()
    pass

def main_window():
    def find_users():
        # TODO Will be used to search the database and return all users that match with the First and Last name passed in
        f_name = search_f_name.get()
        l_name = search_l_name.get()
        results = Backend.search_patients(f_name, l_name, "Admin")
        print(results)
        
    def add_new_patient():
        tabview.set("Patient Data")
    
    def delete_existing_patient():
        raise NotImplementedError


    def select_person(person, window):
        raise NotImplementedError
    
    window = ctk.CTk()
    window.geometry("900x600")
    window.title("Monash University Secured Electronic Health Record")
    
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)
    
    frame = ctk.CTkFrame(window)
    frame.grid(row=0, column=0, sticky="nsew")
    
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    
    tabview = ctk.CTkTabview(master=frame)
    tabview.grid(row=0, column=0, sticky="nsew")

    tabview.add("Patient Search")
    tabview.add("Patient Data")
    tabview.add("Visit Data")
    tabview.set("Patient Search")
    
    # PATIENT SEARCH TAB
    search_tab = tabview.tab("Patient Search")
    
    for i in range(4):
        search_tab.columnconfigure(i, weight=1)
    for i in range(2):
        search_tab.rowconfigure(i, weight=1)
        
    search_f_name_label = ctk.CTkLabel(search_tab, text="First Name:")
    search_f_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    search_f_name = ctk.CTkEntry(search_tab, placeholder_text="Enter First Name")
    search_f_name.grid(row=0, column=1, pady=10, sticky="ew")
    
    search_l_name_label = ctk.CTkLabel(search_tab, text="Last Name:")
    search_l_name_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    search_l_name = ctk.CTkEntry(search_tab, placeholder_text="Enter Last Name")
    search_l_name.grid(row=0, column=3, pady=10, sticky="ew")
    
    search_button = ctk.CTkButton(search_tab, text="Search", command=find_users)
    search_button.grid(row=1, column=1, pady=20)
    
    add_button = ctk.CTkButton(search_tab, text="Add New Patient", command=add_new_patient)
    add_button.grid(row=1, column=0, pady=20)
    
    delete_button = ctk.CTkButton(search_tab, text="Delete Patient Record", command=delete_existing_patient)
    delete_button.grid(row=1, column=2, pady=20)
    
    # PATIENT DATA TAB
    def save_patient_details():
        raise NotImplementedError
    patient_tab = tabview.tab("Patient Data")

    #FIXME Work on grid values and configure values
    for i in range(5):
        patient_tab.columnconfigure(i, weight=1)
    for i in range(7):
        patient_tab.rowconfigure(i, weight=1)

    patient_f_name_label = ctk.CTkLabel(patient_tab, text="First Name:")
    patient_f_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    patient_f_name = ctk.CTkEntry(patient_tab, placeholder_text="Enter First Name")
    patient_f_name.grid(row=0, column=1, pady=10, sticky="ew")
    
    patient_l_name_label = ctk.CTkLabel(patient_tab, text="Last Name:")
    patient_l_name_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    patient_l_name = ctk.CTkEntry(patient_tab, placeholder_text="Enter Last Name")
    patient_l_name.grid(row=0, column=3, pady=10, sticky="ew")
    
    patient_address_label = ctk.CTkLabel(patient_tab, text="Patient Address:")
    patient_address_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    
    # FIXME This needs to be multiline and the placeholder text needs to sit at the top of the entry field.
    patient_address = ctk.CTkEntry(patient_tab, placeholder_text="Enter Address")
    patient_address.grid(row=1, column=1, columnspan=5, sticky="nsew")

    patient_dob_label = ctk.CTkLabel(patient_tab, text="Date of Birth:")
    patient_dob_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    
    patient_dob = ctk.CTkEntry(patient_tab, placeholder_text="Enter Date of Birth")
    patient_dob.grid(row=2, column=1, pady=10, sticky="w")

    button = ctk.CTkButton(patient_tab, text="Save Patient Data", command=save_patient_details)
    button.grid(row=6, column=2, pady=20, sticky="w")
    

    # PATIENT VISIT TAB
    def create_initial_screen():
        visit_tab = tabview.tab("Visit Data") 
            
        visit_add = ctk.CTkButton(visit_tab, text="Add New Patient Record", command=add_new_visit)
        visit_add.grid(row=0, column = 0, pady=20)
        
        visit_search = ctk.CTkButton(visit_tab, text="Search Existing Record", command=search_existing_visit)
        visit_search.grid(row=0, column=1, pady=20)
    
    def add_new_visit():
        raise NotImplementedError
        build_visit_cells()
        
        
    
    def search_existing_visit():
        raise NotImplementedError
    
    
    def build_visit_cells():
        visit_tab = tabview.tab("Visit Data")
            
        patient_f_name_label = ctk.CTkLabel(visit_tab, text="First Name:")
        patient_f_name_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        patient_f_name = ctk.CTkEntry(visit_tab, placeholder_text="Enter First Name")
        patient_f_name.grid(row=1, column=1, pady=10, sticky="ew")

        patient_l_name_label = ctk.CTkLabel(visit_tab, text="First Name:")
        patient_l_name_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        patient_l_name = ctk.CTkEntry(visit_tab, placeholder_text="Enter First Name")
        patient_l_name.grid(row=1, column=3, pady=10, sticky="ew")

        date_of_visit_label = ctk.CTkLabel(visit_tab, text="Date of Visit")
        date_of_visit_label.grid(row=2, column=0, pady=10, sticky="w")   
        
        date_of_visit = ctk.CTkEntry(visit_tab, placeholder_text="This will become a selectable box for the date")     
        date_of_visit.grid(row=2, column=1, pady=10)
        
        specialist_appointed_label = ctk.CTkLabel(visit_tab, text="Specialist Appointed")
        specialist_appointed_label.grid(row=2, column=2, pady=10, sticky="w")
        
        specialist_appointed = ctk.CTkEntry(visit_tab, placeholder_text="Please Select Specialist, This should be a drop-down populated with all specialist names in database")     
        specialist_appointed.grid(row=2, column=1, pady=10)
        
        reason_for_visit_label = ctk.CTkLabel(visit_tab, text="Reason for Visit")
        reason_for_visit_label.grid(row=3, column=0, pady=10, sticky="w")
        
        reason_for_visit = ctk.CTkEntry(visit_tab, placeholder_text="Enter reason for visit")     
        reason_for_visit.grid(row=3, column=1, pady=10)
        
        actions_taken_label = ctk.CTkLabel(visit_tab, text="Actions Taken")
        actions_taken_label.grid(row=4, column=0, pady=10, sticky="w")
        
        actions_taken = ctk.CTkEntry(visit_tab, placeholder_text="Enter any actions taken")     
        actions_taken.grid(row=4, column=1, pady=10)
        
        save_visit_data = ctk.CTkButton(visit_tab, text="Save Visit Data", command=save_visit)
        save_visit_data.grid(row=5, column=0, pady=10, sticky="w")
        
        clear_visit_data = ctk.CTkButton(visit_tab, text="Save Visit Data", command=clear_visit)
        clear_visit_data.grid(row=5, column=2, pady=10, sticky="w")
    
    def save_visit():
        raise NotImplementedError
    
    def clear_visit():
        raise NotImplementedError
        
    visit_tab = tabview.tab("Visit Data")    

    create_initial_screen()
    
    # Runs the main window loop
    window.mainloop()

if __name__ == "__main__":
    #login_window()
    admin_window()
    #main_window()