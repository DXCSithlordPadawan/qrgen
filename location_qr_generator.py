#!/usr/bin/env python3
"""
Location QR Code Generator
Generates QR codes for location numbers from an external file and prints them.
"""

import qrcode
import json
from PIL import Image, ImageDraw, ImageFont
import win32print
import win32ui
from PIL import ImageWin
import os

def load_locations(filename='locations.json'):
    """Load location data from JSON file"""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found. Creating sample file...")
        create_sample_locations_file(filename)
        return load_locations(filename)
    except json.JSONDecodeError:
        print(f"Error reading {filename}. Please check JSON format.")
        return {}

def create_sample_locations_file(filename='locations.json'):
    """Create a sample locations file"""
    sample_data = {
        "locations": [
            {"id": "OP1", "name": "OP1", "description": "Donetsk Oblast"},
            {"id": "OP2", "name": "OP2", "description": "Dnipropetrovsk Oblast"},
            {"id": "OP3", "name": "OP3", "description": "Zaporizhzhia Oblast"},
            {"id": "OP4", "name": "OP4", "description": "Kyiv Oblast"},
            {"id": "OP5", "name": "OP5", "description": "Kirovohrad Oblast"},
            {"id": "OP6", "name": "OP6", "description": "Mykolaiv Oblast"},
            {"id": "OP7", "name": "OP7", "description": "Odesa Oblast"},
            {"id": "OP8", "name": "OP8", "description": "Sumy Oblast"}
        ]
    }
    
    with open(filename, 'w') as file:
        json.dump(sample_data, file, indent=2)
    print(f"Created sample file: {filename}")

def generate_location_qr(location_data):
    """Generate QR code for a location"""
    # Create QR code data
    qr_data = str(location_data['id'])
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Create a new image with space for text
    img_width = 400
    img_height = 500
    img = Image.new('RGB', (img_width, img_height), 'white')
    
    # Resize QR code to fit
    qr_img = qr_img.resize((300, 300))
    
    # Paste QR code onto main image
    img.paste(qr_img, (50, 50))
    
    # Add text
    draw = ImageDraw.Draw(img)
    try:
        font_large = ImageFont.truetype("arial.ttf", 20)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Location ID
    draw.text((50, 360), f"Location: {location_data['id']}", fill="black", font=font_large)
    
    # Location name
    draw.text((50, 390), location_data['name'], fill="black", font=font_small)
    
    # Description
    if location_data.get('description'):
        draw.text((50, 420), location_data['description'], fill="black", font=font_small)
    
    return img

def print_image(img, printer_name=None):
    """Print image to specified printer or default printer"""
    if printer_name is None:
        printer_name = win32print.GetDefaultPrinter()
    
    # Convert PIL image to a format suitable for printing
    img_path = "temp_qr.bmp"
    img.save(img_path, "BMP")
    
    # Print the image
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)
    hDC.StartDoc("Location QR Code")
    hDC.StartPage()
    
    # Get printer dimensions
    printable_area = hDC.GetDeviceCaps(110), hDC.GetDeviceCaps(111)  # HORZRES, VERTRES
    printer_size = hDC.GetDeviceCaps(4), hDC.GetDeviceCaps(6)  # HORZSIZE, VERTSIZE (in mm)
    
    # Load and print image
    bmp = Image.open(img_path)
    dib = ImageWin.Dib(bmp)
    
    # Scale image to fit printer
    scale = min(printable_area[0] / bmp.width, printable_area[1] / bmp.height) * 0.8
    scaled_width = int(bmp.width * scale)
    scaled_height = int(bmp.height * scale)
    
    # Center the image
    x = (printable_area[0] - scaled_width) // 2
    y = (printable_area[1] - scaled_height) // 2
    
    dib.draw(hDC.GetHandleOutput(), (x, y, x + scaled_width, y + scaled_height))
    
    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()
    
    # Clean up temp file
    os.remove(img_path)
    print(f"Printed to {printer_name}")

def main():
    """Main function"""
    print("Location QR Code Generator")
    print("-" * 30)
    
    # Load location data
    locations_data = load_locations()
    
    if not locations_data.get('locations'):
        print("No locations found in file.")
        return
    
    # Display available locations
    print("\nAvailable locations:")
    for i, location in enumerate(locations_data['locations'], 1):
        print(f"{i}. {location['id']} - {location['name']}")
    
    # Get user choice
    try:
        choice = input("\nEnter location number to generate QR code (or 'all' for all locations): ")
        
        if choice.lower() == 'all':
            for location in locations_data['locations']:
                print(f"\nGenerating QR code for {location['id']}...")
                img = generate_location_qr(location)
                
                # Ask if user wants to print
                print_choice = input(f"Print QR code for {location['id']}? (y/n): ")
                if print_choice.lower() == 'y':
                    try:
                        print_image(img)
                    except Exception as e:
                        print(f"Printing failed: {e}")
                        # Save as image instead
                        img.save(f"location_{location['id']}_qr.png")
                        print(f"Saved as location_{location['id']}_qr.png")
                else:
                    img.save(f"location_{location['id']}_qr.png")
                    print(f"Saved as location_{location['id']}_qr.png")
        else:
            choice_num = int(choice) - 1
            if 0 <= choice_num < len(locations_data['locations']):
                location = locations_data['locations'][choice_num]
                print(f"\nGenerating QR code for {location['id']}...")
                img = generate_location_qr(location)
                
                # Ask if user wants to print
                print_choice = input("Print QR code? (y/n): ")
                if print_choice.lower() == 'y':
                    try:
                        print_image(img)
                    except Exception as e:
                        print(f"Printing failed: {e}")
                        # Save as image instead
                        img.save(f"location_{location['id']}_qr.png")
                        print(f"Saved as location_{location['id']}_qr.png")
                else:
                    img.save(f"location_{location['id']}_qr.png")
                    print(f"Saved as location_{location['id']}_qr.png")
            else:
                print("Invalid selection.")
                
    except ValueError:
        print("Invalid input. Please enter a number.")
    except KeyboardInterrupt:
        print("\nOperation cancelled.")

if __name__ == "__main__":
    main()