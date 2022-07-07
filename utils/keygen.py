# 
# Generate a Python Cryptograpic Key File
#
# 
#
# 
import sys
import os
from getopt import getopt

ME       = os.path.split(sys.argv[0])[-1]  # Name of this file
MY_PATH  = os.path.dirname(os.path.realpath(__file__))  # Path for this file
VERSION  = "1.0.1"
VERBOSE  = False
DEBUG    = False
KEY_FILE = "a.key"

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
   print(f"\n\n{ME}, Version {VERSION}, Harold's Cryptographic Key Generator.")
   print(" ")
   print("SUMMARY:")
   print("This program generates a cryptographic key file that you can use to ")
   print("encrypt and decrypt a string or even an entire file.")
   print(" ")
   print(f"USAGE: {ME} [OPTIONS] [KEY_FILENAME]")
   print(" ")
   print("OPTIONS: ")
   print("   -h --help      Display this message. ")
   print("   -v --verbose   Runs the program in verbose mode, default: {VERBOSE}. ")
   print("   -d --debug     Runs the program in debug mode (implies verbose). ")
   print(" ")
   print("EXIT CODES: ")
   print("    0 - Successful completion of the program, all tests passed. ")
   print("    1 - Bad or missing command line arguments. ")
   print("    2 - Generated key file FAILED validation, key file removed")
   print("    3 - Missing required 'cryptography' library" )
   print("    4 - Unable to write key to file")
   print(" ")
   print(f"NOTE: Default KEY_FILENAME is '{KEY_FILE}'")
   print(" ")
   print("EXAMPLES: ")
   print("    TODO - I'll make some examples up later. ")
   print(" ")

# Parse and Process the command line options
try:
   arguments = getopt(sys.argv[1:],'hvd',['help','verbose','debug'])
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
except Exception as e:
    write_message(f"Bad or missing command line option(s)\n         {str(e)}\n\n", 'error')
    usage()
    sys.exit(1)

# Check for an optional key file name
if not sys.argv[-1].startswith('-') and len(sys.argv) > 1:
   KEY_FILE = sys.argv[-1] 

try:
   from cryptography.fernet import Fernet
except ImportError:
   m = "Missing Cryptography Library\nTry: pip install cryptography" 
   write_message(m, "error")    
   sys.exit(3)


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
