
#include "jsmn.h"

char dataRX[50];
char dataTX[50];
osEvent flags;
uint8_t i,j;
char *js;
char *js_end;
jsmn_parser* parser;
jsmntok_t tokens[10];
char buffer[15];

js = strchr((char*)dataRX, '{');
  js_end = strchr((char*)dataRX, '*');
  memset(js_end, 0, strlen(js_end));
  if(js!=NULL){ 
    if(jsmn_parse(parser, js,(strchr((char*)dataRX, '}') - js) , tokens,10)){
      for(i=0;i < NELEMS(tokens); i++){
        if(tokens[i].type != JSMN_STRING)continue;
        if(memcmp("M", js+tokens[i].start, tokens[i].end - tokens[i].start)==0){
          if(memcmp("R", js+tokens[i+1].start, tokens[i+1].end - tokens[i+1].start)==0){
            write_to_flash = false;
            memset(dataTX,0,strlen(dataTX));
            sprintf((char*)dataTX, "{\"%s\":\"%d\"}\n","parameter 1",*(flash_config_data+1));	
            USARTdrv->Send(dataTX, strlen(dataTX));
            osDelay(100);
            
            sprintf((char*)dataTX, "{\"%s\":\"%d\"}\n","parameter 2",*(flash_config_data+2));	
            USARTdrv->Send(dataTX, strlen(dataTX));
            osDelay(100);
          }
          
          if(memcmp("W", js+tokens[i+1].start, tokens[i+1].end - tokens[i+1].start)==0){
            if(memcmp("parameter 1", js+tokens[i+3].start, tokens[i+3].end - tokens[i+3].start)==0){
              memcpy(buffer,js+tokens[i+5].start, tokens[i+5].end - tokens[i+5].start);
              if(sscanf(buffer, "%d", &flash_buffer[1]) == EOF){
                sprintf((char*)dataTX, "{\"parameter 1\":\"fail to write parameter 1\"}");	
                USARTdrv->Send(dataTX, strlen(dataTX));
              }else {
                sprintf((char*)dataTX, "{\"SUCCESS\":\"parameter 1\"}");	
                USARTdrv->Send(dataTX, strlen(dataTX));
              }
            }
           if(memcmp("parameter 2", js+tokens[i+3].start, tokens[i+3].end - tokens[i+3].start)==0){
              memcpy(buffer,js+tokens[i+5].start, tokens[i+5].end - tokens[i+5].start);
              if(sscanf(buffer, "%d", &flash_buffer[2]) == EOF){
                sprintf((char*)dataTX, "{\"parameter 2\":\"fail to write parameter 2\"}");	
                USARTdrv->Send(dataTX, strlen(dataTX));
              }else {
                sprintf((char*)dataTX, "{\"SUCCESS\":\"parameter2\"}");	
                USARTdrv->Send(dataTX, strlen(dataTX));
              }
            }
          }
