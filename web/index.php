<html>
  <head>
    <title>Advent of Code Leaderboards</title>
    <meta property="og:title" content="Advent of Code Leaderboards" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="https://students.cs.byu.edu/~teikn/aoc-boards/data/og.png" />
    <meta property="og:url" content="https://students.cs.byu.edu/~teikn/aoc-boards" />
    <meta property="og:description" content="A ~~better~~ different view of a leaderboard for Advent of Code. WIP." />
    <style>
      body {background-color: black; color: white}
      a {background-color: black; color: white}
    </style>
    <?php
      $readme = "";
      if (isset($_GET['r'])) {
        $readme = " -r ";
      }
      $code = 944847;
      if (isset($_GET['c'])) {
        $code = $_GET['c'];
      }
      $sortby = "";
      if (isset($_GET['s'])) {
        $sortby = " -s " . $_GET['s'];
      }

    ?>
    <script>
      function toggle_readme() {
        var readme = document.getElementById('readme');
        var clicker = document.getElementById('readme-clicker');
        if (readme.style.display == "none") {
          readme.style.display = "block";
          clicker.innerHTML = "okay cool, you can hide that again";
        }  else {
          readme.style.display = "none";
          clicker.innerHTML = "what's going on?";
        }
      }
      var times = document.getElementsByClassName("time");
      var gradient = true;
      function toggle_gradient() {
        gradient = !gradient;
        for (var i = 0; i < times.length; i++) {
          if (gradient) {
            opacity = times[i].getAttribute("data-opacity");
            times[i].setAttribute("style", "filter: opacity("+opacity+");");
          } else {
            times[i].removeAttribute("style");
          }
        }
      }
      window.onload = toggle_readme;
    </script>
  </head>
  <body>
    <p><pre>
      [<a href="javascript:toggle_readme()" id="readme-clicker"></a>]
      [<a href="javascript:toggle_gradient()" id="gradient-clicker">toggle gradient</a>]
      <?php
        exec("./data/leaderboard.py -y " . date("Y") . " -c " . $code . $sortby . " -r -w https://students.cs.byu.edu/~teikn/aoc-boards/?s=~~ 2>&1", $res);
        echo "\n";
        foreach($res as $line) {
          echo $line."\n";
        }
      ?>
    </pre></p>
  </body>
</html>
