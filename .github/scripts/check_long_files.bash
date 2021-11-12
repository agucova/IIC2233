returnCode=0
for i in $(git ls-files | grep -E "\.py$" | xargs -d '\n' ls -1df 2>/dev/null); do
	 echo "Checking $i"
	 lines="$(wc -l < "$i" | xargs)"
     maxlength="$(wc -L < "$i" | xargs)"
	 if [[ "$lines" -gt "400" || "$maxlength" -gt "100" ]] ; then
	 	echo "$i: $lines lines, $maxlength max_length"
	 	returnCode=1
	 fi
done

exit $returnCode
