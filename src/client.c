#define _GNU_SOURCE
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
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <sched.h>
#include <unistd.h>


#define BUFF_SIZE 256
#define STACK_SIZE 2048
#define FALSE 0
#define TRUE 1


int sockfd=0;
int message_size = 8;

//thread to read from the fifo and send out the message
int transmit_fifo(void *sparkle){
  int nr;
  char read_buff[BUFF_SIZE];
   int fifo2 = open("cli_transmit", O_RDONLY); //open fifo for reading
   if(fifo2 == -1){
      printf("error opening fifo for reading, %d", errno);
   }
   while(1){
      //read and send to server
      nr = read(fifo2, read_buff, message_size);
      if(nr != 0){
      	puts("Transmit FiFo read. Sending to Server.");
      	write(sockfd, read_buff, message_size);
      }
 }
  puts("shouldn't go here");
  return(0);
}

int recieve_fifo(void *unused){

  char recvBuff[BUFF_SIZE];
  int fifo3 = open("cli_recieve", O_WRONLY); //open fifo for reading
  if(fifo3 == -1){
    printf("error opening fifo for reading, %d", errno);
  }
  while(1){
    //monitor network and print recieved message to screen
    int num_char = read(sockfd, recvBuff, message_size);
    printf("num read is %d\n", num_char);
    if(num_char != 0){
      puts("Network data recieved. Putting in recieve FiFo");
      write(fifo3, recvBuff, message_size);
    }
   // fputs(recvBuff, stdout);
   // puts(" ");
  }
  return(0);
}


int main(int argc, char const *argv[]){
  int fifo;
  int n = 0;
  char user_input[BUFF_SIZE];  //user input string 
  struct sockaddr_in serv_addr;
  char *stack, *stack_top,*stack2;
  int done = FALSE;
  int numrv;
  int num_char=0;
  char *split_string;
  char ip_addr[16];
  int port_i;
  
  if(argc < 3 || argc > 4){
    puts("Error: Must Specifiy Server IP followed by the port on argument.\nE.G. ./client 192.168.56.101 25565\nOptionally set the message size.");
    exit(1);
  }
  if(argc == 4 && argv[3][0] != '0'){
    message_size = atoi(argv[3]); //TODO: make this idiot proof
    printf("Message size set to %d bytes\n", message_size);
  }
  else{
    puts("Using default message size of 8 bytes.");
  }
  strncpy(ip_addr, argv[1], 15); //15 is max chars in IPV4 address 
  port_i = atoi(argv[2]); //convert command line arg into number
  printf("%s:%d\n", ip_addr, port_i);
  //TODO: Fix server to work with consistent port, add IP configuration option to command line

  if((sockfd = socket(AF_INET, SOCK_STREAM, 0))< 0)
    {
      printf("\n Error : Could not create socket \n");
      return 1;
    }
 
  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons(port_i);
  serv_addr.sin_addr.s_addr = inet_addr(ip_addr); //loopback is 127.0.0.1
 
  if(connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr))<0)
    {
      printf("\n Error : Connect Failed \n");
      return 1;
    }

//Transmit FiFo Setup code
  //create fifo, with all permisssions for everyone
  int res = mkfifo("cli_transmit", S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH);
  if(res && (errno != EEXIST)){ //OK if FiFo already exists
    puts("Error creating the FiFo. Program will now termiate.\n");
    exit(1);
  }
  //open for writing
 // fifo = open("cli_transmit", O_RDWR); //open the fifo for reading and writing 
 // if(fifo == -1){
 //   printf("Fifo failed to open, errno %d\n", errno);
 //   exit(2);
 // }

  //Recieve FiFo setup code
  int res2 = mkfifo("cli_recieve", S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP | S_IROTH | S_IWOTH);
  if(res2 && (errno != EEXIST)){ //OK if FiFo already exists
    puts("Error creating the FiFo. Program will now termiate.\n");
    exit(1);
  }
  //open for writing
//  int fifo2 = open("cli_recieve", O_RDWR); //open the fifo for reading and writing 
 // if(fifo == -1){
 //   printf("Fifo failed to open, errno %d\n", errno);
 //   exit(2);
 // }



   //launch the sending thread
   stack = malloc(STACK_SIZE);
  if(stack == NULL){
     exit(3);;
  }
  stack_top = stack + STACK_SIZE;  /* Assume stack grows toward zero */
  int new_thrd = clone(&transmit_fifo, stack_top,CLONE_THREAD|CLONE_SIGHAND|CLONE_VM, stack);
    if(new_thrd == -1){
    puts("Recieve thread could not be created...Sorry Twilight... :(");
    printf("errno %d\n", errno);
    exit(2);
  }

  //launch the recieving thread
  stack2 = malloc(STACK_SIZE);
  if(stack2 == NULL){
     exit(3);;
  }
  stack_top = stack2 + STACK_SIZE;  /* Assume stack grows toward zero */
  int nw_thrd2 = clone(&recieve_fifo, stack_top, CLONE_THREAD|CLONE_SIGHAND|CLONE_VM, stack);
    if(nw_thrd2 == -1){
    puts("Thread could not be created...Sorry Twilight... :(");
    printf("errno %d\n", errno);
    exit(2);
  }


   while(!done){
     //get user input for message
     //sleep(1);
     //puts("Enter message to send between threads");
     //fgets(user_input, BUFF_SIZE, stdin);
     //put it in the FiFo 
     //write(fifo, user_input, strlen(user_input));
     //rinse and repeat.
    }

  return 0;
}
