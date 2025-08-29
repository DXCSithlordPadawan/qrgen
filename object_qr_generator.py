#!/usr/bin/env python3
"""
Object QR Code Generator
Generates QR codes for object identification from an external file and prints them.
"""

import qrcode
import json
from PIL import Image, ImageDraw, ImageFont
import win32print
import win32ui
from PIL import ImageWin
import os

def load_objects(filename='objects.json'):
    """Load object data from JSON file"""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found. Creating sample file...")
        create_sample_objects_file(filename)
        return load_objects(filename)
    except json.JSONDecodeError:
        print(f"Error reading {filename}. Please check JSON format.")
        return {}

def create_sample_objects_file(filename='objects.json'):
    """Create a sample objects file"""
    sample_data = {
        "objects": [
            {
                "id": "SADrone",
                "name": "SADrone",
                "category": "Unmanned Aircraft",
                "serial": "Russian Federation",
                "description": "Sokol Altius Drone"
            },
            {
                "id": "KA50",
                "name": "KA50",
                "category": "Airframe",
                "serial": "Russian Federation",
                "description": "Ka-50 Helicopter"
            },
            {
                "id": "S500",
                "name": "S500",
                "category": "Vehicle",
                "serial": "Russian Federation",
                "description": "S-500 Prometheus"
            },
            {
                "id": "S400",
                "name": "S400",
                "category": "Vehicle",
                "serial": "Russian Federation",
                "description": "SA-21 Growler"
            },
            {
                "id": "Admiral",
                "name": "Admiral",
                "category": "Vessel",
                "serial": "Russian Federation",
                "description": "Admiral Chabanenko - Destroyer"
            },
            {
                "id": "T90",
                "name": "T90",
                "category": "main-battle-tank",
                "serial": "Russian Federation",
                "description": "T-90 Main Battle Tank"
            },
            {
                "id": "SSu57",
                "name": "SSu57",
                "category": "Aircraft",
                "serial": "Russian Federation",
                "description": "Sukhoi Su-57 Aircraft"
            },
            {
                "id": "35GdsMRBde",
                "name": "35GdsMRBde",
                "category": "militaryorganization",
                "serial": "Russian Federation",
                "description": "35th Guards Motor Rifle Brigade"
            }
        ]
    }
    
    with open(filename, 'w') as file:
        json.dump(sample_data, file, indent=2)
    print(f"Created sample file: {filename}")

def generate_object_qr(object_data):
    """Generate QR code for an object"""
    # Create QR code data
    qr_data = str(object_data['id'])
    
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
    img_height = 550
    img = Image.new('RGB', (img_width, img_height), 'white')
    
    # Resize QR code to fit
    qr_img = qr_img.resize((300, 300))
    
    # Paste QR code onto main image
    img.paste(qr_img, (50, 50))
    
    # Add text
    draw = ImageDraw.Draw(img)
    try:
        font_large = ImageFont.truetype("arial.ttf", 18)
        font_medium = ImageFont.truetype("arial.ttf", 14)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Object ID
    draw.text((50, 360), f"Object ID: {object_data['id']}", fill="black", font=font_large)
    
    # Object name
    draw.text((50, 390), object_data['name'], fill="black", font=font_medium)
    
    # Category
    if object_data.get('category'):
        draw.text((50, 415), f"Category: {object_data['category']}", fill="black", font=font_small)
    
    # Serial number
    if object_data.get('serial'):
        draw.text((50, 435), f"Serial: {object_data['serial']}", fill="black", font=font_small)
    
    # Description
    if object_data.get('description'):
        draw.text((50, 460), object_data['description'], fill="black", font=font_small)
    
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
    hDC.StartDoc("Object QR Code")
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
    print("Object QR Code Generator")
    print("-" * 30)
    
    # Load object data
    objects_data = load_objects()
    
    if not objects_data.get('objects'):
        print("No objects found in file.")
        return
    
    # Display available objects
    print("\nAvailable objects:")
    for i, obj in enumerate(objects_data['objects'], 1):
        print(f"{i}. {obj['id']} - {obj['name']} ({obj.get('category', 'N/A')})")
    
    # Get user choice
    try:
        choice = input("\nEnter object number to generate QR code (or 'all' for all objects): ")
        
        if choice.lower() == 'all':
            for obj in objects_data['objects']:
                print(f"\nGenerating QR code for {obj['id']}...")
                img = generate_object_qr(obj)
                
                # Ask if user wants to print
                print_choice = input(f"Print QR code for {obj['id']}? (y/n): ")
                if print_choice.lower() == 'y':
                    try:
                        print_image(img)
                    except Exception as e:
                        print(f"Printing failed: {e}")
                        # Save as image instead
                        img.save(f"object_{obj['id']}_qr.png")
                        print(f"Saved as object_{obj['id']}_qr.png")
                else:
                    img.save(f"object_{obj['id']}_qr.png")
                    print(f"Saved as object_{obj['id']}_qr.png")
        else:
            choice_num = int(choice) - 1
            if 0 <= choice_num < len(objects_data['objects']):
                obj = objects_data['objects'][choice_num]
                print(f"\nGenerating QR code for {obj['id']}...")
                img = generate_object_qr(obj)
                
                # Ask if user wants to print
                print_choice = input("Print QR code? (y/n): ")
                if print_choice.lower() == 'y':
                    try:
                        print_image(img)
                    except Exception as e:
                        print(f"Printing failed: {e}")
                        # Save as image instead
                        img.save(f"object_{obj['id']}_qr.png")
                        print(f"Saved as object_{obj['id']}_qr.png")
                else:
                    img.save(f"object_{obj['id']}_qr.png")
                    print(f"Saved as object_{obj['id']}_qr.png")
            else:
                print("Invalid selection.")
                
    except ValueError:
        print("Invalid input. Please enter a number.")
    except KeyboardInterrupt:
        print("\nOperation cancelled.")

if __name__ == "__main__":
    main()