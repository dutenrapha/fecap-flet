import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Jogo de Forca',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: JogoForca(),
    );
  }
}

class JogoForca extends StatefulWidget {
  @override
  _JogoForcaState createState() => _JogoForcaState();
}

class _JogoForcaState extends State<JogoForca> {
  String palavra = '';
  String palavraEscondida = '';

  @override
  void initState() {
    super.initState();
    obterNovaPalavra();
  }

  void obterNovaPalavra() async {
    final response = await http.get(Uri.parse('http://localhost:8000/palavra'));
    final jsonData = json.decode(response.body);
    setState(() {
      palavra = jsonData['palavra'];
      palavraEscondida = '_' * palavra.length;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Jogo de Forca'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              'Palavra: $palavraEscondida',
              style: TextStyle(fontSize: 24),
            ),
            ElevatedButton(
              onPressed: () {
                obterNovaPalavra();
              },
              child: Text('Nova Palavra'),
            ),
          ],
        ),
      ),
    );
  }
}