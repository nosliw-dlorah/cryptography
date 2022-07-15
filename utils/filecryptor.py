#
# Encrypr or decrypt a file using a cryptographic key
#
#
#
#
import sys
import os
from getopt import getopt

ME          = os.path.split(sys.argv[0])[-1]  # Name of this file
MY_PATH     = os.path.dirname(os.path.realpath(__file__))  # Path for this file
VERSION     = "1.0.1"
VERBOSE     = False
DEBUG       = False
KEY_FILE    = "a.key"
EXTENSION   = "enc"
ENCRYPT     = False
SOURCE_FILE = None
KEY_FILE    = None

def write_message(message, level="info"):
   """ Write a message to the console """
   WARNING = "\033[33mWARNING\033[0m" # \___ Linux-specific colorization
   ERROR   = "\033[31mERROR\033[0m"   # /
   if level   == "info":
      sys.stdout.write(f"{message}\n")
      sys.stdout.flush()
   elif level == "warning":
      sys.stderr.write(f"{WARNING} -- {message}\n")
      sys.stderr.flush()
   elif level == "error":
      sys.stderr.write(f"{ERROR} -- {message}\n")
      sys.stderr.flush()
   else:
      sys.stdout.write(f"{message}\n")
      sys.stdout.flush()

def usage():
   """ Prints a usage message to the console """
   print(f"\n\n{ME}, Version {VERSION}, Harold's file cryptography utility.")
   print(" ")
   print("SUMMARY:")
   print("This program encrypts or decrypts a source file using a cryptographic key.")
   print("The cryptographic key is supplied via command line argument as a filename. ")
   print("Decrypted reuslts are sent to Standard Out that you may redirect to a file.")
   print(f"Encrypted results are saved directly to a file with the extension .{EXTENSION}")
   print(" ")
   print(f"USAGE: {ME} [OPTIONS] KEY_FILE SOURCE_FILE")
   print(" ")
   print("OPTIONS: ")
   print("   -h --help      Display this message. ")
   print("   -v --verbose   Runs the program in verbose mode, default: {VERBOSE}. ")
   print("   -d --debug     Runs the program in debug mode (implies verbose). ")
   print("   -e --encrypt   Used to encrypt a file, default operation is to decrypt")
   print(" ")
   print("ARGUMENTS: ")
   print("   KEY_FILE      The file that holds the cytptographic key")
   print("   SOURCE_FILE   The source file to be eitehr encrypted or decrypted with the key")
   print(" ")
   print("EXIT CODES: ")
   print("    0 - Successful completion of the program, all tests passed. ")
   print("    1 - Bad or missing command line arguments. ")
   print("    2 - Generated key file FAILED validation, key file removed")
   print("    3 - Missing required 'cryptography' library" )
   print("    4 - Unable to loacate cryptographic key file")
   print("    5 - Unable to read or invalid cryptographic key to file")   
   print("    6 - Unable to loacate source file")   
   print("    7 - Unable to read source file")   
   print("    8 - Unable write encrpyted file")   
   print(" ")
   print("EXAMPLES: ")
   print("   1.) Decrypt a file with a key and save the results to secrets.txt")
   print(f"   {ME} key_file.dat secrets.dat > secrets.txt")
   print(" ")
   print("   2.) Encrypt a text file using a key and save to encrypted file secrets.dat")
   print(f"   {ME} --encrypt key_file.dat secrets.txt")
   print(f"   {ME} -e key_file.dat secrets.txt")
   print(" ") 

# Parse and Process the command line options
try:
   arguments = getopt(sys.argv[1:],'hvde',['help','verbose','debug', 'encrypt'])
   # --- Check for a help option
   for arg in arguments[0]:
      if arg[0]== "-h" or arg[0] == "--help":
         usage()
         sys.exit(0)
   # --- Check for a verbose option
   for arg in arguments[0]:
      if arg[0]== "-v" or arg[0] == "--verbose":
         VERBOSE = True
   # --- Check for a debug option
   for arg in arguments[0]:
      if arg[0]== "-d" or arg[0] == "--debug":
         DEBUG   = True
         VERBOSE = True
   # --- Check for an encrypt option
   for arg in arguments[0]:
      if arg[0]== "-e" or arg[0] == "--encrypt":
         ENCRYPT = True
   # -- Check for the key file and source file arguments
   if len(sys.argv) < 3: 
      raise ValueError("Missing required arguments: key file and/or source file")
   else:
      SOURCE_FILE = sys.argv[-1]
      KEY_FILE = sys.argv[-2]   
except Exception as e:
    write_message(f"Bad or missing command line option(s) and/or arguments\n         {str(e)}\n\n", 'error')
    usage()
    sys.exit(1)

# Check the source file exists
if os.path.isfile(SOURCE_FILE):
   if VERBOSE: 
      m = f"   -- Found source file {SOURCE_FILE}" 
      write_message(m)
else:    
   m = f"Unable to locate supplied source file {SOURCE_FILE}"
   write_message(m, 'error')
   sys.exit(6)

# Check the key file exists
if os.path.isfile(KEY_FILE):
   if VERBOSE: 
      m = f"   -- Found cryptographic key file {KEY_FILE}" 
      write_message(m)
else:
   m = f"Unable to locate supplied key file {KEY_FILE}"  
   write_message(m, 'error')
   sys.exit(4)

# Try to import the Cryptographic library
try:
   import cryptography 
   from cryptography.fernet import Fernet
   m = f"   -- Successfully imported the cryptography library version {cryptography.__version__}"
   if DEBUG: write_message(m)
except ImportError:
   m = "Missing Cryptography Library\nTry: pip install cryptography"
   write_message(m, "error")
   sys.exit(3)

# Verify key file and initialize cryptographic component
try: 
   with open(KEY_FILE, 'rb') as filekey: crypto_key = filekey.read()
   fernet = Fernet(crypto_key)
   if VERBOSE: write_message(f"   -- Valid key file '{KEY_FILE}'")
except Exception as e:
   m = f"Invalid cryptographic key file {KEY_FILE}\n         {str(e)}\n\n" 
   write_message(m , 'error') 
   sys.exit(5)

# Either encrypt or decrypt the source file using the cryptographic component 
if ENCRYPT:
    pass
else: # Decrypt
    pass 

sys.exit(0)

# Generate a random key
if VERBOSE: write_message("   -- Generating key ...")
# this just calls: base64.urlsafe_b64encode(os.urandom(32))
key = Fernet.generate_key()

# Try to write key to file
try:
   if VERBOSE: write_message(f"   -- Writing key file {KEY_FILE}  ...")
   with open(KEY_FILE, 'wb') as filekey: filekey.write(key)
except Exception as e:
   m = f"Unable to write key to file: {KEY_FILE}"
   write_message(m, "error")
   sys.exit(4)

# Verify key file
if VERBOSE: write_message(f"   -- Verifying key file '{KEY_FILE}'")
with open(KEY_FILE, 'rb') as filekey: test_key = filekey.read()
fernet = Fernet(test_key)
test_string = """
So, so you think you can tell
Heaven from Hell,
Blue skys from pain.
Can you tell a green field
From a cold steel rail?
A smile from a veil?
Do you think you can tell?

And did they get you to trade
Your heros for ghosts?
Hot ashes for trees?
Hot air for a cool breeze?
Cold comfort for change?
And did you exchange
A walk on part in the war
For a lead role in a cage?

How I wish, how I wish you were here.
We're just two lost souls
Swimming in a fish bowl,
Year after year,
Running over the same old ground.
What have we found?
The same old fears.
Wish you were here.
"""

if DEBUG: print(test_string)
encrypted_string = fernet.encrypt(test_string.encode())
if DEBUG: print(encrypted_string)
decrypted_string = fernet.decrypt(encrypted_string).decode()
if DEBUG: print(decrypted_string)
if decrypted_string == test_string:
   if VERBOSE: write_message(f"   -- Successfully verified key file '{KEY_FILE}'")
   exit_code = 0
else:
   m = f"Key file '{KEY_FILE}' FAILED validation, removing filels."
   write_message(m, "error")
   os.remove(KEY_FILE)
   exit_code = 2

if VERBOSE: write_message("Task Complete.")
sys.exit(exit_code)
