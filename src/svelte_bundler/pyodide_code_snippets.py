  pyodide.runPython(`
    import cowsay
    cow_output = cowsay.cowsay("I was baked into the JavaScript bundle!")
    print(cow_output)
  `);
