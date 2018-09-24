#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>

#define BUFF_SIZE 256

int main(void)
{
  int sockfd = 0,n = 0;
  int done = 0;
  char recvBuff[1024];
  char sendBUFF[BUFF_SIZE];
  char empty[BUFF_SIZE];
  struct sockaddr_in serv_addr;
 
  //setup empty
  int i =0;
  for(;i < BUFF_SIZE; i++){
     empty[i] = '\0';
  }


  memset(recvBuff, '0' ,sizeof(recvBuff));
  if((sockfd = socket(AF_INET, SOCK_STREAM, 0))< 0)
    {
      printf("\n Error : Could not create socket \n");
      return 1;
    }
 
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(5000);
  serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
 
  if(connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr))<0)
    {
      printf("\n Error : Connect Failed \n");
      return 1;
    }

   while(!done){
        printf("Enter message to send back to server:\n");	   
	strcpy(sendBUFF, empty);
	fgets(sendBUFF, BUFF_SIZE, stdin);
	if(!strcmp(sendBUFF, "done\n")){
	   //said we are done so lets quit
	  // puts("Done Sending!"); 
		done = 1;
	}
        //send data to the server
	//printf("To server: %s", sendBUFF);
        write(sockfd, sendBUFF, strlen(sendBUFF)); 
	
	//recieve data from server and print
	n = read(sockfd, recvBuff, sizeof(recvBuff)-1);
        if( n < 0){
           printf("\n Read Error \n");
        }    
        recvBuff[n] = 0;
        if(fputs(recvBuff, stdout) == EOF){
         printf("\n Error : Fputs error");
        }
        printf("\n");
    }

  return 0;
}
