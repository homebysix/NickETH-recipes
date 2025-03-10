Mozilla Firefox 135.0.0 ML (Multi-Language)

Webbrowser. No one alternative to Chrome/Edge.

Tested mit Windows 10 + 11

See the release notes for changes.
Mozilla Release Notes zu FF 135.0.0: https://www.mozilla.org/en-US/firefox/135.0/releasenotes/

Options: - DEFAULTPREFS=0   --> Default-Prefs can be disabled. See create-log too.
	  - DESKTOP_SC=0     --> Shortcuts on the desktop can be disabled.
	  - QUICKLAUNCH_SC=0 --> Shortcuts on the QuickLaunch-Toolbar can be disabled.
	  - PROFMIGR=0	     --> The Profile Migration Wizard can be disabled.

Start the installation with the following command line:
msiexec /i "FireFox_66.0.2_ML.msi" DESKTOP_SC=0 QUICKLAUNCH_SC=0 DEFAULTPREFS=0

Slient Install: msiexec /i "FireFox_66.0.2_ML.msi" /qn (totally silent) or /qb! (with progress dialog).

Features in this release:
- Multi-Language enu, deu, fra, ita, rum.
- Spellchecker for enu, deu, fra, ita.
- Firefox language follows the system language automatically (with multilanguge-pack too).
- Almost all settings can be set through group policies. See Firefox policies for mor information.
- Extra search plugins for: ETH-Phonebook, NEBIS-/Swissbib query.
- And also for: local.ch, map.search.ch, anibis.ch, ricardo.ch, toppreise.ch
- Noscript: Control the execution of Javascript and other active content on certain sites.
- With romansh interface
- With Adblock Plus extension.

Release 135.0.0, Build1
20190401, Nick Heim
