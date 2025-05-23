# File analysis module for LM Studio Chat
# This handles automatic file analysis based on file type

import os
import json
import csv
import mimetypes
from typing import Dict, Any, List, Optional

# Try to import optional dependencies without causing errors
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class FileAnalyzer:
    """Class for analyzing files of different types and providing insights."""
    
    @staticmethod
    def analyze_file(file_path: str) -> Dict[str, Any]:
        """
        Analyze a file based on its type and return structured insights
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with analysis results
        """
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}
            
        # Get file extension and base name
        _, ext = os.path.splitext(file_path.lower())
        filename = os.path.basename(file_path)
        
        # Initialize analysis result
        analysis = {
            "type": "unknown",
            "summary": f"File: {filename}",
            "details": {}
        }
        
        # Analyze based on file extension
        if ext == '.csv':
            return FileAnalyzer._analyze_csv(file_path, analysis)
        elif ext == '.json':
            return FileAnalyzer._analyze_json(file_path, analysis) 
        elif ext in ['.txt', '.md', '.log']:
            return FileAnalyzer._analyze_text(file_path, analysis)
        elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            return FileAnalyzer._analyze_image(file_path, analysis)
        else:
            # Generic file info
            return FileAnalyzer._analyze_generic(file_path, analysis)
    
    @staticmethod
    def _analyze_csv(file_path: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze CSV files"""
        analysis["type"] = "csv"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.reader(f)
                headers = next(csv_reader, [])
                
                # Count rows (limited to first 1000 for performance)
                row_count = 0
                data_sample = []
                for i, row in enumerate(csv_reader):
                    if i < 5:  # Get sample of first 5 rows
                        if len(row) == len(headers):
                            data_sample.append(dict(zip(headers, row)))
                    row_count += 1
                    if row_count >= 1000:
                        row_count = "1000+ (showing first 1000 only)"
                        break
                        
            analysis["details"] = {
                "headers": headers,
                "rowCount": row_count,
                "sample": data_sample
            }
            
            analysis["summary"] = f"CSV file with {len(headers)} columns and {row_count} rows."
            
        except Exception as e:
            analysis["details"]["error"] = f"Error reading CSV: {str(e)}"
            
        return analysis
    
    @staticmethod
    def _analyze_json(file_path: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze JSON files"""
        analysis["type"] = "json"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # Determine if it's a dict or list
            if isinstance(json_data, dict):
                keys = list(json_data.keys())
                analysis["details"] = {
                    "objectType": "object",
                    "keyCount": len(keys),
                    "topLevelKeys": keys[:10],  # First 10 keys
                    "hasMoreKeys": len(keys) > 10
                }
                analysis["summary"] = f"JSON object with {len(keys)} top-level keys."
                
            elif isinstance(json_data, list):
                analysis["details"] = {
                    "objectType": "array",
                    "length": len(json_data),
                    "sample": json_data[:3] if len(json_data) > 0 else []  # First 3 items
                }
                analysis["summary"] = f"JSON array with {len(json_data)} items."
                
        except Exception as e:
            analysis["details"]["error"] = f"Error reading JSON: {str(e)}"
            
        return analysis
    
    @staticmethod
    def _analyze_text(file_path: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze text files"""
        analysis["type"] = "text"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(5000)  # Read first 5000 chars
                
            lines = content.split('\n')
            line_count = len(lines)
            word_count = len(content.split())
            char_count = len(content)
            
            analysis["details"] = {
                "lineCount": line_count,
                "wordCount": word_count,
                "charCount": char_count,
                "preview": content[:200] + ('...' if len(content) > 200 else '')
            }
            
            analysis["summary"] = f"Text file with {line_count} lines and {word_count} words."
            
        except Exception as e:
            analysis["details"]["error"] = f"Error reading text file: {str(e)}"
            
        return analysis
    
    @staticmethod
    def _analyze_image(file_path: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze image files"""
        analysis["type"] = "image"
        
        try:
            mime_type, _ = mimetypes.guess_type(file_path)
            file_size = os.path.getsize(file_path)
            
            analysis["details"] = {
                "mimeType": mime_type,
                "fileSize": file_size,
            }
            
            # If PIL is available, get image dimensions
            if PIL_AVAILABLE:
                try:
                    with Image.open(file_path) as img:
                        width, height = img.size
                        analysis["details"]["dimensions"] = f"{width} x {height}"
                        analysis["details"]["format"] = img.format
                        analysis["details"]["mode"] = img.mode
                except Exception as img_err:
                    analysis["details"]["pil_error"] = str(img_err)
            
            analysis["summary"] = f"Image file ({os.path.splitext(file_path)[1].replace('.', '')})"
            if "dimensions" in analysis["details"]:
                analysis["summary"] += f", {analysis['details']['dimensions']}"
            
        except Exception as e:
            analysis["details"]["error"] = f"Error analyzing image: {str(e)}"
            
        return analysis
    
    @staticmethod
    def _analyze_generic(file_path: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze any file type with basic information"""
        try:
            file_size = os.path.getsize(file_path)
            mime_type, _ = mimetypes.guess_type(file_path)
            
            analysis["details"] = {
                "fileSize": file_size,
                "mimeType": mime_type or "unknown"
            }
            
            # Format file size
            size_str = f"{file_size} bytes"
            if file_size > 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            if file_size > 1024 * 1024:
                size_str = f"{file_size / (1024 * 1024):.1f} MB"
                
            analysis["summary"] = f"File: {os.path.basename(file_path)}, {size_str}"
            
        except Exception as e:
            analysis["details"]["error"] = f"Error analyzing file: {str(e)}"
            
        return analysis

# Main function for testing
if __name__ == "__main__":
    print("File Analyzer Module")
    # Test with a sample file if needed
    # test_file = "example.csv"
    # print(FileAnalyzer.analyze_file(test_file))
