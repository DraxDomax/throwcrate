ThrowCrate: Dropping boxes is for losers!

A.	What is this?
	A file-synchronization utility. User starts the "server" (a slave that keeps an exact duplicate of the master's files and folders)
	and provides a "destination" folder, where the duplicates will be stored.
	User then starts the client, provides the folder to watch and create a tracked duplicate of.
	
B.	Really, though... What is this?
	This is interview homework prepared by a Java-dude in very shaky Python. It's a POC at best. Just wanted to show a decent
	coding ability in Python.

C.	How to use?
	You will need a platform or two for the client and server to reside in. They should be running OS's that have a Python 3.8
	implementation. ThrowCrate has some ideas about OS-independece but not fully tested. Please use Windows :)
	* Edit the client.py file, line #10, to point to your server host
	* Server and cliet agree on port 9181, which you should either have opened on both platforms, or configured in .py files
	* Each Client or Server should start without any environments configured or modules linked.
	* Start server first ("python3.8 server"), provide back up destination 
	* Then, start client ("python3.8 client"), provide directory to watch
	* Observe consoles of each side of the system
	* Move files/folders in/out of the watched directory. 
	* Try also to add files which the server has already (as different-name or different-location).
	* Try adding the same files (as different-name or different-location) into the watched dir at once.
	* Behold the beauty that is ThrowCrate! (destination folder should have the same stuff as the tracked one)
	* Kill each process when done
	
C.	What are the limitations?
	There are no known limitations but it's a lot easier to define the things that were tested, than the things that were not...
	Tested (all passed):
	- folder-within-folder, up to 5 layers
	- 40 files uploaded to the watched directory at once, each 5KB
	- 3-the-same files (should only upload one)
	- 2-the-same-as-one-on-the-server (should not upload anything, just clone)
	- Delete/create folders while syncing
	- Deleted 10 folders at once
	- Deleted a 5-layer folder
	- Created (copied from an unwatched dir) a 5-layer folder
	- Created excessive files/folders at the "destination" (system detecs and deletes)

D.	Features:
	- Developed initially with some os-agnosticism. Although ultimately untested, I imagine any os-related problem will be quick to fix
	- For now, let's say Windows-only
	- IPv4, streaming sockets only
	- MD5-per-file client-side and server-side file upload optimization
	- Some automated tests
	- Some simple "logging" on screen of each client/server
	
E.	Ideas to improve:
	1.	More tests
	2.	Feedback from users
	3.	"Warning: There's already a used source directory: /// New source directory will invalidate currect files in destination"
	4.	Move hardcoded constancts to config file
	5.	Ignore files by regex (.ds, .ppk)
	6.	Remove files from payload, if quota is exceeded with payload
	7.	Warning for sensitive dirs ("C:\Windows")
	8.  Warning for huge dir content ("Are you sure you want to share this dir with +10,000 files?")
	9.	Support for multiple directories
	10. Support for network dirs
	11. Support for multiple destinations
	12. Low destination disk space warning
	13. Real-time speed indicator
	14. Server Telemetry: Uptime, used/quota, last file update time (transBytes, fileBytes...
	15. Compressed transmission
	16. Fixed-Chunk-Size upload optimization (don't upload parts of files that already exist)
	17. IPv6 Support
	18. SSL by default
	19. Hash client and server executables, use as matching versions (to make sure they can talk to each other
	20. Encrypted file storage
	21. Compressed file storage
	22. Input control (watched vs. watched/)
	23. General code cleanup
	24. Learn what are static fields in Python :)
	
E.	Feedback from candidate:
	That was probably more homework than I've ever done for all my interviews, combined :)
	That being said, it was fun, I learned a lot of Python and maybe the program can even
	be useful to me (I do like my files and I don't like DropBox/OneDrive/etc...)
	
	Yes, you can see I am a Python novice but perhaps not totally hopeless?
	Some of the stuff I copy pasted, I provided links for as code comments
	Some of the stuff I changed a lot, I appropriated as my own work :)
	
	Time spent:
	00:30 - Reading requirement and planning out solution
	04:30 - Crash course in Python and PyCharm
	02:00 - Basic client/server message tranceivers
	02:00 - Basic file/folder create/delete Python IO operations
	01:00 - Combine networking and IO into one working system with hard-coded messages
	01:00 - Settle on a message protocol
	02:00 - Test and patch up
	01:30 - Introduce some automated tests
	00:30 - Docs, chats, github and other admin
	
	Total: 15 hrs
	