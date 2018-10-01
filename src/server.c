#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>


#define BUFF_SIZE 256

int main(void)
{
  int listenfd = 0,connfd = 0;
  int contin = 1; 
  struct sockaddr_in serv_addr;
 
  char sendBuff[1025];  
  char recvBuff[BUFF_SIZE];
  char empty[BUFF_SIZE];
  char resp_to_cly[BUFF_SIZE];
  int numrv;  
  int num_char=0; 
  //initialize empty to all zeros
  int i;
  for(i =0; i < BUFF_SIZE; i++){
     empty[i]=0;
  }
  
  //allow user to set up server response
  puts("Enter server response message:");
  fgets(resp_to_cly, BUFF_SIZE, stdin);


  //server set up code
  listenfd = socket(AF_INET, SOCK_STREAM, 0);
  printf("socket retrieve success\n");
  
  memset(&serv_addr, '0', sizeof(serv_addr));
  memset(sendBuff, '0', sizeof(sendBuff));
      
  serv_addr.sin_family = AF_INET;    
  serv_addr.sin_addr.s_addr = htonl(INADDR_ANY); 
  serv_addr.sin_port = htons(5000);    
 
  bind(listenfd, (struct sockaddr*)&serv_addr,sizeof(serv_addr));
  
  if(listen(listenfd, 10) == -1){
      printf("Failed to listen\n");
      return -1;
  }


  
  connfd = accept(listenfd, (struct sockaddr*)NULL ,NULL); // accept awaiting request.
  
  while(contin)
    { 
      //clear recvBuff
      //strcpy(recvBuff, empty);
      //server reads data from the client and displays it	    
      num_char = read(connfd, recvBuff, sizeof(recvBuff));
      recvBuff[num_char] = '\0'; //must add null termination
      fputs(recvBuff, stdout);
      puts(" ");

      if(!strcmp("done", recvBuff)){
         //client tells us that we are done so close connexion
	 contin = 0;
	 memset(resp_to_cly, '\0', sizeof(char)*BUFF_SIZE);
	 strcpy(resp_to_cly, "Connexion Terminated. :)"); 
      }

      //send data back to the client
      //strcpy(sendBuff, "Luna thanks you for your input!");
      write(connfd, resp_to_cly, strlen(resp_to_cly));

      //sleep(1);
      //Test retreiving data from the client to the server
      
      //puts("Do you want to quit the server? Y/N\n");
      //char reply = 0;
      //reply = getchar();
      //if(reply == 'y' || reply == 'Y'){
      //	   contin = 0;
      //}

    } 

  close(connfd); //close the current request. Moved to the end so that we can test stuff    
  return 0;
}
