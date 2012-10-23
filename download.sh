grep -h "</d:Id>" output/Documenten/* | sed "s/.*>\(.*\)<.*/\1/g" | sort -u | while read i; do
	if [ ! -f "output/Bestanden/$i" ]; then
		wget -O "output/Bestanden/$i" --no-check-certificate --http-user=SOS --http-password=Open2012 "https://api.tweedekamer.nl/APIDataService/v1/Documenten(guid%27$i%27)/\$value"
		# wget -O "output/Bestanden/$i" --no-check-certificate  --content-disposition --http-user=SOS --http-password=Open2012 "https://api.tweedekamer.nl/APIDataService/v1/Documenten(guid%27$i%27)/\$value"
	fi
done
