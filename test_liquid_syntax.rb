#!/usr/bin/env ruby

require 'liquid'

# Test files that had Liquid syntax errors
test_files = [
  'docs/decisions/0023-handlebars-template-engine-01J6KPJ8XM6CDP9YHD1ZQR868H.md',
  'docs/decisions/0023-handlebars-template-engine.md',
  'docs/PROMPT_TEMPLATE_LANGUAGE.md'
]

puts "Testing Liquid syntax in markdown files..."

test_files.each do |file_path|
  full_path = File.join(__dir__, file_path)
  
  if File.exist?(full_path)
    puts "\nTesting #{file_path}..."
    
    begin
      content = File.read(full_path)
      
      # Extract content between VSCode.Cell tags if present
      if content.include?('<VSCode.Cell')
        # Extract markdown cells
        markdown_cells = content.scan(/<VSCode\.Cell[^>]*language="markdown"[^>]*>(.*?)<\/VSCode\.Cell>/m)
        content_to_test = markdown_cells.map(&:first).join("\n")
      else
        content_to_test = content
      end
      
      # Remove YAML frontmatter
      content_to_test = content_to_test.gsub(/^---\s*\n.*?\n---\s*\n/m, '')
      
      # Parse with Liquid to check for syntax errors
      template = Liquid::Template.parse(content_to_test)
      puts "✅ #{file_path} - Liquid syntax OK"
      
    rescue Liquid::SyntaxError => e
      puts "❌ #{file_path} - Liquid syntax error: #{e.message}"
    rescue => e
      puts "⚠️  #{file_path} - Other error: #{e.message}"
    end
  else
    puts "⚠️  #{file_path} - File not found"
  end
end

puts "\nDone testing Liquid syntax."
