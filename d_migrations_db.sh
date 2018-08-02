# Script to delete migrations and db.sqlite3 file
for file in $(ls -l | awk $'{print $9}')
do
	if [ -d "$file/migrations/" ]
	then
		echo "Trying delete $file/migrations/*";
		rm -r "$file/migrations/" &> /dev/null;
		if [ $? -eq 0 ]
		then
			echo "Done...";
		else
			echo "Failed, error code $?";
		fi	
	fi
done

echo "Trying delete db.sqlite3 file";
rm db.sqlite3 &>/dev/null
if [ $? -eq 0 ];
then
	echo "Done..";
else
	echo "Failed, error code $?";
fi
