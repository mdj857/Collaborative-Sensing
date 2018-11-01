#define _GNU_SOURCE
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <sched.h>
#include <unistd.h>


#define BUFF_SIZE 512
#define STACK_SIZE 2048

int recieved_data(void *unused){

  char recvBuff[BUFF_SIZE];
  int getints[12];
  int fifo3 = open("cli_recieve", O_RDONLY); //open fifo for reading
  if(fifo3 == -1){
    printf("error opening fifo for reading, %d", errno);
  }
  while(1){
    //monitor network and print recieved message to screen
    int num_char = read(fifo3, &getints, 8);
    //recvBuff[num_char] = '\0'; //must add null termination
    //fputs(recvBuff, stdout);
    //puts("PONIEZ ");
    printf("bytes read:%d, throw away is %d, lower is  %d\n",num_char, getints[1],getints[0]);
  }
  return(0);
}




int main(void){
  char *stack, *stack_top, *stack2;
  char user_input[BUFF_SIZE];
  //open transmit fifo for writing
  int fifo = open("cli_transmit", O_RDWR); //open the fifo for reading and writing 
  if(fifo == -1){
    printf("Fifo failed to open, errno %d\n", errno);
    exit(2);
  }

  //open recieve fifo for reading
  int fifo2 = open("cli_recieve", O_RDWR); //open the fifo for reading and writing 
  if(fifo == -1){
    printf("Fifo failed to open, errno %d\n", errno);
    exit(2);
  }

  //create thread that listens
  stack = malloc(STACK_SIZE);
  if(stack == NULL){
     exit(3);;
  }
  stack_top = stack + STACK_SIZE;  /* Assume stack grows toward zero */
  int new_thrd = clone(&recieved_data, stack_top,CLONE_THREAD|CLONE_SIGHAND|CLONE_VM, stack);
    if(new_thrd == -1){
    puts("Recieve thread could not be created...Sorry Twilight... :(");
    printf("errno %d\n", errno);
    exit(2);
  }

    
 while(1){
     //get user input for message
     //sleep(1);
     puts("Enter message to send between threads");
     fgets(user_input, BUFF_SIZE, stdin);
     //put it in the FiFo 
     write(fifo, user_input, strlen(user_input));
     //rinse and repeat.
  }




}
