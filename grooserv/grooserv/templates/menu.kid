<html xmlns:py="http://purl.org/kid/ns#">
  <head>
    <title py:content="title">This is replaced.</title>
  </head>
  <body>
    <p py:for="w in wlist">
      <p py:content="w.display()">REPLACED</p>
   </p>
  <a href="/?action=m">main menu</a>
  </body>
</html>

