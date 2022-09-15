#!/usr/bin/perl -w

use strict;
use File::Find;

my $dir = '/home/montse/logon/upf/srg/tsdb/skeletons/bosque/';


find(\&imprimir_archivo, $dir);

sub imprimir_archivo{
my $elemento = $_;


if ($elemento eq "item"){
		changeFile(\$elemento);
}

}

sub changeFile{

my $elemento = $_;
$elemento=$File::Find::name;
my $result="";
open FICHERO, $elemento or die "No existe ".$elemento;
while (<FICHERO>)
{
	$_=~/(.*\@.*\@.*\@.*\@.*\@.*\@.*)(\@)(.*\@.*\@.*\@.*\@.*)/;
	
   $result.=$1."@@@@".$3."\n";
}
close FICHERO;

open (SALIDA,">$elemento") || die "ERROR: No puedo abrir el fichero $elemento\n";

print SALIDA $result;
close SALIDA;


}
