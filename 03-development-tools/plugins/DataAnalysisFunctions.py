import json
import os
import csv
from typing import Optional
import base64
import re

from semantic_kernel.functions.kernel_function_decorator import kernel_function

class DataAnalysisFunctions:
    """Functions for analyzing and processing data files."""
    
    # The uploads directory
    UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
    
    @kernel_function(
        description="Parse and analyze CSV data",
        name="analyze_csv"
    )
    def analyze_csv_data(self, filename: str, query: Optional[str] = None) -> str:
        """
        Parse and analyze CSV data, optionally filtering by a query.
        
        Args:
            filename: The filename in the uploads directory
            query: Optional query to filter data (column=value)
            
        Returns:
            Analysis of the CSV data
        """
        try:
            # Create a safe filename
            safe_filename = os.path.basename(filename)
            file_path = os.path.join(self.UPLOAD_DIR, safe_filename)
            
            # Check if file exists
            if not os.path.exists(file_path):
                return f"Error: File {safe_filename} not found"
                
            # Check if it's a CSV file
            if not file_path.lower().endswith('.csv'):
                return f"Error: {safe_filename} is not a CSV file"
            
            # Read CSV data
            data = []
            columns = []
            with open(file_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.reader(f)
                columns = next(csv_reader)  # Get header row
                for row in csv_reader:
                    if len(row) == len(columns):
                        data.append(dict(zip(columns, row)))
            
            # If no data was found
            if not data:
                return "The CSV file is empty or has no valid rows"
            
            # Filter by query if provided
            if query:
                filtered_data = []
                query_parts = query.split('=')
                
                if len(query_parts) == 2:
                    col_name = query_parts[0].strip()
                    filter_value = query_parts[1].strip()
                    
                    if col_name in columns:
                        filtered_data = [row for row in data if row[col_name] == filter_value]
                    else:
                        return f"Column '{col_name}' not found in CSV"
                else:
                    return "Invalid query format. Use 'column=value'"
                    
                data = filtered_data
            
            # Basic statistics
            result = [f"CSV Analysis: {safe_filename}"]
            result.append(f"Total rows: {len(data)}")
            result.append(f"Columns: {', '.join(columns)}")
            
            # Sample data (first 5 rows)
            result.append("\nSample data (up to 5 rows):")
            for i, row in enumerate(data[:5]):
                result.append(f"Row {i+1}: {row}")
            
            # Column statistics (for numeric columns)
            result.append("\nColumn statistics:")
            for col in columns:
                # Check if column has numeric data
                numeric_values = []
                for row in data:
                    try:
                        numeric_values.append(float(row[col]))
                    except (ValueError, TypeError):
                        pass
                
                if numeric_values:
                    avg = sum(numeric_values) / len(numeric_values)
                    min_val = min(numeric_values)
                    max_val = max(numeric_values)
                    result.append(f"  {col}: avg={avg:.2f}, min={min_val}, max={max_val}, count={len(numeric_values)}")
                else:
                    # For non-numeric columns, show unique value count
                    unique_values = set(row[col] for row in data)
                    result.append(f"  {col}: {len(unique_values)} unique values")
            
            return "\n".join(result)
            
        except Exception as e:
            return f"Error analyzing CSV: {str(e)}"
            
    @kernel_function(
        description="Parse and extract information from JSON file",
        name="parse_json"
    )
    def parse_json_data(self, filename: str, path: Optional[str] = None) -> str:
        """
        Parse JSON data and extract information using a path expression.
        
        Args:
            filename: The filename in the uploads directory
            path: Optional JSON path expression (e.g., "data.items[0].name")
            
        Returns:
            Extracted JSON data
        """
        try:
            # Create a safe filename
            safe_filename = os.path.basename(filename)
            file_path = os.path.join(self.UPLOAD_DIR, safe_filename)
            
            # Check if file exists
            if not os.path.exists(file_path):
                return f"Error: File {safe_filename} not found"
                
            # Check if it looks like a JSON file
            if not file_path.lower().endswith('.json'):
                return f"Warning: {safe_filename} might not be a JSON file"
            
            # Read and parse JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # If path is provided, navigate through the JSON
            if path:
                parts = re.split(r'\.|\[|\]', path)
                parts = [p for p in parts if p]
                
                current = json_data
                for part in parts:
                    if part.isdigit():  # Array index
                        index = int(part)
                        if isinstance(current, list) and 0 <= index < len(current):
                            current = current[index]
                        else:
                            return f"Error: Invalid array index {index}"
                    else:  # Object property
                        if isinstance(current, dict) and part in current:
                            current = current[part]
                        else:
                            return f"Error: Property '{part}' not found"
                
                # Format the extracted data
                if isinstance(current, (dict, list)):
                    return json.dumps(current, indent=2)
                else:
                    return str(current)
            
            # For large JSON, summarize instead of returning everything
            if isinstance(json_data, dict):
                key_count = len(json_data.keys())
                top_keys = list(json_data.keys())[:5]  # First 5 keys
                summary = [f"JSON object with {key_count} top-level keys:"]
                summary.append(f"Keys: {', '.join(top_keys)}{' ...' if key_count > 5 else ''}")
                
                # Show first 2 keys with their values
                for key in top_keys[:2]:
                    value = json_data[key]
                    if isinstance(value, (dict, list)):
                        summary.append(f"{key}: {type(value).__name__} with {len(value)} items")
                    else:
                        summary.append(f"{key}: {value}")
                        
                return "\n".join(summary)
                
            elif isinstance(json_data, list):
                list_len = len(json_data)
                summary = [f"JSON array with {list_len} items"]
                
                # Show first 3 items
                for i, item in enumerate(json_data[:3]):
                    if isinstance(item, dict):
                        keys = list(item.keys())
                        summary.append(f"[{i}]: Object with keys: {', '.join(keys[:3])}{' ...' if len(keys) > 3 else ''}")
                    else:
                        summary.append(f"[{i}]: {item}")
                
                if list_len > 3:
                    summary.append("...")
                    
                return "\n".join(summary)
            
            else:
                return str(json_data)
            
        except json.JSONDecodeError:
            return f"Error: {safe_filename} is not valid JSON"
        except Exception as e:
            return f"Error parsing JSON: {str(e)}"
            
    @kernel_function(
        description="Extract and generate a chart from data",
        name="generate_chart"
    )
    def generate_chart_from_data(self, filename: str, chart_type: str, x_column: str, y_column: str) -> str:
        """
        Generate a base64-encoded chart image from data.
        
        Args:
            filename: The filename in the uploads directory
            chart_type: Type of chart ('bar', 'line', 'scatter', 'pie')
            x_column: Column name for X axis
            y_column: Column name for Y axis
            
        Returns:
            HTML with embedded chart image
        """
        try:
            # Check if matplotlib is available
            try:
                import matplotlib
                matplotlib.use('Agg')  # Use non-interactive backend
                import matplotlib.pyplot as plt
                import io
            except ImportError:
                return "Error: matplotlib is not installed. Cannot generate charts."
                
            # Create a safe filename
            safe_filename = os.path.basename(filename)
            file_path = os.path.join(self.UPLOAD_DIR, safe_filename)
            
            # Check if file exists
            if not os.path.exists(file_path):
                return f"Error: File {safe_filename} not found"
                
            # Check if it's a CSV file
            if not file_path.lower().endswith('.csv'):
                return f"Error: {safe_filename} is not a CSV file"
            
            # Read CSV data
            data = []
            columns = []
            with open(file_path, 'r', encoding='utf-8') as f:
                csv_reader = csv.reader(f)
                columns = next(csv_reader)  # Get header row
                for row in csv_reader:
                    if len(row) == len(columns):
                        data.append(row)
            
            # Validate columns
            if x_column not in columns:
                return f"Error: Column '{x_column}' not found"
                
            if y_column not in columns:
                return f"Error: Column '{y_column}' not found"
                
            # Get column indices
            x_idx = columns.index(x_column)
            y_idx = columns.index(y_column)
            
            # Extract X and Y data
            x_data = []
            y_data = []
            for row in data:
                x_val = row[x_idx]
                y_val = row[y_idx]
                
                # Try to convert Y to numeric
                try:
                    y_val = float(y_val)
                except ValueError:
                    continue
                    
                x_data.append(x_val)
                y_data.append(y_val)
            
            if not x_data or not y_data:
                return "Error: Not enough valid data points for chart"
                
            # Create the chart
            plt.figure(figsize=(10, 6))
            
            if chart_type.lower() == 'bar':
                plt.bar(x_data, y_data)
            elif chart_type.lower() == 'line':
                plt.plot(x_data, y_data)
            elif chart_type.lower() == 'scatter':
                plt.scatter(x_data, y_data)
            elif chart_type.lower() == 'pie':
                plt.pie(y_data, labels=x_data, autopct='%1.1f%%')
            else:
                return f"Error: Unsupported chart type '{chart_type}'"
                
            plt.title(f"{chart_type.capitalize()} Chart: {y_column} by {x_column}")
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            
            # Save chart to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            
            # Convert to base64
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
            
            # Return chart as embedded HTML image
            return f"""
            <div style="text-align: center;">
                <h3>{chart_type.capitalize()} Chart: {y_column} by {x_column}</h3>
                <img src="data:image/png;base64,{img_base64}" alt="Chart" style="max-width: 100%;">
            </div>
            """
            
        except Exception as e:
            return f"Error generating chart: {str(e)}"
