
grep '^-' TICCL.Black.config |cut -d '#' -f 1 |tr -d '\t' |tr '\n' ' ' |sed -e 's/$/#/' |sed -e 's/^/perl \/exp2\/mre\/ticclops\/TICCLops.PICCL.pl /g' |tr '#' '\n' >RunTICCL.commandline.sh | chmod 755 RunTICCL.commandline.sh
