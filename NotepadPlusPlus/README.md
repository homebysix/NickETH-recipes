# recipes
Notepad++ AutoPkg recipes
download (get the actual installer)
build (create an MSI with all the features)
BMS (import the package into baramundi server)

Features:
NPP main progam
Plugins:
HexEdit
CompareP
JS Tool
Auto updater will not be installed and is disabled.
Desktop shortcut is disabled by default.

To use the baramundi import recipe, 
the following varibles need to be specified in the AutoPkg config.json file:
  "BMS_IMPORT_OU_GUID": "11111111-ABCD-1234-ABCD-12345678ABCD",
  "BMS_IMPORT_PATH_TST": "\\\\domain\\path",
  "BMS_SERVER1": "server.domain.tld",
  "BMS_SERVER_PORT": "443",
  "BMS_USERNAME": "",