# Machine Configurator Desktop app

## Description
  This is a simple software written in python to configure elecrtonic boards throught Serial communication. It is a system based on "key" "value" settings, so, you are going to send a read parameters request and the board will answer with its parameters in the format : {"key":"value"}\n
  Give it a delay in between sending of each parameter (in firmware). After that, the software will send the parameters to the board in the same json format. 
