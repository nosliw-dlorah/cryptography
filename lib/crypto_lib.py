# 
# This library holds some common functionality like reading and writing 
# flat text config file and reading and writing JSON files that support 
# both a clear text implementation and an encryption implementation.
# To access encrypt or decrypt functionality, just call the same method 
# you would normally call but, add a key file argument.  
# 
# To execute the unit tests simply run this libray as a main program.
# -- H. Wilson, July 2022

import os
import sys
import pytest 
from cryptography.fernet import Fernet


# For support of Lunux console test colorization 
# on windows platform systems.
if sys.platform == "win32":
   try:
      import colorama 
      colorama.init()
   except: 
      sys.stderr.write("WARNING -- Sorry, No color for Windows platform systems.\nTry: pip install colorama.\n")

def read_config_file(config_file, key_file=None, delimiter=' '):
   """ Read a text flat file where each line in the file is 
       a key-valueH pair and return a dictionary of key-valuie 
       pairs parsed from that file. Supports text flat files 
       with white space and comment lines starting with a '#' 
       character. 
       Optionally supports a cryptographic key file 
       if decrypting the config file is necessary. """
   configs = {}
   WARNING = "\033[33mWARNING\033[0m" # \___ Linux-specific colorization
   ERROR   = "\033[31mERROR\033[0m"   # /
   try:
      # Get the configuration data from the config file as one big string.
      # Decrypt if necessary   
      if key_file != None:
         if not os.path.isfile(key_file): raise ValueError(f"Unable to locate key file '{key_file}'")        
         with open(key_file, 'rb') as filekey: crypto_key = filekey.read()
         cryptographic_component = Fernet(crypto_key)
         with open(config_file, 'rb') as enc_file: encrypted = enc_file.read() 
         config_data  = cryptographic_component.decrypt(encrypted).decode() 
      else: 
         config_data = open(config_file, 'r').read() 
      # Parse the config data obtained from the file and try to compile a 
      # dictionary of key-value pairs from the lines of the file respecting 
      # white space and comment lines .
      line_counter = 0 
      for line in config_data.split('\n'):   
         line_counter += 1 
         line = line.strip()
         if len(line) == 0: pass
         elif line.startswith('#') : pass
         elif delimiter not in line: 
            sys.stderr.write(f"{WARNING} -- Invalid line missing delimiter in {config_file} line {line_count}\n'{line}'\n")
            sys.stderr.flush()
         else:
            data_elements = line.split(delimiter, 1)
            if len(data_elements) != 2: 
               sys.stderr.write(f"{WARNING} -- Invalid line in {config_file} line {line_count}\n'{line}'\n")
               sys.stderr.flush()
            configs[data_elements[0]] = str(data_elements[-1])    
   except Exception as e: 
      sys.stderr.write(f"{ERROR} -- \n{str(e)}\n")
      sys.stderr.flush()
      configs = None
   finally: return configs

def write_config_file(config_file, config_data, key_file=None, delimiter=' '):
   """ writes a text flat file where each line in the file is 
       a key-value pair obtained from the config_data dictoinary supplied.  
       Optionally supports a cryptographic key file 
       if decrypting the config file is necessary. if Anything goes wrong 
       then None is returned. """
   WARNING = "\033[33mWARNING\033[0m" # \___ Linux-specific colorization
   ERROR   = "\033[31mERROR\033[0m"   # /
   config_string = ""
   try: 
      if not type(config_data) == type({}): raise ValueError(f"The config_data argument must be of type dictionary")
      if os.path.isfile(config_file): sys.stderr.write(f"\n{WARNING} -- Config file {config_file} exists and will be overwritten\n")
      for item in config_data:
         config_string += f"{str(item)}{delimiter}{str(config_data[item])}\n"
      print(f"CONFIG STRING:\n{config_string}")   
      if key_file != None:
         if not os.path.isfile(key_file): raise ValueError(f"Unable to locate key file '{key_file}'")        
         with open(key_file, 'rb') as filekey: crypto_key = filekey.read()
         cryptographic_component = Fernet(crypto_key)
         encrypted = cryptographic_component.encrypt(config_string.encode())
         with open(config_file, 'wb') as encrypted_file: encrypted_file.write(encrypted)
      else:
         with open(config_file, 'w') as output_file: output_file.write(config_string)
      if os.path.isfile(config_file): return_value = True
      else: raise ValueError(f"Unable to create configfile {config_file}")   
   except Exception as e:
      sys.stderr.write(f"{ERROR} -- \n{str(e)}\n")
      sys.stderr.flush()
      return_value = False 
   finally: return return_value   
   
# === UNIT TESTS ==============================================================   
@pytest.fixture(scope="class")
def setup(request):
   # Test Setup: Define test data and create test files 
   key             = Fernet.generate_key()
   key_file        = "a.key"
   config_file     = "test_config_file.txt"
   enc_config_file = "test_config_file.txt"
   config_data     = {"Key_1":"Value 1", "Key_2":"2", "Key_3":"3.1415926"}
   request.cls.key_file        = key_file         # \
   request.cls.config_data     = config_data      #  \__ Data for test cases 
   request.cls.config_file     = config_file      #  /
   request.cls.enc_config_file = enc_config_file  # /
   with open(key_file, 'wb') as filekey: filekey.write(key)
   # Execute test cases 
   yield  
   # Test Takedown: Clean up any left over files
   if os.path.isfile(key_file):        os.remove(key_file) 
   if os.path.isfile(config_file):     os.remove(config_file)
   if os.path.isfile(enc_config_file): os.remove(enc_config_file)

@pytest.mark.usefixtures("setup")
class Test_crypto_lib:

   def test_01_write_config_file(self):
      assert write_config_file(self.config_file, self.config_data)

   def test_02_read_config_file(self):
      config_data = read_config_file(self.config_file)
      assert config_data == self.config_data

   def test_03_write_enc_config_file(self):
      assert write_config_file(self.enc_config_file, self.config_data, self.key_file)

   def test_04_read_enc_config_file(self):
      config_data = read_config_file(self.enc_config_file, self.key_file)
      assert config_data == self.config_data




if __name__ == "__main__":
   pytest.main(['-vv', '-s', __file__])