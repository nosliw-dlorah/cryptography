#
# Encrypr or decrypt a file using a cryptographic key.
# -- H. Wilson, July 2022
#
# Please see keygen.py for generating a cryptographic key file.
#
# Cryptographic Specificastions:
# According to https://cryptography.io/en/latest/fernet/#limitations 
# Standard cryptographic primitives in use are:
#  AES in CBC mode with a 128-bit key for encryption; using PKCS7 padding.
#  HMAC using SHA256 for authentication.
#  Initialization vectors are generated using os.urandom().
# 
# TODO: Futuire version -- implement MultiFernet([key1, key2]) option 

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
   print(f"USAGE: {ME}  [OPTIONS]  KEY_FILE  SOURCE_FILE")
   print(" ")
   print("OPTIONS: ")
   print("   -h --help      Display this message. ")
   print("   -v --verbose   Runs the program in verbose mode, default: {VERBOSE}. ")
   print("   -d --debug     Runs the program in debug mode (implies verbose). ")
   print("   -e --encrypt   Used to encrypt a file, default operation is to decrypt")
   print(" ")
   print("REQUIRED ARGUMENTS: ")
   print("   KEY_FILE      The file that holds the cytptographic key")
   print("   SOURCE_FILE   The source file to be eitehr encrypted or decrypted with the key")
   print(" ")
   print("EXIT CODES: ")
   print("    0 - Successful completion of the program. ")
   print("    1 - Bad or missing command line arguments. ")
   print("    2 - Reserved, not used.")
   print("    3 - Missing required 'cryptography' library" )
   print("    4 - Unable to loacate cryptographic key file")
   print("    5 - Unable to read or invalid cryptographic key to file")   
   print("    6 - Unable to loacate source file")   
   print("    7 - Unable to read source file")   
   print("    8 - Unable write encrpyted file") 
   print("    9 - Unable decrypt encrpyted file with the key provided") 
   print(" ")
   print("EXAMPLES: ")
   print("   1.) Decrypt a file with a key and save the results to secrets.txt")
   print(f"   {ME} key_file.dat secrets.dat > secrets.txt")
   print(" ")
   print(f"   2.) Encrypt a text file using a key and save to encrypted file secrets.txt.{EXTENSION}")
   print(f"   {ME} --encrypt key_file.dat secrets.txt")
   print(f"   {ME} -e key_file.dat secrets.txt")
   print(" ") 

# Parse and process the command line options and arguments.
# I know the kids today are using argparse, but I like having 
# the help message readable in the source code. --HMW 
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
    write_message(f"Bad or missing command line option(s) and/or argument(s)\n         {str(e)}\n\n", 'error')
    usage()
    sys.exit(1)

# Check the source file exists
# Доверяй, но проверяй
if os.path.isfile(SOURCE_FILE):
   if VERBOSE: 
      m = f"   -- Found source file {SOURCE_FILE}" 
      write_message(m)
else:    
   m = f"Unable to locate source file {SOURCE_FILE}"
   write_message(m, 'error')
   sys.exit(6)

# Check the key file exists
# Доверяй, но проверяй
if os.path.isfile(KEY_FILE):
   if VERBOSE: 
      m = f"   -- Found cryptographic key file {KEY_FILE}" 
      write_message(m)
else:
   m = f"Unable to locate supplied key file {KEY_FILE}"  
   write_message(m, 'error')
   sys.exit(4)

# Try to import the Cryptographic library
#    This import is here in the middle of the code so that 
#    users may access the help/usage message even if the 
#    cryptographic library is not installed on hte system. 
try:
   import cryptography 
   from cryptography.fernet import Fernet
   m = f"   -- Successfully imported the cryptography library version {cryptography.__version__}"
   if DEBUG: write_message(m)
except ImportError:
   m = "Missing Cryptography Library\nTry: pip install cryptography"
   write_message(m, "error")
   sys.exit(3)

# Verify key file and initialize the cryptographic component
# Доверяй, но проверяй
try: 
   with open(KEY_FILE, 'rb') as filekey: crypto_key = filekey.read()
   cryptographic_component = Fernet(crypto_key)
   if VERBOSE: write_message(f"   -- Valid key file '{KEY_FILE}'")
except Exception as e:
   m = f"Invalid cryptographic key file {KEY_FILE}\n         {str(e)}\n\n" 
   write_message(m , 'error') 
   sys.exit(5)

# Either encrypt or decrypt the source file using the cryptographic component 
if ENCRYPT:
    OUTPUT_FILE = f"{SOURCE_FILE}.{EXTENSION}"
    if VERBOSE: 
       m = f"   -- Encrypting {SOURCE_FILE} with {KEY_FILE}, saving outout to {OUTPUT_FILE}"
       write_message(m)
    try:
       with open(SOURCE_FILE, 'rb') as file: clear_text = file.read()     
       encrypted = cryptographic_component.encrypt(clear_text)
       with open(OUTPUT_FILE, 'wb') as encrypted_file: encrypted_file.write(encrypted)
       if not os.path.isfile(OUTPUT_FILE): raise ValueError(f"Output file {OUTPUT_FILE} not created") 
       if VERBOSE: 
          m = f"   -- Successfully generated encrypted file {OUTPUT_FILE}"
          write_message(m)
    except Exception as e:
       m = f"Unable to create encrypted file.\n         {str(e)}\n\n" 
       write_message(m , 'error') 
       sys.exit(8)
else: # Decrypt
    if VERBOSE:
       m = f"   -- Decrypting {SOURCE_FILE} with {KEY_FILE}, writing results to standard out"
       write_message(m)
    try:
       with open(SOURCE_FILE, 'rb') as enc_file: encrypted = enc_file.read()
       clear_text = cryptographic_component.decrypt(encrypted).decode()
       print(clear_text)
    except Exception as e:
       m = f"Unable to create decrypted {SOURCE_FILE} with {KEY_FILE}.\n         {str(e)}\n\n" 
       write_message(m , 'error') 
       sys.exit(9)

sys.exit(0)
