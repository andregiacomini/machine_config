# Machine Configurator Desktop app

## Description
  This is a simple software written in python to configure electronic boards throught Serial communication. It is a system based on "key" "value" settings, so, you are going to send "Read parameters" request and the board should answer with its parameters in the format : {"key":"value"}\n
  Give it a delay in between sending of each parameter (in firmware). Pushing the "Write to Flash" button, the software will send the parameters to the board in the same json format. 
  
## Example of firmware to communicate 

- The file example.c contains a shunk of code to read and write the parameters from UART 
- Dependency to read json in C, thanks to zserge for jsmn.h lib
- https://github.com/zserge/jsmn

