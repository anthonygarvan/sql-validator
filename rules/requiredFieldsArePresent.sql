SELECT fieldname FROM schemas 
LEFT JOIN raw_header rh
ON fieldname = col_name
WHERE required = 'TRUE'
AND rh.col_name IS NULL;