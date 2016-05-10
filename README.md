# TICCL and TICCLops #

Text-induced Corpus Clean-up is the stand-alone command line version of the spelling correction and OCR post-correction system we have been developing since about 2008.  

TICCLops is TICCL as an 'online processing system'. It is a fully
fledged web application and web service due to [CLAM]
(http://proycon.github.io/clam/), developed  by Maarten van Gompel.

The current repository mainly houses the wrapper scripts, variably Perl and Python scripts.  

The main TICCL modules were developed by Ko van der Sloot in C++ in
various projects over the past years. These are available from:
[TICCLtools at LanguageMachines] (https://github.com/LanguageMachines/ticcltools)  

We have prepared TICCL for work in many languages, mainly on the basis of available open source lexicons due to Aspell. The language specific files are available here:  

[All languages]
(http://ticclops.uvt.nl/TICCL.languagefiles.ALLavailable.20160421.tar.gz)  
[Dutch] (http://ticclops.uvt.nl/TICCL.languagefiles.nld.20160421.tar.gz)  
[English] (http://ticclops.uvt.nl/TICCL.languagefiles.eng.20160421.tar.gz)  
[Finnish] (http://ticclops.uvt.nl/TICCL.languagefiles.fin.20160421.tar.gz)  
[French] (http://ticclops.uvt.nl/TICCL.languagefiles.fra.20160421.tar.gz)  
[Friesian] (http://ticclops.uvt.nl/TICCL.languagefiles.fry.20160421.tar.gz)  
[German]
(http://ticclops.uvt.nl/TICCL.languagefiles.deu.20160421.tar.gz)  
[German Fraktur]
(http://ticclops.uvt.nl/TICCL.languagefiles.deu-frak.20160421.tar.gz)  
[Greek (antique)] (http://ticclops.uvt.nl/TICCL.languagefiles.grc.20160421.tar.gz)  
[Greek (modern)] (http://ticclops.uvt.nl/TICCL.languagefiles.ell.20160421.tar.gz)  
[Icelandic] (http://ticclops.uvt.nl/TICCL.languagefiles.isl.20160421.tar.gz)  
[Italian] (http://ticclops.uvt.nl/TICCL.languagefiles.ita.20160421.tar.gz)  
[Latin] (http://ticclops.uvt.nl/TICCL.languagefiles.lat.20160421.tar.gz)  
[Polish] (http://ticclops.uvt.nl/TICCL.languagefiles.pol.20160421.tar.gz)  
[Portuguese] (http://ticclops.uvt.nl/TICCL.languagefiles.por.20160421.tar.gz)  
[Romanian] (http://ticclops.uvt.nl/TICCL.languagefiles.ron.20160421.tar.gz)  
[Russian] (http://ticclops.uvt.nl/TICCL.languagefiles.rus.20160421.tar.gz)  
[Spanish] (http://ticclops.uvt.nl/TICCL.languagefiles.spa.20160421.tar.gz)  
[Swedish]
(http://ticclops.uvt.nl/TICCL.languagefiles.swe.20160421.tar.gz)  

Unpack in your main TICCL directory. A subdirectory data/int/ will be
created to house the required files for the specific language(s).  

We also provide some sample corpora. These come with TICCLops for demonstration and test purposes. These are available here:  

[All demo and test sets]
(http://ticclops.uvt.nl/TICCL.SampleCorpora.20160504.ALL.tar.gz)  
[DjVu format]
(http://ticclops.uvt.nl/TICCL.SampleCorpora.DJVU.20160504.tar.gz)  
[FoLiA XML format]
(http://ticclops.uvt.nl/TICCL.SampleCorpora.FOLIA.20160504.tar.gz)  
[OCR] (http://ticclops.uvt.nl/TICCL.SampleCorpora.OCR.20160504.tar.gz)  
[PDF with embedded page images] (http://ticclops.uvt.nl/TICCL.SampleCorpora.PDF.20160504.tar.gz)  
[Tab-separated list] (http://ticclops.uvt.nl/TICCL.SampleCorpora.TSV.20160504.tar.gz)  
[Text files] (http://ticclops.uvt.nl/TICCL.SampleCorpora.TXT.20160504.tar.gz)  
[TIFF image files]
(http://ticclops.uvt.nl/TICCL.SampleCorpora.TIFF.20160504.tar.gz)

## Running TICCL from the command line  ##

Use ``TICCLops.PICCL.pl`` to run TICCL from the command line.  

Examples of input parameters with some further documentation are to be found in file: ``TICCL.Black.config`` .

Edit file ``TICCL.Template.config`` in order to specify the specific settings and file locations for your own installation.

You can then start TICCL by running the following command: ``$
perl TICCLops.PICCL.pl TICCL.Template.config``  

## Running TICCL from the command line  -- specific parameter settings##

The first parameter set in TICCL's config file, or the first parameter
i.e. ARGV[0] when all parameters are specified on the command line, is
typically a combination of alphabetical characters that when set,
activate particular TICCL C++ modules.  

As default we have: ``abcmdef``. This means all of TICCL's C++ modules will be
run sequentially, but two of them will be run in 'word focus
mode'. This refers to our main TICCL publication (Reynaert 2010). In
its essence, this is the cheapest option to run TICCL if the corpus
you want to have (OCR post-)corrected is not very big.  

We next describe we each letter invokes.  

### Parameter setting ``a`` ###

The letter ``a`` in fact works in tandem with line 8 in the config
file, parameter ``-h`` on the full command line. The character ``a``
specifies that your input will be running text. This running text may
be in three formats, either FoLiA XML, else some unspecified XML
format or finally plain text format. For FoLiA XML, specify ``FOLIA``
in line 8, for unspecified XML put ``XML``, for plain text put
``TXT``.  

For unspecified XML, the text will be extracted from the ``<t>`` nodes
in the XML.  

In fact, the module invoked will derive a frequency list for your
corpus from your input files. This entails that in case you already
have a frequency file, or even in case that you only have a frequency
file for your corpus (which might be the case if you acquired OCRed
books from the Hathi Trust collection, for instance), you can skip
this step and proceed from the next.  

### Parameter setting ``b`` ###

The letter ``b`` envokes the module TICCL-unk. This performs an
elementary clean-up of the input frequency list. In fact, this removes
character strings that have no hope of ever being corrected into what
is commonly understood to be a meaningful word in any natural
language.  

### Parameter setting ``c`` ###

The letter ``c`` invokes C++ module TICCL-anahash. This converts the
cleaned frequency file into the TICCL anagram hash. Can be used in
conjunction with the letter ``m`` (please, see there) to provide a speedier further
processing for smaller corpora.  

### Parameter setting ``m`` ###

If specified, the letter ``m`` makes the module TICCL-anahash also
output the list of word strings that TICCL needs to search correction
candidates for. This is effected on the basis of the artificial
frequency we let the system assign to word types that are present in
the validated lexicon.  This list serves as the focus words list for
the subsequent module TICCL-indexerNT. For smaller corpora this
results in less work and therefore shorter running times than when one
runs TICCL-indexer, which exhaustively gathers all correction
candidates for all the words in the cleaned up corpus frequency list,
i.e. performs character confusion based corpus clean-up.  

## TICCLops available online as demonstrator system ##

We have a demonstrator system online in an official Dutch CLARIN Center at
[TICCLopsCLAM] (http://ticclops.clarin.inl.nl/ticclops/). An interface
developed specifically for philosopher-users is available here:
[TICCLopsPhilosTEI] (http://ticclops.clarin.inl.nl/ticclops/).  

In fact, both systems are geared at letting you upload scanned images of
book pages, to have them automatically converted into electronic text
by way of the Tesseract OCR engine and then to have them
OCR post-corrected by TICCL. For e.g. PDF files for book chapters, you
will receive back a full, reconstituted book in both FoLiA and TEI
formats. Please take into account that this process requires, well,
the time required.  
