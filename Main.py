
from tkinter import * # so we can use Tk() instead of Tkinter.Tk() ...
from tkinter import ttk
from tkinter import filedialog 
import tkinter.messagebox
import pandas as pd
from PIL import Image,ImageTk
import os
import webbrowser
#from docx import Document
#from docx.shared import Inches

JOURNAL_DIR = "./Journal Entries"
PHOTOS_DIR = "./Journal Photos"


class App(Frame):
    def __init__(self, master):     
        '''main application window setup for journal and learn tabs'''
        self.master = master # store link to master window, use as frame to put all other widgets into
        
        # Part 1a Tabular Journal (Default) vs. Learn Windows Set Up
        self.notebook = ttk.Notebook(self.master, width=850, height=800)

        # Frames
        self.frame1 = Frame(self.notebook)
        self.frame2 = Frame(self.notebook)
        self.frame1.pack(padx=10, pady=10)
        self.frame2.pack(padx=10, pady=10)

        # Tabs
        self.notebook.add(self.frame1, text="Journal")
        self.notebook.add(self.frame2, text="Learn")
        self.notebook.pack(padx=10, pady=10)

        # Initial instructions for user to review upon viewing each tab
        self.frame1_label = Label(self.frame1, text="To create a new journal entry, click the Create new journal entry button below.")
        self.frame2_label = Label(self.frame2, text="To learn about a US National Park, select the appropriate National Park from the dropdown menu.")
        self.frame1_label.pack(padx=10, pady=(10,5), anchor=W)
        self.frame2_label.pack(padx=10, pady=(10), anchor=W)

        # Create new journal button
        self.journal_button = Button(self.frame1, text="Create new journal entry", command=self.enter_new_journal_entry)
        self.journal_button.pack(padx=10, pady=(0,5), anchor=W)

        # Existing entries label
        self.ext_entries_label = Label(self.frame1, text="To view an existing journal entry, click on the Open a journal entry button or double click on an entry from the list below.")
        self.ext_entries_label.pack(padx=10, pady=(15,5), anchor=W)

        # Listbox listing existing entries
        self.entries_list = Listbox(self.frame1, width=50, height=10, selectmode=SINGLE)
        self.entries_list.bind("<Double-Button-1>", self.double_click_journal)

        # Open a journal entry button
        self.open_journal_button = Button(self.frame1, text="Open a journal entry",  command=self.open_journal_entry) 
        self.open_journal_button.pack(padx=10, pady=0, anchor=W)
        
        # Existing entries listbox
        self.entries_list.pack(padx=15, pady=10, anchor=W)
        self.journal_entry_list = os.listdir(JOURNAL_DIR)
        for item in self.journal_entry_list:
            self.entries_list.insert(END, item)

        self.click_journal_file = ""
        
        # Drop down menu on Learn tab + read in excel file
        app_data = pd.read_excel("Database - Learn.xlsx")
        park_names = app_data["Name"]
        self.parks_list = list(park_names)
        self.natpark_learn_var = StringVar()
        self.natpark_learn_var.set("Select a National Park") # default shown before a national park is selected from the dropdown menu
        self.learn_dropdown = OptionMenu(self.frame2, self.natpark_learn_var, *self.parks_list, command=self.new_learn_inquiry)
        self.learn_dropdown.pack(padx=15, pady=(0,5), anchor=W)

        # Frame that will be cleared below each time a user selects a park to learn about
        self.learn_info_frame=Frame(self.frame2) 
        self.learn_info_frame.pack(padx=10, pady=10, anchor=W)

        # Image display CTA
        self.pic_CTA_label = Label(self.frame1, text="Have some pictures from your visits to US National Parks? Add them to the Journal Photos folder to see them below!")
        self.pic_CTA_label.pack(padx=10, pady=(15,0), anchor=W)
        
        # Image display instruction
        self.pic_instruction_label = Label(self.frame1, text="Use the Forward and Back buttons to scroll through the images.")
        self.pic_instruction_label.pack(padx=10, pady=(0,0), anchor=W)
        
        # Image display
        global pic_list
        pic_list = []
        self.pic_number = 0
        pics = os.listdir(PHOTOS_DIR)
        for pic in pics:
            pics_path = os.path.join(PHOTOS_DIR, pic)
            with Image.open(pics_path) as picture:
                picture.thumbnail((300,225))
                displayed_pic = ImageTk.PhotoImage(picture)
                pic_list.append(displayed_pic)
        
        # Image display label
        self.pic_display_label = Label(self.frame1, image=displayed_pic)
        self.pic_display_label.pack(padx=10, pady=(15,0), anchor=W)

        # Navigation buttons
        self.back_button = Button(self.frame1, text="Back", command=self.scroll_backward)
        self.forward_button = Button(self.frame1, text="Forward", command=lambda: self.scroll_forward(2))
        self.forward_button.pack(padx=10, pady=(0,2.5), anchor=W)
        self.back_button.pack(padx=10, pady=(0,2.5), anchor=W)

    # Part 1b Image Scroll Forward Button Function 
    def scroll_forward(self, pic_number):
        self.forward_button.pack_forget()
        self.back_button.pack_forget()
        self.pic_display_label.pack_forget()
        self.pic_display_label = Label(self.frame1, image=pic_list[(pic_number-1) % len(pic_list)])
        self.pic_display_label.pack(padx=10, pady=(15,0), anchor=W)
        self.forward_button.config(command=lambda: self.scroll_forward((pic_number + 1) % len(pic_list)))
        self.back_button.config(command=lambda: self.scroll_backward((pic_number - 1) % len(pic_list)))
        self.forward_button.pack(padx=10, pady=(0,2.5), anchor=W)
        self.back_button.pack(padx=10, pady=(0,2.5), anchor=W)
        
    # Part 1c Image Scroll Backward Button Function 
    def scroll_backward(self, pic_number):
        self.forward_button.pack_forget()
        self.back_button.pack_forget()
        self.pic_display_label.pack_forget()
        self.pic_display_label = Label(self.frame1, image=pic_list[(pic_number-1) % len(pic_list)])
        self.pic_display_label.pack(padx=10, pady=(15,0), anchor=W)
        self.forward_button.config(command=lambda: self.scroll_forward((pic_number + 1) % len(pic_list)))
        self.back_button.config(command=lambda: self.scroll_backward((pic_number - 1) % len(pic_list)))
        self.forward_button.pack(padx=10, pady=(0,2.5), anchor=W)
        self.back_button.pack(padx=10, pady=(0,2.5), anchor=W)

       
    # Part 2a New Journal Entry Function
    def enter_new_journal_entry(self):
        '''method for creating a new journal entry'''
        self.journal_entry = Toplevel() # new window

      # -------------------------------------------------------------------------------------------------------------------------------------
      # SCROLLBAR WIDGETS
      # First frame
        self.textframe=Frame(self.journal_entry) 
        self.textframe.pack(fill=BOTH, expand=1)

      # Canvas
        self.journal_canvas = Canvas(self.textframe, height=800, width=700)
        self.journal_canvas.pack(side=LEFT, fill=BOTH, expand=1)

      # Scrollbar
        self.journal_scrollbar = Scrollbar(self.textframe, orient=VERTICAL, command=self.journal_canvas.yview)
        self.journal_scrollbar.pack(side=RIGHT, fill=Y)

      # Configure canvas
        self.journal_canvas.configure(yscrollcommand=self.journal_scrollbar.set)
        self.journal_canvas.bind('<Configure>', lambda e: self.journal_canvas.configure(scrollregion=self.journal_canvas.bbox("all")))

      # Second frame
        self.second_frame = Frame(self.journal_canvas) # widgets go here

      # Add second frame to a window in canvas
        self.journal_canvas.create_window((0,0), window=self.second_frame, anchor="nw")
      # -------------------------------------------------------------------------------------------------------------------------------------
        
        # Instructions
        self.journal_label = Label(self.second_frame, text="To complete a new journal entry and log the details of your national park experience, select the appropriate\nnational park from the dropdown menu and then record your memories in the text field. When finished, save\nyour entry by clicking the ‘Save’ button.", justify='left')
        self.journal_label.pack(side=TOP , padx=10, pady=10)

        # Step-by-step instruction
        self.dropdown_label = Label(self.second_frame, text="1. Select a US National Park:")
        self.dropdown_label.pack(padx=10, anchor=W)
        
        # Drop down menu on Journal window
        self.natpark_var = StringVar()
        self.natpark_dropdown = OptionMenu(self.second_frame, self.natpark_var, *self.parks_list)
        self.natpark_dropdown.pack(padx=10, pady=10, anchor=W)

        # Step-by-step instruction
        self.text_label = Label(self.second_frame, text="2. Enter the details of your visit:")
        self.text_label.pack(padx=10, anchor=W)

        # Text box for journal details
        self.text=Text(self.second_frame, width=90, height=10, wrap=WORD)
        self.text.pack(padx=10, pady=10, anchor=W)

        # Step-by-step instruction
        self.image_upload_label = Label(self.second_frame, text="3. Upload a picture from your visit:")
        self.image_upload_label.pack(padx=10, anchor=W)
        
        # Upload image button
        self.image_button = Button(self.second_frame, text="Upload image", command = self.upload_image)
        self.image_button.pack(padx=10, pady=10, anchor=W)

        # Label for an uploaded image
        self.pic_label = Label(self.second_frame)
        self.pic_label.pack(padx=10, pady=0, anchor=W)

        # Step-by-step instruction
        self.rating_label = Label(self.second_frame, text="4. Rate the selected US National Park:")
        self.rating_label.pack(padx=10, anchor=W)

        # Drop down menu for rating
        self.rating_var = StringVar()
        self.rating_dropdown = OptionMenu(self.second_frame, self.rating_var, "0", "1", "2", "3", "4", "5")
        self.rating_dropdown.pack(padx=10, pady=10, anchor=W)

        # Step-by-step instruction
        self.ratingtext_label = Label(self.second_frame, text="5. Optionally, justify your rating:")
        self.ratingtext_label.pack(padx=10, anchor=W)

        # Text box for rating details
        self.rating_text=Text(self.second_frame, width=90, height=10, wrap=WORD)
        self.rating_text.pack(padx=10, pady=10, anchor=W)

        # Save button
        self.journalentry_button = Button(self.second_frame, text="Save", command=self.save_journal_entry)
        self.journalentry_button.pack(padx=10, pady=10)

        # Cancel button
        self.cancel_button = Button(self.second_frame, text="Cancel", command=self.cancel_journal_entry)
        self.cancel_button.pack(padx=10, pady=10)
    
    # Part 2b Upload an Image Into New Journal Entry
    def upload_image(self):
        '''method for uploading an image as part of a new journal entry'''
        self.upload_img_file = filedialog.askopenfilename(title="Select an image to upload", filetypes=[("Image Files", ".png .jpeg .jpg")])
        global img_file_uploaded # global variable to support part 2c below (.docx code)
        img_file_uploaded = self.upload_img_file
        self.image_open = Image.open(self.upload_img_file)
        self.image_open.thumbnail((300, 225))  # thumbnail internally changes the image, and does NOT return a changed copy!
        self.selected_pic = ImageTk.PhotoImage(self.image_open)
        self.pic_label.configure(image=self.selected_pic)
        self.selected_pic.image=self.selected_pic # for garbage collection
    
    # Part 2c Save Journal Entry Function - WIP
    def save_journal_entry(self):
        '''method for saving the details of a new journal entry as a file that can be accessed later'''
        self.text_file = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text File", ".txt")], initialdir=JOURNAL_DIR, initialfile=self.natpark_var.get())
        get_image = self.pic_label.cget('image') # wip
        image_str = str(get_image + "\n") # wip
        file_text = str("National Park Visited: " + self.natpark_var.get() + "\n" + "Details: " + self.text.get(1.0, END) + "\n"+ image_str + "\n" + "Rating: " + self.rating_var.get() + "\n" + "Rating Details: " + self.rating_text.get(1.0, END))
        self.text_file.write(file_text) # write contents
        self.text_file.close() # close file

        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # this code would need to go with .docx filetypes and supports text and images, but can't be displayed in tkinter :(
        # might be useful later, but would need to activate the docx imports in lines 10-11 above
        #self.text_file = filedialog.asksaveasfile(defaultextension=".docx", filetypes=[("Word File", ".docx")], initialdir=JOURNAL_DIR, initialfile=self.natpark_var.get())
        #document.add_paragraph("National Park Visited: " + self.natpark_var.get())
        #document.add_paragraph("Details: " + self.text.get(1.0, END))
        #document.add_paragraph("Rating: " + self.rating_var.get())
        #document.add_paragraph("Rating Details: " + self.rating_text.get(1.0, END))
        #document.add_picture(img_file_uploaded, width=Inches(4), height=Inches(3))
        #document.save(self.text_file.name)
        #self.text_file.close()
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.journal_entry.destroy() # close window
        self.entries_list.delete(0,END) # clear entries
        self.journal_entry_list = os.listdir(JOURNAL_DIR) # grab list
        for item in self.journal_entry_list: # populate entries list
            self.entries_list.insert(END, item) 
    
    # Part 2d Cancel New Journal Entry Function
    def cancel_journal_entry(self):
        '''method for canceling creation of a new journal entry'''
        self.journal_entry.destroy() # close window

    
    # Part 3a Open Existing Journal Entry Function
    def open_journal_entry(self):
        '''method for opening a journal entry via the 'Open a journal entry' button'''
        
        # Select file to open
        self.journal_file = filedialog.askopenfilename(initialdir=JOURNAL_DIR, title="Open Journal Entry Text File")
        self.journal_file = open(self.journal_file, 'r')
        read_journal = self.journal_file.read()
        
        # New window for frame and text box
        self.open_journal_entry = Toplevel() # new window
        
        # Frame for text box
        self.open_journal_frame=Frame(self.open_journal_entry)
        self.open_journal_frame.pack(padx=10, pady=10)   
        
        # Text box for file contents to appear in when opened
        self.open_text_file = Text(self.open_journal_frame, width=90, height=20)
        self.open_text_file.pack(padx=10, pady=10)
       
        # Insert file contents
        self.open_text_file.insert(END, read_journal)
        self.journal_file.close()
        
        # Menu for opening and saving files
        self.file_menu = Menu(self.open_journal_entry)
        self.open_journal_entry.config(menu=self.file_menu)
        self.entry_menu = Menu(self.file_menu)
        self.file_menu.add_cascade(label="File", menu=self.entry_menu)
        self.entry_menu.add_command(label="Open", command=self.open_file)
        self.entry_menu.add_command(label="Save", command=self.save_file)

        # Save button
        self.journal_save_entry_button = Button(self.open_journal_frame, text="Save", command=self.save_file)
        self.journal_save_entry_button.pack(padx=10, pady=5)

        # Cancel button
        self.cancel_journal_button = Button(self.open_journal_frame, text="Cancel", command=self.cancel_journal_changes)
        self.cancel_journal_button.pack(padx=10, pady=5)

    # Part 3b Open File Menu Function
    def open_file(self):
        '''method for opening a different existing journal entry via file menu 'Open' option'''
        self.open_text_file.delete("1.0", END)
        self.journal_file = filedialog.askopenfilename(initialdir=JOURNAL_DIR, title="Open Journal Entry Text File")
        self.journal_file = open(self.journal_file, 'r')
        read_journal = self.journal_file.read()
        self.open_text_file.insert(END, read_journal)
        self.journal_file.close()

    # Part 3c Save File Menu Function
    def save_file(self):
        '''method for saving a journal file via the file menu Save option or the Save button'''
        self.existing_filename = os.path.basename(self.journal_file.name)
        self.journal_file_save = filedialog.asksaveasfilename(defaultextension=".*", initialdir=JOURNAL_DIR, initialfile=self.existing_filename, title="Save Journal Entry Text File")
        self.journal_file_save = open(self.journal_file_save, 'w+') 
        self.journal_file_save.write(self.open_text_file.get("1.0", END))
        self.journal_file_save.close()

    # Part 3d Double Click Open Existing Journal Entry Function
    def double_click_journal(self, event):
        '''method for opening and accessing a journal file from the listbox by double clicking on the applicable journal file'''

        # New window for frame and text box
        self.click_journal_entry = Toplevel() # new window
        
        # frame for text file
        self.click_journal_frame=Frame(self.click_journal_entry)
        self.click_journal_frame.pack(padx=10, pady=10)   
        
        # Text box for text file to appear in when opened
        self.click_text_file = Text(self.click_journal_frame, width=90, height=20)
        self.click_text_file.pack(padx=10, pady=10)

        # Open the journal entry file clicked on from the listbox
        self.click_journal_file = self.entries_list.get(ACTIVE)
        folder_path = JOURNAL_DIR
        file_path = os.path.join(folder_path, self.click_journal_file)
        file_clicked = open(file_path, 'r')
        read_journal_clicked = file_clicked.read()
        self.click_text_file.insert(END, read_journal_clicked)
        file_clicked.close()

        # Menu for opening and saving files
        self.option_menu = Menu(self.click_journal_entry)
        self.click_journal_entry.config(menu=self.option_menu)
        self.entry_menu = Menu(self.option_menu)
        self.option_menu.add_cascade(label="File", menu=self.entry_menu)
        self.entry_menu.add_command(label="Open", command=self.open_clicked_file)
        self.entry_menu.add_command(label="Save", command=self.save_clicked_file)

        # Save button
        self.journal_save_entry_button = Button(self.click_journal_frame, text="Save", command=self.save_clicked_file)
        self.journal_save_entry_button.pack(padx=10, pady=5)

        # Cancel button
        self.cancel_journal_button = Button(self.click_journal_frame, text="Cancel", command=self.cancel_journal_edits)
        self.cancel_journal_button.pack(padx=10, pady=5)

    # Part 3e Cancel Journal Edits Button Function
    def cancel_journal_edits(self):
        '''method for canceling the viewing/editing of an existing journal entry - via double clicked mode'''
        self.click_journal_entry.destroy()

    # Part 3f Cancel Journal Changes Button Function
    def cancel_journal_changes(self):
        '''method for canceling the viewing/editing of an existing journal entry - via 'Open a journal entry' button mode'''
        self.open_journal_entry.destroy()

    # Part 3g Open File Menu Function for Double Click Mode
    def open_clicked_file(self):
        '''method for opening a different existing journal entry via file menu 'Open' option for double clicked mode'''
        self.click_text_file.delete("1.0", END)
        self.clicked_journal_file = filedialog.askopenfilename(initialdir=JOURNAL_DIR, title="Open Journal Entry Text File")
        self.clicked_journal_file = open(self.clicked_journal_file, 'r')
        read_journals = self.clicked_journal_file.read()
        self.click_text_file.insert(END, read_journals)
        self.clicked_journal_file.close()
        
    # Part 3h Save File Function for Double Click Mode
    def save_clicked_file(self):
        '''method for saving an existing journal entry via file menu option or button for double clicked mode'''
        try: # for simply saving the same journal file that was opened directly from the listbox
            self.click_existing_filename = os.path.basename(self.click_journal_file)
            self.click_journal_file_save = filedialog.asksaveasfilename(defaultextension=".*", initialdir=JOURNAL_DIR, initialfile=self.click_existing_filename, title="Save Journal Entry Text File")

            with open(self.click_journal_file_save, 'w+') as self.click_journal_file_save:
                self.click_journal_file_save.write(self.click_text_file.get("1.0", END))

                self.click_journal_file_save.close()
        except: # for saving a different journal file that is opened with the 'Open' file menu option after opening an initial journal file from the listbox (still a WIP, but without this, this function was not working at all)
            self.clicked_existing_filename = os.path.basename(self.clicked_journal_file)
            self.click_journal_file_saved = filedialog.asksaveasfilename(defaultextension=".*", initialdir=JOURNAL_DIR, initialfile=self.clicked_existing_filename, title="Save Journal Entry Text File")

            with open(self.click_journal_file_saved, 'w+') as self.click_journal_file_saved:
                self.click_journal_file_saved.write(self.click_text_file.get("1.0", END))

                self.click_journal_file_saved.close()


    # Part 4 New Learn Inquiry Function
    def new_learn_inquiry(self, event):
        '''method for learning about a national park after selecting one from dropdown menu'''

        # Destroy frame created above to clear contents of the frame
        self.learn_info_frame.destroy() 
        
        # Recreate frame to show widgets
        self.learn_info_frame=Frame(self.frame2) 
        self.learn_info_frame.pack(padx=10, pady=10, anchor=W)
        
        # Read in excel file and get selected item from drop down menu
        learn_excel = pd.read_excel("Database - Learn.xlsx")
        park_from_list = self.natpark_learn_var.get()

        park_info = learn_excel[learn_excel['Name'] == park_from_list]
        park_info_list = park_info.values.tolist() 

        # Image
        img_open = Image.open(park_info_list[0][2])
        img_resize = img_open.resize((300, 225), Image.LANCZOS)
        park_pic = ImageTk.PhotoImage(img_resize)
        self.image_label = Label(self.learn_info_frame, image=park_pic)
        self.image_label.image = park_pic
        self.image_label.pack(padx=10, pady=5, anchor=W)

        # Location
        self.location_label = Label(self.learn_info_frame, text=("Location: "+park_info_list[0][1]))
        self.location_label.pack(padx=10, pady=5, anchor=W)
        self.location_label.configure(wraplength=800, justify=LEFT)

        # Description
        self.desc_label = Label(self.learn_info_frame, text="Description: "+park_info_list[0][7])
        self.desc_label.pack(padx=10, pady=5, anchor=W)
        self.desc_label.configure(wraplength=800, justify=LEFT)

        # NPS page link
        self.link_label = Label(self.learn_info_frame, text="National Park Service Official Web Page", fg="blue", cursor="hand2", font=('TkDefaultFont', 13, 'underline'))
        self.link_label.pack(padx=10, pady=(0,5), anchor=W)
        self.link_label.bind("<Button-1>", lambda e: webbrowser.open_new(park_info_list[0][3]))

        # Nature and wildlife
        self.wildlife_label = Label(self.learn_info_frame, text="Common wildlife to be seen in the park includes: "+park_info_list[0][10]+ ", and more! For more information about nature and wildlife, please visit:")
        self.wildlife_label.pack(padx=10, pady=0, anchor=W)
        self.wildlife_label.configure(wraplength=800, justify=LEFT)

        # Nature and wildlife URL
        self.nw_link_label = Label(self.learn_info_frame, text=str(park_info_list[0][11]) , fg="blue", cursor="hand2", font=('TkDefaultFont', 13, 'underline'))
        self.nw_link_label.pack(padx=10, pady=(0,10),anchor=W)
        self.nw_link_label.bind("<Button-1>", lambda e: webbrowser.open_new(park_info_list[0][11]))

        # Activities
        self.activities_label = Label(self.learn_info_frame, text="Common activities throughout the park include: "+park_info_list[0][12]+ ", and more! For more information about nature and wildlife, please visit:")
        self.activities_label.pack(padx=10, pady=0, anchor=W)
        self.activities_label.configure(wraplength=800, justify=LEFT)

        # Activities URL
        self.act_link_label = Label(self.learn_info_frame, text=str(park_info_list[0][13]) , fg="blue", cursor="hand2", font=('TkDefaultFont', 13, 'underline'))
        self.act_link_label.pack(padx=10, pady=(0,10), anchor=W)
        self.act_link_label.bind("<Button-1>", lambda e: webbrowser.open_new(park_info_list[0][13]))

        # Operating hours and seasons
        self.ops_label = Label(self.learn_info_frame, text="Operating hours: "+park_info_list[0][8]+ ". For more information about hours and holiday closures, please visit:")
        self.ops_label.pack(padx=10, pady=0, anchor=W)
        self.ops_label.configure(wraplength=800, justify=LEFT)

        # Operating hours and seasons URL
        self.ops_link_label = Label(self.learn_info_frame, text=str(park_info_list[0][9]) , fg="blue", cursor="hand2", font=('TkDefaultFont', 13, 'underline'))
        self.ops_link_label.pack(padx=10, pady=(0,10), anchor=W)
        self.ops_link_label.bind("<Button-1>", lambda e: webbrowser.open_new(park_info_list[0][9]))
        
        # Cost per vehicle
        self.costv_label = Label(self.learn_info_frame, text="Cost of Entry Per Vehicle: $"+str(park_info_list[0][4]))
        self.costv_label.pack(padx=10, pady=(5,0), anchor=W)
        
        # Cost per person
        self.costp_label = Label(self.learn_info_frame, text="Cost of Entry Per Person: $"+str(park_info_list[0][5]))
        self.costp_label.pack(padx=10, anchor=W)

        # Cost per motorcyle
        self.costm_label = Label(self.learn_info_frame, text="Cost of Entry Per Motorcycle: $"+str(park_info_list[0][6]))
        self.costm_label.pack(padx=10, anchor=W)
        
       
        
# WIP parts:
# Part 2c - incorporating uploaded image from part 2b
# Part 3h - system error preventing filename from autopopulating after a different entry is opened using the part 3g function




master = Tk()  # create a Tk window called master
master.title("National Park Journal for Outdoor Enthusiasts TkInter GUI")
myapp = App(master) # create App object within master (Tk) windowmaster.mainloop() # draw master window, react to events only
master.mainloop() # draw master window, react to events 
print("Done")


