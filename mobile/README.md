# Bill Generator Mobile App

A cross-platform mobile application for generating professional tax invoices from Excel data, with automated PDF and Excel export. Built with Flutter and Python (via Chaquopy), this app streamlines invoice creation for businesses.

---

## Features

- **Cross-platform:** Runs on Android, iOS, Windows, Linux, and Web (Flutter).
- **Automated Invoice Generation:** Reads Excel files, extracts billing data, and generates formatted invoices.
- **PDF & Excel Export:** Outputs both PDF and Excel versions of each invoice.
- **Customizable Templates:** Professional invoice layouts with company branding.
- **Persistent Invoice Tracking:** Automatically increments and tracks invoice numbers.
- **Easy Integration:** Uses Python for data processing and PDF generation via Chaquopy on Android.

---

## Folder Structure

```
mobile/
├── android/         # Android native & build files (Chaquopy integration)
├── ios/             # iOS native & build files
├── lib/             # Flutter Dart source code
├── assets/          # App assets (images, etc.)
├── python/          # Python business logic (Excel/PDF generation)
├── test/            # Flutter/Dart tests
├── windows/         # Windows build files
├── linux/           # Linux build files
├── web/             # Web build files
├── pubspec.yaml     # Flutter dependencies
└── README.md
```

---

## Getting Started

### Prerequisites

- [Flutter SDK](https://flutter.dev/docs/get-started/install)
- Python 3.8+ (for development and Chaquopy integration)
- Android Studio or VS Code (recommended)

### Setup

1. **Clone the repository:**

   ```sh
   git clone <your-repo-url>
   cd Bill-generator-mobile-app/mobile
   ```

2. **Install Flutter dependencies:**

   ```sh
   flutter pub get
   ```

3. **Android-specific:**

   - Ensure Python is installed and available in your system PATH.
   - Chaquopy dependencies are managed in `android/app/build.gradle.kts`.

4. **Run the app:**
   - **Android/iOS:**
     ```sh
     flutter run
     ```
   - **Windows/Linux/Web:**
     ```sh
     flutter run -d windows
     flutter run -d linux
     flutter run -d web
     ```

---

## How It Works

- **User uploads an Excel file** with billing data.
- The app processes the file using embedded Python scripts (see [`bill_generator.py`](android/app/src/main/python/bill_generator.py)).
- Invoice details are extracted, formatted, and exported as both PDF and Excel.
- Invoice numbers are tracked and incremented automatically (see [`invoice_tracker.py`](../../python/utils/invoice_tracker.py)).

---

## Key Python Modules

- [`bill_generator.py`](android/app/src/main/python/bill_generator.py): Main entry for processing Excel and generating invoices.
- [`pdf_generator.py`](../../python/bill/pdf_generator.py): Handles PDF invoice formatting and export.
- [`invoice_tracker.py`](../../python/utils/invoice_tracker.py): Manages persistent invoice numbering.

---

## Customization

- **Company Info:**  
  Update company name, address, and GST details in the Python scripts or metadata files.
- **Invoice Template:**  
  Modify the layout in [`pdf_generator.py`](../../python/bill/pdf_generator.py) and Excel formatting in [`bill_generator.py`](android/app/src/main/python/bill_generator.py).

---

## License

This project is licensed under the MIT License. See [LICENSE](../LICENSE) for details.

---

## Acknowledgements

- [Flutter](https://flutter.dev/)
- [Chaquopy](https://chaquo.com/chaquopy/)
- [ReportLab](https://www.reportlab.com/dev/docs/)
- [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/)

---

## Contact

For questions or support, please contact [Your Name] at [your.email@example.com].
