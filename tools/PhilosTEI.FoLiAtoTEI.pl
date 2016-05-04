# Follow up from PhilosTEI.hOCRtoTEI.pl
# by Martin Reynaert
# TiCC - Tilburg University - The Netherlands
# 2014 - Licensed under GPLv3

##Usage: Basic

##Requires: Perl module XML::Twig::XPath and POSIX. Further requires the basic TEI XML template Simple.xml

## Copyright Martin Reynaert 2016
## MRE 2014-07-16
## Written in CLARIN-NL project @PhilosTEI

##Actual command lines used: 
## This script is part of the @PhilosTEI workflow and gets initialised by TICCLops.pl, the script which steers the whole workflow.

##This script converts FoLiA XML files for e.g. a book into a single electronic book in TEI XML format.


##Which directory/ies do we want to work on?
if ($ARGV[0] =~ /\#/){
($dir, $teidir) = split '#', $ARGV[0];
}
##Extension for the files to be processed
if ($ARGV[1] =~ /\#/){
($ext, $exttei) = split '#', $ARGV[1];
}

$template = $ARGV[2];
$prefix = $ARGV[3];

use File::Find;
use POSIX qw/strftime/;
use Sort::Naturally;

##We set the binmode to UTF-8 for STDOUT and STDERR--BEGIN
binmode(STDOUT, ":utf8");
binmode(STDERR, ":utf8");
#binmode($template, ":utf8");
##We set the binmode to UTF-8 for STDOUT and STDERR--END

find( sub{
            -f $_ and push @documents, $File::Find::name;
            -d $_ and push @dirs,  $File::Find::name;
}, $dir );
	 print LOG "DOCNAMESREAD: $imdidir >> @documents\n" if ($mode =~ /Z/);
	 foreach $docname (@documents){
           if ($docname =~ /$ext$/){
           push(@coldocs, $docname);
           }
         }

@coldocs = nsort @coldocs;



#$teishadow = $doc;
#$teishadow =~ s/$ext/$exttei/;
$teishadow = $teidir . $prefix . '.ticcl.tei.xml';

print STDERR "TEIDOC: $doc\t$teishadow\n";
print STDOUT "TEIDOC: $doc\t$teishadow\n";

open (SHADOW, ">$teishadow");
binmode(SHADOW, ":utf8");

use XML::Twig::XPath;
##We use the use XML::Twig::XPath Perl module in this mode--END

##We write the number of documents to be processed to the log file
$nrdocs = $#coldocs + 1;
print STDERR "NR DOCS: $nrdocs\n";

##Numbering the documents starts at '1'
$document_number = 0;
$follow = -1;
##We next process each document listed in the array in turn
foreach $doc (@coldocs) {
binmode($doc, ":utf8");
##That is: if the particular document listed has the extension specified on the command-line
    if ($doc =~ /$ext$/){

##Used to have file data info here!!

##Numbering the documents is incremented by '1' for each document to be processed
    $document_number++;
##We write info about the document being processed to the log file

my $t = XML::Twig::XPath->new( 
           twig_roots   => {
          #"//p/t[@lass]" => \&getfromfolia, ##Sowieso typo in!! Wil hier dus ook de id van de //p vatten en meenemen!!
"//p" => \&getfromfolia1,
"//p/t" => \&getfromfolia,
##<p xml:id="dpo_35_0300_master.tif.text.par_1_8">
##<t class="OCR">
##Ninus-, en cussfchen Mnuiusrs en cis-EIN- unanwend-
##</t>
##<t class="Ticcl">negus en cussfchen Mnuiusrs en cissen aanwend</t>

          #"//div//p/span" => \&getfromhtml2,
         #"//body//p" => \&getfromalto5,
         #"//body//head" =>\&getfromalto1,
         #"//body//note" =>\&getfromalto2,
         #"//body//l" =>\&getfromalto3,
         #"//body//speaker" =>\&getfromalto4,
           },
                      );

$t->parsefile( $doc );

sub getfromfolia1
    { my( $t, $item1)= @_;
        {
##$elt->parent('p[@conref != ""]')
#$ref = $item->{'..'}->{'att'}->{'xml:id'};        # get the reference
#$ref = $item->{'parent'}->{'att'}->{'xml:id'};        # get the reference
	    $ref = $item1->{'att'}->{'xml:id'};        # get the reference
#print STDOUT "REF1: $ref ITEM: $item1\n";
	    push @PATTS, $ref;
	}}
sub getfromfolia
{ my( $t, $item)= @_;
  {
$class = $item->{'att'}->{'class'};        # get the class
#print STDOUT "REF: $ref ITEM: $item CLASS: $class T: $t\n";
if ($class =~ /TICCL/i){ ##MRE: Ticcl hoger staat dus anders gecapitaliseerd... Nu case insensitive??
            $txt = $item->text;
            $step++;
            #push @TEXT, 'par@#@';
            push @TEXT, $txt;
            #print STDOUT "TEXT: @TEXT STEPS: $step\n";
}}}

#sub getfromfolia2
#    { my( $t, $item2)= @_;
#        {
#            $txt = $item2->text;
#            $step2++;
#            push @TEXT, 'line@#@' . $txt;
#            print STDOUT "TEXT2: @TEXT STEPS: $step >> $step2\n";
#	}}

#sub getfromalto5
#    { my( $t, $item5)= @_;
#        {
#            $txt = $item5->text;
#            push @TEXT, 'par@#@' . $txt;
#	}}

#foreach $par (@TEXT){
#print STDOUT "PAR: $par\n\n";
#}
}}
my $t = XML::Twig::XPath->new(PrettyPrint => 'indented',
           twig_roots   => { 
            #"//TEI" => \&filltei,
            "//TEI//text/body/p" => \&filltei2,
            #"//FoLiA//div" => \&fillfolia1,
           },
twig_print_outside_roots => \*SHADOW,
                      );



$t->parsefile( $template );

#sub fillfolia2
#    { my( $t, $fill2)= @_;
#        {
#        $fill2->set_att("xml:id" => "$shortnamedoc");      
#        $fill2->print(\*SHADOW);   
#	}}

#sub fillfolia3
#    { my( $t, $fill3)= @_;
#        {
#	    $txtname = $shortnamedoc . '.text';        
#        $fill3->set_att("xml:id" => "$txtname");      
#	}}

sub filltei2
    { my( $t, $fill)= @_;
        {
	    #$divnr++;
	    #$divname = $shortnamedoc . '.div' . $divnr;
        #$fill->set_att("xml:id" => "$divname"); 

##Zoiets als voor elke content CONTENT, maak een nieuwe <p> en kleef dat erin...     
foreach $par (@TEXT){
      print STDERR "PAR1: $par LC: $linecollect\n";
    #$parid++;
    chomp $par;
  $new_elt = XML::Twig::XPath::Elt->new('p');
  $new_elt->set_text( $par );
      $new_elt->set_att("xml:id" => "@PATTS[$parid]");
  $new_elt->print;
#print STDOUT "PARFILL: $par\n\n";
$parid++;
}
#$t->purge;           # frees the memory
}    
      $parid = ();
@TEXT = ();
@PATTS = ();
#	}} ###MRE: move/divide(?) to collate all pages into 1 TEI??
}
#}}    
close(SHADOW);
    

