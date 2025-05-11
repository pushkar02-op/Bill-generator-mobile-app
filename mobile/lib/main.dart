import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:file_picker/file_picker.dart';
import 'package:open_file/open_file.dart';
import 'package:permission_handler/permission_handler.dart';
import 'dart:convert';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Permission.storage.request();
  // Lock orientation to portrait
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
  runApp(const BillApp());
}

class BillApp extends StatelessWidget {
  const BillApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Bill Generator',
      theme: ThemeData(
        primarySwatch: Colors.green,
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            minimumSize: const Size.fromHeight(48),
          ),
        ),
        inputDecorationTheme: const InputDecorationTheme(
          border: OutlineInputBorder(),
          contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        ),
      ),
      home: const BillHomePage(),
    );
  }
}

class BillHomePage extends StatefulWidget {
  const BillHomePage({super.key});
  @override
  _BillHomePageState createState() => _BillHomePageState();
}

class _BillHomePageState extends State<BillHomePage> {
  static const _channel = MethodChannel('chaquopy');

  final List<String> _places = ['Bhagalpur', 'Begusarai'];
  String _selectedPlace = 'Bhagalpur';
  String? _inputPath;
  String _status = "No file selected";

  Future<void> _pickFile() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['xlsx'],
    );
    if (result != null && result.files.single.path != null) {
      setState(() {
        _inputPath = result.files.single.path;
        _status = "Selected: ${_inputPath!.split('/').last}";
      });
    }
  }

  Future<void> _generateBill() async {
    if (_inputPath == null) {
      _showSnack("Please select an Excel file first");
      return;
    }
    setState(() => _status = "Generating…");
    try {
      final jsonRaw = await _channel.invokeMethod<String>('generateBill', {
        'data': _inputPath,
        'place': _selectedPlace,
      });
      final paths = jsonDecode(jsonRaw!);
      final pdfPath = paths['pdf'] as String;

      setState(() => _status = "Generated PDF: ${pdfPath.split('/').last}");
      await OpenFile.open(pdfPath);
    } on PlatformException catch (e) {
      setState(() => _status = "Error: ${e.message}");
    }
  }

  void _showSnack(String message) {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(SnackBar(content: Text(message)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Excel Bill Generator")),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 400),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Place selector
                DropdownButtonFormField<String>(
                  value: _selectedPlace,
                  decoration: const InputDecoration(labelText: "Select Place"),
                  items:
                      _places.map((place) {
                        return DropdownMenuItem(
                          value: place,
                          child: Text(place),
                        );
                      }).toList(),
                  onChanged: (v) => setState(() => _selectedPlace = v!),
                ),
                const SizedBox(height: 20),

                // File picker
                ElevatedButton.icon(
                  icon: const Icon(Icons.attach_file),
                  label: const Text("Select Excel File"),
                  onPressed: _pickFile,
                ),
                const SizedBox(height: 12),

                // Generate button
                ElevatedButton.icon(
                  icon: const Icon(Icons.receipt_long),
                  label: const Text("Generate Bill"),
                  onPressed: _generateBill,
                ),
                const SizedBox(height: 24),

                // Status
                Center(
                  child: Text(
                    _status,
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.bodyLarge,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
