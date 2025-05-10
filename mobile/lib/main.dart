import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() {
  runApp(BillApp());
}

class BillApp extends StatelessWidget {
  const BillApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(title: 'Bill Generator', home: BillHomePage());
  }
}

class BillHomePage extends StatefulWidget {
  const BillHomePage({super.key});

  @override
  _BillHomePageState createState() => _BillHomePageState();
}

class _BillHomePageState extends State<BillHomePage> {
  String result = "Waiting...";
  final TextEditingController _inputCtrl = TextEditingController();

  Future<void> callPython() async {
    const platform = MethodChannel('chaquopy');
    try {
      final String userData = _inputCtrl.text;
      final output = await platform.invokeMethod<String>('generateBill', {
        "data": userData,
      });
      setState(() {
        result = output!;
      });
    } on PlatformException catch (e) {
      setState(() {
        result = "Error: ${e.message}";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Bill Generator")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24),
              child: TextField(
                controller: _inputCtrl,
                decoration: InputDecoration(
                  labelText: "Enter data",
                  border: OutlineInputBorder(),
                ),
              ),
            ),
            SizedBox(height: 12),
            Text(result),
            SizedBox(height: 20),
            ElevatedButton(onPressed: callPython, child: Text("Generate Bill")),
          ],
        ),
      ),
    );
  }
}
