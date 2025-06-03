# Illuvium Web Application with Wallet Connect Integration

This project provides multiple ways to run the Illuvium website with wallet connect functionality.

## Available Versions

### 1. Original Proxy App (Port 8000)
The original implementation that proxies content from the Illuvium website and injects wallet connect functionality.

```
python app.py
```

### 2. Static Standalone Version (Port 8002)
A completely static version that looks identical to the original site but is built from scratch with a working wallet modal.

```
python serve_static_site.py
```

## Features

- Proxy functionality to serve content from the original Illuvium website
- Fixed permission policy issues and CORS problems
- Working wallet connect modal implementation
- All buttons properly trigger the wallet connection modal
- Clean design matching the original site's appearance

## Prerequisites

- Python 3.7 or higher
- Flask and other dependencies (listed in requirements.txt)

## Setup Instructions

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Choose one of the versions to run (see above)
4. Open your browser to the corresponding port (8000 or 8002)

## How It Works

### Original Proxy App
The original implementation works by proxying requests to the actual Illuvium website, modifying the HTML content on-the-fly to insert custom JavaScript that enables the wallet connect functionality.

### Static Standalone Version
The static version is a completely self-contained HTML/CSS/JS implementation that mimics the look and feel of the original site. It provides a simpler, more reliable alternative with all the wallet connect functionality working properly.

## Testing Wallet Connect

Both versions support clicking on any of the following buttons to trigger the wallet connect modal:
- "Connect Wallet" in the header
- "Connect Wallet" in the hero section
- "Get Started", "Enter Arena", or "Build Now" in the game cards
- Any other button with similar text

## Troubleshooting

If you encounter issues with the proxy version, try the static standalone version instead, which avoids many of the complexities of proxying content from the original site.

## License

This code is provided as-is with no warranty.
