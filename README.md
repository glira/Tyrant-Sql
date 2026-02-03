Tyrant-SQL
==========

Powerful GUI SQL injection Tool. SQLMap's GUI version.

## ⚠️ Important Notice

**This is an updated version of the original Tyrant-SQL project.**

This fork has been updated by **Gemayel** to work with Python 3.10+ and modern libraries. The original code was written for Python 2.7 and PySide 1.2.0.

### Original Project

This project is based on the original work by **aron-bordin**. Special thanks to the original developer for creating this excellent SQLMap GUI tool.

**Original Repository:** [https://github.com/aron-bordin/Tyrant-SQL](https://github.com/aron-bordin/Tyrant-SQL)

### What Was Updated

- ✅ Migrated from Python 2.7 to Python 3.10+
- ✅ Updated from PySide 1.2.0 to PySide6
- ✅ Fixed all Python 2 to Python 3 syntax issues
- ✅ Updated Qt API calls to PySide6 compatible versions
- ✅ Improved error handling and output parsing
- ✅ Added SQLMap path configuration option
- ✅ Enhanced database and table detection algorithms
- ✅ Better support for modern SQLMap versions

## Requirements (Must be installed!!)
============

- **Python 3.10 or higher**
    - Download: https://www.python.org/downloads/
    
- **PySide6**
    - Install with: `pip install -r requirements.txt`
    
- **SQLMap** (optional - can use bundled version or configure custom path)
    - Download: https://github.com/sqlmapproject/sqlmap

## How to run
==========

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python3 Tyrant.py
   ```

3. Configure SQLMap path (if using external installation):
   - Go to **Tyrant → Preferences → Python tab**
   - Set the SQLMap path (e.g., `/home/user/.sec/sqlmap/sqlmap.py` or `/home/user/.sec/sqlmap` directory)

## Using
=====

### Method GET:
Just put the vulnerable link in the edit line and press **Analyze**.
Wait for the process to finish and navigate through the databases and tables available.

### Method POST:
Put the vulnerable link without the POST variables and set these variables in **POST Data** input.
(e.g., Link = `192.168.0.4/index.php`, Post data = `id=1`).
Press **Analyze** and wait for the process to finish.

## Raw Data
========

With Raw Data table you can see more information about the SQL injection. Raw Data is the SQLMap output.

## License
========

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## Credits
========

- **Original Developer:** aron-bordin - [Original Repository](https://github.com/aron-bordin/Tyrant-SQL)
- **Updated by:** Gemayel
- **Fork Repository:** [https://github.com/glira/Tyrant-Sql](https://github.com/glira/Tyrant-Sql)
- **Based on:** SQLMap (https://github.com/sqlmapproject/sqlmap) 
