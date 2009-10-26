#!/bin/sh
<<<<<<< .mine
mysqldump -u redtide --password="Wocej2KmEeb8Quak" --ignore-table=redtide2.registration_registrations_payment --ignore-table=redtide2.auth_permission --compact --compatible=ansi --default-character-set=binary redtide1 | grep -v '  KEY "' | grep -v '  UNIQUE KEY "' |
=======
mysqldump -u redtide --password="Wocej2KmEeb8Quak" --ignore-table=redtide2.registration_registrations_payment --ignore-table=redtide2.auth_permission --compact --compatible=ansi --default-character-set=binary redtide2 | grep -v '  KEY "' | grep -v '  UNIQUE KEY "' |
>>>>>>> .r666
perl -e 'local $/;$_=<>;s/,\n\)/\n\)/gs;print "begin;\n";print;print "commit;\n"' | 
perl -e 'local $/;$_=<>;s/ auto_increment//g; s/ unsigned//g; print;' |
perl -pe '
	if (/^(INSERT.+?)\(/) { 
		$a=$1; 
		s/\\'\''/'\'\''/g; 
		s/\\n/\n/g; s/\),\(/\);
		\n$a\(/g; 
	} ' > dump.sql
