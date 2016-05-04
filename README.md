# TICCL and TICCLops #

Text-induced Corpus Clean-up is the stand-alone command-line version of the spelling correction and OCR post-correction system we have been developing since about 2008.  

TICCLops is TICCL as an 'online processing system'. It is a fully fledged web application and web service due to CLAM, developed  by Maarten van Gompel.  

The current repository mainly houses the wrapper scripts, variably Perl and Python scripts.  

The main TICCL modules were developed by Ko van der Sloot in C++ in various projects over the past years. These are available from: ``https://github.com/LanguageMachines/ticcltools``  

We have prepared TICCL for work in many languages, mainly on the basis of available open source lexicons due to Aspell. The language specific files are available here:  

[All languages] (http://ticclops.uvt.nl/TICCL.languagefiles.ALLavailable.20160421.tar.gz)
[German] (http://ticclops.uvt.nl/TICCL.languagefiles.deu.20160421.tar.gz)
http://ticclops.uvt.nl/TICCL.languagefiles.deu-frak.20160421.tar.gz
http://ticclops.uvt.nl/TICCL.languagefiles.ell.20160421.tar.gz
http://ticclops.uvt.nl/TICCL.languagefiles.eng.20160421.tar.gz
http://ticclops.uvt.nl/TICCL.languagefiles.fin.20160421.tar.gz
http://ticclops.uvt.nl/TICCL.languagefiles.fra.20160421.tar.gz
http://ticclops.uvt.nl/TICCL.languagefiles.fry.20160421.tar.gz
http://ticclops.uvt.nl/TICCL.languagefiles.grc.20160421.tar.gz
http://ticclops.uvt.nl/TICCL.languagefiles.isl.20160421.tar.gz
http://ticclops.uvt.nl/TICCL.languagefiles.ita.20160421.tar.gz
http://ticclops.uvt.nl/TICCL.languagefiles.lat.20160421.tar.gz
http://ticclops.uvt.nl/TICCL.languagefiles.nld.20160421.tar.gz
http://ticclops.uvt.nl/TICCL.languagefiles.pol.20160421.tar.gz
http://ticclops.uvt.nl/TICCL.languagefiles.por.20160421.tar.gz
http://ticclops.uvt.nl/TICCL.languagefiles.ron.20160421.tar.gz
http://ticclops.uvt.nl/TICCL.languagefiles.rus.20160421.tar.gz
http://ticclops.uvt.nl/TICCL.languagefiles.spa.20160421.tar.gz
http://ticclops.uvt.nl/TICCL.languagefiles.swe.20160421.tar.gz``

We also provide some sample corpora. These come with TICCLops for demonstration and test purposes. These are available here:  

[All demo and test sets] (http://ticclops.uvt.nl/TICCL.SampleCorpora.20160504.ALL.tar.gz)
[DjVu format] (http://ticclops.uvt.nl/TICCL.SampleCorpora.DJVU.20160504.tar.gz)
http://ticclops.uvt.nl/TICCL.SampleCorpora.FOLIA.20160504.tar.gz
http://ticclops.uvt.nl/TICCL.SampleCorpora.OCR.20160504.tar.gz
http://ticclops.uvt.nl/TICCL.SampleCorpora.PDF.20160504.tar.gz
http://ticclops.uvt.nl/TICCL.SampleCorpora.TIFF.20160504.tar.gz
http://ticclops.uvt.nl/TICCL.SampleCorpora.TSV.20160504.tar.gz
http://ticclops.uvt.nl/TICCL.SampleCorpora.TXT.20160504.tar.gz``

## Running TICCL from the command line  ##

Use ``TICCLops.PICCL.pl`` to run TICCL from the command line.  

Examples of input parameters with some further documentation are to be found in file: ``TICCL.Black.config`` .

Edit file ``TICCL.Template.config`` in order to specify the specific settings and file locations for your own installation.

Running script ``TICCL.BuildCommandLine.sh`` (edit to specify your own filled out config-file!) will print the command line required to run TICCL to file: ``RunTICCL.commandline.sh`` .

You can then start TICCL by running the following command: ``$
./RunTICCL.commandline.sh``  



