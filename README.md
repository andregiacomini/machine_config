# Machine Configurator Desktop app

## Description
  This is a simple software written in python to configure electronic boards throught Serial communication. It is a system based on "key" "value" settings, so, you are going to send "Read parameters" request and the board should answer with its parameters in the format : {"key":"value"}\n
  Give it a delay in between sending of each parameter (in firmware). Pushing the "Write to Flash" button, the software will send the parameters to the board in the same json format. 
  
## Example of firmware to communicate 

- Dependency to read json in C, example.c, thanks to zserge for jsmn.h lib

