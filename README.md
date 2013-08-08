Tyrant-SQL
==========

Powerful GUI SQL injection Tool. SQLMap's GUI version.


Requeriments
============

->Python 2.7
    Site: http://www.python.org/download/releases/2.7.5/
    
->PySide 1.2.0
    Site: http://qt-project.org/wiki/Category:LanguageBindings::PySide::Downloads
    
    
How to run
==========

Unzip the folder and run the file Tyrant.py with your Python 2.7.

Using
=====

->Method GET:
    Just put the vulnerable link in the edit line and press Analyze.
    Wait the process finish and navigate by the databases and tables avaliables
    
->Method POST:
    Put the vulnerable link, without the POST variables and set this variables in POST Data input
    (e.g. Link = 192.168.0.4/index.php
    Posta data = id=1).
    Press Analyze and wait the process finish.
    
Raw Data
========

With Raw Data table you can see more information about the sql injection. Raw Data is the Sqlmap output. 
