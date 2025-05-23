











































trying to analyze
                             # Analyze based on file        try:
                       if ext == '.csv':
                ret                return FileAnalyzer._   return FileAnalyzer._analyze_csv(file_path, analysis)
:
) 

    @staticmethod
    def _analyze_csv(file_path    @static    ddef _analyze_csv(file_path: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
e CSV files"""
        analysis["details"] = {}  # Initialize de  # Initialize details dictionary
        try:
           try:
with open(file_path, 'r', encoding='utf-8') as f:
                    csv_reader = csv.reader(f)
        
y
                  ader, [])
       ]["warning"] = "Failed to parse CSV headers"
                    # Count rows (limited t 1000 for performance)
   row_count = 0
                    
                    for i,     
sv_reader):
t sample of first 5 rows
a sample entry if headers exist and row size matches headers
n(row) == len(headers):
                                    data_sample.appen                   data_sample.append(dict(zip(headers, row)))
                                                  # If we can't create dict, just store the row
      data_sample.append({"row": row})
                        if row_coun            if row_count >= 1000:
     row_count = "1000+ (showing first 1000 only)"
                        break
           
                        "headers": hea": headers,
": row_count,
                "sample": data_sample
        }
                    analysis["summary"] headers)} columns and {row_count} rows."
except csv.Error as csv_error:
["error"] = f"CSV parsing error: {str(csv_error)}"
ry"] = "CSV file (parsing error)"
        except UnicodeDecodeErro  analysis["details"]["error"] = "CSV file contains non-UTF-8 characters"
CSV file (encoding error)"
          = f"Error reading CSV: {str(e)}"
ile (read error)"
        return analysis
    
    @staticmethod
    def _analyze_json analysis
    @st    def _analyze_json(file_path: str, analysis: Dict[str, Any]) -> Dict[str,lyze_json(file_path: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
""
        
        try:
            with open(f                     with open(file_path, 'r', encoding='utf-8') as f:
ry:
                
                    #                 it's a dict or list
            if isinstance(json_data, dict):
            keys = list(json_data.keys())
          ,
                "keyCount": len(keys),
elKeys": keys[:10],  # First 10 keys
ys": len(keys) > 10
                       analysis["summary"] = f"JSON object with {len(keys)} top-level keys."
            
 sis["details"] = {
        "objectType": "array",
:3] if len(json_data) > 0 else []  # First 3 items
                        analysis["summary"] = f"JSON aren(json_data)} items."
                        analysis["de= {
                            "value": str(json_data)
                        analysis["summary"] = f"JSON primitive value: {stN primitive value: {str(json_data)[:50]}"
                    analysis[        analysis["details"]["error"] = f"JSON syntax error: {str(e)}"
summary"] = "JSON file (invalid format)"
            analysis["details"]["error"] =analysis["details"]["error"] = "JSON file contains non-UTF-8 characters"
ummary"] = "JSON file (encoding error)"
    except Exception as e:
sis["details"]["error"] = f"Error reading JSON: {str(e)}"
        return analysis
    
    @staticmethod
    def _analyze_text(fil    
    @staticmethod
    def _an    @st    def _analyze_text(file_path:Any]) -> Dict[str, Any]:
nalyze text files"""
         try:
            # Tr            # Try to detect if it's a Try to detect if it's a binary file first
if FileAnalyzer._is_binary_file(file_path):
ils"] = {"error": "File appears to be binary, not text"}
ry file detected (not text)"
            with open(file_path, 'r', ncoding='utf-8') as f:
s

            line_count = len(lines)
        line_count = len(lines)
ontent.split())
            
            analysis["det
etails"] = {
                "lineCount": line_count,
: word_count,
": char_count,
t[:300] + ('...' if len(content) > 300 else '')
            
                        analysh {line_count} lines and {word_count} words."
