# Microsoft Teams [per User and per Computer] (x64) AutoPkg recipes
**download** (get the actual installer)  
**build** (alter the MSI to get the needed behaviour)  
**BMS** (import the package into baramundi server)  

**Features:**  
Installs per machine or per user.  
Auto updater is disabled (on per machine version only).  
Desktop shortcut is disabled by default.  

# Microsoft Teams Teams Work or School MSIX (x64) AutoPkg recipes
**download** (get the actual installer)  
**build** (alter the MSI to get the needed behaviour)  
**BMS** (import the package into baramundi server)  

**Features:**  
Installs per machine.  
Auto updater is enabled.  

# Microsoft Edge Chromium (x64/x86) AutoPkg recipes
**download** (get the actual installer)  
**build** (enhance the MSI with additional properties)  
**BMS** (import the package into baramundi server)  

**Features:** 
Installs per machine.  
Auto updater is disabled (by GPO setting).  
Desktop shortcut is disabled by default.  


# Microsoft DotNet Desktop Runtime x64 AutoPkg recipes
**download** (get the actual installer)  
**build** (bring the installer into position)  
**BMS** (import the package into baramundi server)  

**Features:**  
Installs per machine.  
Use the 'RELEASE' property in a seperate override to get another major release than '6.0'  
Auto updater is enabled.  


# Microsoft WebView2Runtime x64 AutoPkg recipes
**download** (get the actual installer)  
**build** (bring the installer into position)  
**BMS** (import the package into baramundi server)  

**Features:**  
Installs per machine.  
Auto updater is enabled.  
Has a recipe for the evergreen installer too.  


# Microsoft Microsoft PowerToys (x64) AutoPkg recipe
**download** (get the actual installer)  
**build** (extract the MSI and bring into into position)  
**BMS** (import the package into baramundi server)  

**Features:** 
Installs per machine.  
Auto updater is disabled.  
Desktop shortcut is disabled by default.  


# Microsoft Visual Studio Code (x64) AutoPkg recipes
**download** (get the actual installer)  
**build** (enhance the MSI with additional properties)  
**BMS** (import the package into baramundi server)  

**Features:** 
Installs per machine.  
Auto updater is disabled (by GPO setting).  
Desktop shortcut is disabled by default.  


To use the baramundi import recipes,<br>
the following variables need to be specified in the AutoPkg config.json file:<br>
  ```"BMS_IMPORT_OU_GUID": "11111111-ABCD-1234-ABCD-12345678ABCD",
  "BMS_IMPORT_PATH_TST": "\\\\domain\\path",
  "BMS_SERVER1": "server.domain.tld",
  "BMS_SERVER_PORT": "443",
  "BMS_USERNAME": "domain\user",