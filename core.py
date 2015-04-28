import string, sys, sqlite3, cmd, dropbox, webbrowser
from Lib import archersys
class ProducktivShellRolodex(cmd.Cmd):
    def __init__(self):
         

         cmd.Cmd.__init__(self)
         self.id_f = open("conchtack_id.dat","wb")
         self.id = 0
         self.intro = "ArcherSys OS Producktiviti ConchTack Shell Environment \n 1.0.0 -- Open Source, Made in 2015"
         self.database_name = input("Database Name:")
         self.db = sqlite3.connect(self.database_name + ".db")
         self.cursor = self.db.cursor()
         self.prompt =  self.database_name + " -> ProducktivShell:"
    def do_CreateDB(self,args):
         """ Creates a new ArcherDB Database (MySQl or SQLite3 for Python) 
        
          Define  do_CreateDB
          Ask  Contact Address Book Name:
          Save_To_DB
          Create Tables -> contacts(family, friends, etc.)
          ResetDictionary """
         self.db = sqlite3.connect(self.database_name + ".db")
         self.cursor = self.db.cursor()
         try:
             self.cursor.execute("create table family (id text, first_name text,last_name text,phone text,email text)")
         except sqlite3.OperationalError:
              print("The family contacts group already exists.")
         try:
             self.cursor.execute("create table friend (id text, first_name text,last_name text,phone text,email text)")
         except sqlite3.OperationalError:
             print("The Friends Contact Group already exists.")
   
    def do_NewContact(self,arg):
          """Creates a record for the contacts database
             Define   NewContact
             New_contact = Ask Name: Phone Number: Email:
             SaveNewDBRecord New_Contact """
          self.id += 1
          first_name = input("First Name")
          last_name = input("Last Name:")
          family_type = input("Type of Contact:")
          self.cursor.execute("insert into " + family_type + " values (?, ?, ?, ?, ?)",(str(self.id),first_name,last_name,input("Phone"),input("Email:")))
          print("="*41)
          self.cursor.execute("select * from " + family_type + " WHERE id = (SELECT COUNT(*) FROM " + family_type + " )")
          record = self.cursor.fetchone()
          
          print("Name: " + record[1] + " " + record[2])
 
          print("="*41)
          print("Phone Number: " + record[3])
          print("="*41)
          print("Email: " + record[3])
          print("="*41)
    def do_EditContact(self,arg):
          """ Edits a Record
          Define     EditContact
          Edit_Contact = Select_Record Ask Index
          Ask RECORD_EDIT_PART
          Ask(Edit) RECORD_EDIT_PART 
          Save_To_DB (Ans)"""

          field = input("Field:")
          edit_id = int(input("ID to Edit:"))
          query = "UPDATE " + input("Contact Type:") + " SET "+field+"=\""+ input(field) + "\" WHERE id="+str(int(input("ID:")))
         
         
          self.cursor.execute(query)
    def do_DeleteContact(self,arg):
          """Deletes a Contact
          Ask Select_Record
          DELETE_RECORD Ans
          SaveChanges"""
          field = input("Search Field:")
          value = input("Value:")
          print("Deleting...")
          self.cursor.execute("DELETE FROM " + input("Contact Type:") + " WHERE " + field + "=" + value)
          print("Deleted Record.")
    def do_InitDropbox(self,arg):
          app_key = archersys.ARCHERSYS_FOR_DROPBOX_KEY
          app_secret = archersys.ARCHERSYS_FOR_DROPBOX_SECRET


          flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

          # Have the user sign in and authorize this token
          authorize_url = flow.start()
          print('1. Go to: ' + authorize_url)
          print('2. Click "Allow" (you might have to log in first)')
          print ('3. Copy the authorization code.')
          webbrowser.open(authorize_url)
          code = input("Enter the authorization code here: ").strip()

           
          # This will fail if the user enters an invalid authorization code
          access_token, user_id = flow.finish(code)

          self.client = dropbox.client.DropboxClient(access_token)
          print('linked account: ', self.client.account_info())
    def do_Download(self, arg):
          """ Downloads a file From Dropbox of Your Choice """ 
          f, metadata = self.client.get_file_and_metadata('/Documents/' + input('File'))
          out = open(input('File'), 'wb')
          out.write(f.read())
          out.close()
          print(metadata)
    def  do_Save(self, arg): 
          """ Saves the Database and all of its contents 
          Define Save
          Save_To_Dropbox DB """
          self.db.commit()
          f = open(self.database_name + ".db","rb")    
          response = self.client.put_file(self.database_name + ".db", f)
          print("uploaded:", response)
    def  do_ReadOneContact(self, arg):
          """Reads One Contact selected by an index you specify"""
          self.cursor.execute("SELECT * FROM "+input("Contact Type:") + " WHERE id="+input("ID:"))
          record = self.cursor.fetchone()
          print("="*41)
          print("Name: " + record[1] + " " + record[2])
          print("="*41)
          print("Phone Number:" + record[3])
          print("="*41)
          print("Email: " + record[4])
          print("="*41)
          
    def  do_ReadAllContacts(self, arg):
          """Reads all of the Contacts."""
          for row in self.cursor.execute("SELECT * FROM " + input("Contact Type:")):
             print("="*41)
             print("Contact "+row[0])
             print("="*41)
             print("Name: " + row[1] + " " + row[2])
             print("="*41)
             print("Phone Number:" + row[3])
             print("="*41)
             print("Email: " + row[4])
             print("="*41)
    def  do_Load(self, arg): 
          """ Loads a  SQLite Database
          Define Load
          Load_From_ArcherVMFS Ask File:"""

          self.database_name = arg
          self.db = sqlite3.connect(self.database_name + ".db")
          self.cursor = self.db.cursor()
    def  help_overview(self):
          print("APPLICATION TITLE:  ProducktivShell\n")
          print("="*41)  
          print("CREATOR: Weldon Henson\n")
          print("="*41)

          print("The ProducktivShell Application is a cli application that deals with not just cloud services,\n") 
          print("but also has a special part of this python package for the contacts list.\n")
          print("ProdSh (ProducktivShell for short) uses Dropbox to save contacts using the pickle module,\n")
          print(" the Dropbox core API, and the Evernote API is used to save the contacts to an Evernote note, and more.\n")

    def  do_EOF(self, args):
          """Quits this program"""
          self.db.commit()
          sys.exit()
          
        


          
 
         