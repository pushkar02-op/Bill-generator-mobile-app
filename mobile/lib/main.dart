import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:file_picker/file_picker.dart';
import 'package:open_file/open_file.dart';
import 'package:permission_handler/permission_handler.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Permission.storage.request();
  SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
  runApp(const BillApp());
}

class BillApp extends StatelessWidget {
  const BillApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Bill Generator',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.green,
        scaffoldBackgroundColor: Colors.grey[50],
        appBarTheme: const AppBarTheme(
          elevation: 0,
          backgroundColor: Colors.green,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            minimumSize: const Size.fromHeight(50),
            textStyle: const TextStyle(fontSize: 16),
          ),
        ),
        inputDecorationTheme: const InputDecorationTheme(
          border: OutlineInputBorder(),
          contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 10),
        ),
      ),
      home: const BillHomePage(),
    );
  }
}

class BillHomePage extends StatefulWidget {
  const BillHomePage({super.key});
  @override
  State<BillHomePage> createState() => _BillHomePageState();
}

class _BillHomePageState extends State<BillHomePage> {
  static const _channel = MethodChannel('chaquopy');

  final List<String> _places = ['Bhagalpur', 'Begusarai'];
  String _selectedPlace = 'Bhagalpur';
  String? _inputPath;
  String _status = "";

  Future<void> _pickFile() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['xlsx'],
    );
    if (result != null && result.files.single.path != null) {
      setState(() {
        _inputPath = result.files.single.path;
        _status = "Ready to generate for “${_inputPath!.split('/').last}”";
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
      setState(() => _status = "Generated: ${pdfPath.split('/').last}");
      await OpenFile.open(pdfPath);
    } on PlatformException catch (e) {
      setState(() => _status = "Error: ${e.message}");
    }
  }

  void _showSnack(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), behavior: SnackBarBehavior.floating),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Bill Generator"), centerTitle: true),
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 500),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Place selector
                  DropdownButtonFormField<String>(
                    value: _selectedPlace,
                    decoration: const InputDecoration(
                      labelText: "Select Place",
                    ),
                    items:
                        _places
                            .map(
                              (place) => DropdownMenuItem(
                                value: place,
                                child: Text(place),
                              ),
                            )
                            .toList(),
                    onChanged: (v) => setState(() => _selectedPlace = v!),
                  ),
                  const SizedBox(height: 24),

                  // File picker & display
                  OutlinedButton.icon(
                    icon: const Icon(Icons.attach_file),
                    label: const Text("Choose Excel File"),
                    onPressed: _pickFile,
                  ),
                  if (_inputPath != null) ...[
                    const SizedBox(height: 8),
                    Text(
                      _inputPath!.split('/').last,
                      style: const TextStyle(color: Colors.black87),
                      textAlign: TextAlign.center,
                    ),
                  ],
                  const SizedBox(height: 24),

                  // Generate button
                  ElevatedButton.icon(
                    icon: const Icon(Icons.receipt_long),
                    label: const Text("Generate & Open Bill"),
                    onPressed: _generateBill,
                  ),
                  const SizedBox(height: 24),

                  // Status
                  if (_status.isNotEmpty)
                    Text(
                      _status,
                      textAlign: TextAlign.center,
                      style: Theme.of(context).textTheme.bodyMedium,
                    ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
