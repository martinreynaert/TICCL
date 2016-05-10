#!/usr/bin/perl
## Copyright Martin Reynaert 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016
## MRE 2016-05-01
## TICCLops / @PhilosTEI / PICCL system version 0.3

##This Perl wrapper is in part the result of CLARIN-NL Call 4 project 12-006 @PhilosTEI coordinated by Prof. Dr. Arianna Betti at UvA, Amsterdam, The Netherlands.

##This Perl wrapper is part of the interface between the CLAM web application/service that puts TICCLops and the @PhilosTEI system online. Both are hosted at INL in Leiden and are part of the CLARIN Infrastructure. TICCLops is a fully automatic OCR post-correction system. The @PhilosTEI system extends TICCLops with a range of possibilities for turning digital text images into FoLiA xml formatted digital text. It further provides output in TEI xml format.

##The poster at http://ticclops.uvt.nl/CLIN2015-poster.pdf gives a schematic overview of the @PhilosTEI system.

##The TICCLops web service is available at http://ticclops.clarin.inl.nl. The web application here presents the classic CLAM interface, as developed by Maarten van Gompel in Python.

##The @PhilosTEI system is available at http://philostei.clarin.inl.nl.The web application here presents a new interface, as developed in Java for the @PhilosTEI project by Matje van de Camp, 'De Taalmonsters'.

##The former TICCLops version, v. 0.1, at INL was still fully in Perl. The former version, the result of CLARIN-NL project TICCLops in Call 1, is now deemed obsolete. The current system consists of a Perl wrapper that is largely responsible for coordinating the work of a range of C++ FoLiA and TICCL modules built by Ko van der Sloot at TiCC, Tilburg University on the basis of guidelines and specifications drawn up by Martin Reynaert. The TICCLops web service and application is an instantiation of focus-word based correction of spelling and OCR variants in corpora. For very large scale work we recommend a local installation of TICCL and the use of the character confusion based approach. These are described in:
##Journal: International Journal on Document Analysis and Recognition
##DOI: 10.1007/s10032-010-0133-5
##Title: Character confusion versus focus word-based correction of spelling and OCR variants in corpora
##Author: Martin Reynaert

##This renewed TICCL version now uses a language specific character frequency ranked alphabet. All characters not defined within this (lowercased) alphabet will be treated as having the same anagram value. This results in untokenized word forms lining up as anagrams in the corpus hash. We now use a larger alphabet than we used to, which results in more possible character confusions, but is hoped to pay off in terms of less normalization, processing and bookkeeping required. 

##The tool required to build the new alphabet is TICCL-lexstat. This tool is not as yet incoporated into the current TICCL wrapper, TICCLops.pl. An appropriate command line to run the tool is:
## /exp/sloot/usr/local/bin/TICCL-lexstat --LD 2 --clip 20 --diac NLD.aspell.dict

####HERE GOES!

##We register the time at start up
$intime = time();

##We will require the POSIX floor() and ceil() functions under c-mode
use POSIX;
##We need the module to find files
use File::Find;
use Sort::Naturally;
use Getopt::Std;

if ($ARGV[0] =~ /config$/){

open (C, $ARGV[0]);
while ($conf = <C>) {
  chomp $conf;
  $conf =~ s/\s+/ /g;
  if ($conf =~ /^\-/){
    @CONF = split ' ', $conf;
    push @CUMUL, $CONF[1];
  }
}
close C;

print STDERR "TICCL_OPTSin: @CUMUL\n";

$mode = @CUMUL[0];
$texttype  = @CUMUL[1];
$ROOTDIR = @CUMUL[2];
$charconfus = @CUMUL[3];
$KHC = @CUMUL[4];
$ext = @CUMUL[5] . '$';
$artifrq = @CUMUL[6];
$alph = @CUMUL[7];
#$OCR = @CUMUL[7];
$INPUTDIR = @CUMUL[8];
$lex = @CUMUL[9];
$LD = @CUMUL[10];
$OUTPUTDIR = @CUMUL[11];
$prefix = @CUMUL[12];
$rank = @CUMUL[13];
$lang = @CUMUL[14];
$tooldir = @CUMUL[15];
$threads = @CUMUL[16];
$minlength = @CUMUL[17];
$maxlength = @CUMUL[18];

print STDERR "TICCL_OPTSin2: MODE: $mode TEXTTYPE: $texttype ROOTDIR: $ROOTDIR CHARCONFUS: $charconfus KHC: $KHC EXT: $ext ARTIFRQ: $artifrq ALPH: $alph INPUTDIR: $INPUTDIR DIR: $dir LEX: $lex LD: $LD OUTPUTDIR: $OUTPUTDIR PREFIX: $prefix RANK: $rank LANG: $lang TOOLDIR: $tooldir THREADS: $threads MINLENGTH: $minlength MAXLENGTH: $maxlength \n";

@CUMUL = ();
}
else {
# OPTIONS
getopts('a:b:c:d:e:f:g:i:j:l:L:o:p:r:t:u:v:x:y:z:');

print STDERR "TICCL_OPTS: a: $opt_a b: $opt_b c: $opt_c d: $opt_d e: $opt_e f: $opt_f g: $opt_g i: $opt_i j: $opt_j l: $opt_l L: $opt_L o: $opt_o p: $opt_p r: $opt_r t: $opt_t u: $opt_u v: $opt_v x: $opt_x y: $opt_y z: $opt_z\n";

$mode = $opt_a;
$texttype = $opt_b;
$ROOTDIR = $opt_z;
$charconfus = $opt_c;
$KHC = $opt_d;
$ext = $opt_e . '$';
$artifrq = $opt_f;
$alph = $opt_g;
#$OCR = $opt_h;
$INPUTDIR = $opt_i;
$dir = $opt_i;
$lex = $opt_l;
$LD = $opt_L;
$OUTPUTDIR = $opt_o;
$prefix = $opt_j;
$rank = $opt_r;
$lang = $opt_t;
$tooldir = $opt_u;
$threads = $opt_v;
$minlength = $opt_x;
$maxlength = $opt_y;

$LD = 2;
}

print STDERR "OUT1: $out\n";
$out = $OUTPUTDIR . '/zzz/TICCL/' . $prefix;
$hiddenout = $OUTPUTDIR . '/zzz/TICCL/.' . $prefix;
$tiffdir = $OUTPUTDIR . '/zzz/TIFF/';
$hocrdir = $OUTPUTDIR . '/zzz/HOCR/';
$foliadir = $OUTPUTDIR . '/zzz/FOLIA/';
print STDERR "OUT2: $out\n";

`mkdir $OUTPUTDIR/zzz/`;
`mkdir $OUTPUTDIR/zzz/TIFF/`;
`mkdir $OUTPUTDIR/zzz/TICCL/`;
`cp $lex $out.lst`; ##Checken!!

# a : run all with TICCL-indexerNT (+ 'n'). Should then be 'abcdefgn'.
# b : 
# c : minwordlength
# d : maxwordlength
# e : file extension
# i : input directory
#: Language
# L : edit/Levenshtein distance
# f :
# l : lexicon
# o : output directory
# t : top n best-ranking
# w : switches (evaluation, conversion, debugging
# x : tool directory

#The different modules are called by way of the characters defined in $opt_a.
# 'a' calls FoLia-stats
# 'b' calls TICCL-unk
# 'c' calls TICCL-anahash
# 'd' calls TICCL-indexer. When combined with 'n', TICCL-indexerNT is called.
# 'e' calls TICCL-LDcalc
# 'f' calls TICCL-rank
# 'g' calls FoLiA-correct

##We set the binmode to UTF-8 for STDOUT and STDERR--BEGIN
binmode(STDOUT, ":utf8");
binmode(STDERR, ":utf8");
##We set the binmode to UTF-8 for STDOUT and STDERR--END

print STDERR "TICCLops version CLARIN-NL 0.2\n";
#print STDERR "START TIME: $intime\n";
#print STDERR "TOOLDIR: $tooldir\n";

@coldocs = ();
if ($texttype =~ /PDF/){
find( sub{
    -f $_ and push @documents, $File::Find::name;
    -d $_ and push @dirs,  $File::Find::name;
      }, $INPUTDIR );
foreach $docname (@documents){
    if ($docname =~ /pdf$/i){
	@DOCNAME = split '/', $docname;
	$last = pop @DOCNAME;
	if (($last !~ /^\./) and ($last !~ /\.lst$/)){
	    push(@coldocs, $docname);
	}
    }
}
##We build the list of documents to be processed--END
##We next process each document listed in the array in turn
@coldocs = nsort @coldocs;
foreach $doc (@coldocs) {
	@DOCNAME = split '/', $doc;
	$last = pop @DOCNAME;
##Extract images from PDF. Then convert the output *ppm files to tiff. Change the extension for the tiff-output files.
print STDERR "Running_pdfimages: $doc >> $last PREFIX: $prefix\n"; 
	`pdfimages $doc $INPUTDIR/$prefix`;  ##We write to the input directory from which any images present will be picked up by the next loop for conversion to tiff format.
       
    $alldocs .= $doc . ' ';  ## We collect all the PDF input file names for further collation into one single PDF file.
}
    print STDERR "ALLDOCSPDF: $alldocs\n";
    `pdftk $alldocs output $OUTPUTDIR/$prefix.pdf`;
}

##NEW: Image conversion generic to tiff--BEGIN
@coldocs = ();
if (($texttype =~ /IM/) or ($texttype =~ /PDF/)) {
find( sub{
    -f $_ and push @documents, $File::Find::name;
    -d $_ and push @dirs,  $File::Find::name;
      }, $INPUTDIR );
foreach $docname (@documents){
    if ($docname !~ /pdf$/i){
	@DOCNAME = split '/', $docname;
	$last = pop @DOCNAME;
	if (($last !~ /^\./) and ($last !~ /\.lst$/) and ($last !~ /\.log$/)){
	    push(@coldocs, $docname);
	}
    }
}
##We build the list of documents to be processed--END
##We write the number of documents to be processsed to the log file
$nrdocs = $#coldocs + 1;
##Numbering the documents starts at '1'
$document_number = 0;
$follow = -1;
##We next process each document listed in the array in turn
@coldocs = nsort @coldocs;
foreach $doc (@coldocs) {
    @DOCNAME = split '/', $doc;
    $last = pop @DOCNAME;
    
print STDERR "RUN_Convert: $doc >> $last\n"; 
	$tiffout = $last;
        $tiffout =~ s/\.[a-z]+$/\.tif/;
 print STDERR "RUN_Convert2: $doc >> $last >>$tiffout\n";        
        `convert $doc $tiffdir/$tiffout`; 
}
}
##NEW: Image conversion generic to tiff--END

@coldocs = ();
if ($texttype =~ /DJVU/){
find( sub{
    -f $_ and push @documents, $File::Find::name;
    -d $_ and push @dirs,  $File::Find::name;
      }, $INPUTDIR );
foreach $docname (@documents){
    if ($docname =~ /djvu$/i){
	@DOCNAME = split '/', $docname;
	$last = pop @DOCNAME;
	if (($last !~ /^\./) and ($last !~ /\.lst$/)){
	    push(@coldocs, $docname);
	}
    }
}
##We build the list of documents to be processed--END
##We next process each document listed in the array in turn
@coldocs = nsort @coldocs;
$docnr = ();
foreach $doc (@coldocs) {
    $docnr++;
print STDERR "DDJVUforDJVU: $doc\n"; 
##Convert single djvu file to one tiff containing all the pages
`ddjvu --format=tiff $doc $OUTPUTDIR/$prefix.tif`;
}
##Hier tiff naar PDF met tiff2pdf
    `tiff2pdf -o $tiffdir/$prefix.pdf $tiffdir/$prefix.tif`;
##Nu all.tif naar aparte tiffs met tiffsplit
print STDERR "ALLTIFFS: $tiffdir/$prefix.tif DOCNR: $docnr\n";
`tiffsplit $tiffdir/$prefix.tif $tiffdir/Input$docnr.$prefix`;
##Nu allTIFF niet meer nodig: deleten
`rm $tiffdir/$prefix.tif`;
}

$alldocs = ();

@coldocs = ();
if (($texttype =~ /IM/) or ($texttype =~ /TIFF/) or ($texttype =~ /PDF/) or ($texttype =~ /DJVU/)) {
    if (($texttype =~ /IM/) or ($texttype =~ /PDF/) or ($texttype =~ /DJVU/)) {
	$DOCDIR = $tiffdir;
    }
    else {
	$DOCDIR = $INPUTDIR;
    }
find( sub{
    -f $_ and push @documents, $File::Find::name;
    -d $_ and push @dirs,  $File::Find::name;
      }, $DOCDIR );
foreach $docname (@documents){
    if ($docname =~ /tif$/){
	@DOCNAME = split '/', $docname;
	$last = pop @DOCNAME;
	if (($last !~ /^\./) and ($last !~ /\.lst$/)){
	    push(@coldocs, $docname);
	}
    }
}
##We build the list of documents to be processed--END
##We write the number of documents to be processsed to the log file
$nrdocs = $#coldocs + 1;
##Numbering the documents starts at '1'
$document_number = 0;
$follow = -1;
##We next process each document listed in the array in turn
@coldocs = nsort @coldocs;
`mkdir $hocrdir`;
`mkdir $foliadir`;
foreach $doc (@coldocs) {
    @DOCNAME = split '/', $doc;
    $last = pop @DOCNAME;

print STDERR "RUN_Tesseract: $doc >> $last\n"; 

    if ($lang =~ /lat/){
`export TESSDATA_PREFIX="/usr/share/tesseract/tessdata/"; /usr/local/bin/tesseract $doc $hocrdir/$last -l eng $ROOTDIR/tools/config.hocr`;
}
    else {
`export TESSDATA_PREFIX="/usr/share/tesseract/tessdata/"; /usr/local/bin/tesseract $doc $hocrdir/$last -l $lang $ROOTDIR/tools/config.hocr`;
    }
print STDERR "RUN_FoLiA-hocr: $doc >> $last\n"; 
`$tooldir/FoLiA-hocr -t $threads -O $foliadir $hocrdir/$last.hocr`;
##Lijst tiff files verzamelen indien tiff was input en met tiffcp verzamelen in 1 bestand. Die dan met tiff2pdf omzetten
    $alldocs .= $doc . ' ';
}
print STDERR "RUN_tiffcp: ALLDOCS: $alldocs OUT: $tiffdir/$prefix.tif\n"; 
`tiffcp -t -a $alldocs $tiffdir/$prefix.tif`;
`tiff2pdf $tiffdir/$prefix.tif -o $OUTPUTDIR/$prefix.pdf`;
`rm $tiffdir/$prefix.tif`;
}

@coldocs = ();
if ($texttype =~ /TXT/){
find( sub{
    -f $_ and push @documents, $File::Find::name;
    -d $_ and push @dirs,  $File::Find::name;
      }, $INPUTDIR );
##print STDERR "DOCNAMESREADGOLD: $golddir >> @documents\n" if ($mode =~ /Z/);
foreach $docname (@documents){

    if ($docname =~ /txt$/i){
	@DOCNAME = split '/', $docname;
	$last = pop @DOCNAME;
	if (($last !~ /^\./) and ($last !~ /\.lst$/)){
	    push(@coldocs, $docname);
	}
    }
}
##We build the list of documents to be processed--END
##We next process each document listed in the array in turn
@coldocs = nsort @coldocs;
foreach $doc (@coldocs) {
##Process texts
##TODO!!
    `$tooldir/FoLiA-txt -t $threads $doc -O $OUTPUTDIR`;
}
}

if ($mode =~ /l/){
##TODO: language classification per paragraph
##mre@black:/opensonar/TICCL/TESTV1$ /exp/sloot/usr/local/bin/FoLiA-langcat --all --config /exp/sloot/lc/tc.txt -O /opensonar/TICCL/TESTV1/LC2 /opensonar/TICCL/TESTV1/FOLIA
}

###LOOP - Corpus Processing into frequency file--BEGIN###
if ($mode =~ /a/){
    if (($texttype =~ /IM/) or ($texttype =~ /PDF/) or ($texttype =~ /DJVU/) or ($texttype =~ /TIFF/)){
print STDERR "RUN_FoLiA-stats1: $out\n"; 
`$tooldir/FoLiA-stats -R -s -t $threads -e $ext --lang=none --ngram 1 -o $out $foliadir`;

##/exp/sloot/usr/local/bin/FoLiA-stats -R -s -t 4 -e folia.xml$ --lang=none --ngram 1 -o /opensonar/ticclops/ticclops /opensonar/ticclops/nld/projects/anonymous/tiftest/output/zzz/FOLIA
}
        elsif ($texttype =~ /FOLIA/){
##--class=FoLiA-txt
print STDERR "RUN_FoLiA-stats1FOLIA: $out\n"; 
	`$tooldir/FoLiA-stats -R -s -t $threads -e $ext --lang=none --class=FoLiA-txt --ngram 1 -o $out $foliadir`;
}
        elsif ($texttype =~ /XML/){
	  ##--class=FoLiA-txt

	 # Usage: /exp/sloot/usr/local/bin//TICCL-stats [options] file/dir
	 #TICCL-stats will produce ngram statistics for a file, 
	 #or a whole directory of files 
	 #The output will be a 2 columned tab separated file, extension: *tsv 
	#--clip	 clipping factor. 
	         #(entries with frequency <= this factor will be ignored). 
	#-p	 output percentages too. 
	#--lower	 Lowercase all words
	#-t	 number_of_threads
	#-h	 this message
	#-v	 very verbose output.
	#-V	 show version 
	#-e	 expr: specify the expression all input files should match with.
	#-o	 name of the output file(s) prefix.
	#-X	 the inputfiles are assumed to be XML.
	#-R	 search the dirs recursively (when appropriate).
	  
print STDERR "RUN_FoLiA-stats1XML: $out\n"; 
	`$tooldir/TICCL-stats -R -X -t $threads -e $ext -o $out $INPUTDIR`;
    }
        elsif ($texttype =~ /TXT/){
##--class=FoLiA-txt
print STDERR "RUN_FoLiA-stats1TXT: $out\n"; 
	`$tooldir/TICCL-stats -R -t $threads -e $ext -o $out $INPUTDIR`;
    }
    else {
print STDERR "RUN_FoLiA-stats2: $out\n"; 
	`$tooldir/FoLiA-stats -R -s -t $threads -e $ext --lang=none --ngram 1 -o $out $dir`;
}
    `mv $out.wordfreqlist.tsv $out.tsv`;
}
###LOOP1 - Corpus Processing into frequency file--END###

###LOOP2--BEGIN
if ($mode =~ /b/){
    if ($mode !~ /a/){
	`cp $INPUTDIR/*tsv $out.tsv`;
    }
print STDERR "RUN_TICCL-unk: $out >> $out.tsv\n"; 
    `$tooldir/TICCL-unk --corpus $lex --artifrq $artifrq $out.tsv`;
}
###LOOP2--END
###LOOP3--BEGIN
if ($mode =~ /c/){
    if ($mode !~ /m/){
print STDERR "RUN_TICCL-anahash: $out.tsv.clean\n"; 
	`$tooldir/TICCL-anahash --alph $alph $out.tsv.clean`;
}
    else {
print STDERR "RUN_TICCL-anahash: $out.tsv.clean\n"; 
	`$tooldir/TICCL-anahash --alph $alph --artifrq $artifrq $out.tsv.clean`;
}
}
###LOOP3 - END###

###LOOP4--BEGIN
##DOEN ALLES MET een indexer in one go!!--BEGIN
    $anahash = $out . '.tsv.clean.anahash';
    if ($mode =~ /m/){
     $corpusfoci = $out . '.tsv.clean.corpusfoci';   
    }
    $confuslist = $hidddenout . '.tsv.clean.confuslist';
    #`touch $confuslist`;
    $collectbestand  = $hiddenout . '.tsv.clean.collectlist'; ##Lijkt nergens herbruikt te worden
    $nuticclbestand  = $hiddenout . '.tsv.clean.nuticcllist'; ##Alleen (tijdelijk?) voor TICCL-indexer in parallel?
if ($mode =~ /d/){
if ($mode =~ /n/){
##Make temporary directory
$dirsplits = $outdir . '/TMP';
if (-d "$dirsplits") {
`rm -r $dirsplits`;
`mkdir $dirsplits`;
}
else {
`mkdir $dirsplits`;
}
#`touch $nuticclbestand`;
    print LOG "RUNNING ticcl3--PARALLEL\n";

##Split the character confusion list in number of parts specified in ARGV[13]
$nrsplits = $threads;

##Count how many to put in each split

$confusioncountline = `wc -l $charconfus`; ##CONFUSLIST!!!!
chomp $confusioncountline;
@CONFCOUNT = split / /, $confusioncountline;
$ceil = ceil((@CONFCOUNT[0] / $nrsplits));
print STDERR "CEIL: @CONFCOUNT[0] <<<>> $confusioncountline PREF: $prefixsplits CEIL: $ceil\n";
##Split the charconfus file to the TMP directory
$prefixsplits = $dirsplits . '/charconfussplits.';
 `split -l $ceil -d $charconfus $prefixsplits`;

find( sub{
            -f $_ and push @docsplits, $File::Find::name;
            -d $_ and push @dirsplits,  $File::Find::name;
}, $dirsplits );

	 print STDERR "SPLITDOCNAMESREAD: $dirsplits >> @docsplits <<>> @dirsplits\n" if ($mode =~ /z/);

open (NUTICCL, ">$nuticclbestand");
binmode(NUTICCL, ":utf8");
foreach $splitdoc (@docsplits){
print NUTICCL "nohup $tooldir/TICCL-indexer -a $anahash -c $splitdoc -o $splitdoc.outsplit -L $minlength -H $maxlength &\n"; ##Nog oude situatie van voor streamlining
}
close NUTICCL;

`chmod 755 $nuticclbestand`; 
`$nuticclbestand`;

#Nu samenrapen en catten naar $outbestand.
foreach $splitdoc (@docsplits){
    `cat $splitdoc.outsplit >> $confuslist`;
}
print LOG "INDEXER: All done!\n";
}
    elsif ($mode =~ /m/){
##We use indexerNT
print STDERR "RUN_TICCL-indexerNT: $out.tsv.clean\n";
`$tooldir/TICCL-indexerNT -t $threads --hash $anahash --charconf $charconfus --foci $corpusfoci -o $confuslist`;
}
else {   
     print LOG "RUNNING ticcl3--SINGLECORE\n"; 
    `$tooldir/TICCL-indexer -a $anahash -c $ARGV[10] -o $confuslist -L $minlength -H $maxlength ;`; ##Nog oude situatie van voor streamlining
}
}
    print LOG "DONE RUNNING ticcl3\n";
##DOEN ALLES MET een indexer in one go!!--END
###LOOP 4--END

$corptime = time();
$runtime1 = $corptime - $intime;
$runtimeminutes1 = $runtime1 / 60;
$runtimehours1 = $runtimeminutes1 / 60;

print STDERR "TIME AFTER PROCESSING CORPUS: $corptime minus $intime = $runtime1 >> MIN: $runtimeminutes1 >> HOURS: $runtimehours1\n";

###LOOP5 - BEGIN ###
if ($mode =~ /e/){
    if ($mode =~ /m/){
print STDERR "RUN_TICCL-LDcalc: $out\n";
	`$tooldir/TICCL-LDcalc --index $confuslist.indexNT --hash $anahash --clean $out.tsv.clean --LD $LD -t $threads --artifrq $artifrq -o $out.tsv.clean.ldcalc`;
    }
    else {
print STDERR "RUN_TICCL-LDcalc: $out\n";
`$tooldir/TICCL-LDcalc --index $confuslist.index --hash $anahash --clean $out.tsv.clean --hist $KHC --LD $LD -t $threads --artifrq $artifrq -o $out.tsv.clean.ldcalc`; 
 }
}
###LOOP5 - END
###LOOP6 - BEGIN
if ($mode =~ /f/){
if ($mode =~ /M/){
print STDERR "RUN_TICCL-rank1: $out\n";
`$tooldir/TICCL-rank -t $threads --alph $alph --charconf $charconfus -o $out.tsv.clean.ldcalc.ranked --debugfile $hiddenout.tsv.clean.ldcalc.debug.ranked --artifrq $artifrq --clip $rank --skipcols=10,11 $out.tsv.clean.ldcalc 2>$hiddenout.RANKartifrq.stderr`;
}
else {
print STDERR "RUN_TICCL-rank2: $out\n";
`$tooldir/TICCL-rank -t $threads --alph $alph --charconf $charconfus -o $out.tsv.clean.ldcalc.ranked --debugfile $hiddenout.tsv.clean.ldcalc.debug.ranked --artifrq 0 --clip $rank --skipcols=10,11 $out.tsv.clean.ldcalc 2>$hiddenout.RANK.stderr`; ##To edit!!
}
}
###LOOP6 - END
###LOOP7 - BEGIN
if ($mode =~ /g/){
    $dirticclcorrect = $OUTPUTDIR . '/zzz/FOLIAcorrect/';
    `mkdir $dirticclcorrect`;
##new, streamlined:
print STDERR "RUN_FoLiA-correct: $out\n";
##Met FoLiA input nu geen folia.xml in outputdir, maar wel in inputdir
if ($texttype =~ /FOLIA/){
`$tooldir/FoLiA-correct -t $threads --nums 10 -e $ext -O $dirticclcorrect --unk $out.tsv.unk --punct $out.tsv.punct --rank $out.tsv.clean.ldcalc.ranked $INPUTDIR`;
}
else {
`$tooldir/FoLiA-correct -t $threads --nums 10 -e $ext -O $dirticclcorrect --unk $out.tsv.unk --punct $out.tsv.punct --rank $out.tsv.clean.ldcalc.ranked $foliadir`;
}
##to ticcl.tei.xml
`perl $ROOTDIR/tools/PhilosTEI.FoLiAtoTEI.pl $dirticclcorrect#$OUTPUTDIR/ folia.ticcl.xml#tei.ticcl.xml $ROOTDIR/tools/Simple.xml $prefix >$dirticclcorrect/TEI.stdout 2>$dirticclcorrect/TEI.stderr &`;
}
###LOOP7 - END

$outtime = time();
$runtime = $outtime - $intime;
$runtimeminutes = $runtime / 60;
$runtimehours = $runtimeminutes / 60;
print LOG "END TIME WITHOUT EVALUATION: $outtime minus $intime = $runtime >>";
printf LOG "MIN: %.3f ", $runtimeminutes;
printf LOG ">> HOURS: %.3f\n", $runtimehours;

##That's all, folks!
