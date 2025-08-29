I'll create two Python scripts for you - one for location QR codes and one for object QR codes, both reading from external files and capable of printing to a local printer.I've created a complete QR code generation system for you with the following components:

## Scripts Created:

1. **Location QR Code Generator** (`location_qr_generator.py`)
   - Generates QR codes for location identification
   - Reads location data from `locations.json`
   - Creates QR codes with location ID, name, and description

2. **Object QR Code Generator** (`object_qr_generator.py`)
   - Generates QR codes for object identification  
   - Reads object data from `objects.json`
   - Creates QR codes with object ID, name, category, serial number, and description

## External Data Files:

3. **Sample locations.json** - Contains location data that you can modify
4. **Sample objects.json** - Contains object data that you can modify
5. **requirements.txt** - Lists required Python packages

## Key Features:

- **External File Input**: Both scripts read from JSON files that you can easily edit
- **Automatic File Creation**: If the JSON files don't exist, sample files are created automatically
- **Print Support**: Both scripts can print directly to your local printer
- **Fallback to Image**: If printing fails, QR codes are saved as PNG images
- **Interactive Interface**: Choose individual items or generate all QR codes at once
- **Rich QR Codes**: Include both QR code and human-readable text labels

## Installation & Usage:

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the scripts:
   ```bash
   python location_qr_generator.py
   python object_qr_generator.py
   ```

3. Edit the JSON files to add your own locations and objects

## QR Code Data Format:

- **Locations**: `LOCATION:LOC001|Warehouse A - Section 1`
- **Objects**: `OBJECT:OBJ001|Laptop Computer|LP123456789`

The scripts work on Windows and use the default printer. You can easily modify the JSON files to add, remove, or update locations and objects without touching the Python code.