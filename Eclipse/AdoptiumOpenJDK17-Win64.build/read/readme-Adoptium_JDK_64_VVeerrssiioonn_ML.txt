Adoptium Open JDK x64 11.0.100 ML (Multi-Language)
Java Development Kit for x64 Windows.
Adoptium is the successor of AdoptOpenJDK.
1:1 substitution for Oracle JavaDK

Tested on Windows 10 + 11

Optional features:
FeatureEnvironment	Add to PATH environment variable.
FeatureJavaFX		Install JavaFX
FeatureJarFileRunWith	Associate .jar files to run with AdoptOpenJDK
FeatureJavaHome		Set JAVA_HOME environment variable.
FeatureOracleJavaSoft	JavaSoft (Oracle) registry keys	Overwrites the reg keys HKLM\Software\JavaSoft (Oracle).
To install an additional feature, add ADDLOCAL=feature1,feature2...

To install all features to a machine, use this command:
msiexec /i "Adoptium_JDK_Hotspot_64_11.0.100.0_ML.msi" ALLUSERS=1 ADDLOCAL=ALL

Slient Install: msiexec /i "Adoptium_JDK_Hotspot_64_11.0.100.0_ML.msi" /qn (absolute silent) or /qb! (with progress-dialog).

All MSI-versions from Adopt are found and automatically removed. Only one version can be installed.

Features in this version:
- Multi-Language enu, deu, fra.
- JavaFX support.

Release 1.0, Build 1
20191115, by AutoPkg