# Hazel programming language.
Hazel is a source-available interpreted scripting language created by John O' Regan. It runs .haz files using a Python-based interpreter and a simple batch CLI.

## Installation Warning

To install Hazel, you **must manually add the `Hazel` folder to your system's `PATH` environment variable**.

> Example:  
> Add `C:\Users\YourName\OneDrive\Desktop\Hazel` to your user PATH variable.

Without this, the `HAZEL` and `HAZA` commands will not work globally.

# Manual setup
To run HAZEL from any terminal, you must add Hazel’s folder to your system’s environment PATH manually.
> Example path:  
> C:\Users\YourName\OneDrive\Desktop\Hazel

 # Steps:

**1.**  Open System Properties → Environment Variables.

**2.**  Under User variables, find and select Path → click Edit.

**3.**  Click New and add Hazel’s directory.

**4.**  Click OK and restart your terminal.

> If you see:  
> 'HAZEL' is not recognized as an internal or external command

It means your PATH isn’t set correctly.

If your environment variable is too long, remove unnecessary entries first.

# Included files

> HAZEL.bat – CLI interface  
> HAZA.bat – Script runner  
> HAZINT.py – Hazel interpreter  
> licence.md – Hazel license information


# Licence

Hazel is source-available. See licence.md for terms.
You can use, study, and build tools for Hazel, but you may not do the follwing:

- Rebrand or sell Hazel

- Distribute malware with Hazel

- Remove author attribution
