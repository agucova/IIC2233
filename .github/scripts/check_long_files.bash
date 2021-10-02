returnCode=0
for i in $(find . -name "*.py" -type f); do
	 lines="$(wc -l < "$i" | xargs)"
     maxlength="$(wc -L < "$i" | xargs)"
	 if [[ "$lines" -gt "400" || "$maxlength" -gt "100" ]] ; then
	 	echo "$i: $lines lines, $maxlength max_length"
	 	returnCode=1
	 fi
done

exit $returnCode
