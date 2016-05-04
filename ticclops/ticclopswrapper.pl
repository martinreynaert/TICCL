#!/usr/bin/perl
## Copyright Martin Reynaert 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015
## MRE 2015-02-23
## TICCLops / @PhilosTEI system version 0.2

##This Perl wrapper, ticclopswrapper.pl, is the result of CLARIN-NL project 12-006 @PhilosTEI coordinated by Prof. Dr. Arianna Betti at UvA, Amsterdam, The Netherlands.

##This Perl wrapper is part of the interface between the CLAM web application/service that puts TICCLops and the @PhilosTEI system online. Both are hosted at INL in Leiden and are part of the CLARIN Infrastructure. TICCLops is a fully automatic OCR post-correction system. The @PhilosTEI system extends TICCLops with a range of possibilities for turning digital text images into FoLiA xml formatted digital text. It further provides output in TEI xml format.

##This wrapper passes on user parameters as defined in the web application to the main Perl wrapper, TICCLops.pl.

use Getopt::Std;

# OPTIONS
getopts('L:f:x:y:r:t:h:');

$ROOTDIR = $ARGV[0];
$INPUTDIR = $ARGV[1];
$OUTPUTDIR = $ARGV[2];
$STATUSFILE = $ARGV[3];
$PROJECT = $ARGV[4];

$file = $OUTPUTDIR . '/out.txt';

print STDERR "TEST: ROOT: $ROOTDIR IN: $INPUTDIR OUT: $OUTPUTDIR NAME: $PROJECT\n";

$lexicon = "$INPUTDIR/lexicon.lst";

$lang = $opt_t;
$opt_f = 1000000000;
$opt_p = 'TICCLopsOutput';

if (($opt_h =~ /IM/) or ($opt_h =~ /TXT/) or ($opt_h =~ /PDF/) or ($opt_h =~ /DJVU/) or ($opt_h =~ /FOLIA/)){                                    $ARGUMENTS = '-a abcdefgm' . ' -b ' . $opt_L . ' -c ' . $ROOTDIR . "/data/int/$lang/$lang*confusion" . ' -e folia.xml' . ' -f ' . $opt_f . ' -g ' . $ROOTDIR . "/data/int/$lang/$lang*chars" . ' -h ' . $opt_h . ' -i ' . $INPUTDIR . ' -j ' . $PROJECT . ' -l ' . $lexicon . ' -L ' . $opt_L . ' -o ' . $OUTPUTDIR . ' -p ' .  $opt_p . ' -r ' . $opt_r . ' -t ' . $opt_t . ' -u /exp/sloot/usr/local/bin/' . ' -v 6' . ' -x ' .  $opt_x . ' -y ' . $opt_y . ' -z ' . $ROOTDIR;
}                                                                              
elsif ($opt_h =~ /FRQ/){                                                        $ARGUMENTS = '-a bcdefm' . ' -b' . $opt_L . ' -c' . $ROOTDIR . "/data/int/$lang/$lang*confusion" . ' -e folia.xml' . ' -f' . $opt_f . ' -g' . $ROOTDIR . "/data/int/$lang/$lang*chars" . ' -h ' . $opt_h . ' -i' . $INPUTDIR . ' -j ' . $PROJECT . ' -l' . $lexicon . ' -L' . $opt_L . ' -o' . $OUTPUTDIR . ' -p' .  $opt_p . ' -r' . $opt_r . ' -t' . $opt_t . ' -u /exp/sloot/usr/local/bin/' . ' -v 6' . ' -x' .  $opt_x . ' -y' . $opt_y . ' -z ' . $ROOTDIR;
}    
else {
##Nothing happens..
}  

print STDERR "ARGUMENTS: $ARGUMENTS\n";

open (STATUS, ">>$STATUSFILE");

$pid = open(README, " perl $ROOTDIR/TICCLops.pl $ARGUMENTS |")  or die "Couldn't fork: $!\n";
while (<README>) { 
    #$gonetime = time();
    #$lapse = $gonetime - $donetime;
    #if ($lapse == 20){
        #$donetime = $gonetime;
        #$count++;
        #print STATUS "SEENTWENTYSECONDS $count TIMES\n";
    #}
    #$mtime = (stat(STATUS))[9];
    #$mtime = (stat($STATUSFILE))[9];
    #$nowtime = time();
    #$difftime = $nowtime - $mtime; 
    #print STDERR "MTIME: $mtime\n";
    #if ($difftime =~ /20/){
    #$count++;
    #print STATUS "SEENTWENTYSECONDS $count TIMES\n";
    #$mtime = ();
    #}
}
close(README) or die "Couldn't close: $!\n";
close(STATUS);
