# Machine Configurator Desktop app

## Description
  This is a simple software written in python to configure electronic boards throught Serial communication. It is a system based on "key" "value" settings, so, you are going to send a read parameters request and the board will answer with its parameters in the format : {"key":"value"}\n
  Give it a delay in between sending of each parameter (in firmware). After that, pushing the "Write to Flash" button, the software will send the parameters to the board in the same json format. 
