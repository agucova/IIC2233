returnCode=0
for i in $(find . -name "*.py" -type f); do
	 length="$(wc -l < "$i" | xargs)"
	 if [[ "$length" -gt "400" ]] ; then
	 	echo "$i: $length"
	 	returnCode=1
	 fi
done

exit $returnCode
