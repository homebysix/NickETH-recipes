# Nessus-Agent AutoPkg recipes
**download** (get the actual installer)  
**build** (create an MSI with all the features)  
**BMS** (import the package into baramundi server)  

**Features:**  
Nessus-Agent main progam  
Auto updater will not be installed and is disabled.  
Desktop shortcut is disabled by default.  
See the BDS-Script for options.  
A varible for the Nessus Group has to be created in BMS.  

To use the baramundi import recipe,<br>
the following varibles need to be specified in the AutoPkg config.json file:<br>
  ```"BMS_IMPORT_OU_GUID": "11111111-ABCD-1234-ABCD-12345678ABCD",
  "BMS_IMPORT_PATH_TST": "\\\\domain\\path",
  "BMS_SERVER1": "server.domain.tld",
  "BMS_SERVER_PORT": "443",
  "BMS_USERNAME": "user",
  "NESSUS_SERVER": "yourserver.com",
  "NESSUS_KEY": "yourkey",
  "NESSUS_PORT": "yourport",