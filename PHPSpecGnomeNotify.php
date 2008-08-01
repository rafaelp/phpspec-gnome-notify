#!/usr/bin/php
<?php

/*
PHPSpecGnomeNotify v0.1.1
Rafael Lima (http://rafael.adm.br)
http://rafael.adm.br/phpspec_gnome_notify
License: http://creativecommons.org/licenses/by/2.5/

Dependencies:

* PHPSPec
  http://dev.phpspec.org/manual/en/index.html
  sudo pear install phpspec/PHPSpec-beta

* libnotify
  sudo apt-get install libnotify-bin

* pyinotify
  sudo apt-get install python-pyinotify

*/

class PHPSpecGnomeNotify {

  private $expiration_in_secs = 2;
  private $fail_image    = "gtk-dialog-error";
  private $pending_image = "gtk-dialog-warning";
  private $success_image = "gtk-dialog-info";
  private $phpspec_options = "--recursive";

  public function run($path = '.') {
    chdir($path);
    $command = 'phpspec '.$this->phpspec_options;
    
    $return = shell_exec($command);

    $lines = split("\n",$return);
    foreach($lines as $line) {
      if(preg_match('/^([0-9]+) example/', $line, $matches)) {
        $examples = $matches[1];
        preg_match('/([0-9]+) failure/', $line, $matches);
        $failures = $matches[1];
        preg_match('/([0-9]+) pending/', $line, $matches);
        $pendings = $matches[1];
      }
    }

    if($failures > 0) {
      $this->notify("Tests Failed", $failures.(($failures == 1) ? " test failed" :  " tests failed"), $this->fail_image);
    }
    elseif($pendings > 0) {
      $this->notify("Tests Pending", $pendings.(($pendings == 1) ? " test is pending" : " tests are pending"), $this->pending_image);
    }
    else {
      $this->notify("Tests Passed", "All tests passed", $this->success_image);
    }
  }
  
  private function notify($title, $message, $stock_icon) {
    $options = "-t ".($this->expiration_in_secs*1000)." -i ".$stock_icon;
    shell_exec("notify-send ".$options." '".$title."' '".$message."'");
  }

}

$path = $argv[1];
if(empty($path)) $path = getcwd();

$test = new PHPSpecGnomeNotify();
$test->run($path);

?>
